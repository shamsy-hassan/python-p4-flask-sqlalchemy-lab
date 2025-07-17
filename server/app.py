#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal = Animal.query.get(id)
    if animal:
        return f'''
            <ul>Name: {animal.name}</ul>
            <ul>Species: {animal.species}</ul>
            <ul>Zookeeper: {animal.zookeeper.name}</ul>
            <ul>Enclosure: {animal.enclosure.environment}</ul>
        '''
    return make_response('<h1>Animal not found</h1>', 404)


@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper = Zookeeper.query.get(id)
    if zookeeper:
        animals_list = ''.join(
            [f'<li>{animal.name}</li>' for animal in zookeeper.animals]
        )
        return f'''
            <ul>Name: {zookeeper.name}</ul>
            <ul>Birthday: {zookeeper.birthday}</ul>
            <ul>Animal: <ul>{animals_list}</ul></ul>
        '''
    return make_response('<h1>Zookeeper not found</h1>', 404)

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    enclosure = Enclosure.query.get(id)
    if enclosure:
        animals_list = ''.join(
            [f'<li>{animal.name}</li>' for animal in enclosure.animals]
        )
        return f'''
            <ul>Environment: {enclosure.environment}</ul>
            <ul>Open to Visitors: {enclosure.open_to_visitors}</ul>
            <ul>Animal: <ul>{animals_list}</ul></ul>
        '''
    return make_response('<h1>Enclosure not found</h1>', 404)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
