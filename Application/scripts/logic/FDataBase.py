import sqlite3


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def add_links(self, **kwargs):
        """The method for add some links to db."""
        long_link = kwargs.get('long_link')
        short_link = kwargs.get('short_link')
        try:
            request = f"""INSERT INTO link(long_link, short_link)
                                 VALUES('{long_link}', '{short_link}')
                       """
            self.__cur.execute(request)
            self.__db.commit()
            return True

        except sqlite3.Error as e:
            print(f"Error - {str(e)} in the method add_links(file - FDataBase.py)")
            return False

    def get_long_link(self, *_, **kwargs):
        """The method can to get a long link from db."""
        short_link = kwargs.get('short_link')
        request = f"""SELECT long_link FROM link WHERE short_link = '{short_link}'"""
        try:
            self.__cur.execute(request)
            response = self.__cur.fetchall()[0]
            if response:
                for link in response:
                    origin_link = link
                    return origin_link

        except sqlite3.Error as e:
            print(f"Error - {str(e)} in the method get_long_link(file - FDataBase.py)")
        return []
