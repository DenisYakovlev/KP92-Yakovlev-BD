from sqlalchemy import Column, Text, Integer, ForeignKey, Sequence, Date
from sqlalchemy.orm import relation
from base import Base
from orders import Orders
from products import Products


class OP_relations(Base):
    __tablename__ = 'order_products_relations'

    id = Column(Integer, Sequence('seq_op_relation'), primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    order = relation(Orders, backref='order_products_relations')
    product = relation(Products, backref='order_products_relations')

    def __init__(self, id, order_id, product_id):
        self.id = id
        self.order_id = order_id
        self.product_id = product_id
