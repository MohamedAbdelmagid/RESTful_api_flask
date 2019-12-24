#!flask/bin/python
from flask import Flask, jsonify

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

if __name__ == '__main__':
    app.run(debug=True)