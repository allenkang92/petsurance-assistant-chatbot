import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from backend.engine import RAGManager
import uvicorn
import json
import shutil
from fastapi import UploadFile, File
from typing import Optional

app = FastAPI(title="Petsurance RAG API")
rag_manager = RAGManager()

# 세션별 커스텀 벡터 스토어 관리
custom_vs_store = {}

class ChatRequest(BaseModel):
    question: str
    session_id: str = "default_user"

@app.get("/")
def read_root():
    return {"message": "Petsurance RAG API is running"}

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        chain, memory = rag_manager.create_chain(request.session_id)
        
        async def stream_generator():
            full_answer = ""
            # 스트리밍 결과 생성
            for chunk in chain.stream({"question": request.question}):
                full_answer += chunk
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"
            
            # 스트리밍 완료 후 메모리 저장
            memory.save_context({"input": request.question}, {"output": full_answer})

        return StreamingResponse(stream_generator(), media_type="text/event-stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload")
async def upload_file(session_id: str, file: UploadFile = File(...)):
    try:
        temp_dir = f"./temp_uploads/{session_id}"
        os.makedirs(temp_dir, exist_ok=True)
        file_path = os.path.join(temp_dir, file.filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 문서 인덱싱
        custom_vs = rag_manager.index_custom_file(file_path)
        custom_vs_store[session_id] = custom_vs
        
        return {"filename": file.filename, "message": "성공적으로 학습되었습니다."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/custom")
async def chat_custom(request: ChatRequest):
    if request.session_id not in custom_vs_store:
        raise HTTPException(status_code=400, detail="먼저 문서를 업로드해 주세요.")
    
    try:
        custom_vs = custom_vs_store[request.session_id]
        chain, memory = rag_manager.create_chain(request.session_id, custom_vs=custom_vs)
        
        async def stream_generator():
            full_answer = ""
            for chunk in chain.stream({"question": request.question}):
                full_answer += chunk
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"
            memory.save_context({"input": request.question}, {"output": full_answer})

        return StreamingResponse(stream_generator(), media_type="text/event-stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
