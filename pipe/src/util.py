#!/usr/bin/env python
import csv
import pymysql


class Util:

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

    def get_messages(self):
        sql = "SELECT * FROM message_store"
        cursor = self.query_db(sql)


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

    def write_new_objects(self, sql, objects):
        """
        Batch write to mySQL database
        :param sql: String script
        :param objects: List of message or citation objects to be written to db
        :return: Cursor
        """
        row_data = [i.get_values() for i in objects]

        host, user, password, database = self.get_keys('server-permissions.txt')

        with pymysql.connect(host=host, user=user, password=password, db=database) as cursor:
            try:
                cursor.executemany(sql, row_data)
                return cursor
            except pymysql.Error as e:
                print(e)

    def write_new_normals(self, sql, row_data):
        """
        Batch write to mySQL database
        :param sql: String script
        :param objects: List of message or citation objects to be written to db
        :return: Cursor
        """
        host, user, password, database = self.get_keys('server-permissions.txt')

        with pymysql.connect(host=host, user=user, password=password, db=database) as cursor:
            try:
                cursor.executemany(sql, row_data)
                return cursor
            except pymysql.Error as e:
                print(e)

    def update_repo(self):
        # Export citation-level data
        sql_citation_level = "SELECT * FROM vw_citation_level"
        citation_header =  ['authors', 'doi', 'title', 'classification_id', 'type', 'issued_date', 'subject',
                            'journal_title', 'publisher', 'issn', 'isbn', 'issue', 'volume', 'page', 'nhm_sub',
                            'oa_id', 'best_oa_url', 'updated_date', 'pdf_url', 'is_oa', 'doi_url', 'host_type',
                            'version', 'retrieved_date']

        cursor = self.query_db(sql_citation_level)
        self.write_object_to_csv(cursor.fetchall(), citation_header, 'csv_out/citation_export.csv')

        # Export message-level data
        sql_message_level = "SELECT * FROM vw_message_level"
        message_header = ['doi', 'label_name', 'date_sent']

        cursor = self.query_db(sql_message_level)
        self.write_object_to_csv(cursor.fetchall(), message_header, 'csv_out/message_export.csv')

        # Export impact data
        sql_impact = "SELECT * FROM vw_impact"
        impact_header = ['doi', 'times_cited', 'retrieved_date']

        cursor = self.query_db(sql_impact)
        self.write_object_to_csv(cursor.fetchall(), impact_header, 'csv_out/impact_export.csv')


    # Writes result set to csv. Takes a list of dictionaries: one per message
    @staticmethod
    def write_object_to_csv(list_data, headers, filename):
        with open(filename, 'w', newline='\n') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)

            try:
                writer.writerows(list_data)
            except AttributeError as error:
                print(error.__repr__())
