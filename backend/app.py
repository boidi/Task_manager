from flask import Flask, jsonify, request
#from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
#db = SQLAlchemy(app)
CORS(app)
tasks = []
@app.route('/')
def index():
    return "Bienvenue sur l'API de gestion des tâches"

@app.route('/taches', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/taches', methods=['POST'])
def add_task():
    data = request.get_json()
    task = {
        'id': len(tasks) + 1,
        'title': data['title'],
        'description': data.get('description', ''),
        'completed': False
    }
    tasks.append(task)
    return jsonify(task), 201

@app.route('/taches/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task:
        tasks.remove(task)
        return jsonify({'message': 'Task deleted successfully'})
    else:
        return jsonify({'message': 'Task not found'}), 404

@app.route('/taches/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task:
        data = request.get_json()
        task['title'] = data.get('title', task['title'])
        task['description'] = data.get('description', task['description'])
        if 'completed' in data:
            task['completed'] = data['completed']
        return jsonify(task)
    else:
        return jsonify({'message': 'Task not found'}), 404

@app.route('/taches/<int:task_id>/complete', methods=['PUT'])
def complete_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task:
        task['completed'] = True
        return jsonify(task)
    else:
        return jsonify({'message': 'Task not found'}), 404
    
if __name__ == '__main__':
    app.run(debug=True)