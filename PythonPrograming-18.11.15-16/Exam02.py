import pymysql

# 다국어 사용을 위해 charset 지정하는 것에 유의
# mysql 연결
connect = pymysql.connect(host='mysql 서버주소', user='사용자', password='pwd', db='', charset='utf8')

# Cursor 생성을 위해 쿼리문을 사용
cs = connect.cursor() # Array based cursor: array 또는 tuple(linked list)

sqlQuery = """insert into membertb(name, id, pwd)
           values (%s, %s, %s)"""

cs.execute(sqlQuery, ('홍길동', 'aaaa', '1234'))
cs.execute(sqlQuery, ('홍길동1', 'aaaa2', '12343'))
connect.commit()

data = (
    ("홍길동1", "aaaa", "1234"),
    ("홍길동2", "bbbb", "1234")
)
cs.executemany(sqlQuery, data)
connect.commit()

# 연결 종료(닫기)
connect.close()
