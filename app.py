#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request

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

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task_with_id(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)

    return jsonify({'task': task[0]})

@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    # If there is someting wrong with the sent json or it has no title then abort
    if not request.json or not 'title' in request.json:
        abort(404)

    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)

    return jsonify({'task': task}), 201

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'There is no task with this id, or there is something wrong with your new task for exmaple "missing title"!!'}))

if __name__ == '__main__':
    app.run(debug=True)