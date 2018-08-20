import csv
import pymysql


class Util:

    # Writes result set to csv. Takes a list of dictionaries: one per message
    @staticmethod
    def write_object_to_csv(list_dict_data, filename):
        with open(filename, 'w', newline='\n') as csvfile:

            headers = list(list_dict_data[0].get_values().keys())
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()

            try:
                for i in list_dict_data:
                    writer.writerow(i.get_values())
            except AttributeError as error:
                print(error.__repr__())

    def query_db(self, sql):
        """
        Read and write from mySQL database
        :param sql: String script to run
        :return: Cursor
        """
        host, user, password, database = self.get_keys('server-permissions.txt')
        with pymysql.connect(host=host, user=user, password=password, db=database) as cursor:
            try:
                cursor.execute(sql)
                return cursor
            except pymysql.Error as e:
                print(e)

    @staticmethod
    def get_keys(filename):
        """
        Reads server auth details from file
        :param filename: String filename
        :return: List<String> of auth details
        """
        with open(filename, 'r') as f:
            keys = f.read().splitlines()
            return keys

    def update_db(self, sql, row_data):
        """
        Batch write to mySQL database
        :param sql: String script
        :param row_data: List of parameters to be used with the query
        :return: Cursor
        """
        host, user, password, database = self.get_keys('server-permissions.txt')
        with pymysql.connect(host=host, user=user, password=password, db=database) as cursor:
            try:
                cursor.executemany(sql, row_data)
                return cursor
            except pymysql.Error as e:
                print(e)
