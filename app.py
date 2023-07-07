"""Flask app for Cupcakes"""
from flask import Flask, request, render_template, redirect, flash, session, jsonify
from models import db, connect_db, serialize, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'it is a secret'

connect_db(app)

@app.route('/', methods=['GET'])
def display_home_page():
    return render_template('home.html')

@app.route('/api/cupcakes', methods=['GET'])
def lookup_all_cupcakes():
    with app.app_context():
        types_of_cupcakes = Cupcake.query.all()
        all_cupcakes = [serialize(cupcake) for cupcake in types_of_cupcakes]
        return jsonify({'cupcakes': all_cupcakes})

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['GET'])
def lookup_a_cupcake(cupcake_id):
    cupcake_id = request.view_args['cupcake_id']
    with app.app_context():
        cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify({'cupcake': serialize(cupcake)})

@app.route('/api/cupcakes', methods=['POST'])
def add_new_cupcake():
    info = request.json
    print('------------------')
    print(info['flavor'])
    print(info['size'])
    print(info['rating'])
    print(info['image'])
    print('------------------')
    new_cupcake = Cupcake(flavor=info['flavor'], size=info['size'], rating=info['rating'], image=info['image'])
    with app.app_context():
        db.session.add(new_cupcake)
        db.session.commit()
        # assuming flavors are kept unique, 
        new_cup = Cupcake.query.filter(Cupcake.flavor == new_cupcake.flavor).first()
        response_json = jsonify({'cupcake': serialize(new_cup)})
        return (response_json, 201)
    #return serialize(added_cupcake)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    cupcake_id = request.view_args['cupcake_id']
    with app.app_context():
        current_cupcake = Cupcake.query.get_or_404(cupcake_id)
        print('--------------------')
        print(current_cupcake.id)
        print('--------------------')
        current_cupcake.flavor = request.json['flavor']
        current_cupcake.size = request.json['size']
        current_cupcake.rating = request.json['rating']
        current_cupcake.image = request.json['image']
        db.session.commit()
        updated_cupcake = Cupcake.query.get(cupcake_id)
    return jsonify({'cupcake': serialize(updated_cupcake)})

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    cupcake_id = request.view_args['cupcake_id']
    with app.app_context():
        current_cupcake = Cupcake.query.get_or_404(cupcake_id)
        db.session.delete(current_cupcake)
        db.session.commit()
    return jsonify({'message': 'Deleted'})