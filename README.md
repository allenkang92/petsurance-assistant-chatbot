# 펫보험 어시스턴트 챗봇 (Petsurance Assistant Chatbot)

## 프로젝트 개요 (Project Overview)
반려동물이 가족의 일원이 되는 '펫 휴머니제이션' 시대가 도래했음에도 불구하고, 복잡한 약관과 정보의 비대칭으로 인해 펫보험 가입률은 저조한 실정입니다. 본 프로젝트는 이러한 문제를 해결하기 위해 **약관을 쉽게 해석해주고, 개인 맞춤형 정보를 제공하는 챗봇**을 개발하는 것을 목표로 합니다.

*Despite the rise of "Pet Humanization," pet insurance adoption rates in Korea remain low (approx. 1.4%) due to complex terms and information asymmetry. This project aims to solve this by developing a **chatbot that interprets complex insurance terms and provides personalized information**.*

## 배경 (Background)
- **시장 성장**: 국내 반려동물 산업은 2027년 6조 원 규모로 성장할 전망이며, 동물병원 이용률은 80.4%에 달합니다.
  - **Market Growth**: *The Korean pet industry is projected to reach ~6 trillion KRW by 2027, with high veterinary service usage (80.4%).*
- **현실적인 문제**: 높은 진료비 부담으로 보험 수요는 증가하고 있으나, 2024년 기준 펫보험 가입률은 **약 1.4%**에 불과합니다.
  - **Real-world Issues**: *High veterinary costs drive demand, but the actual adoption rate remains extremely low at around 1.4% (as of 2024).*
- **주요 장벽**: 약관의 복잡성, 면책 기간, 보장 제외 조항 등 전문적인 내용이 소비자에게 큰 진입 장벽이 되고 있습니다.
  - **Major Barriers**: *Complex policy terms, such as coverage exclusions and waiting periods, act as significant barriers for consumers.*


## 문제점 (Problems)

### 1. 약관 복잡성으로 인한 소비자 역량 부족 (Complexity & Consumer Gap)
- 반려인의 89%가 펫보험을 인지하고 있으나, 전문 용어와 복잡한 특약 구조로 인해 내용을 이해하기 어렵습니다.
  - *89% of pet owners are aware of insurance, but struggle with legalistic jargon and complex special riders.*
- 이로 인해 '보장 범위가 좁다', '가입 필요성이 낮다'는 오해와 부정적 인식이 확산되고 있습니다.
  - *This leads to misconceptions like "narrow coverage" or "low necessity," discouraging adoption.*

### 2. 약관 기반 Q&A의 어려움 (Difficulty in Q&A)
- **사례**: "5살 치와와가 슬개골 수술을 받는데 보상이 되나요?"와 같은 구체적인 질문에 답하기 위해 소비자가 직접 방대한 약관을 뒤져야 합니다.
  - *Users struggle to answer specific questions (e.g., "Is patella surgery covered for my 5-year-old Chihuahua?") without digging through massive policy documents.*
- 보험사별(삼성, 현대, DB 등)로 상이한 약관 구조로 인해 직접적인 비교가 불가능에 가깝습니다.
  - *Different policy structures across insurers (Samsung, Hyundai, DB, etc.) make direct comparison nearly impossible.*

이처럼 개별 약관에 대한 질문에 답하기도 어려운데, 여러 상품을 한 번에 비교하거나 청구 절차를 이해하는 일은 더 높은 난이도의 작업입니다.
*While answering questions about individual policies is difficult, comparing multiple products at once or understanding claims procedures is even more challenging.*


### 3. 상품 비교 및 청구 가이드 부재 (Lack of Comparison & Claims Guide)
- 진료비 편차가 큰 상황에서 내 반려동물에게 적합한 플랜을 찾기 어렵습니다.
  - *It's hard to find a suitable plan amidst wide variances in veterinary costs.*
- 사고 발생 시 청구 절차나 필요 서류, 제도적 제약 사항(등록 여부 등)에 대한 정보가 흩어져 있어 파악이 힘듭니다.
  - *Information on claims procedures, required documents, and regulations (e.g., pet registration) is scattered and hard to grasp.*

## 솔루션: 정보 비대칭 해소를 위한 챗봇 (Solution: AI Chatbot)
이 챗봇은 소비자가 겪는 정보의 격차를 해소하고, 보험 가입·유지·청구 전 과정에서 든든한 가이드 역할을 수행합니다.

*This chatbot acts as a reliable guide to bridge the information gap throughout the entire insurance journey (subscription, maintenance, claims).*

### 주요 기능 (Key Features)
- **자연어 질의응답**: "우리 강아지 상황에서 이 조항이 무슨 뜻인가요?", "이 상품에서 슬개골 탈구는 보장되나요?" 등의 질문에 알기 쉽게 답변합니다.
  - ***Natural Language Q&A**: Simply ask, "What does this clause mean for my dog?" or "Is patella dislocation covered?"*
- **맞춤형 정보 제공**: 사용자의 반려동물 정보(견종, 나이, 병력 등)를 기반으로 해당 약관 조항을 찾아 매칭해줍니다.
  - ***Personalized Insights**: Matches policy details to your specific pet's profile (breed, age, medical history).*
- **청구 가이드**: 복잡한 청구 서류와 절차를 안내하고, 누락 없이 준비할 수 있도록 돕습니다.
  - ***Claims Guide**: Provides step-by-step guidance on required documents and procedures.*
- **문서 연결 및 요약**: 답변의 근거가 되는 약관의 해당 부분을 직접 연결하고 요약하여 신뢰도를 높입니다.
  - ***Source Linking**: Connects and summarizes relevant policy clauses directly to ensure trust.*

※ 챗봇은 보험료 산정, 가입 심사 결과 예측, 법적 자문 등은 제공하지 않습니다.
*※ The chatbot does not provide premium calculations, underwriting predictions, or legal advice.*


## 기대 효과 (Expected Impact)
- **정보 비대칭 해소**: 전문적인 보험 약관을 소비자의 언어로 해석하여 전달함으로써 오해와 불신을 줄입니다.
  - **Resolving Information Asymmetry**: *Translates professional terms into consumer-friendly language to reduce misunderstanding.*
- **분쟁 예방**: 가입 단계에서부터 정확한 보장 범위를 인지시켜 향후 발생할 수 있는 보상 분쟁을 예방합니다.
  - **Preventing Disputes**: *Prevents future disputes by clarifying coverage scope upfront.*
- **접근성 향상**: 누구나 쉽게 펫보험 정보를 확인하고 비교할 수 있게 하여, 반려동물 양육의 경제적 부담 완화에 기여합니다.
  - **Improving Accessibility**: *Makes insurance info accessible to everyone, helping to ease the economic burden of pet ownership.*

