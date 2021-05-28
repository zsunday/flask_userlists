from flask import Flask, render_template
from data import Articles

app=Flask(__name__)


@app.route('/',methods=['GET','POST'])
def hello_world():
    return render_template('home.html',name="HOME")

@app.route('/about',methods=['GET','POST'])
def about():
    return render_template('about.html',name="ABOUT")

@app.route('/articles',methods=['GET','POST'])
def articles():
    articles = Articles()
    return render_template( "articles.html", articles = articles )

@app.route('/article/<id>',methods=['GET','POST'])
def article(id):
    articles=Articles()
    print(len(articles))
    if len(articles) >=int(id):
        article=articles[int(id)-1]
        return render_template('article.html', article = article)
    else:
        return render_template('article.html', article = "NO DATA")

@app.route('/add_article',methods=['GET','POST'])
def add_article():
    return render_template('add_article.html')

if __name__=='__main__':
    app.run(debug=True)