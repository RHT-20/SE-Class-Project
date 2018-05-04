from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import MySQLdb

app = Flask(__name__)

mysql = MySQL(app)
conn = MySQLdb.connect(host="localhost", user="root", password="rht20", db="Future_Tech_Software_Company")
mysql.init_app(app)


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/sign_up_form')
def sign_up_form():
    return render_template("sign_up_form.html",
                           message="",
                           name="Name", email="Email", mobile="Mobile No",
                           address="Address", dob="Date of Birth")


@app.route('/sign_up_response', methods=['POST'])
def sign_up_response():

    u_name = request.form['InputName']
    u_email = request.form['InputEmail']
    u_mobile = request.form['InputMobile']
    u_address = request.form['InputAddress']
    u_dob = request.form['InputDOB']

    if request.method == 'POST':

        if u_name == "" or u_email == "" or u_mobile == "" or u_address == "" or u_dob == "":
            return render_template("sign_up_form.html",
                                   message="*Please fill up all the fields",
                                   name="Name", email="Email", mobile="Mobile No",
                                   address="Address", dob="Date of Birth")

        cur = conn.cursor()
        cur.execute("SELECT * FROM Employee WHERE email = (%s)", (u_email,))
        data = cur.fetchall()

        print(data)

        if not data:
            cur.execute("INSERT INTO Employee(name, email, mobile, address, birth_date)"
                        " VALUES(%s, %s, %s, %s, %s)",
                            (u_name, u_email, u_mobile, u_address, u_dob))

            return str("Welcome")

        else:
            return render_template("sign_up_form.html",
                                   message="*Email address already in use",
                                   name="Name", email="Email", mobile="Mobile No",
                                   address="Address", dob="Date of Birth")

        cur.execute("SELECT * FROM Employee WHERE email = (%s)", (u_email,))
        data = cur.fetchall()
        return str(data)


@app.route('/sign_in_form')
def sign_in_form():
    return render_template("sign_in_form.html",
                           email="Email", password="Password")


@app.route('/sign_in_response')
def sign_in_response():
    u_email = request.form['InputEmail']
    u_password = request.form['InputPassword']

    if request.method == 'POST':

        if u_email == "" or u_password == "":
            return render_template("sign_in_form.html",
                                   message="*Invalid email address or password",
                                   email="Email", password="Password")

        cur = conn.cursor()
        cur.execute("SELECT * FROM Employee WHERE email = (%s)", (u_email,))
        data = cur.fetchall()

        print(data)

        if not data:
            return render_template("sign_in_form.html",
                                   message="*Invalid email address or password",
                                   email="Email", password="Password")

        else:
            return str("Welcome")


if __name__ == '__main__':
    app.run()
