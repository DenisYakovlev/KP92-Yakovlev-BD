from sqlalchemy import Column, Text, Integer, ForeignKey, Sequence, Date
from sqlalchemy.orm import relation
from base import Base
from categories import Categories
from departments import Departments

class Products(Base):
    __tablename__ = 'products'

    id = Column(Integer, Sequence('seq_products'), primary_key=True)
    name = Column(Text, nullable=False)
    price = Column(Integer, nullable=False)
    fk_department = Column(Integer, ForeignKey('departments.id'))
    fk_category = Column(Integer, ForeignKey('categories.id'))
    department = relation(Departments, backref='products')
    category = relation(Categories, backref='products')

    def __init__(self, id, name, price, fk_department, fk_category):
        self.id = id
        self.name = name
        self.price = price
        self.fk_department = fk_department
        self.fk_category = fk_category

