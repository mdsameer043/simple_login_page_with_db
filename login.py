from flask import Flask,render_template,request
from sqlalchemy import create_engine,text
app = Flask(__name__)


db_connection="mysql+pymysql://14bbo2hcgkaai42wovbv:pscale_pw_XVmQyzSLTTIy2rx0tJudh5TttPkCsztpFBIROTfko8a@ap-south.connect.psdb.cloud/smd?charset=utf8mb4"
engine= create_engine(db_connection,connect_args={
    "ssl":{
        "ssl_ca": "/etc/ssl/cert.pem"   
    }
})
def load_database(email,password,number):
    if number==0:
        with engine.connect() as conn:
            db_result=conn.execute(text("select * from emailpassword"))
            result=db_result.all()
            jobs=[]
            for row in result:
                jobs.append(dict(row))
            return jobs  
        
    elif number==1:
        with engine.connect() as conn:
            db_result=conn.execute(text(f"select * from emailpassword where email='{email}'"))
            result=db_result.all()
            result=dict(result)
            return result.get(email)
        
    else:
        with engine.connect() as conn:
            db_result=conn.execute(text(f"insert into emailpassword values('{email}','{password}')"))
            return "successful"

# database=load_database(0,0,1)
# print(database[0]['email'])
# print(database[0]['password'])
# print(load_database('mmoulana443@gmail.com','78627863k',1))



@app.route("/")
def login():
    return signup()


@app.route("/signup", methods=['GET','POST'])
def signup():
    try:
        email=request.form['email']
        password=request.form['password']
        dbpassword=load_database(email,password,1)
        if password==dbpassword:
            return main_page()
        else:
            return render_template("signup_page.html",invalid="ab")
    except Exception as e:
        print(e)
    
    return render_template("signup_page.html")
    
    

@app.route("/signin", methods=['GET','POST'])
def signin():
    try:
        email1=request.form['email']
        password1=request.form['password']
        if len(password1)>7:
            load_database(email1,password1,2)
            return render_template("signup_page.html")
        else:
            return render_template("signin_page.html",invalid="a")
    except Exception as e:
        print(e)
        
    return render_template("signin_page.html")


@app.route("/main_page", methods=['GET','POST'])
def main_page():
    return render_template("main_page.html",email="mmoulana706@gmail.com",password="78627863k")


if __name__=="__main__":
    app.run(debug=True)