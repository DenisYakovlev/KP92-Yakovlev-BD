from pgsql_backend import DataBase


class ModelPGSQL:
    def __init__(self, dbname, password, user):
        self.db = DataBase(dbname, password, user)

    def read_items(self, table_name):
        return self.db.select_all(table_name);

    def write_item(self, table_name, item):
        self.db.insert(table_name, item)

    def write_items(self, table_name, items):
        self.db.insert_many(table_name, items)

    def update_item(self, table_name, id, new_values):
        self.db.update(table_name, id, new_values)

    def read_order_products(self, order_id: int):
        return self.db.select_order_products(order_id)

    def read_orders_between(self, start, end):
        return self.db.select_orders_between(start, end)

    def read_products_between(self, start, end):
        return self.db.select_products_between(start, end)

    def read_items_with_restriction(self, restriction: bool):
        return self.db.select_product_by_restriction(restriction)

    def read_columns_of_table(self, table_name):
        return self.db.select_table_columns_name(table_name)

    def generate(self):
        self.db.generate()