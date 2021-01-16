import psycopg2
from psycopg2 import OperationalError, errorcodes, errors


class DataBase:
    def __init__(self, dbname, password, user):
        try:
            self.conn = psycopg2.connect(dbname=dbname, password=password,
                                         user=user, host='localhost')
            self.cursor = self.conn.cursor()
        except OperationalError as err:
            raise Exception('Init error occurred:\n', str(err))

    def __del__(self):
        self.close()

    def is_open(self):
        return not self.conn.closed()

    def close(self):
        self.conn.close()
        self.cursor.close()

    def select_all(self, table_name):
        try:
            self.cursor.execute(f'SELECT * FROM {table_name}')
            items = self.cursor.fetchall()
            return items

        except Exception as err:
            raise Exception('DataBase select error: \n', str(err))

    def insert(self, table_name, item):
        try:
            values = ','.join(map(str, item))
            self.cursor.execute(f"INSERT INTO {table_name} VALUES (default, {values})")

            self.conn.commit()
        except Exception as err:
            raise Exception('DataBase insert error:\n', str(err))

    def insert_many(self, table_name, items):
        try:
            values = ','.join(str(item) for item in items)
            self.cursor.execute(f'INSERT INTO {table_name} VALUES {values[1:-1]}')

            self.conn.commit()
        except Exception as err:
            raise Exception('DataBase insert many error\n', str(err))

    def update(self, table_name, id, new_values: dict):
        try:
            set_values = ','.join('='.join(map(str, value)) for value in new_values.items())
            self.cursor.execute(f'UPDATE {table_name} SET {set_values} WHERE id = {id}')

            self.conn.commit()
        except Exception as err:
            raise Exception('DataBase update error\n', str(err))

    def select_order_products(self, order_id: int):
        try:
            self.cursor.execute(f'''SELECT * FROM products
                                    INNER JOIN order_products_relations opl
                                    ON opl.product_id = products.id
                                    WHERE opl.order_id = {order_id}''')

            items = self.cursor.fetchall()
            return items
        except Exception as err:
            raise Exception('DataBase select order products error\n', str(err))

    def select_orders_between(self, start, end):
        try:
            self.cursor.execute(f"""SELECT * FROM orders AS ord
                                    WHERE ord.date 
                                    BETWEEN '{start}' AND '{end}'""")

            items = self.cursor.fetchall()
            return items
        except Exception as err:
            raise Exception('DataBase select orders between error\n', str(err))

    def select_products_between(self, start, end):
        try:
            items = self.select_orders_between(start, end)

            values = tuple(item[0] for item in items)
            self.cursor.execute(f'''SELECT * FROM products AS pr
                                    WHERE pr.id IN {values}
                                    ''')

            result = self.cursor.fetchall()
            return result
        except Exception as err:
            raise Exception('DataBase select products between error\n', str(err))

    def select_product_by_restriction(self, restricted: bool):
        try:
            self.cursor.execute(f'''SELECT * FROM products as pr
                                    INNER JOIN categories as ct
                                    ON pr.fk_category = ct.id
                                    WHERE ct.age_restricted = {restricted}''')

            items = self.cursor.fetchall()
            return items
        except Exception as err:
            raise Exception('DataBase select products by restriction error\n', str(err))

    def select_table_columns_name(self, table_name):
        try:
            self.cursor.execute(f"SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'")

            items = self.cursor.fetchall()
            return items
        except Exception as err:
            raise Exception('DataBase wrong table:\n', str(err))

    def generate(self):
        try:
            self.cursor.execute('''INSERT INTO orders(date, customer)
                                   (SELECT timestamp '2020-01-01 20:00:00' + random() * 
		                           (timestamp '2020-12-31 20:00:00' - timestamp '2020-01-01 10:00:00'), 
 		                           md5(random()::text) FROM generate_series(1,50000));
 		                            
 		                           INSERT INTO products(name, price, fk_department, fk_category)
                                   (SELECT md5(random()::text), floor(random() * 1000 + 1)::int, 
                                   floor(random() * (SELECT COUNT(*) FROM departments) + 1)::int, floor(random() * (SELECT COUNT(*) FROM categories) + 1)::int 
                                   FROM generate_series(1,100000));
                                    
                                   INSERT INTO order_products_relations(order_id, product_id)
                                   (SELECT floor(random() * (SELECT COUNT(*) FROM orders) + 1)::int, floor(random() * (SELECT COUNT(*) FROM products) + 1)::int 
                                   FROM generate_series(1,50000));''')

            self.conn.commit()
        except Exception as err:
            raise Exception('DataBase generate error\n', str(err))

'''
    INSERT INTO categories(name, age_restricted)
    (SELECT md5(random()::text), (round(random())::int)::boolean FROM generate_series(1,5));

    INSERT INTO departments(name, location)
    (SELECT md5(random()::text), md5(random()::text) FROM generate_series(1,100000));

    INSERT INTO orders(date, customer)
    (SELECT timestamp '2020-01-01 20:00:00' + random() * 
		(timestamp '2020-12-31 20:00:00' - timestamp '2020-01-01 10:00:00'), 
 		md5(random()::text) FROM generate_series(1,50000));

 	INSERT INTO products(name, price, fk_department, fk_category)
    (SELECT md5(random()::text), floor(random() * 1000 + 1)::int, 
    floor(random() * (SELECT COUNT(*) FROM departments) + 1)::int, floor(random() * (SELECT COUNT(*) FROM categories) + 1)::int FROM generate_series(1,100000))

    INSERT INTO order_products_relations(order_id, product_id)
(SELECT floor(random() * (SELECT COUNT(*) FROM orders) + 1)::int, floor(random() * (SELECT COUNT(*) FROM products) + 1)::int FROM generate_series(1,50000))
    '''