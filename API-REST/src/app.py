from flask import Flask, jsonify, request

app = Flask(__name__)

data = [
    {'id': 1, 'title': 'Tarea 1', 'done': False},
    {'id': 2, 'title': 'Tarea 2', 'done': True}
]

# GET /tasks - Obtener todas las tareas
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': data})

# GET /tasks/<int:task_id> - Obtener una tarea por ID
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((t for t in data if t['id'] == task_id), None)
    if task is None:
        return jsonify({'error': 'Tarea no encontrada'}), 404
    return jsonify({'task': task})

# POST /tasks - Crear una nueva tarea
@app.route('/tasks', methods=['POST'])
def create_task():
    if not request.is_json:
        return jsonify({'error': 'La solicitud debe ser en formato JSON'}), 400
    content = request.get_json()
    if 'title' not in content:
        return jsonify({'error': 'El campo "title" es requerido'}), 400
    new_task = {
        'id': len(data) + 1,
        'title': content['title'],
        'done': content.get('done', False)  # 'done' es opcional, por defecto False
    }
    data.append(new_task)
    return jsonify({'task': new_task}), 201  # 201 Created

# PUT /tasks/<int:task_id> - Actualizar una tarea existente
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((t for t in data if t['id'] == task_id), None)
    if task is None:
        return jsonify({'error': 'Tarea no encontrada'}), 404
    if not request.is_json:
        return jsonify({'error': 'La solicitud debe ser en formato JSON'}), 400
    content = request.get_json()
    task['title'] = content.get('title', task['title'])
    task['done'] = content.get('done', task['done'])
    return jsonify({'task': task})

# DELETE /tasks/<int:task_id> - Eliminar una tarea
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global data
    data = [t for t in data if t['id'] != task_id]
    return jsonify({'result': True})

@app.route('/')
def index():
    return "¡API REST con Flask!"

if __name__ == '__main__':
    app.run(debug=True)