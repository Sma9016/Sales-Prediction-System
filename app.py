from flask import *
from predict import predict
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re



app=Flask(__name__)

app.config['SECRET_KEY']='abc'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'mini_project'

mysql = MySQL(app)

def graph(store):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM store WHERE store = %s',(store,))
    account=cursor.fetchone()
    num=account['store']
    result=account['result']

@app.route('/')
@app.route('/home',methods=['GET','POST'])
def home():
    message = ''
    if request.method == 'POST':
        name = request.form['uname']
        email = request.form['email']
        pswrd = request.form['pass']
        repswrd = request.form['cpass']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if pswrd!=repswrd:
            message = 'Please Enter the same Password'
            return render_template('register.html',message=message)
        elif not re.match(r'[^@]+@[^@]+\.[^@]',email):

            \


            
            message = 'Invalid email address !'
            return render_template('register.html',message=message)
        else:
            cursor.execute('SELECT * FROM admin WHERE email=%s',(email,))
            account = cursor.fetchone()
            if account:
                message = 'Username or Email Already Exists'
                return render_template('register.html',message=message)
            else:
                cursor.execute('INSERT INTO admin VALUES (%s,%s,%s)',(name,email,pswrd))
                mysql.connection.commit()
    return render_template('home.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/enter',methods=['GET','POST'])
def enter():
    if request.method=='POST':
        email=request.form['email']
        password = request.form['pass']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin WHERE email = %s and password = %s',(email,password))
        account=cursor.fetchone()
        if account:
            return render_template('main.html')
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')



@app.route('/dummy',methods=['POST'])
def dummy():
    if request.method=='POST':
        values=[1,2,3,4,5,6,7,8,0,0,0,12,0,0,0,0,0,0,0]
        values[0]=int(request.form['storeno'])
        values[1]=int(request.form['clothtype'])
        values[2]=int(request.form['assortment'])
        values[3]=int(request.form['competitiondistance'])
        values[4]=int(request.form['cosm'])
        values[5]=int(request.form['cosy'])
        values[6]=int(request.form['promo2'])
        values[7]=int(request.form['promo2sinceweek'])
        values[8]=int(request.form['dayinaweek'])
        values[9]=int(request.form['customers'])
        values[10]=int(request.form['storeopen'])
        values[11]=int(request.form['promo'])
        values[12]=int(request.form['stholiday'])
        values[13]=int(request.form['scholiday'])
        values[14]=int(request.form['sclothtype'])
        promointerval=request.form['promointerval']
        if promointerval==0:
            values[15]=1
        elif promointerval==1:
            values[16]=1
        elif promointerval==2:
            values[17]=1
        else:
            values[18]=1
        result=predict(values)
        result=int(result[0])
        store=str(values[0])
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO store VALUES (%s,%s)',(store,result))
        mysql.connection.commit()
        return render_template('result.html',result=result,store=store)


@app.route('/register')
def register():
    return render_template('register.html')


if __name__=='__main__':
    app.run(debug=True)