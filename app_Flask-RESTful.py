from flask import Flask, request, url_for, abort
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

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

# This funtion return a task with specific id from the tasks list
def get_task_with_id(id):
    task = filter(lambda task: task['id'] == id, tasks)
    if len(task) == 0:
        abort(404)
    task = task[0]  # because filter fun get you a list of one element
    
    return task

class TasksAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()

        self.reqparse.add_argument('title', type=str, required=True, help='No task title provided', location='json')
        self.reqparse.add_argument('description', type=str, default="", location='json')

        super(TasksAPI, self).__init__()

    def get(self):
        return {'task': [task for task in tasks]}

    def post(self):
        args = self.reqparse.parse_args()
        task = {
            'id': tasks[-1]['id'] + 1 if len(tasks) > 0 else 1,
            'title': args['title'],
            'description': args['description'],
            'done': False
        }
        tasks.append(task)

        return {'task': task}, 201

class TaskAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()

        self.reqparse.add_argument('title', type=str,  location='json')
        self.reqparse.add_argument('description', type=str, location='json')
        self.reqparse.add_argument('done', type=bool, location='json')

        super(TaskAPI, self).__init__()

    def get(self, id):
        task = get_task_with_id(id)
        return {'task': task}

    def put(self, id):
        task = get_task_with_id(id)

        args = self.reqparse.parse_args()
        for key, value in args.iteritems():
            if value != None:
                task[key] = value

        return {'task': task}

    def delete(self, id):
        task = get_task_with_id(id)
        tasks.remove(task)
        print(tasks)

        return {'Removed': True, 'Task': task['title']}

api.add_resource(TasksAPI, '/todo/api/v1.0/tasks', endpoint='tasks')
api.add_resource(TaskAPI, '/todo/api/v1.0/tasks/<int:id>', endpoint='task')


if __name__ == '__main__':
    app.run(debug=True)