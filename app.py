from flask import Flask, render_template, redirect, request, session
from data import Articles
import pymysql
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)

db = pymysql.connect(
    host='localhost',
    user='root',
    password='1234',
    db='gangnam',
    charset='utf8mb4')

cur = db.cursor()

def is_loged_in(f):
    @wraps(f) 
    def _wraps(*args, **kwargs):
        if 'is_loged' in session :
            return f(*args,**kwargs) #다음 함수로 넘어가게 해주는 기능
        else:
            return render_template('home.html')
    return _wraps
    

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        username=request.form['username']
        password=request.form['password']
        password = sha256_crypt.encrypt(password)
        # print(password)
        # print(sha256_crypt.verify("1234", password))        
        sql=f"SELECT email FROM users WHERE email='{email}' ;"
        cur.execute(sql)
        db.commit()
        user_email=cur.fetchone()
        if user_email==None:
            query =f"INSERT INTO users (name , email , username, password) VALUES ('{name}', '{email}', '{username}' , '{password}');"
            cur.execute(query)
            db.commit()
            return redirect('/') ###########################
        else :
            return redirect('/register')
    else :
        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        query=f"SELECT * FROM users WHERE email='{email}' ;"
        cur.execute(query)
        db.commit()
        user=cur.fetchone()
               
        if user==None :
            return redirect('/login')

        else :
            if sha256_crypt.verify(password, user[4]) :
                session['is_loged']=True
                session['email']=user[2]
                session['username']=user[3]
                print(session)
                return redirect('/')
            else :
                return redirect('/login')
    
    else :
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return render_template('home.html')

@app.route('/', methods=['GET', 'POST'])
@is_loged_in
def hello_world():
    return render_template('home.html', user_name=session['username'])


@app.route('/about', methods=['GET', 'POST'])
@is_loged_in
def about():
    return render_template('about.html', user_name=session['username'])


@app.route('/articles', methods=['GET', 'POST'])
@is_loged_in
def articles():
    # articles = Articles()
    query = 'SELECT * FROM topic ;'
    cur.execute(query)
    db.commit()

    articles = cur.fetchall()  # 조회
    print(articles)
    return render_template("articles.html", articles=articles, user_name=session['username'])


# <> parameter 전달 하는 flask
@app.route('/article/<id>', methods=['GET', 'POST'])
@is_loged_in
def article(id):
    # articles=Articles()

    # print(len(articles))
    # if len(articles) >=int(id):
    #     article=articles[int(id)-1]
    #     return render_template('article.html', article = article)
    # else:
    #     return render_template('article.html', article = "NO DATA")
    query = f'SELECT * FROM topic WHERE id= {id};'
    cur.execute(query)
    db.commit()
    article = cur.fetchone()
    print(article)
    if article == None:
        return redirect('/articles')
    else:
        return render_template('article.html', article=article, user_name=session['username'])


# @app.route('/add_article', methods=['GET'])
# def add_article():
#     return render_template('add_article.html')


@app.route('/add_article', methods=['GET','POST'])
@is_loged_in
def add_articles():
    if request.method=='POST' :
        title = request.form['title']
        description = request.form['description']
        author = request.form['author']
        
        # return render_template('add_article.html')

        query='INSERT INTO `topic` (`title`, `description`, `author`) VALUES (%s, %s, %s) ;'
        input_data=[title,description,author]
        cur.execute(query, input_data)
        db.commit()
        print(cur.rowcount)
        return redirect("/articles")

    else :
        return render_template('add_article.html', user_name=session['username'])


@app.route('/article/<id>/delete')
@is_loged_in
def delete_artice(id):
    query = f'DELETE FROM `gangnam`.`topic` WHERE id={id} ;'
    cur.execute(query)
    db.commit()
    # db.close()
    return redirect('/articles')

@app.route('/article/<id>/edit', methods=['GET','POST'])
@is_loged_in
def edit_article(id):
    if request.method=='POST':
        title=request.form['title']
        description=request.form['description']
        author=request.form['author']
        query=f"UPDATE `gangnam`.`topic` SET `title`='{title}', `description` = '{description}',`author`='{author}' WHERE (`id` = {id}) ;"
        cur.execute(query)
        db.commit()
        return redirect('/articles')        

    else :        
        query=f'SELECT * FROM topic WHERE id={id} ;'
        cur.execute(query)
        db.commit()
        article=cur.fetchone()
        return render_template('edit_article.html',article=article, user_name=session['username'])

@app.route('/admin', methods=['GET','POST'])
@is_loged_in
def admin():
    if session['username']=="admin" :
        query="SELECT * FROM gangnam.users ;"
        cur.execute(query)
        db.commit()
        members=cur.fetchall()
        return render_template("admin.html", members=members, user_name=session['username'])

    else :
        message="관리자 권한입니다."
        return render_template('home.html', message=message, user_name=session['username'])



if __name__ == '__main__':
    app.secret_key="gangnamStyle"
    app.run(debug=True)
    
