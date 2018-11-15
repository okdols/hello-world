import pymssql

# 접속 구문을 꼭 확인
# MS SQL 내부 계정 / Windows 인증 계정(MS에서 선호) / Active Directory 계정(보안 관리가 필요할 때)
connect = pymssql.connect(host='mssql 서버주소@인스턴스', user='사용자', password='pwd', db='', charset='utf8')

# Windows 인증인 경우(ConnectionStrings 참조, trusted connection)
host = r'(IP 또는 컴퓨터명)'
database='UserInfo'

try:
    # insert
    with connect.cursor() as cs:
        sqlQuery = """insert into membertb(name, id, pwd)
           values (%s, %s, %s)"""
        data = (
            ("홍길동1", "aaaa", "1234"),
            ("홍길동2", "bbbb", "1234")
            )
        cs.executemany(sqlQuery, data)
    connect.commit()

    with connect.cursor() as cs:
        sqlQuery  = "select * from table"
        cs.execute(sqlQuery)
except ConnectionRefusedError as cre:
    print(cre)
finally:
    connect.close() # 연결 종료(닫기)
