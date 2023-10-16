import uuid
from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_migrate import Migrate
from  werkzeug.security import generate_password_hash, check_password_hash

import os

from models import Data, User, db

#Загрузка переменных окружения
load_dotenv('.env')

#Конфигурация приложения
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)


@app.route('/users/login/', methods =['POST'])
def login():
    """Авторизация для пользователя. При успешной авторизации возвращает токен авторизации"""
    auth = request.form
  
    if not auth or not auth.get('email') or not auth.get('password'):
        return make_response(
            'Невозможно авторизоваться',
            401,
            {'WWW-Authenticate' : 'Basic realm ="Требуется вход"'}
        )
  
    user = User.query.filter_by(email = auth.get('email')).first()
  
    if not user:
        return make_response(
            'Невозможно авторизоваться',
            401,
            {'WWW-Authenticate' : 'Basic realm ="Пользовтель не существует"'}
        )
  
    if check_password_hash(user.password, auth.get('password')):
        access_token = create_access_token(identity=auth.get('email'))
        return make_response(jsonify(access_token=access_token))
    return make_response(
        'Невозможно авторизоваться',
        403,
        {'WWW-Authenticate' : 'Basic realm ="Неправильный пароль"'}
    )


@app.route('/users/signup/', methods =['POST'])
def signup():
    """Регистрация  пользователя"""
    data = request.form
  
    email = data.get('email')
    password = data.get('password')
  
    user = User.query.filter_by(email = email).first()
    if not user:
        user = User(
            public_id = str(uuid.uuid4()),
            email = email,
            password = generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
  
        return make_response('Регистрация прошла успешно', 201)
    else:
        return make_response('Пользователь уже существует. Пожалуйста, авторизуйтесь', 202)
    

@app.route('/data', methods=['POST'])
@jwt_required()
def data_create():
    """Создание данных. Защищено токеном авторизации"""
    if request.is_json:
        r = request.get_json()
        new_data = Data(name=r['name'], data=r['data'])
        db.session.add(new_data)
        db.session.commit()
        return {"message": f"Новые данные {new_data.name} были успешно добавлены"}
    else:
        return {"message": "Данные не в формате JSON"}


@app.route('/data', methods=['GET'])
def data_list():
    """Список всех данных"""
    data = Data.query.all()
    response = [
        {
        "id": data.id,
        "name": data.name,
        "data": data.data
        } for data in data
    ]

    return {"data": response}

@app.route('/data/<data_id>', methods=['GET'])
def data_retrieve(data_id):
    """Получения одного экземпляра данных"""
    data_obj = Data.query.get_or_404(data_id)
    response = {
        "id": data_obj.id,
        "name": data_obj.name,
        "data": data_obj.data
    }
    return {"data_object": response}


@app.route('/data/<data_id>', methods=['PUT', 'DELETE'])
@jwt_required()
def data_update_or_delete(data_id):
    """Исправление и удаление данных. Защищено токеном авторизации"""
    data_obj = Data.query.get_or_404(data_id)
    if request.method == 'PUT':
        r = request.get_json()
        data_obj.name = r['name']
        data_obj.data = r['data']
        db.session.add(data_obj)
        db.session.commit()
        return {"message": f"Данные {data_obj.name} успешно обновлены"}
    elif request.method == 'DELETE':
        db.session.delete(data_obj)
        db.session.commit()
        return {"message": f"Данные {data_obj.name} успешно удалены"}

if __name__ == '__main__':
    app.run()