import pyodbc
import ConnectDB as db
class Users:
    def __init__(self):
        self.data=db.ConnectDataBase()
        self.dataConnect=self.data.ConnectDB()
        self.dataQuery=self.dataConnect.cursor()
    def __del__(self):
        if self.data != None:
            self.dataConnect.close()
    def showAllUser(self):
        query="select email,password,roleUsser from Users"
        try:
            self.dataQuery.execute(query)
            return self.dataQuery.fetchmany()
        except ValueError as error:
            print("Log Error",error)
    def showDataUser(self):
        query="select idUser,email,password,roleUsser from Users"
        try:
            return self.dataQuery.execute(query).fetchall()
        except ValueError as error:
            print('Log Error',error)
    def checkEmail(self,email):
        query="select email from Users where email=?"
        params=(email)
        try:
            return self.dataQuery.execute(query,params)
        except ValueError as error:
            print('Log Error',error)
    def insertUserRoleMenu(self,email,password,role):
        query="insert into Users(email,password,roleUsser) values(?,?,?)"
        params=(email,password,role)
        try:
            self.dataQuery.execute(query,params)
            return self.dataQuery.commit()
        except ValueError as error:
            print('Log Error',error)
    def updateUserRoleMenu(self,password,role,email):
        query="update Users set password=?,roleUsser=? where email=?"
        params=(password,role,email)
        try:
            self.dataQuery.execute(query,params)
            return self.dataQuery.commit()
        except ValueError as error:
            print('Log Error',error)
    def deleteUserRoleMenu(self,email):
        query="delete from Users where email=?"
        params=(email)
        try:
            self.dataQuery.execute(query,params)
            return self.dataQuery.commit()
        except ValueError as error:
            print('Log Error',error)
    # Check Author Program
    def checkLogin(self,email):
        query="select email,password,roleUsser from Users where email=?"
        params=(email)
        try:
            self.dataQuery.execute(query,params)
            return self.dataQuery.fetchall()
        except ValueError as error:
            print("Log Error",error)
    def checkRegister(self,email):
        query="select email,password from Users where email=?"
        params=(email)
        try:
            self.dataQuery.execute(query,params)
            return self.dataQuery.fetchall()
        except ValueError as error:
            print("Log Error",error)
        # finally:
        #     self.dataQuery.close()
    def insertUserScreenLog(self,email,password):
        query="INSERT INTO Users(email,password) VALUES (?,?)"
        params=(email,password)
        try:
            self.dataQuery.execute(query,params)
            return self.dataQuery.commit()
        except ValueError as error:
            print('Log Error',error)
        finally:
            self.dataQuery.close()
    # Show value Combobox
    def showValueRoleUser(self):
        query="select roleUsser from Users"
        try:
            self.dataQuery.execute(query)
            return self.dataQuery.fetchall()
        except ValueError as error:
            print("Log Error",error)
    def changePasswordUser(self):
        print
