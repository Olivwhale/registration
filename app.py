from flask import Flask, render_template, redirect, request
import psycopg2 

app=Flask(__name__)

@app.route('/',methods=['GET'])
def ref():
    return redirect("/login/")

@app.route('/login/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get("login"):
            errors=""
            login = request.form.get('username').strip()
            if login == "":
                errors += "введите логин,вместо пустой строки <br>"
            password = request.form.get('password').strip()
            if password == "":
                errors += "введите пароль,вместо пустой строки <br>"
            if errors != "" :
                return errors 
            conn = psycopg2.connect(database = "service",
                                    user="postgres",
                                    password="112233",
                                    host="localhost",
                                    port="5432")
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM users.user WHERE login=%s and password=%s",
            (str(login), str(password)))
            records = cursor.fetchall()
            if len(records)!=0:   
                return render_template('account.html', full_name = records[0][0])
            else: 
                return "Введите пароль или логин заново" 
        if request.form.get("registration"):
            return redirect("/registration/")
    return render_template('login.html')


@app.route('/registration/', methods=['GET', 'POST'])
def index2():
    if request.method == 'POST':
        errors = ""
        name = request.form.get('name') 
        if name == "":
            errors+="введите имя,вместо пустой строки <br>"
        password = request.form.get('password').strip()
        if password == "":
            errors+= "введите пароль,вместо пустой строки <br>"      
        login = request.form.get('login').strip()
        if login == "":
            errors+="введите логин,вместо пустой строки <br>"
        if errors != "" :
            return errors 
        conn = psycopg2.connect(database = "service",
                                user="postgres",
                                password="112233",
                                host="localhost",
                                port="5432")
        cursor = conn.cursor()
        cursor.execute(("INSERT INTO users.user (name, login, password) VALUES (%s, %s, %s)"),
        (str(name), str(login), str(password)))
        conn.commit()
        return redirect("/login/")
    return render_template('registration.html')
    