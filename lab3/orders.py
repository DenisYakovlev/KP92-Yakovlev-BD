from sqlalchemy import Column, Text, Integer, ForeignKey, Sequence, Date
from sqlalchemy.orm import relation
from base import Base


class Orders(Base):
    __tablename__ = 'orders'

    id = Column(Integer, Sequence('seq_orders'), primary_key=True)
    date = Column(Date, nullable=False)
    customer = Column(Text, nullable=False)

    def __init__(self, id, date, customer):
        self.id = id
        self.date = date
        self.customer = customer
