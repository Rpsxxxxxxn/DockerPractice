import flask
from datetime import timedelta 
from crypt import methods
from flask import jsonify, session, render_template,request, url_for, redirect
import mysql.connector

app = flask.Flask(__name__)
app.secret_key = 'XXXXXXXXXXXXXXXXXXXXXX'
app.permanent_session_lifetime = timedelta(minutes=60) 

# データベース接続設定
# host='mysql-service',
# port='3306',
# user='guest',
# password='1qazaq!',
# database='project_db'
db_config = {
  'host': 'mysql-service',
  'user': 'guest',
  'password': '1qazaq!',
  'database': 'project_db'
}

# root処理
@app.route("/", methods=["GET"])
def index():
  return "<h1>ようこそ</h1>"

# login処理
@app.route("/login", methods=["GET", "POST"])
def login():
  if request.method == "GET":
    session["name"]="name"
    return render_template("login.html", title="test", name="ore")
  elif request.method == "POST":
    email = request.form.get("email")
    password = request.form.get("password")
    
    # データベースへ接続
    conn = mysql.connector.connect(**db_config)
    app.logger.info("MySQLConnectionInfo: %s", conn.is_connected())

    if conn.is_connected() == True:
      cursor = conn.cursor()
      cursor.execute("select * from user")
      rows = cursor.fetchall()
      cursor.close()
      conn.close()
      print(rows)
    
    return render_template("login.html", title=email, name=password)

# 登録画面
@app.route("/regist_user", methods=["GET", "POST"])
def regist_user():
  if request.method == "GET":
    return render_template("regist_user.html")
  elif request.method == "POST":
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    
    conn = mysql.connector.connect(**db_config)
    if conn.is_connected() == True:
      try:
        sql = "insert into user(username, email, password) values(%s, %s, %s);"
        cursor = conn.cursor()
        cursor.executemany(sql, [(username, email, password)])
        conn.commit()
        cursor.close()
        conn.close()
      except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
    return redirect(url_for("login"))


# topページ
@app.route("/top", methods=["GET"])
def top():
  if request.method == "GET":
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.connect()
    cursor.close()
    conn.close()
    return render_template("top.html")

# init
if __name__ == "__main__":
  app.run(host="0.0.0.0", port=80, debug=True)