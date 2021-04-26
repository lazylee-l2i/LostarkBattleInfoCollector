class SyncCursor:
    def __init__(self, _host:str='IP ADDRESS', _user:str='ID', _password:str='PW', _db:str='Schema Name', _charset='utf8'):
        import pymysql

        self.conn = pymysql.connect(host=_host, user=_user, password=_password, db=_db, charset=_charset)
        self.cur = self.conn.cursor()

        sql = "SELECT s.salesId, s.date, m.menuId, m.name, m.price " \
              "FROM salesstatics as s " \
              "INNER JOIN menulist as m " \
              "ON s.menuId = m.menuId;"

    def selectTable(self, _tableName:str="table name"):
        sql = f"select * from {_tableName}"
        return self.executeSQL(sql)

    def executeSQL(self, _sql:str="SQL"):
        self.cur.execute(_sql)
        return self.cur.fetchall()

    def updateTable(self, _tableName:str="table name"):
        sql = f"UPDATE {_tableName} SET [Data here]"
        self.executeSQL(sql)        


if __name__ == "__main__":
    Sync = SyncCursor()
    print(Sync.menu_list[1])