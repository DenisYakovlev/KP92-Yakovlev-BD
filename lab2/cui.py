from controller import  Controller
from model import ModelPGSQL
from view import View
import re

class Cui:
    commands = \
'''
Commands:
1. Read items in table
2. Insert item to table
3. Update item in table
4. Read all products in order
5. Read all orders in dates
6. Read all products in dates
7. Read products by restriction
8. Generate some data 
9. Exit
'''

    def __init__(self):
        self.controller = Controller(ModelPGSQL('lab1', '22112001_D', 'postgres'), View())

    def start(self):
        while(True):
            print(self.commands)
            command = int(input('\ncommand: '))

            if command == 1:
                table_name = input('Enter table name: ')
                self.controller.read_columns_of_table(table_name)
                self.controller.read_items(table_name)

            elif command == 2:
                table_name = input('Enter table name: ')
                self.controller.read_columns_of_table(table_name)
                item = self.get_insert_input()

                self.controller.write_item(table_name, item)

            elif command == 3:
                id = input('Enter item id: ')
                table_name = input('Enter table name: ')
                self.controller.read_columns_of_table(table_name)
                values = self.get_update_input()

                self.controller.update_item(table_name, id, values)

            elif command == 4:
                id = input('Enter order id: ')
                self.controller.read_all_order_products(id)

            elif command == 5:
                dates = self.get_dates()

                self.controller.read_orders_in_dates(dates[0], dates[1])

            elif command == 6:
                dates = self.get_dates()
                self.controller.read_products_in_dates(dates[0], dates[1])

            elif command == 7:
                restricted = (input('Restricted: '))
                print(restricted)
                self.controller.read_products_by_restriction(restricted)

            elif command == 8:
                self.controller.generate()

            elif command == 9:
                break

            else:
                print('Try again')

            input('Press any key to continue')

    def get_dates(self):
        dates = input('Enter date range(start/end): ').split('/')

        for date in dates:
            if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', date):
                print('Wrong date format. Try again\n')
                return self.get_dates()

        return dates

    def get_insert_input(self):
        data = input('Enter data(strings must be in columns): ').split('/')
        return data.split('/')

    def get_update_input(self):
        data = input('Enter data(coma split, dict): ')
        data = dict(map(lambda l: l.split('='), data.split(',')))
        return data
