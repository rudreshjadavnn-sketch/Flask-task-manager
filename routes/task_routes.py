from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId

from database import tasks_collection
from middleware.auth import verify_token

task_bp = Blueprint("task", __name__)

@task_bp.route("/addtask", methods=["POST"])
def add_task():

    decoded, error, status = verify_token()

    if error:
        return error, status

    data = request.json

    name = data.get("name")
    subj = data.get("subj")

    if not name or not subj:

        return jsonify({
            "message": "All fields required"
        }),400

    tasks_collection.insert_one({

        "email": decoded["email"],

        "taskname": name,

        "subj": subj

    })

    return jsonify({

        "message":"Task Added"

    }),201

@task_bp.route("/gettask", methods=["POST"])
def get_task():

    decoded, error, status = verify_token()

    if error:
        return error, status

    tasks = list(tasks_collection.find({

        "email": decoded["email"]

    }))

    result=[]

    for task in tasks:

        result.append({

            "id": str(task["_id"]),

            "name": task["taskname"],

            "subj": task["subj"]

        })

    return jsonify(result),200

@task_bp.route("/updatetask", methods=["POST"])
def update_task():

    decoded, error, status = verify_token()

    if error:
        return error, status

    data = request.json

    taskid = data.get("taskid")

    name = data.get("name")

    subj = data.get("subj")

    tasks_collection.update_one(

        {

            "_id": ObjectId(taskid),

            "email": decoded["email"]

        },

        {

            "$set":{

                "taskname":name,

                "subj":subj

            }

        }

    )

    return jsonify({

        "message":"Task Updated"

    }),200

@task_bp.route("/deletetask", methods=["POST"])
def delete_task():

    decoded, error, status = verify_token()

    if error:
        return error, status

    data=request.json

    taskid=data.get("taskid")

    tasks_collection.delete_one({

        "_id":ObjectId(taskid),

        "email":decoded["email"]

    })

    return jsonify({

        "message":"Task Deleted"

    }),200

