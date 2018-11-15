# python의 indent는 space 이며, 기본 4칸
# https://devguide.python.org <- 개발 가이드
'''
a = 10
b = 20
print(a + b)
'''

# pip install pymysql

import pymysql

# 다국어 사용을 위해 charset 지정하는 것에 유의
# mysql 연결
connect = pymysql.connect(host='mysql 서버주소', user='사용자', password='pwd', db='', charset='utf8')

# Cursor 생성을 위해 쿼리문을 사용
cs = connect.cursor() # Array based cursor: array 또는 tuple(linked list)

# Dictionary base query -> hash table 형태로 가져온다고 보면됨
# 처음부터 hash table(dict)로 가져와서 바로 활용하기 수월함(배열로 가져와서 hash table에 넣던게 기존에 익숙한 방식)
# 대량으로 데이터를 가져오는 경우 자료구조가 이미 형성되어 있어 활용 및 이전이 쉬움
cs2 = connect.cursor(pymysql.cursors.DictCursor) # HashTable(Dictionary) based cursor
# hashTable 은 메모리에 테이블형태로 올라가는 자료구조이므로 iot 장비와 같이 성능이 떨어지는 경우 오히려 장애 포인트

# 실제로는 쿼리문을 다이렉트로 날리는 경우는 없고, 프로시저나 저장(stored) 프로시저를 사용
sqlQuery = "select * from table"
sqlQuery2 = "select * from table where userid=%s and pwd=%s" # mysql 에서는 %s 주로 사용
cs.execute(sqlQuery)
cs.execute(sqlQuery2, ('aaa', '1234'))

rows1 = cs.fetchall() # 모든 데이터
rows2 = cs.fetchmany(5) # n개의 row
rows3 = cs.fetchone # 한개의 row
# [0] 의 의미는 indexer 번호가 0 인 것을 의미
print(rows1[0])

for data in rows1:
    print(data['컬럼명'], data['컬럼명'])

# 연결 종료(닫기)
connect.close()
