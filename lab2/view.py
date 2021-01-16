class View(object):

    @staticmethod
    def display_items(items, time):
        for item in items:
            print(item)

        print(f'\n{time} ms')

    @staticmethod
    def display_columns(items):
        print('|'.join(item[0] for item in items))

    @staticmethod
    def display_insert_result(time):
        print(f'Just added new item!\n\n{time} ms')

    @staticmethod
    def display_generate_result(time):
        print(f'Just generated some data!\n\n{time} ms')

    @staticmethod
    def display_update_result(id, time):
        print(f'Just updated item with id#{id}!\n\n{time} ms')

    @staticmethod
    def display_select_error(table_name, err):
        print(f'Error with displaying items: \n{str(err)}\ntable name: {table_name}')

    @staticmethod
    def display_update_error(table_name, id, err):
        print(f'Error with updating items: \n{str(err)}\nid: {id}, table name: {table_name}')

    @staticmethod
    def display_insert_error(table_name, err):
        print(f'Error with inserting item: \n{str(err)}\ntable name: {table_name}')

    @staticmethod
    def display_connection_error(err):
        print(f'Error with connecting to DB: \n{str(err)}')

    @staticmethod
    def display_generate_error(err):
        print(f"Error with generating data: \n{str(err)}")