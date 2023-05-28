from flask import Flask,render_template,request,redirect,url_for
import pymongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['SECRET_KEY']='921f7eded1fb9a9fb71118ed8e0162047b8a71e753d667ccd3a53486a445821d'
client=pymongo.MongoClient('mongodb://localhost:27017')
db=client['TODO_List']
collection=db['todos']

@app.route("/")
def home():
    todos_lst=collection.find()
    return render_template("index.html",todos_lst=todos_lst)

@app.route("/add",methods=['POST','GET'])
def add():
    if request.method=='POST':
        new_task=request.form.get('task')
        collection.insert_one({
            "task":new_task
        })
        return redirect(url_for('home'))

@app.route("/delete/<id>")
def delete(id):
    find_todo=collection.find_one({'_id':ObjectId(id)})
    collection.delete_one(find_todo)
    return redirect(url_for('home'))

@app.route("/update/<id>")
def update(id):
    return render_template("update.html",id= ObjectId(id))

@app.route("/updated_todo/<id>",methods=['POST','GET'])
def updated_todo(id):
    updated_task=request.form.get('updated_task')
    prev_todo={'_id':ObjectId(id)}
    updated_todo={'$set':{'task':updated_task}}
    collection.update_one(prev_todo,updated_todo)
    return redirect(url_for('home'))


if __name__=="__main__":
    app.run(debug=True)