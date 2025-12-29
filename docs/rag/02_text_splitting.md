## 2. 텍스트 분할 (Text Splitting)

### 정의
텍스트 분할은 **RAG 전처리 과정에서 문서를 청크(Chunk)로 나누는 단계**

### 왜 필요한가?
| 문제 | 해결 |
|:---|:---|
| LLM 입력 토큰 제한 | 문서를 작은 청크로 나눠 필요한 부분만 전달 |
| 전체 페이지 검색 시 정확도 저하 | 청크 단위로 유사도 계산하여 관련 정보만 추출 |
| 불필요한 정보 포함 (Hallucination) | 잘 나눈 청크는 특정 주제에 집중 가능 |

### 핵심 개념

*   **청크 크기 (Chunk Size)**: 너무 크면 불필요한 정보 포함, 너무 작으면 맥락 부족
*   **청크 오버랩 (Chunk Overlap)**: 청크 사이에 일부 겹치는 부분을 만들어 **문장이 자연스럽게 이어지도록** 함

### 분할 전략 종류

| 전략 | 설명 | 적합한 경우 |
|:---|:---|:---|
| **문단 단위** | 빈 줄(`\n\n`) 기준 분할 | 일반 텍스트 |
| **문장 단위** | 마침표(`.`) 기준 분할 | 정밀한 검색 필요 시 |
| **글자 수 기준** | `chunk_size=1000` 등 고정 | 균일한 청크 필요 시 |
| **토큰 수 기준** | 토크나이저 활용 | LLM 토큰 제한 고려 시 |
| **헤더 기준 (Markdown)** | `#`, `##` 등 헤더로 분할 | 구조화된 문서 (약관 등) |

> ** 정해진 정답은 없습니다. 실험을 통해 최적의 전략을 찾아야 합니다.**

---

## 청킹 전략 실험 

### 실험 목표
펫보험 약관 데이터에 **최적화된 청킹 전략**을 찾아 RAG 답변 품질을 극대화합니다.

### 실험 변수

| 변수 | 테스트 값 |
|:---|:---|
| `chunk_size` | 500 / 1000 / 2000 |
| `chunk_overlap` | 0 / 100 / 200 |
| 분할 방식 | MarkdownHeader / Recursive / 조합 |

### 평가 지표

1.  **검색 정확도**: 질문에 맞는 조항이 Top-5에 포함되는가?
2.  **답변 품질**: 조항 번호를 정확히 인용하는가?
3.  **청크 수**: 너무 많으면 검색 효율 저하

### 실험 절차

```
[Step 1] 테스트 질문 세트 준비 (10~20개)
    ├── "슬개골 탈구 보장 여부"
    ├── "면책 기간은 얼마인가요?"
    ├── "노령견 가입 가능 나이"
    └── ...

[Step 2] 청킹 조합별 벡터스토어 생성
    ├── A: MarkdownHeader only
    ├── B: Recursive (chunk=500, overlap=50)
    ├── C: Recursive (chunk=1000, overlap=100)
    ├── D: MarkdownHeader + Recursive (chunk=1000)
    └── E: MarkdownHeader + Recursive (chunk=500)

[Step 3] 각 조합에서 테스트 질문 실행
    └── Retriever가 가져온 문서 확인 (Top-5)

[Step 4] 결과 비교
    ├── 정답 조항 포함률 (%)
    ├── 평균 청크 수
    └── 답변 품질 (수동 평가)

[Step 5] 최적 전략 선정
```

### 테스트 코드 예시

```python
# 다양한 청킹 설정 테스트
configs = [
    {"chunk_size": 500, "overlap": 50},
    {"chunk_size": 1000, "overlap": 100},
    {"chunk_size": 2000, "overlap": 200},
]

test_questions = [
    "슬개골 탈구 수술비가 보장되나요?",
    "면책 기간은 얼마인가요?",
    "보험금 청구 시 필요한 서류는?",
]

for config in configs:
    print(f"\n=== chunk_size={config['chunk_size']}, overlap={config['overlap']} ===")
    
    # 청킹 수행
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config["chunk_size"],
        chunk_overlap=config["overlap"]
    )
    chunks = splitter.split_documents(documents)
    print(f"총 청크 수: {len(chunks)}")
    
    # 벡터스토어 생성 후 검색 테스트
    # ... (생략)
```
