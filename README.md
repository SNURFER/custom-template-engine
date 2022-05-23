## custom-template-engine
- 사용자 정보를 template 코드에 삽입해주는 템플릿 엔진
  - 테스트를 위한 템플릿코드는 input/template1, input/template2, input/template3에 위치  
  - 테스트를 위한 사용자 정보 json은 input/data.json에 위치 
- 아래의 동작 설명과 같이 수행됨

## 실행법 안내

### 방식 1. 
- input/data.json 에 사용자 정보의 Array로 이루어진 파일 작성
- input/template 에 템플릿 작성
- 아래의 커맨드 수행
```bash
$ python3 main.py
```
### 방식 2.
- input/data.json 에 사용자 정보의 Array로 이루어진 파일 작성
- 아래의 커맨드 수행
```bash
$ python3 main.py [TEMPLATE_PATH]
$ # 특정 템플릿 파일을 입력으로 받고 싶은 경우
```

### 출력 파일 확인 
- 프로젝트 디렉토리 최상단에 output.txt 파일에 결과가 출력됨
```
$ cat output.txt
```


## 동작 설명
- `<?[variable]?>` 이외의 스트링은 패턴으로 인정하지 않음 
  - 안되는 예시 
    - `< ?? >` 처럼 < 과 ? 간 공백이 있는경우
    - `< >`과 같이 물음표가 없는 경우
    - `<? >` 과 같이 물음표가 하나 부족한 경우
  - 기타 `<? ?>` 가 아닌 모든 패턴은 사용자가 의도한 고정 값으로 간주하여 그대로 출력을 해주도록 구현
  - 즉, syntax error는 따로 존재하지 않으며, 패턴이 맞지 않을 시, 고정 스트링으로 가정하여 출력함
- `<?[variable]?>` 내의 변수에 대응되는 데이터가 없을 경우 `?`를 출력함
- for loop을 제공
  - `<? for USER in USERS.* ?>`   
- USERS를 입력으로 받음 
  - USERS는 data.json 파일에 작성된 데이터 객체(사용자 Array)를 의미함
  - JS object prop에 접근하듯이, '.'을 이용하여 속성에 접근 가능 
    - 예) USERS.0.info.name.family   
  - input/template2처럼 nested한 for loop을 제공 
    - for loop을 한번 더 감싸면 기대 결과에 맞게 출력가능(input/template1, input/template2 참고)
    ```
    <? for USER in USERS.* ?>
    Family name: <?=USER.info.name.family?>\n
    Given name: <?=USER.info.name.given ?>\n
    Address : <?= USER.info.addrs.0.addr1?> <?= USER.info.addrs.0.addr2?>\n
    MemberShip : <?=USER.membership.grade?> <?= USER.membership.id ?>\n
    \n
    <? endfor ?>
    ```
  - array의 item은 index로 접근 가능
    - 예) USERS.0.info.name.family
- 텍스트 에디터로 직접 입력한 개행은 무시
  - 파일에 작성된 `\n`만 찾아서 개행을 함 
