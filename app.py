from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#db = SQLAlchemy()
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"

db = SQLAlchemy(app)

class todo(db.Model):
    Sno=db.Column(db.Integer,primary_key=True)
    Task=db.Column(db.String(200),nullable=False)
    Explanation=db.Column(db.String(1000),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.Sno} -{self.Task}"

@app.route("/",methods=['GET','POST'])
def index():
    if request.method=="POST":
        Task=request.form['Task']
        Explanation=request.form['Explanation']
        Todo=todo(Task=Task,Explanation=Explanation)
        db.session.add(Todo)
        db.session.commit()
    allTodo=todo.query.all()
    print(allTodo)
    return render_template("index.html", allTodo=allTodo)
    # return render_template("index.html");
    #return "Index!"


@app.route('/update<int:sno>',methods=['GET','POST'])
def update(sno):
    if request.method == 'POST':
        Task=request.form['Task']
        Explanation=request.form['Explanation']
        Todo=todo.query.filter_by(Sno=sno).first()
        Todo.Task=Task
        Todo.Explanation=Explanation
        db.session.add(Todo)
        db.session.commit()
        return redirect('/')
    Todo=todo.query.filter_by(Sno=sno).first()
    return render_template('update.html',Todo=Todo)

@app.route('/delete<int:sno>')
def delete(sno):    
    Todo=todo.query.filter_by(Sno=sno).first()
    db.session.delete(Todo)
    db.session.commit()
    return redirect ('/')


if __name__ == "__main__":
    app.run(debug=True)
