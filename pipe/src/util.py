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
