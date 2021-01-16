from sqlalchemy import Column, Text, Integer, ForeignKey, Sequence, Date, Boolean
from sqlalchemy.orm import relation
from base import Base


class Categories(Base):
    __tablename__ = 'categories'

    id = Column(Integer, Sequence('seq_categories'), primary_key=True)
    name = Column(Text, nullable=False)
    age_restricted = Column(Boolean, nullable=False)

    def __init__(self, id, name, age_restricted):
        self.id = id
        self.name = name
        self.age_restricted = age_restricted
