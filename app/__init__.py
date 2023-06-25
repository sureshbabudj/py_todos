from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config[
    "SECRET_KEY"
] = "vkabascdsabdkajsbckdjsabkcdjsureur"  # Set a secret key for sessions
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "sqlite:///todos.sqlite"  # Specify the SQLite database URI
db = SQLAlchemy(app)


class Todo(db.Model):
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(255), nullable=False)


@app.route("/")
def index():
    todos = Todo.query.all()
    return render_template("index.html", todos=todos)


@app.route("/add", methods=["GET", "POST"])
def add_todo():
    todo = request.form["todo"]
    new_todo = Todo(task=todo)
    db.session.add(new_todo)
    db.session.commit()
    return redirect("/")


@app.route("/delete/<int:todo_id>", methods=["POST"])
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


with app.app_context():
    db.create_all()  # Create the database tables
