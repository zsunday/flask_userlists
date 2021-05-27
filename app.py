from flask import Flask, render_template

app=Flask(__name__)


@app.route('/',methods=['GET','POST'])
def hello_world():
    return render_template('home.html',name="황지선")

if __name__=='__main__':
    app.run(debug=True)