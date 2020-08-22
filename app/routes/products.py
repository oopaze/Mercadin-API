from flask import Blueprint, jsonify, request
from app.models.schemas import ProductsSchema
from app.models import db

prod = Blueprint('products', __name__)
