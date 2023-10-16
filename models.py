from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    """Модель пользователя"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    public_id = db.Column(db.String(50), unique = True)
    email = db.Column(db.String(70), unique = True)
    password = db.Column(db.String())


class Data(db.Model):
    """Модель данных"""
    __tablename__ = 'data'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String())
    data = db.Column(db.String())
    