# 식품 영양소 API(food_api)
## 개요
이 프로젝트는 식품 영양 정보 데이터베이스에 접근할 수 있는 Flask 기반의 RESTful API입니다. 사용자는 식품 항목에 대해 CRUD 작업을 수행하고 영양 정보를 조회할 수 있습니다.

## 기능
생성(Create): 데이터베이스에 새로운 식품 항목을 추가합니다.
읽기(Read): 기존 식품 항목의 정보를 검색합니다.
갱신(Update): 기존 식품 항목의 정보를 수정합니다.
삭제(Delete): 데이터베이스에서 식품 항목을 제거합니다.
검색(Search): 특정 조건을 기반으로 식품 항목을 쿼리합니다.

## 설치 방법
로컬 환경에서 프로젝트를 설정하려면 다음 단계를 따르세요:

```
#저장소를 클론합니다:
git clone https://github.com/ironfactory8684/food_api.git
```

```
#프로젝트 디렉토리로 이동합니다:
cd food_api
```
```
#필요한 의존성을 설치합니다:
pip install -r requirements.txt
```

```
#Flask 애플리케이션을 실행합니다:
python food_api.py
```
## 사용 방법
애플리케이션이 실행되면 http://127.0.0.1:5000/에서 API 엔드포인트에 접근할 수 있습니다.

### 엔드포인트
GET /foods - 모든 식품 항목을 검색합니다.  
GET /foods/<id> - ID로 특정 식품 항목을 검색합니다.  
POST /foods - 새로운 식품 항목을 추가합니다.  
PUT /foods/<id> - 기존 식품 항목을 갱신합니다.  
DELETE /foods/<id> - 식품 항목을 삭제합니다.  

### 요청 예시


```
# 새로운 식품 항목을 추가하기:
import requests

response = requests.post('http://127.0.0.1:5000/foods', json={
    'food_name': '사과',
    'calories': 95,
    # 추가 속성...
})

print(response.json())
```

## 기술 스택
Flask: API를 구축하기 위한 웹 프레임워크.  
SQLAlchemy: 데이터베이스 상호작용을 위한 ORM.  
SQLite: 식품 항목을 저장하기 위한 데이터베이스.  
Pandas: Excel 파일에서 데이터베이스를 처리하고 초기화하기 위함.  

## 기여
기여는 환영합니다! 버그나 개선 사항에 대한 풀 리퀘스트나 이슈를 자유롭게 제출해주세요.
