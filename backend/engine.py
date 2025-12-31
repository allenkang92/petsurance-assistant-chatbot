import os
import warnings
from typing import List, Dict, Any, Optional
from operator import itemgetter
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain_classic.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain_classic.retrievers.document_compressors.cross_encoder_rerank import CrossEncoderReranker
from langchain_community.memory.kg import ConversationKGMemory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 환경 변수 설정
os.environ["OMP_NUM_THREADS"] = "1"
warnings.filterwarnings('ignore')

class RAGManager:
    def __init__(self, persist_directory: str = None):
        # 1. 절대 경로 설정
        from pathlib import Path
        current_file = Path(__file__).resolve()
        project_root = current_file.parent.parent
        
        # 기본 경로 (루트)
        root_db = project_root / "chroma_db"
        # 노트북 경로 (학습 데이터가 실제 저장된 곳일 확률이 높음)
        notebook_db = project_root / "notebooks" / "chroma_db"
        
        # 실제 데이터가 있는 곳을 우선적으로 찾습니다.
        if notebook_db.exists() and (notebook_db / "chroma.sqlite3").exists():
            self.persist_directory = str(notebook_db)
        else:
            self.persist_directory = str(persist_directory or root_db)
        
        print(f"DEBUG: Selected DB Path: {self.persist_directory}")
        
        # 2. API 키 확인
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY가 설정되지 않았습니다.")
            
        # 3. 모델 설정 (사용자 요청에 따라 gemini-2.5-flash 사용)
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", 
            temperature=0,
            google_api_key=api_key
        )
        
        # 4. 임베딩 모델
        self.embeddings = HuggingFaceEmbeddings(
            model_name="snunlp/KR-SBERT-V40K-klueNLI-augSTS",
            model_kwargs={"device": "cpu"}
        )
        
        # 5. 벡터 스토어 로드
        print(f"DEBUG: Checking path: {self.persist_directory}")
        if os.path.exists(self.persist_directory):
            print(f"DEBUG: Path exists. Loading Chroma...")
            self.vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
            print(f"DEBUG: VectorStore successfully loaded.")
        else:
            print(f"DEBUG: Path does NOT exist: {self.persist_directory}")
            self.vectorstore = None

        # 6. 리랭커 설정
        self.re_ranker_model = HuggingFaceCrossEncoder(
            model_name="BAAI/bge-reranker-v2-m3",
            model_kwargs={"device": "cpu"}
        )
        self.compressor = CrossEncoderReranker(model=self.re_ranker_model, top_n=5)
        self.memories: Dict[str, ConversationKGMemory] = {}

    def get_memory(self, session_id: str) -> ConversationKGMemory:
        if session_id not in self.memories:
            self.memories[session_id] = ConversationKGMemory(llm=self.llm, memory_key="kg_context", return_messages=False)
        return self.memories[session_id]

    def _get_prompt(self):
        return ChatPromptTemplate.from_messages([
            ("system", "당신은 펫보험 전문 상담 AI '펫슈런스'입니다. 제공된 문맥과 기억을 바탕으로 답변하세요."),
            ("system", "[문맥]:\n{context}\n\n[기억]:\n{kg_context}"),
            ("user", "{question}")
        ])

    def get_retriever(self, custom_vs: Optional[Chroma] = None):
        target_vs = custom_vs or self.vectorstore
        if not target_vs:
            raise ValueError(f"데이터베이스를 찾을 수 없습니다: {self.persist_directory}")
        return ContextualCompressionRetriever(
            base_compressor=self.compressor,
            base_retriever=target_vs.as_retriever(search_kwargs={"k": 25})
        )

    def create_chain(self, session_id: str, custom_vs: Optional[Chroma] = None):
        retriever = self.get_retriever(custom_vs)
        memory = self.get_memory(session_id)
        
        def format_docs(docs):
            return "\n\n".join([f"[출처: {d.metadata.get('source', '약관')}]\n{d.page_content}" for d in docs])

        chain = (
            {
                "context": itemgetter("question") | retriever | format_docs,
                "question": itemgetter("question"),
                "kg_context": RunnableLambda(lambda x: memory.load_memory_variables({"input": x["question"]})["kg_context"])
            }
            | self._get_prompt()
            | self.llm
            | StrOutputParser()
        )
        return chain, memory

    def index_custom_file(self, file_path: str) -> Chroma:
        import uuid
        loader = PyPDFLoader(file_path) if file_path.endswith(".pdf") else TextLoader(file_path, encoding="utf-8")
        chunks = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100).split_documents(loader.load())
        return Chroma.from_documents(documents=chunks, embedding=self.embeddings, collection_name=f"c_{uuid.uuid4().hex}")
