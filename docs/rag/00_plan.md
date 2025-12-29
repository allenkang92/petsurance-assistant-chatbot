***

# 펫보험 RAG 시스템 구현 계획 (Gemini + LangChain)

### 전체 개요
RAG(Retrieval-Augmented Generation)는 **외부 지식 기반을 LLM과 결합**하여 정확하고 근거 있는 답변을 생성하는 구조.  
LangChain을 활용하면 이 과정을 구성 요소 단위로 직접 설계하고, 각 단계를 세밀하게 제어할 수 있다.

***

## 사전 단계: 데이터 준비 및 인덱싱

### 1️⃣ 문서 로드 (Document Load)
- **목표:** `data/petsurance_markdown/` 디렉토리 내의 모든 마크다운 파일 로드
- **LangChain 도구:** `DirectoryLoader` (glob="**/*.md"), `TextLoader`
- **전략:** 폴더 구조(보험사별)를 유지하며 전체 파일을 읽어옵니다.

### 2️⃣ 텍스트 분할 (Text Split)
- **목표:** 약관의 **조항(Article) 단위**로 의미론적 분할 수행
- **핵심 포인트:** `refine_markdown.py`로 복원한 `#### 제N조` 구조 활용
- **LangChain 도구:** 
  1. `MarkdownHeaderTextSplitter`: 1차 분할 (헤더 기준)
  2. `RecursiveCharacterTextSplitter`: 2차 분할 (긴 조항 처리)

### 3️⃣ 임베딩 (Embedding)
- **목표:** 텍스트를 Google Gemini Embedding 모델을 통해 벡터로 변환
- **LangChain 도구:** `GoogleGenerativeAIEmbeddings`
- **모델:** `models/embedding-001`

### 4️⃣ 벡터 스토어 저장 (Vector Store)
- **목표:** 로컬 환경에서 테스트 및 지속성을 위한 벡터 DB 구축
- **LangChain 도구:** `Chroma`
- **전략:** `./chroma_db` 경로에 영구 저장(persist)하여 재사용 가능하게 함

***

## 실행 단계: 검색 및 생성

### 5️⃣ 리트리버 (Retriever)
- **목표:** 질문과 가장 관련성 높은 약관 조항 검색
- **LangChain 도구:** `vectorstore.as_retriever()`
- **설정:** 
  - `search_type="mmr"` (다양성 확보)
  - `k=5` (상위 5개 문맥 추출)

### 6️⃣ 프롬프트 구성 (Prompt)
- **목표:** 보험 전문가 페르소나와 펫보험 특화 답변 유도
- **LangChain 도구:** `PromptTemplate`
- **전략:** "반드시 제공된 [약관]에 근거하여 답변하고, 해당 조항 번호를 인용하시오."

### 7️⃣ LLM 응답 생성 (LLM)
- **목표:** Gemini Pro 모델을 통해 자연스러운 답변 생성
- **LangChain 도구:** `ChatGoogleGenerativeAI`
- **모델:** `gemini-1.5-pro` (또는 `gemini-pro`)

### 8️⃣ 체인 생성 (Chain Integration)
- **목표:** 검색(Retriever)과 생성(LLM)을 연결
- **LangChain 도구:** `RetrievalQA` (또는 `create_retrieval_chain`)
- **전략:** `chain_type="stuff"` (검색된 문서를 프롬프트에 모두 넣어 전달)

***

## 정리

| 단계 | 이름 | 구현 내용 | LangChain/Gemini 도구 |
|------|------|-----------|------------------|
| 1 | 문서 로드 | `data/petsurance_markdown/*.md` 로드 | `DirectoryLoader` |
| 2 | 텍스트 분할 | 헤더(`#`) 및 문자수 기준 청킹 | `MarkdownHeaderTextSplitter` |
| 3 | 임베딩 | Gemini 임베딩 모델 적용 | `GoogleGenerativeAIEmbeddings` |
| 4 | 벡터 스토어 | ChromaDB에 로컬 저장 | `Chroma` |
| 5 | 리트리버 | MMR 방식 검색 설정 | `.as_retriever(search_type="mmr")` |
| 6 | 프롬프트 | 약관 전문가 프롬프트 설계 | `PromptTemplate` |
| 7 | LLM | Gemini Pro 모델 설정 | `ChatGoogleGenerativeAI` |
| 8 | 체인 생성 | QA 체인 통합 | `RetrievalQA` |

***

RAG의 각 단계를 LangChain 구성요소로 세밀하게 다루면, **LLM의 응답 품질을 체계적으로 개선하고 내부 알고리즘을 조정할 수 있는 제어권** 확보 가능.

***

