from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///callbacks.db'
db = SQLAlchemy(app)

class Callback(db.Model):
    id = db.Column(db.String, primary_key=True)
    data = db.Column(db.JSON)

@app.route('/webhook', methods=['POST'])
def webhook_callback():
    data = request.json  # Отримуємо дані з POST-запиту

    # Перевіряємо, чи є параметр 'task_id' в даних зворотного виклику
    if 'task_id' not in data:
        logging.error('Missing task_id parameter in the callback data')
        return jsonify({'error': 'Missing task_id parameter in the callback data'}), 400

    # Використовуємо значення параметра 'task_id' як ідентифікатор зворотного виклику
    callback_id = data['task_id']

    # Зберігаємо дані зворотного виклику в базі даних
    callback = Callback(id=callback_id, data=data)
    db.session.add(callback)
    db.session.commit()

    response = {'status': 'success', 'callback_id': callback_id}
    return jsonify(response)

@app.route('/webhook/<string:callback_id>', methods=['GET'])
def get_callback(callback_id):
    # Отримуємо дані зворотного виклику з бази даних за його ідентифікатором
    callback = Callback.query.get(callback_id)

    if callback:
        return jsonify(callback.data)
    else:
        return jsonify({'error': 'Callback not found'}), 404

@app.route('/webhook/all', methods=['GET'])
def get_all_callbacks():
    # Отримуємо всі дані зворотних викликів з бази даних
    all_callbacks = Callback.query.all()

    # Створюємо список для зберігання даних зворотних викликів
    all_callbacks_data = [{'task_id': callback.id, 'data': callback.data} for callback in all_callbacks]

    return jsonify(all_callbacks_data)

@app.route('/webhook/delete-all', methods=['DELETE'])
def delete_all_callbacks():
    # Видаляємо всі зворотні виклики з бази даних
    Callback.query.delete()
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'All callbacks deleted'})

if __name__ == '__main__':
    # Ініціалізація бази даних
    db.create_all()

    logging.basicConfig(level=logging.DEBUG)
    logging.info('Starting the application...')

    app.run(host='0.0.0.0', port=5000)