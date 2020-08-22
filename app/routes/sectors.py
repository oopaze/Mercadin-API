from flask import Blueprint, jsonify, request
from sqlalchemy.orm.exc import UnmappedInstanceError
from sqlalchemy.exc import IntegrityError
from app.models.schemas import SectionSchema
from app.models.sectors import Sectors
from app.models import db

sec = Blueprint('sectors', __name__)

@sec.route('/', methods=['GET'])
def show_sector():
    """ Route that show all sectors in DataBase """
    ss = SectionSchema()
    ss.many = True

    sector = Sectors.query.all()

    return ss.jsonify(sector), 200


@sec.route('/', methods=['POST'])
def insert_sector():
    """
        Route that allows us to insert sector in a DataBase
        JSON: {'name': 'sector-name'}
    """
    try:
        ss = SectionSchema()

        sector = Sectors(**request.json)

        db.session.add(sector)
        db.session.commit()

        json = {'Data':ss.dump(sector), 'Message':'Sector added successfully!'}

        return jsonify(json), 201

    except TypeError:
        json = {'Message':'Invalid Data!'}
        return jsonify(json), 406

    except IntegrityError:
        json = {'Message':'Sector name already registered!'}
        return jsonify(json), 409


@sec.route('/<int:id>', methods=['DELETE'])
def delete_sector(id):
    """
        Router that delete a single sector from DataBase by ID
    """
    try:
        ss = SectionSchema()

        sector = Sectors.query.get(id)

        db.session.delete(sector)
        db.session.commit()

        json = {'Data':ss.dumps(sector), 'Message':'Sector deleted successfully!'}

        return jsonify(json), 200

    except UnmappedInstanceError:
        json = {'Message':'Sector element not found!'}
        return jsonify(json), 404


@sec.route('/<int:id>', methods=['PUT'])
def update_sector(id: int):
    """
        Router that update a sector from DataBase by ID
        JSON: {'name': 'new-name'}
    """
    try:
        ss = SectionSchema()
        sector = Sectors.query.get(id)
        sector.name = request.json['name']

        db.session.commit()

        json = {'Data':ss.dump(sector), 'Message':'Sector updated successfully!'}

        return jsonify(json), 200

    except AttributeError:
        json = {'Message':'Unable to find sector!'}
        return jsonify(json), 404

    except IntegrityError:
        json = {'Message':'Sector name already registered!'}
        return jsonify(json), 409
