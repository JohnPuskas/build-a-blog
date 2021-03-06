from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import pymysql

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blogger@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    body = db.Column(db.String(255))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/blog', methods=['POST', 'GET'])
def index():
    
    blog_id = request.args.get('id')

    if blog_id == None:
        blogs = Blog.query.all()

        return render_template('/blogs.html', blogs=blogs)
        
    else:
        blog_id_int= int(blog_id)
        blog = Blog.query.get(blog_id_int)

        return render_template('/blogdisplay.html',
            blog=blog)    
    

@app.route('/newpost')
def display_add_blog():
   
    return render_template('addblog.html')

    
@app.route('/newpost', methods=['POST'])
def add_blog():

    title = request.form['title']
    body = request.form['body']
    title_error = ''
    body_error = ''

    if title == '':
        title_error = "Please fill in the title"
        

    if body == '':
        body_error = "Please fill in the body"
    

    if title_error or body_error:
        return render_template('addblog.html',
            title_error = title_error,
            body_error = body_error,
            title = title,
            body = body)

    else:
        new_blog = Blog(title, body)
        db.session.add(new_blog)
        db.session.commit()      
        
        new_blog_id = new_blog.id

        return redirect("/blog?id={0}".format(new_blog_id))



if __name__ == '__main__':
    app.run()