import pyodbc
class ConnectDataBase:
    def __init__(self):
        self.nServer="192.168.22.247"
        self.nDatabase="QLNVS"
        self.nLogin="sa"
        self.nPassword="123"
        self.ConnectDB()
    # def __del__(self):
    #     self.conn.close()
    #     print()
    def ConnectDB(self):
        try:
            self.conn = pyodbc.connect('DRIVER={SQL Server};Server='+self.nServer+';Database='+self.nDatabase+';Login='+self.nLogin+';Password='+self.nPassword+'')
            return self.conn
        except ValueError as error:
            print('Log Error',error)