from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    body = db.Column(db.String(255))
    

    def __init__(self, title):
        self.title = title
        self.completed = False


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        return render_template('addblog.html',title="Build-a-Blog")

    blogs = Blog.query.filter_by(completed=False).all()
    completed_blogs = Blog.query.filter_by(completed=True).all()
    return render_template('blogs.html',title="Build-a-Blog", 
        blogs=blogs)

@app.route('/add-blog', methods=['POST'])
def add_blog():
    blog_title = request.form['blog']
    new_blog = Blog(blog_title)
    db.session.add(new_blog)
    db.session.commit()
    return redirect('/')

@app.route('/delete-blog', methods=['POST'])#REVISIT to correctly Delete
def delete_blog():

    blog_id = int(request.form['blog-id'])
    blog = Blog.query.get(blog_id)
    db.session.add(blog)
    db.session.commit()

    return redirect('/')


if __title__ == '__main__':
    app.run()