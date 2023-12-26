# boj-account-transfer (BOJ 계정 이전)
Automatically re-submit submission history of previous BOJ account to the new BOJ account.

기존 BOJ 계정의 제출기록을 새 BOJ 계정으로 제출합니다.

## 설계
### 1. login
`id, password -> cookies`
+ <https://www.acmicpc.net/login> 에 접근.
+ 아이디와 비밀번호를 적절한 곳에 써 넣음.
+ ‘로그인’ 버튼 클릭.
+ 반환받은 새 페이지에서 쿠키를 얻어온다.

### 2. search
`id -> submission info(submission id, problem id) list`
+ [https://www.acmicpc.net/status?user_id=[아이디]](https://www.acmicpc.net/status?user_id=povwhm) 에 접근.
+ 제출번호와 문제번호를 크롤링.
+ ‘다음 페이지’ 버튼 클릭.
+ 다시 크롤링. ‘다음 페이지’ 버튼이 사라질 때까지 반복.
  
### 3. get_source
`cookies, submission id -> source code`
+ 쿠키를 가진 채로 [https://www.acmicpc.net/source/[제출번호]](https://www.acmicpc.net/source/56892412) 에 접근.
+ 소스코드를 크롤링.

### 4. preprocess
`source code -> source code`
+ `&amp;` 등을 해당하는 문자로 변환
+ [HTML의 특수 코드 정리](https://ooz.co.kr/199) 참고.

### 5. submit
`cookies, source code, problem id -> new_submission id`
+ 쿠키를 가진 채로 [https://www.acmicpc.net/submit/[문제번호]](https://www.acmicpc.net/problem/2517) 에 접근.
+ 소스코드를 적절한 곳에 써 넣음.
+ ‘제출’ 버튼 클릭.
+ 반환받은 새 페이지에서 새 제출번호를 얻어온다.

### 6. check_result
`old_submission id, new_submission id -> (success/failure) info`
+ 각 기존_제출번호, 새_제출번호마다,
  + [https://www.acmicpc.net/status?top=[제출번호]](https://www.acmicpc.net/source/56892412) 에 접근.
  + 가장 첫째 줄에서 ‘결과’ 열 확인.
+ 기존_결과와 새_결과가 같으면 성공.
+ 기존_결과와 새_결과가 다르면 실패 정보 반환 및 실시간으로 정보 출력.

### 7. main
`old_id, old_password, new_id, new_password -> (success/failure) info list`
+ 기존 아이디, 비밀번호로 login() 후 기존_쿠키 발행.
+ 신규 아이디, 비밀번호로 login() 후 신규_쿠키 발행.
+ search(기존_아이디) 수행. 제출정보(기존_제출번호, 문제번호) 리스트 획득.
+ 각 (기존_제출번호, 문제번호)에 대해, (추가로 사용자가 제출번호를 지정할 수 있음)
  + get_source(기존_쿠키, 기존_제출번호) 수행. 소스코드 획득.
  + preprocess(소스코드) 수행. 특수 코드가 제거된 소스코드 획득
  + submit(신규_쿠키, 소스코드, 문제번호) 수행. 새_제출번호 획득.
  + check_result(기존_제출번호, 새_제출번호)의 결과를 리스트에 append
+ 실패 정보 리스트를 출력.

## 설계
### 1. Language
`Python 3.12`

### 2. Library
+ BeautifulSoup : 웹 페이지 정보를 쉽게 스크랩할 수 있도록 도와준다
+ Requests : HTTP 요청을 보낼 수 있도록 도와준다

### 3. Timeline
+ ~2023.01.01 : 개발 준비, interaction 형식 및 라이브러리 탐색
+ ~2023.01.31 : login과 search 구현
+ ~2023.02.28 : submit 까지 구현
+ ~2023.03.31 : main 구현 후 마무리