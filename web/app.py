from email import message
import flask
import mysql.connector
from flask import jsonify, session, render_template, request, url_for, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from crypt import methods
from datetime import timedelta 

# ================================================
# 環境設定
# ================================================
app = flask.Flask(__name__)
app.secret_key = 'XXXXXXXXXXXXXXXXXXXXXX'
app.permanent_session_lifetime = timedelta(minutes=60)

# データベース接続設定
# host='mysql-service',
# port='3306',
# user='guest',
# password='1qazaq!',
db_config = {
  'host': 'mysql-service',
  'user': 'guest',
  'password': '1qazaq!',
  'database': 'project_db'
}

# ================================================
# アプリケーション
# ================================================

# root処理
@app.route("/", methods=["GET"])
def index():
  return redirect(url_for("login"))

# login処理
@app.route("/login", methods=["GET", "POST"])
def login():
  if request.method == "GET":
    return render_template("login.html", message="")

  elif request.method == "POST":
    email = request.form.get("email")
    password = request.form.get("password")
    
    conn = mysql.connector.connect(**db_config)
    app.logger.info("MySQLConnectionInfo: %s", conn.is_connected())

    try:
      conn = mysql.connector.connect(**db_config)
      cursor = conn.cursor(prepared=True)
      stmt = "SELECT * FROM user WHERE email = %s;"
      cursor.execute(stmt, (email,))
      row = cursor.fetchone()

      if row is not None:
        if check_password_hash(row[3], password):
          session["user"] = row
          return redirect(url_for("top"))
        else:
          return render_template("login.html", message="パスワードが違います。")
      else:
        return render_template("login.html", message="そのメールアドレスは登録されていません。")
    except mysql.connector.Error as err:
      print("Something went wrong: {}".format(err))
      return render_template("login.html", message="エラーが発生しました。")
    finally:
      cursor.close()
      conn.close()
    
    return render_template("login.html", message="")

# 登録画面
@app.route("/regist_user", methods=["GET", "POST"])
def regist_user():
  if request.method == "GET":
    return render_template("regist_user.html", message="")

  elif request.method == "POST":
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    password_confirm = request.form.get("check_password")

    if password != password_confirm:
      return render_template("regist_user.html", message="確認パスワードが違います。")

    password_hash = generate_password_hash(password)

    try:
      conn = mysql.connector.connect(**db_config)
      cursor = conn.cursor(prepared=True)

      stmt = "SELECT * FROM user WHERE email = ?"
      cursor.execute(stmt, (email,))
      row = cursor.fetchone()

      if row is not None:
        return render_template("regist_user.html", message="このメールアドレスは既に登録されています。")

      stmt = "insert into user(email, username, password) values(?, ?, ?);"
      cursor.execute(stmt, (email, username, password_hash))
      conn.commit()

    except mysql.connector.Error as err:
      conn.rollback()
      print("Something went wrong: {}".format(err))
      return render_template("regist_user.html", message="システムエラーが発生しました。")
    finally:
      cursor.close()
      conn.close()

    return redirect(url_for("login"))

# topページ
@app.route("/top", methods=["GET"])
def top():
  if request.method == "GET":
    if "user" in session:
      sql = " SELECT"
      sql += "  user.username, "
      sql += "  post_info.post_at,"
      sql += "  post_info.comment"
      sql += " FROM post_info"
      sql += "  INNER JOIN user"
      sql += "  ON user.email = post_info.email"
      sql += " ORDER BY"
      sql += "  post_info.post_at DESC"

      try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(prepared=True)
        cursor.execute(sql)
        list_data = cursor.fetchall()
      except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return render_template("regist_user.html", message="エラーが発生しました。")
      finally:
        cursor.close()
        conn.close()
      return render_template("top.html", list_data=list_data)
    else:
      return redirect(url_for("error_page"))
      

# ログアウト
@app.route("/logout", methods=["GET", "POST"])
def logout():
  if request.method == "GET":
    session.pop("user", None)
    session.clear()
    return redirect(url_for("login"))

# エラーページ
@app.route("/error", methods=["GET"])
def error_page():
  if request.method == "GET":
    return redirect(url_for("login"))
    # return render_template("error.html")

# 投稿ページ
@app.route("/post", methods=["GET", "POST"])
def post():
  if request.method == "GET":
    return render_template("post.html")
  elif request.method == "POST":
    if "user" in session:
      comment = request.form.get("comment")
      try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(prepared=True)
        cursor.execute("INSERT INTO post_info(email, comment) VALUES(?, ?)", (session["user"][1], comment))
        conn.commit()
      except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return render_template("post.html", message="エラーが発生しました。")
      finally:
        cursor.close()
        conn.close()
      return redirect(url_for("top"))
    else:
      return redirect(url_for("login"))

# init
if __name__ == "__main__":
  app.run(host="0.0.0.0", port=80, debug=True)