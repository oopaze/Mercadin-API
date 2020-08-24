from .employees import Employees
from .products import Products
from .sectors import Sectors
from .carts import Carts
from .sales import Sales
from app.models import ma

class EmployeeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Employees
        fields = ('id', 'name', 'registration', 'admin')

class ProductsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Products
        fields = ('id', 'name', 'price', 'amount', 'weight', 'sector')

class SectionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Sectors
        fields = ('id', 'name', 'slug')

class CartSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Carts
        fields = ('id', 'total_price')

class SaleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Sales
        fields = ('id', 'costumer', 'total_price', 'sold_at')
