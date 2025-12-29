## 5. 리트리버 (Retriever)

### 정의
리트리버는 **RAG 시스템의 5번째 단계**로, 벡터 DB에서 사용자 질문과 가장 관련성 높은 정보를 검색하는 단계입니다.

```
문서 로드 → 텍스트 분할 → 임베딩 → 벡터 스토어 → 리트리버 검색
```

### 왜 중요한가?

> **효율적인 리트리버 없이는 LLM이 아무리 좋아도 제대로 된 결과를 낼 수 없다.**

| 문제 | 결과 |
|:---|:---|
| 관련 문서 검색 실패 | LLM이 엉뚱한 답변 생성 |
| 불필요한 정보 포함 | 할루시네이션 증가 |
| 검색 속도 저하 | 전체 시스템 응답 지연 |

### 작동 방식

```
[사용자 질문] ──임베딩──▶ [질문 벡터]
                              │
                    ▼ 유사도 계산 (코사인, MMR 등)
                              │
[벡터 스토어] ◀──────────────┘
      │
      ▼ 상위 N개 문서 선정
      │
[관련 문서들] ──전달──▶ 프롬프트 생성 단계
```

### 유사도 계산 방법

| 방법 | 설명 |
|:---|:---|
| **코사인 유사도** | 두 벡터 간 각도 기반 유사도 (가장 일반적) |
| **MMR** (Maximal Marginal Relevance) | 유사도 + 다양성 고려 (중복 방지) |

### 리트리버 최적화 포인트

*  필요한 정보는 **반드시 검색 결과에 포함**
*  불필요한 정보는 **최소화**
*  검색 속도 최적화로 **응답 시간 단축**
*  LangSmith 활용하여 **검색 품질 실험**

---

## 문서 압축기 (ContextualCompressionRetriever)

### 왜 필요한가?
검색된 문서에는 질문과 무관한 텍스트가 많이 포함되어 있을 수 있습니다.  
이를 그대로 LLM에 전달하면 **할루시네이션**이 증가합니다.

### 작동 방식

```
[질문] ──▶ 기본 리트리버 검색 ──▶ 압축기 ──▶ 압축된 문서
                                    │
                        • 관련 정보만 추출
                        • 불필요한 문서 제거
                        • 내용 자체를 축약
```

### 코드 예시

```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

# 기본 리트리버
base_retriever = vectorstore.as_retriever(search_kwargs={"k": 10})

# LLM 기반 압축기
compressor = LLMChainExtractor.from_llm(llm)

# 압축 리트리버 생성
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=base_retriever
)

# 검색 (압축된 결과 반환)
results = compression_retriever.invoke("슬개골 탈구 보장 여부")
```

---

## 

| 단계 | 역할 |
|:---|:---|
| **리트리버** | 질문과 유사한 문서 검색 |
| **문서 압축기** | 검색 결과에서 관련 정보만 추출 |

```
질문 → 리트리버(검색) → 압축기(정제) → LLM(답변 생성)
```