from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow())

    def __repr__(self):
        return '<Task %r>' %self.id


@app.route('/testing')
def helloWorld():
    return "<h>Hello World!</h>"


@app.route('/', methods =['POST','GET'])
def mainPage():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = ToDo(content=task_content)

        try:
            db.session.add (new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "Issue with adding task"

    else:
        tasks = ToDo.query.order_by(ToDo.date_created).all()
        return render_template("index.html", tasks = tasks)


if __name__ == "__main__":
    app.run(debug=True)
