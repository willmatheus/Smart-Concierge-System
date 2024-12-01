import datetime
import jwt
import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from config import db
from dotenv import load_dotenv
from models.resident import Resident

# load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)


def generate_token(resident):
    # Carregar a chave secreta do arquivo .env
    secret_key = os.getenv('SECRET_KEY', 'defaultsecretkey')  # A chave secreta deve ser configurada no .env
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expira em 1 hora

    payload = {
        'cpf': resident.cpf,
        'apartment_number': resident.apartment_number,
        'exp': expiration_time  # Tempo de expiração
    }

    # Gerar o token JWT
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token


@app.route("/resident", methods=['POST'])
def register_resident():
    cpf = request.json['cpf']
    name = request.json['name']
    apartment_number = request.json['apartment_number']
    new_resident = Resident(cpf=cpf, name=name, apartment_number=apartment_number)
    db.session.add(new_resident)
    db.session.commit()
    return jsonify({'message': 'User successfully registered', 'Name': name}), 200


@app.route("/login", methods=['POST'])
def login_resident():
    cpf = request.json['cpf']
    apartment_number = request.json['apartmentNumber']

    resident = Resident.query.filter_by(cpf=cpf, apartment_number=apartment_number).first()
    if not resident:
        return jsonify({'message': 'Resident not found'}), 404

    # Gerar o token
    token = generate_token(resident)

    return jsonify({
        'message': 'User successfully logged in',
        'resident_apartment_number': resident.get_apartment_number(),
        'resident_name': resident.get_name(),
        'token': token  # Enviar o token na resposta
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
