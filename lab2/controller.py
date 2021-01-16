from model import ModelPGSQL
from view import View
import time


class Controller:
    def __init__(self, model: ModelPGSQL, view: View):
        self.model = model
        self.view = view

    def read_items(self, table_name):
        try:
            start = time.time()

            items = self.model.read_items(table_name)
            self.view.display_items(items, time.time() - start)
        except Exception as e:
            self.view.display_select_error(table_name, e)

    def write_item(self, table_name, items):
        try:
            start = time.time()

            self.model.write_item(table_name, items)
            self.view.display_insert_result(time.time() - start)
        except Exception as e:
            self.view.display_insert_error(table_name, e)

    def update_item(self, table_name, id, new_values: dict):
        try:
            start = time.time()

            self.model.update_item(table_name, id, new_values)
            self.view.display_update_result(id, time.time() - start)
        except Exception as e:
            self.view.display_update_error(table_name, id, e)

    def read_all_order_products(self, order_id):
        try:
            start = time.time()

            items = self.model.read_order_products(order_id)
            self.view.display_items(items, time.time() - start)
        except Exception as e:
            self.view.display_select_error('orders', e)

    def read_orders_in_dates(self, start, end):
        try:
            start_t = time.time()

            items = self.model.read_orders_between(start, end)
            self.view.display_items(items, time.time() - start_t)
        except Exception as e:
            self.view.display_select_error('orders', e)

    def read_products_in_dates(self, start, end):
        try:
            start_t = time.time()

            items = self.model.read_products_between(start, end)
            self.view.display_items(items, time.time() - start_t)
        except Exception as e:
            self.view.display_select_error('orders', e)

    def read_products_by_restriction(self, restricted):
        try:
            start = time.time()

            items = self.model.read_items_with_restriction(restricted)
            self.view.display_items(items, time.time() - start)
        except Exception as e:
            self.view.display_select_error('orders', e)

    def read_columns_of_table(self, table_name):
        try:
            items = self.model.read_columns_of_table(table_name)

            self.view.display_columns(items)
        except Exception as e:
            self.view.display_select_error(table_name, e)

    def generate(self):
        try:
            start = time.time()

            self.model.generate()
            self.view.display_generate_result(time.time() - start)
        except Exception as e:
            self.view.display_generate_error(e)