import pymysql

# 다국어 사용을 위해 charset 지정하는 것에 유의
# mysql 연결
connect = pymysql.connect(host='mysql 서버주소', user='사용자', password='pwd', db='', charset='utf8')

# Cursor 생성을 위해 쿼리문을 사용
# 예외처리
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
    connect.close()# 연결 종료(닫기)
