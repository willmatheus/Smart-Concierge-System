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


@app.route("/resident", methods=['POST'])
def register_resident():
    cpf = request.json['cpf']
    name = request.json['name']
    apartment_number = request.json['apartment_number']
    new_resident = Resident(cpf=cpf, name=name, apartment_number=apartment_number)
    db.session.add(new_resident)
    db.session.commit()
    return jsonify({'message': 'User successfully registered', 'Name': name}), 200


if __name__ == "__main__":
    app.run(debug=True)

