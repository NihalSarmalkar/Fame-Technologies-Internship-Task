from flask import Flask ,render_template,url_for
from flask.globals import current_app, request
from werkzeug.utils import redirect
from flask_mysqldb import MySQL

app=Flask(__name__)

app.config['MYSQL_HOST']="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]=""
app.config["MYSQL_DB"]="users"

mysql=MySQL(app)





@app.route('/',methods=['POST','GET'])
def index():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        cur = mysql.connection.cursor()
        user=cur.execute("SELECT password, username FROM users_table WHERE username=%s and password=%s ",(username,password))
        data=cur.fetchall()

        
        count=0
        for i in range(len(data)):
        

            if(password==str(data[i][0])):
    
                count=count+1
            else:

                print("no")

        if count >=1:
            return redirect(url_for('.profile', username=username))
        else:
            return redirect('/')
    else:
        return render_template('index.html')


@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']

        cur=mysql.connection.cursor()

        cur.execute("INSERT INTO users_table(username,password) VALUES(%s,%s)",(username,password))
        mysql.connection.commit()
        cur.close()

        return redirect('/')

    else:
        return render_template('Sign up.html')

@app.route('/profile/<string:username>',methods=['POST','GET'])
def profile(username):
    user=username
    

    


    return render_template('profile.html',username=user)

if __name__ == "__main__":
    app.run(debug=True)