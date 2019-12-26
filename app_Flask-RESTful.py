from flask import Flask, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

class TasksAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()

        self.reqparse.add_argument('title', type=str, required=True, help='No task title provided', location='json')
        self.reqparse.add_argument('description', type=str, default="", location='json')

        super(TasksAPI, self).__init__()

    def get(self):
        pass

    def post(self):
        pass

class TaskAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()

        self.reqparse.add_argument('title', type=str,  location='json')
        self.reqparse.add_argument('description', type=str, location='json')
        self.reqparse.add_argument('done', type=bool, location='json')

        super(TaskAPI, self).__init__()

    def get(self, id):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass

api.add_resource(TasksAPI, '/todo/api/v1.0/tasks', endpoint='tasks')
api.add_resource(TaskAPI, '/todo/api/v1.0/tasks/<int:id>', endpoint='task')


if __name__ == '__main__':
    app.run(debug=True)