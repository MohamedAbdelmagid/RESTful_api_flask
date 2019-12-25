#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request, url_for

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy new laptop',
        'description': u'Options are Microsoft Surface, Dell XPS 15, HP Pavilion, Lenovo-Yoga, Asus TUF', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn to code',
        'description': u'Need to find a good programming tutorial on the web', 
        'done': False
    },
    {
        'id': 3,
        'title': u'Make breakfast for my father',
        'description': u'Need to wash dishes first', 
        'done': False
    }
]

# This funtion make another version of task with uri field
def add_uri_to_task(task):
    task_with_uri = {}
    for field in task:
        task_with_uri[field] = task[field]
    task_with_uri['uri'] = url_for('get_task_with_id', task_id=task['id'], _external=True)

    return task_with_uri

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': [add_uri_to_task(task) for task in tasks]})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task_with_id(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)

    return jsonify({'task': add_uri_to_task(task[0])})

@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    # If there is something wrong with the sent json or it has no title then abort
    if not request.json or not 'title' in request.json:
        abort(404)

    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)

    return jsonify({'task': add_uri_to_task(task)}), 201
   
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:  # if there is no task with this id
        abort(404)
    if not request.json: # if the request doesn't have a json
        abort(404)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(404)  # if there is something wrong the the title
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(404)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(404)

    # Update the task with the new info
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])

    return jsonify({'task': add_uri_to_task(task[0])})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)

    tasks.remove(task[0])

    return jsonify({'result': True})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'There is no task with this id, or there is something wrong with your new task for exmaple "missing title"!!'}))

if __name__ == '__main__':
    app.run(debug=True)