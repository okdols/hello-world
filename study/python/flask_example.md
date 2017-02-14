## FLASK
- 파이썬의 웹 서비스 프레임워크 중 하나

#### 설치
 1. pip - 파이썬 패키지 설치 및 관리를 위한 패키지
   ```
   $ apt-get install python-pip
   ```
   혹은 [직접 설치](https://pip.pypa.io/en/stable/installing/)할 수도 있다.
   
 1. flask
   ```
   $ pip install flask
   ```
   
**(옵션)** virtualenv - 파이썬 가상 환경(프로젝트 별 파이썬 라이브러리를 구분하고자 하는 경우 사용)
  - 기본적으로 virtualenv는 pip이 설치된 상태, 필요한 경우 pip 설치
  
  ```
  $ sudo apt-get install virtualenv
  ```
  
  (pip 사용할 경우)
  ```
  $ pip install virtualenv
  ```
  
  가상 환경 설정 및 실행
  ```
  $ mkdir myproject
  $ cd myproject
  $ virtualenv myproject
  $ source myproject/bin/activate
  ```
  
  쉘 프롬프트가 프로젝트 명(디렉토리명)으로 변경되어 있으면 실행 된 것, 종료는 다음과 같다.
  ```
  $ deactivate
  ```

#### Hello World (기본 어플리케이션)
- 다음과 같이 hello.py 작성 ([참고](http://flask-docs-kr.readthedocs.io/ko/latest/quickstart.html))
  
  ```python
  from flask import Flask


  app = Flask(__name__)
  

  @app.route('/')
  def hello_world():
      return 'Hello World!'

  if __name__ == '__main__':
      app.run()
  ```
  
- 실행
  ```sh
  $ python hello.py
   * Running on http://localhost:5000/ (Press CTRL+C to quit)
  ```
  
 - 웹 브라우저로 위 주소에 접속하면 **Hello World!** 문구를 볼 수 있다.
 
#### Database ([Sqlite3](https://sqlite.org))
- 파이썬 embedded database 인 sqlite3 을 사용([pysqlite](https://pypi.python.org/pypi/pysqlite))
  ```python
  import sqlite3


  # sqlite3 db 연결
  conn = sqlite3.connect("test.db")

  # Create cursor from connection
  cur = conn.cursor()

  # Create table test
  cur.execute("CREATE TABLE test(Name text, Value text);")

  # Insert value (list insert)
  datalist = (('HongGildong', 'A'), ('Mobigen', 'B'))
  cur.execute("INSERT INTO test VALUES(?, ?);", datalist)

  # Select all and print
  cur.execute("SELECT * FROM test;")
  for row in cur:
      print(row)

  # Close connection (and cursor) when task ends.
  cur.close()
  conn.close()
  ```

## Flask CRUD 예제 (RESTful)
- Flask를 이용한 사용자 정보 RESTful CRUD
  - POST - Insert, GET - Select, PUT - Update, DELETE - Delete

  ```python
  # exam1.py
  import sqlite3
  import uuid
  
  from flask import Flask, request, jsonify
  
  DATABASE = 'exam.db'
  app = Flask(__name__)
  app.config.from_object(__name__)
  
   
  # HTTP GET: list of all users
  # @Request: Nothing
  # @Response: Json list
  # [
  #   {
  #     "id": [10-digit integer],
  #     "name": "[user name]",
  #     "salary": [integer]
  #   },
  #   {
  #     "id": 3645825710,
  #     "name": "Mobigen2",
  #     "salary": 20000
  #   }
  # ]
  @app.route('/users', methods=['GET'])
  def list_all_users():
      # table check
      _check_table()
      return _select_all_users()
  
  
  # HTTP GET: list of specific user
  # @Request: /users/<integer_user_id>
  # @Response: Json
  # {
  #     "id": [10-digit integer],
  #     "name": "[user name]",
  #     "salary": [integer]
  # }
  @app.route('/users/<int:user_id>', methods=['GET'])
  def list_user(user_id=None):
      # table check
      _check_table()
      return _select_user(user_id)
  
  
  # HTTP POST: insert a new user
  # @Request: Json
  # {
  #     "name": "[user name]",
  #     "salary": [integer]
  # }
  # @Response: Json
  # {
  #     "id": [10-digit integer]
  # }
  @app.route('/users', methods=['POST'])
  def create_users():
      # table check
      _check_table()
      return _insert_users(request.get_json())
  
  
  # HTTP PUT: update a user
  # @Request: /users/<integer_user_id>, Json(user info)
  # {
  #     "name": "[user name]",
  #     "salary": [integer]
  # }
  # @Response: Json
  # {
  #     "id": [10-digit integer]
  # }
  @app.route('/users/<user_id>', methods=['PUT'])
  def modify_user(user_id=None):
      # Table check
      _check_table()
      return _update_user(user_id, request.get_json())
  
  
  # HTTP DELETE: delete a user
  # @Request: /users/<integer_user_id>
  # @Response: Json
  # {
  #     "id": [10-digit integer]
  # }
  @app.route('/users/<user_id>', methods=['DELETE'])
  def remove_user(user_id=None):
      # Table check
      return _delete_user(user_id)
  
  
  # Check if the table exists.
  def _check_table():
      conn = sqlite3.connect(DATABASE)
      cur = conn.cursor()
      cur.execute(
          "SELECT name FROM sqlite_master WHERE type='table' AND name='user';")
      rs = cur.fetchall()
      if len(rs) <= 0:
          # Create table when table doesn't exist.
          _create_table()
      cur.close()
      conn.close()
  
  
  # Create Table
  def _create_table():
      conn = sqlite3.connect(DATABASE)
      cur = conn.cursor()
      cur.execute(
          "CREATE TABLE IF NOT EXISTS "
          "user(id int PRIMARY KEY, name text, salary int);")
      conn.commit()
      cur.close()
      conn.close()
      print "CREATE TABLE"
      return None
  
  
  # Select all users and return it in json format.
  def _select_all_users():
      conn = sqlite3.connect(DATABASE)
      cur = conn.cursor()
      cur.execute("SELECT * FROM user;")
      # return SQL table as JSON in python.
      rv = [dict((cur.description[i][0], value) for i, value in enumerate(row))
            for row in cur.fetchall()]
      if len(rv) > 0:
          cur.close()
          conn.close()
          return jsonify(rv)
      else:
          cur.close()
          conn.close()
          # If empty table return empty.
          return jsonify({"HTTP": "GET", "status": "all_empty"})
  
  
  # Select specific user and return it in json format.
  def _select_user(reqdata):
      conn = sqlite3.connect(DATABASE)
      cur = conn.cursor()
      cur.execute("SELECT * FROM user WHERE id=?;", (reqdata,))
      # return SQL table as JSON in python.
      rv = [dict((cur.description[i][0], value) for i, value in enumerate(row))
            for row in cur.fetchall()]
      if len(rv) > 0:
          cur.close()
          conn.close()
          return jsonify(rv)
      else:
          cur.close()
          conn.close()
          # if empty table
          return jsonify({"HTTP": "GET", "status": "empty"})
  
  
  # Insert a new user and returns generated ID in json format.
  def _insert_users(reqdata):
      # If request body is empty.
      if reqdata is None:
          return jsonify({"HTTP": "POST", "status": "empty"})
      conn = sqlite3.connect(DATABASE)
      cur = conn.cursor()
      # Generate 32bit integer UUID
      int_uuid = uuid.uuid4().int & (1 << 32)-1
      # Insert users data, id generated uuid.
      cur.execute(
          "insert into user values(?,?,?);",
          (int_uuid, reqdata['name'], reqdata['salary']))
      conn.commit()
      cur.close()
      conn.close()
      return jsonify({"id": int_uuid})
  
  
  # Update a user and return ID in json format.
  def _update_user(user_id, reqdata):
      conn = sqlite3.connect(DATABASE)
      cur = conn.cursor()
      cur.execute("UPDATE user SET name=?, salary=? WHERE id=?;",
                  (reqdata['name'], reqdata['salary'], user_id))
      conn.commit()
      cur.close()
      conn.close()
      return jsonify({"id": user_id})
  
  
  # Delete a user and return ID in json format.
  def _delete_user(user_id):
      conn = sqlite3.connect(DATABASE)
      cur = conn.cursor()
      cur.execute("DELETE FROM user WHERE id=?;", (user_id,))
      conn.commit()
      cur.close()
      conn.close()
      return jsonify({"id": user_id})
  
  
  # Drop Table: Only for testing.
  @app.route('/reset')
  def _drop_table():
      conn = sqlite3.connect(DATABASE)
      cur = conn.cursor()
      cur.execute("DROP TABLE 'user';")
      conn.commit()
      cur.close()
      conn.close()
      return "DROP TABLE"
  
  
  # Flask App running on localhost:8000
  if __name__ == "__main__":
      app.run(host='0.0.0.0', port=8000)
  ```

## 참고
| 구분 | URL |
| :-----: | ----- |
| **Flask** | [Flask](http://flask.pocoo.org/) |
|  | [Flask 참조](http://flask-docs-kr.readthedocs.io/ko/latest/) |
|  | [sqlite3](https://docs.python.org/2/library/sqlite3.html) |
