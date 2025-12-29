# 펫보험 데이터 전처리 (Data Preprocessing)

## 1. 개요
수집한 펫보험 PDF 데이터를 RAG(Retrieval-Augmented Generation) 시스템에서 효과적으로 활용하기 위해 마크다운(Markdown) 형식으로 변환 및 정제 과정

- **수행 일자**: 2025-12-25
- **대상 데이터**: 펫보험 관련 9개 보험사의 총 122개 PDF 파일
- **목표**: 텍스트 추출 및 문서 구조(헤더, 표 등) 보존을 통한 검색 품질 향상

## 2. 사용 도구 및 기술
### Microsoft MarkItDown
- **선정 이유**: PDF의 구조적 정보(제목, 표, 다단 편집 등)를 마크다운 문법으로 변환해주는 강력한 기능을 제공하기 때문입니다.
- **설치**: `pip install markitdown`

### 주요 코드 로직 및 설명
아래는 `preprocess_all.py`의 구현 내용 중 일부입니다. 

```python
import os
from markitdown import MarkItDown

def batch_convert():
    # 원본 PDF 파일이 위치한 최상위 경로 (각 보험사 폴더 포함)
    source_root = r"your/path/to/petsurance"
    # 변환된 Markdown 파일이 저장될 경로
    dest_root = r"your/path/to/petsurance_markdown"
    
    # MarkItDown 인스턴스 생성 (PDF -> Markdown 변환기)
    md = MarkItDown()
    
    print(f"변환 시작: {source_root} -> {dest_root}")

    # os.walk를 사용하여 하위 디렉토리까지 탐색
    for root, dirs, files in os.walk(source_root):
        for file in files:
            # .pdf 확장자를 가진 파일만 처리 대상으로 선정
            if file.lower().endswith(".pdf"):
                source_path = os.path.join(root, file)
                rel_path = os.path.relpath(root, source_root)
                dest_dir = os.path.join(dest_root, rel_path)
                
                # 저장할 디렉토리가 없으면 생성
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                
                # 변환 수행 (Convert) 및 예외 처리
                try:
                    # MarkItDown 라이브러리를 사용하여 변환 수행
                    result = md.convert(source_path)
                    
                    # 확장자를 .pdf에서 .md로 변경
                    dest_file_name = os.path.splitext(file)[0] + ".md"
                    
                    # 변환된 텍스트 내용(text_content)을 utf-8 인코딩으로 저장
                    with open(os.path.join(dest_dir, dest_file_name), "w", encoding="utf-8") as f:
                        f.write(result.text_content)
                        
                except Exception as e:
                    # 변환 중 오류 발생 시 멈추지 않고 로그 출력 후 다음 파일 진행
                    print(f"Failed to convert {file}: {e}")
```

## 3. 수행 결과
- **처리 완료**: 총 122개 파일 변환 완료
- **출력 위치**: `r/your/path/to/petsurance_markdown`
- **결과물 특징**:
    - **헤더(Headers)**: `#`, `##` 등을 사용하여 문서의 계층 구조가 식별됨.
    - **표(Tables)**: 마크다운 파이프(`|`) 테이블로 변환되어 데이터의 행렬 구조 유지.
    - **이미지/텍스트**: 텍스트 위주로 깨끗하게 추출됨.