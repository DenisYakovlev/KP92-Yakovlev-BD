from sqlalchemy import Column, Text, Integer, ForeignKey, Sequence, Date, Boolean
from sqlalchemy.orm import relation
from base import Base


class Departments(Base):
    __tablename__ = 'departments'

    id = Column(Integer, Sequence('seq_departments'), primary_key=True)
    name = Column(Text, nullable=False)
    location = Column(Text, nullable=False)

    def __init__(self, id, name, location):
        self.id = id
        self.name = name
        self.location = location
