from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date_created = db.Column(db.DateTime , nullable=False, default = datetime.now(timezone.utc))
    
    def __repr__(self):
        return f"{self.id} - {self.title}"

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/', methods = ['GET', 'POST'])
def home():
    if request.method== "POST":
        # print("POST->")
        # print(request.form['todoTitle'])
        title = request.form['todoTitle']
        description= request.form['todoDescription']
        todo = Todo(title=title, description=description)
        db.session.add(todo)
        db.session.commit()
        title = ''
        description = ''
    allTodos = Todo.query.all()
    return render_template('index.html', allTodos=allTodos)
    # return render_template('index.html')

@app.route('/delete/<int:id>')
def delete(id):
    todo = Todo.query.filter_by(id=id).first()
    if todo:
        db.session.delete(todo)
        db.session.commit()
        return redirect('/')
        # return f"Deleted this id :{id} data."
    else:
        return redirect('/')
        # return f"Todo is not found --- id :{id}."

@app.route('/update/<int:id>', methods = ['GET','POST'])
def update(id):
    if request.method == 'POST':
        title = request.form['todoTitle']
        description= request.form['todoDescription']
        todo = Todo.query.filter_by(id = id).first()
        todo.title = title
        todo.description = description 
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
        
    todo = Todo.query.filter_by(id = id).first()
    
    return render_template('update.html', todo = todo)

if __name__ == '__main__':
    app.run(debug=True, port=8000)