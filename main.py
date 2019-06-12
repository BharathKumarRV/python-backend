import pymysql
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request
from werkzeug import generate_password_hash, check_password_hash



def application(environ, start_response):
  if environ['REQUEST_METHOD'] == 'OPTIONS':
    start_response(
      '200 OK',
      [
        ('Content-Type', 'application/json'),
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Headers', 'Authorization, Content-Type'),
        ('Access-Control-Allow-Methods', 'POST','PUT'),
      ]
    )
    return ''
		
@app.route('/add', methods=['POST'])
def add_user():
		conn = mysql.connect()
		cursor = conn.cursor()
		try:
			_json = request.json
			_name = _json['name']
			_email = _json['email']
			_password = _json['pwd']
			# validate the received values
			if _name and _email and _password and request.method == 'POST':
				#do not save password as a plain text
				_hashed_password = generate_password_hash(_password)
				# save edits
				sql = "INSERT INTO tbl_user(user_name, user_email, user_password) VALUES(%s, %s, %s)"
				data = (_name, _email, _hashed_password,)
				cursor.execute(sql, data)
				conn.commit()
				resp = jsonify('User added successfully!')
				resp.headers.add('Access-Control-Allow-Origin', '*')
				resp.status_code = 200
				return resp
			else:
				return not_found()
		except Exception as e:
			print(e)
		finally:
			cursor.close() 
			conn.close()
		
@app.route('/users')
def users():
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		try:
			cursor.execute("SELECT user_id id, user_name name, user_email email, user_password pwd FROM tbl_user")
			rows = cursor.fetchall()
			resp = jsonify(rows)
			resp.status_code = 200
			return resp
		except Exception as e:
			print(e)
		finally:
			cursor.close() 
			conn.close()
		
@app.route('/user/<int:id>')
def user(id):
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		try:
			cursor.execute("SELECT user_id id, user_name name, user_email email, user_password pwd FROM tbl_user WHERE user_id=%s", id)
			row = cursor.fetchone()
			resp = jsonify(row)
			resp.status_code = 200
			return resp
		except Exception as e:
			print(e)
		finally:
			cursor.close() 
			conn.close()

@app.route('/update', methods=['PUT'])
def update_user():
		conn = mysql.connect()
		cursor = conn.cursor()
		try:
			_json = request.json
			_id = _json['id']
			_name = _json['name']
			_email = _json['email']
			_password = _json['pwd']		
			# validate the received values
			if _name and _email and _password and _id and request.method == 'PUT':
				#do not save password as a plain text
				_hashed_password = generate_password_hash(_password)
				# save edits
				sql = "UPDATE tbl_user SET user_name=%s, user_email=%s, user_password=%s WHERE user_id=%s"
				data = (_name, _email, _hashed_password, _id,)
				cursor.execute(sql, data)
				conn.commit()
				resp = jsonify('User updated successfully!')
				resp.status_code = 200
				return resp
			else:
				return not_found()
		except Exception as e:
			print(e)
		finally:
			cursor.close() 
			conn.close()
			
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_user(id):
		conn = mysql.connect()
		cursor = conn.cursor()
		try:
			cursor.execute("DELETE FROM tbl_user WHERE user_id=%s", (id,))
			conn.commit()
			resp = jsonify('User deleted successfully!')
			resp.status_code = 200
			return resp
		except Exception as e:
			print(e)
		finally:
			cursor.close() 
			conn.close()
		
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp
	
		
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5000"))