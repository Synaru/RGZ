from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from

# Создаем Flask-приложение
app = Flask(__name__)

# Настраиваем Flasgger для генерации документации
app.config['SWAGGER'] = {
    'title': 'Phone Contacts API',
    'description': 'API для управления телефонными контактами',
    'uiversion': 3
}
swagger = Swagger(app)

# Хранилище контактов (Python-словарь)
contacts_db = {}
current_id = 1

@app.route('/contacts', methods=['POST'])
@swag_from({
    'tags': ['Contacts'],
    'description': 'Создание нового контакта',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string', 'example': 'Имя Фамилия'},
                    'phone': {'type': 'string', 'example': '+7-9XX-XX-XX'},
                    'email': {'type': 'string', 'example': 'email@email.com'}
                },
                'required': ['name', 'phone']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Контакт успешно создан',
            'examples': {
                'application/json': {
                    'id': 1,
                    'name': 'Имя Фамилия',
                    'phone': '+7-9XX-XX-XX',
                    'email': 'email@email.com'
                }
            }
        },
        400: {
            'description': 'Неверные данные'
        }
    }
})
def create_contact():
    """Создание нового контакта"""
    global current_id
    
    data = request.get_json()
    
    # Проверяем обязательные поля
    if not data or 'name' not in data or 'phone' not in data:
        return jsonify({'error': 'Необходимы поля name и phone'}), 400
    
    # Создаем контакт
    contact_id = current_id
    contact = {
        'id': contact_id,
        'name': data['name'],
        'phone': data['phone'],
        'email': data.get('email', '')
    }
    
    # Сохраняем в хранилище
    contacts_db[contact_id] = contact
    current_id += 1
    
    return jsonify(contact), 201

@app.route('/contacts/<int:contact_id>', methods=['GET'])
@swag_from({
    'tags': ['Contacts'],
    'description': 'Получение информации о контакте по ID',
    'parameters': [
        {
            'name': 'contact_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID контакта'
        }
    ],
    'responses': {
        200: {
            'description': 'Информация о контакте',
            'examples': {
                'application/json': {
                    'id': 1,
                    'name': 'Иван Иванов',
                    'phone': '+79991234567',
                    'email': 'ivan@example.com'
                }
            }
        },
        404: {
            'description': 'Контакт не найден'
        }
    }
})
def get_contact(contact_id):
    """Получение контакта по ID"""
    contact = contacts_db.get(contact_id)
    
    if not contact:
        return jsonify({'error': 'Контакт не найден'}), 404
    
    return jsonify(contact), 200

@app.route('/contacts/<int:contact_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Contacts'],
    'description': 'Удаление контакта по ID',
    'parameters': [
        {
            'name': 'contact_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID контакта'
        }
    ],
    'responses': {
        200: {
            'description': 'Контакт успешно удален',
            'examples': {
                'application/json': {
                    'message': 'Контакт удален'
                }
            }
        },
        404: {
            'description': 'Контакт не найден'
        }
    }
})
def delete_contact(contact_id):
    """Удаление контакта по ID"""
    if contact_id not in contacts_db:
        return jsonify({'error': 'Контакт не найден'}), 404
    
    # Удаляем контакт
    del contacts_db[contact_id]
    
    return jsonify({'message': 'Контакт удален'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)