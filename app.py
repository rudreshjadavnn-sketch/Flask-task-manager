from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from bson.objectid import ObjectId
import jwt
import datetime
import bcrypt

app=Flask(__name__)
app.config["SECRET_KEY"]="mysecretkey"

client=MongoClient("mongodb://localhost:27017/")
db=client["mydatabase"]
users_collection=db["users"]
tasks_collection=db["tasks"]

@app.route("/")
def home():
    return render_template("index.html")
@app.route("/loginpage")
def loginpage():
    return render_template("login.html")
@app.route("/dashboard")
def dasboard():
    return render_template("dashboard.html")

@app.route("/index", methods=["POST"])
def register():
    data=request.json
    name=data.get('name')
    email=data.get('email')
    password=data.get('password')

    hashed_password = bcrypt.hashpw(
    password.encode('utf-8'),
    bcrypt.gensalt()
    )

    users_collection.insert_one({
        "name":name,
        "email":email,
        "password":hashed_password
    })

    return jsonify({
        "meassage":"Register success"
    })

@app.route("/login", methods=["POST"])
def login():
    data=request.json
    email=data.get('email')
    password=data.get('password')

    user=users_collection.find_one({
        "email":email
    })

    if user:
        if bcrypt.checkpw(
            password.encode('utf-8'),
            user['password']
            ):
            token = jwt.encode({
                "email": email,
                "name": user["name"],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
                }, app.config["SECRET_KEY"], algorithm="HS256")
            return jsonify({
                "meassage":"Login success",
                "token": token,
                "name": user["name"],
                "email": email
                })
        else:
            return jsonify({
                "meassage":"Wrong password"
                })
    else:
        return jsonify({
            "meassage":"User not found"
        })

@app.route("/addtask", methods=["POST"])
def addtask():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({
            "message":"Unauthorized"
        }), 401

    decoded = jwt.decode(
        token,
        app.config["SECRET_KEY"],
        algorithms=["HS256"]
    )

    email = decoded["email"]
    data = request.json
    name = data.get('name')
    subj = data.get('subj')
    tasks_collection.insert_one({
        "email": email,
        "taskname": name,
        "subj": subj
    })

    return jsonify({
        "message":"Task Added"
    })

 
@app.route("/gettask", methods=["POST"])
def gettasks():

    token = request.headers.get("Authorization")

    if not token:

        return jsonify({
            "message":"Unauthorized"
        }), 401

    decoded = jwt.decode(
        token,
        app.config["SECRET_KEY"],
        algorithms=["HS256"]
    )

    email = decoded["email"]
    tasks = list(tasks_collection.find({
        "email": email
    }))

    result=[]

    for task in tasks:

        result.append({
            "id": str(task["_id"]),
            "name": task["taskname"],
            "subj": task["subj"]
        })

    return jsonify(result)

@app.route("/deletetask", methods=["POST"])
def deletetask():

    token = request.headers.get("Authorization")

    if not token:

        return jsonify({
            "message":"Unauthorized"
        }), 401

    decoded = jwt.decode(

        token,

        app.config["SECRET_KEY"],

        algorithms=["HS256"]
    )

    data = request.json

    taskid = data.get("taskid")

    tasks_collection.delete_one({
        "_id": ObjectId(taskid),
        "email": decoded["email"]
    })

    return jsonify({
        "message":"Task Deleted"
    })

if __name__=="__main__":
    app.run(debug=True,port=5000)