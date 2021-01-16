from products import Products
from orders import Orders
from categories import Categories
from departments import Departments
from op_relations import OP_relations
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from base import Base


class DataBase:

    def __init__(self):
        self.engine = create_engine('postgresql://postgres:22112001_D@localhost/lab3')
        self.Session = sessionmaker(bind=self.engine)

        self.session = self.Session()

    def __del__(self):
        self.session.close()

    def select_all(self, table_instance):
        try:
            return self.session.query(table_instance).all()

        except Exception as err:
            raise Exception('DataBase select error: \n', str(err))

    def insert(self, table_name, item):
        try:
            values = ','.join(map(str, item))
            self.engine.execute(f"INSERT INTO {table_name} VALUES (default, {values})")

        except Exception as err:
            raise Exception('DataBase insert error:\n', str(err))

    def insert_many(self, items: list):
        try:
            self.session.add_all(items)
            self.session.commit()

        except Exception as err:
            raise Exception('DataBase insert many error\n', str(err))

    def update(self, table_instance, id, new_state: dict):
        try:
            self.session.query(table_instance).filter(table_instance.id == id).update(new_state)
            self.session.commit()

        except Exception as err:
            raise Exception('DataBase update error\n', str(err))

    def select_order_products(self, order_id):
        try:
            items = self.session.query(Products, OP_relations).filter(Products.id == OP_relations.product_id). \
                filter(OP_relations.order_id == order_id).all()

            return items
        except Exception as err:
            raise Exception('DataBase select order products error\n', str(err))

    def select_orders_between(self, start, end):
        try:
            items = self.session.query(Orders).filter(Orders.date.between(start, end))
            return items

        except Exception as err:
            raise Exception('DataBase select orders between error\n', str(err))

    def select_products_between(self, start, end):
        try:
            items = self.select_orders_between(start, end)
            id_list = [item.id for item in items]

            items = self.session.query(OP_relations).filter(OP_relations.order_id.in_(id_list)).all()
            return self.session.query(Products).filter(Products.id.in_([item.id for item in items]))
        except Exception as err:
            raise Exception('DataBase select products between error\n', str(err))

    def select_product_by_restriction(self, restricted: bool):
        try:
            items = self.session.query(Products, Categories).filter(Products.fk_category == Categories.id). \
                filter(Categories.age_restricted == restricted)

            return items
        except Exception as err:
            raise Exception('DataBase select products by restriction error\n', str(err))

    def select_table_columns_name(self, table_instance):
        try:
            items = table_instance.__table__.columns.keys()
            return items
        except Exception as err:
            raise Exception('DataBase wrong table:\n', str(err))

    def get_class_by_tablename(self, table_name):
        for c in Base._decl_class_registry.values():
            if hasattr(c, '__tablename__') and c.__tablename__ == table_name:
                return c

    def generate(self):
        try:
            self.engine.execute(text('''INSERT INTO orders(date, customer)
                                   (SELECT timestamp '2020-01-01 20:00:00' + random() * 
		                           (timestamp '2020-12-31 20:00:00' - timestamp '2020-01-01 10:00:00'), 
 		                           md5(random()::text) FROM generate_series(1,50000));

 		                           INSERT INTO products(name, price, fk_department, fk_category)
                                   (SELECT md5(random()::text), floor(random() * 1000 + 1)::int, 
                                   floor(random() * (SELECT COUNT(*) FROM departments) + 1)::int, floor(random() * (SELECT COUNT(*) FROM categories) + 1)::int 
                                   FROM generate_series(1,100000));

                                   INSERT INTO order_products_relations(order_id, product_id)
                                   (SELECT floor(random() * (SELECT COUNT(*) FROM orders) + 1)::int, floor(random() * (SELECT COUNT(*) FROM products) + 1)::int 
                                   FROM generate_series(1,50000));''')).execution_options(autocommit=True)

        except Exception as err:
            raise Exception('DataBase generate error\n', str(err))