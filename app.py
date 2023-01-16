from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///blog.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
db = SQLAlchemy(app)

class Article(db.Model):
    id= db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    intro = db.Column(db.String(300), nullable = False)
    title = db.Column(db.String(100), nullable = False)
    text = db.Column(db.Text, nullable = False)
    date = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/create', methods = ['POST','GET'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        article = Article(title= title, intro = intro, text=text, name = name)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/home')
        except:
            return 'При добавлении статьи произошла ошибка'
        pass
    else:
        return render_template('create.html')


@app.route('/home')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all() #или first если нужна первая запись
    return render_template("index.html", articles = articles)

@app.route('/home/<int:id>')
def delete(id):
    article = Article.query.get(id)
    return render_template("delete.html", article = article)

@app.route('/posts/<int:id>/delete')
def post_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect("/home")
    except:
        return "ПРИ УДАЛЕНИИ СТАТЬИ ПРОИЗОШЛА ОШИБКА"


@app.route('/home/<int:id>/update', methods = ["POST","GET"])
def post_update(id):
    article = Article.query.get(id)
    if request.method == "POST":
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']


        try:
            db.session.add(article)
            db.session.commit()
            return redirect("/home")
        except:
            return "ПРИ РЕДАКТИРОВАНИИ СТАТЬИ ПРОИЗОШЛА ОШИБКА"
    else:
        article = Article.query.get(id)
        return render_template('update.html', article=article)


if __name__=='__main__':
    app.run(debug=True)