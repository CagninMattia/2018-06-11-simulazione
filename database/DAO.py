from database.DB_connect import DBConnect
from model.stato import Stato


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_anni():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct(year(s.`datetime`)) as d
                    from sighting s 
                    order by d"""

        cursor.execute(query)

        for row in cursor:
            result.append(row["d"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_num_apparizioni(anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select count(*) as conta
                    from sighting s 
                    where Year(`datetime`) = %s"""

        cursor.execute(query, (anno,))

        for row in cursor:
            result.append(row["conta"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_vertici(anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select s.*
                    from state s, (select distinct state from sighting s where YEAR(`datetime`) = %s and country = 'us') as s2
                    where s.id = s2.state
                         """

        cursor.execute(query, (anno,))

        for row in cursor:
            result.append(Stato(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_archi(anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select s1.s as A, s2.s as B
                    from (select state s, `datetime` d from sighting s 
                    where YEAR(`datetime`) = %s and country = 'us') as s1, 
                    (select state s, `datetime` d from sighting s 
                    where YEAR(`datetime`) = %s and country = 'us') as s2
                    where s1.s <> s2.s and s1.d < s2.d
                    group by A, B 
                    """

        cursor.execute(query, (anno, anno, ))

        for row in cursor:
            result.append([row["A"], row["B"]])

        cursor.close()
        conn.close()
        return result
