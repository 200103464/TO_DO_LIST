from hashlib import scrypt
from flask import Flask, jsonify,render_template, url_for,request,redirect,flash
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="postgresql://postgres:qwerty@localhost:5432/todoproject"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)
app.secret_key = 'secret key 111111'
migrate = Migrate(app, db)
class Todo(db.Model):
    __tablename__='todo'
    id=db.Column(db.Integer, primary_key=True)
    content=db.Column(db.String(200), nullable=False)
    completed=db.Column(db.Integer , default=0)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)
    
    due_date = db.Column(db.Date, nullable=True) 
    days_left = db.Column(db.Integer, nullable=True) 

    def __repr__(self):
        return f"<Task {self.id}>"
    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'completed': self.completed,
            'date_created': self.date_created,
            'deadline': self.due_date,
            'days_left': self.days_left
        }
class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    """ def __init__(self, email, password):
        self.email = email
        self.password = scrypt.generate_password_hash(password)
        self.created_on = datetime.now()"""
        
    
    def __repr__(self):
        return f"<email {self.email}>"


    

@app.route('/', methods=['POST','GET'])
def index():

    if request.method=='POST':
        task_content=request.form['content']
        deadline=request.form['due_date']
        deadline = datetime.strptime(deadline, '%Y-%m-%d').date()
        days_left = (deadline - datetime.today().date()).days

        new_task=Todo(content=task_content,due_date=deadline,days_left=days_left)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "there was a problem adding your task"


    else:
        tasks=Todo.query.order_by(Todo.date_created).all()

        return render_template('index.html',tasks=tasks)
    
@app.route('/toggle/<int:id>', methods=['POST'])
def toggle(id):
    task = Todo.query.get_or_404(id)
    task.completed = 0 if task.completed else 1
    
    db.session.commit()
    return redirect('/')
    

@app.delete('/delete/<int:id>')
def delete(id):
    task_to_delete=Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "there was a problem deleting that task"


@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    task=Todo.query.get_or_404(id)
    if request.method=='POST':
        task.content=request.form['content']
        deadline=request.form['due_date']
        deadline = datetime.strptime(deadline, '%Y-%m-%d').date()
        task.due_date=deadline
        
        task.days_left = (deadline - datetime.today().date()).days
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "there was a problem updating that task"
    else:
        return render_template('update.html',task=task)
    




#to test with postman 

@app.route('/all_tasks', methods=['POST','GET'])
def all_tasks():

    if request.method=='POST':
        if request.is_json:
            data=request.get_json()
            task_content=data.get('content')
            new_task=Todo(content=task_content)
            if not task_content:
                return jsonify({'error': 'Task content is required'}), 400
        try:
            db.session.add(new_task)
            db.session.commit()
            return jsonify({"message":f" task {new_task.content} has been created succesfully", 
                            "task":new_task.to_dict()}), 201
        except:
            return jsonify({"error":"The request isn't JSON format"}), 500


    else: 
        tasks = Todo.query.order_by(Todo.date_created).all()

        return jsonify({'tasks': [task.to_dict() for task in tasks]})
    


@app.route('/deletepostman/<int:id>',methods=["DELETE"])
def deletepostman(id):
    task_to_delete=Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return jsonify({"message":f"task {id} is deleted",
                        "deleted task":{"id":task_to_delete.id,
                                        "content":task_to_delete.content}}), 200
    except:
        return jsonify({"error":"The request isn't JSON format"}), 500
        


@app.route('/updatepostman/<int:id>', methods=['PUT'])
def updatepostman(id):
    
    if request.method=='PUT':
        task=Todo.query.get_or_404(id)
        data=request.get_json()
        content = data.get('content')
        deadline = data.get('due_date')

        if not content or not deadline:
            return jsonify({'error': 'Content and deadline are required'}), 400
        

        try:
            deadline=datetime.strptime(deadline, '%Y-%m-%d').date()
            task.content=content
            task.deadline=deadline
            task.days_left = (deadline - datetime.today().date()).days

            db.session.commit()

            return jsonify({"message":f" task {task.content}  is updated", 
                            "task":task.to_dict()}), 200
        except:
            return jsonify({"error":"The request isn't JSON format"}), 500
        






"""@app.route('/')
def index():
    return "Flask is working with PostgreSQL!"
"""

@app.route("/register", methods=["POST","GET"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        error = None

        if not email:
            error = "Email address is required."
        elif not password:
            error = "Password is required."

        if error is None:
            try:
                
                new_user = User(email=email, password=password)
                db.session.add(new_user)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                error = f"Email address {email} is already registered."
            else:
                return redirect(url_for("login"))

        flash(error)

    return render_template("register.html")

@app.route("/registerpostman", methods=["POST"])
def registerpostman():
    if request.method == "POST":
        data=request.get_json()
        email = data.get("email")
        password = data.get("password")
        error = None

        if not email:
            error = "Email address is required."
        elif not password:
            error = "Password is required."

        if error is None:
            try:
                
                new_user = User(email=email, password=password)
                db.session.add(new_user)
                db.session.commit()
                return jsonify({"message":f"{new_user.email} registered succesfully"}), 201
            except Exception as e:
                db.session.rollback()
                error = f"Email address {email} is already registered."
                return jsonify({"error": error}), 400
            
        return jsonify({"error": error}), 400
        

@app.route("/login", methods=["POST","GET"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        error = None
        user = User.query.filter_by(email=email).first()

        if user is None:
            error = 'User is not found '
        elif user.password != password:
            error = 'Incorrect password.'

        if error is None:

            return redirect(url_for('index'))
           
        print(error)

    return render_template('login.html')

@app.route('/loginpostman', methods=['GET'])
def loginpostman():
    users = User.query.all()

   
    users_data = []
    for user in users:
        users_data.append({
            "id": user.id,
            "email": user.email,
            "password":user.password
        })

    return jsonify(users_data), 200


@app.route('/logout')
def logout():
    db.session.clear()
    return redirect(url_for('login'))
    
    
if __name__=="__main__":
    app.run(debug=True)