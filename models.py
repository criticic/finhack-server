from main import db
from passlib.hash import pbkdf2_sha256 as sha256
from sqlalchemy_utils import EmailType, UUIDType
import uuid

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(EmailType, unique = True, nullable = False)
    password = db.Column(db.String(120), nullable = False)
    name = db.Column(db.String(120), nullable = False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email = email).first()

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'id' : x.id,
                'name': x.name,
                'email': x.email,
                'password': x.password
            }
        return {'users': list(map(lambda x: to_json(x), UserModel.query.all()))}

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)


class ClientModel(db.Model):
    __tablename__ = 'clients'

    relation_id = db.Column(db.Integer, primary_key = True)
    worker_email = db.Column(EmailType, db.ForeignKey(UserModel.email), nullable = False)
    client_email = db.Column(EmailType, nullable = False)
    client_phone_no = db.Column(db.String(120), nullable = False)
    client_name = db.Column(db.String(120), nullable = False)
    worker = db.relationship(UserModel, foreign_keys=worker_email)


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_email(cls, email, worker_email):
        return cls.query.filter_by(client_email = email, worker_email = worker_email).first()
        print(cls.query.filter_by(client_email = email, worker_email = worker_email).first())

    @classmethod
    def return_my(cls, worker_email):
        def to_json(x):
            return {
                'relation_id' : x.relation_id,
                'client_email': x.client_email,
                'client_phone_no': x.client_phone_no
            }
        return {'clients': list(map(lambda x: to_json(x), ClientModel.query.filter_by(worker_email = worker_email).all()))}

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'relation_id' : x.relation_id,
                'client_email': x.client_email,
                'client_phone_no': x.client_phone_no
            }
        return {'clients': list(map(lambda x: to_json(x), ClientModel.query.all()))}
