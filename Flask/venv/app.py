#For deployment -> pip3 freeze > requirements.txt for the version requirements of library dependencies
#need to add a Procfile for gunicorn deployment - web: gunicorn app:"app name here"

from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#Set variable app as a Flask object
app = Flask(__name__)

#keyword SQLALCHEMY_DATABASE_URI used to configurate the flask object's database identifier to be sqlite using the name "test"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
#create a sqlaclchemy object with the configuration of app as the flask object
db = SQLAlchemy(app)

#create the "ToDo" database for sqlite
class ToDo(db.Model):
    #all the different attributes of the ToDo table with ID as the primary string
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow())

    #when object represented as a string, return the string for the task ID
    def __repr__(self):
        return '<Task %r>' %self.id

#keyword to create a directory called testing for this webserver. Default set to only allow GET requests
@app.route('/testing')
def helloWorld(): #contents of the testing page
    return "<h>Hello World!</h>"

#home directory allowing both POST and GET Requests
@app.route('/', methods =['POST','GET'])
def mainPage():
    #if the Flask object detects a POST request
    if request.method == 'POST':
        #save the contents of the html form attribute named "content"
        task_content = request.form['content']
        #create a "ToDo" table object using task_content as the content column
        #other two columns are automatically generated
        new_task = ToDo(content=task_content)

        #add the ToDo table object to the sqlite database
        try:

        #db = SQL alchemy object referencing SQLlite database test.db. Session creates a temporary place holder for queries
        #adding new task ToDo table column to temporary placeholder
        #commiting data from placeholder into actual test.db database
            db.session.add (new_task)
            db.session.commit()
        #return to the home directory
            return redirect('/')
        except:
            return "Issue with adding task"

    else:
        #if the request is not POST
        #get all the rows from test.db ordered by datacreated column
        tasks = ToDo.query.order_by(ToDo.date_created).all()
        #return to GET requester the html+CSS template with the list of tasks for the html to render
        return render_template("index.html", tasks = tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = ToDo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem with deleting the task"

@app.route('/update/<int:id>', methods = ['POST', 'GET'])
def update(id):

    task_to_update = ToDo.query.get_or_404(id)

    if request.method == 'POST':
        task_to_update.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was a problem with updating the task"

    else:
        return render_template('update.html',task = task_to_update)

if __name__ == "__main__":
    app.run(debug=True)
