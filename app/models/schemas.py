from .products import Products
from .sectors import Sectors
from app.models import ma

class ProductsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Products
        fields = ('name', 'price', 'amount', 'weight', 'sector')

class SectionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Sectors
        fields = ('name', )
