import pyodbc
import ConnectDB as db
class NhanVien:
    def __init__(self):
        self.data=db.ConnectDataBase()
        self.dataConnect=self.data.ConnectDB()
        self.dataQuery=self.dataConnect.cursor()
    def __del__(self):
        if self.data != None:
            self.dataConnect.close()
    def showDataNhanVien(self):
        query='''select nv.maNV,name,email,phone,address,gender,birthday,tenCV as 'Position',tenPB as 'Deparment',luongThucNhan as 'Wage',tenTrinhDo as 'Level'
            from NhanVien nv, ChucVu cv, PhongBan pb,BangLuong bl, TrinhDoHocVan hv
            where nv.maNV=cv.maNV and nv.maNV=pb.maNV and nv.maNV=bl.maNV and nv.maNV=hv.maNV'''
        try:
            return self.dataQuery.execute(query).fetchall()
        except ValueError as error:
            print('Log Error',error)
    def showDataProfile(self,maNV):
        query='''select nv.maNV,name,email,phone,address,gender,birthday,tenCV as 'Position',tenPB as 'Deparment',luongThucNhan as 'Wage',tenTrinhDo as 'Level',password
            from NhanVien nv, ChucVu cv, PhongBan pb,BangLuong bl, TrinhDoHocVan hv
            where nv.maNV=cv.maNV and nv.maNV=pb.maNV and nv.maNV=bl.maNV and nv.maNV=hv.maNV and nv.maNV=?'''
        params=(maNV)
        try:
            self.dataQuery.execute(query,params)
            return self.dataQuery.fetchone()
        except ValueError as error:
            print('Log Error',error)
    def checkEmployee(self,manv):
        query="select maNV from NhanVien where maNV=?"
        params=(manv)
        try:
            return self.dataQuery.execute(query,params)
        except ValueError as error:
            print('Log Error',error)
    def insertEmployeeMenuScreen(self,maNV,name,email,phone,address,gender,birthday,avatar):
        query="insert into NhanVien (maNV,name,email,phone,address,gender,birthday) VALUES (?,?,?,?,?,?,?)"
        parrams=(maNV,name,email,phone,address,gender,birthday)
        try:
            self.dataQuery.execute(query,parrams)
            return self.dataQuery.commit()
        except ValueError as error:
            print('Log Error',error)
    def deleteEmployee(self,maNV,maCV,maL,maPB,maTD):
        query=      '''
                    Delete from TrinhDoHocVan where maNV=?
                    Delete from PhongBan where maNV=?
                    Delete from BangLuong where maNV=?
                    Delete from ChucVu where maNV=?
                    Delete from NhanVien where maNV=?
                    '''
        params=(maNV,maCV,maL,maPB,maTD)
        try:
            self.dataQuery.execute(query,params)
            return self.dataQuery.commit()
        except ValueError as error:
            print('Log Error',error)
    def updateEmployee(self,email,name,phone,address,gender,birthday,maNV):
        query="update NhanVien set email=?,name=?,phone=?,address=?,gender=?,birthday=? where maNV=?"
        params=(email,name,phone,address,gender,birthday,maNV)
        try:
            self.dataQuery.execute(query,params)
            return self.dataQuery.commit()
        except ValueError as error:
            print('Log Error',error)
    def findDataEmployee(self,employeeFind):
        query='''
            select nv.maNV,name,email,phone,address,gender,birthday,tenCV as 'Position',tenPB as 'Deparment',luongThucNhan as 'Wage',tenTrinhDo as 'Level'
            from NhanVien nv, ChucVu cv, PhongBan pb,BangLuong bl, TrinhDoHocVan hv
            where nv.maNV=cv.maNV and nv.maNV=pb.maNV and nv.maNV=bl.maNV and nv.maNV=hv.maNV and name like '%' + ? + '%'
            '''
        params=(employeeFind)
        try:
            return self.dataQuery.execute(query,params)
        except ValueError as error:
            print('Log Error',error)
    def findIDDataEmployee(self,employeeFind):
        query='''
            select nv.maNV,name,email,phone,address,gender,birthday,tenCV as 'Position',tenPB as 'Deparment',luongThucNhan as 'Wage',tenTrinhDo as 'Level'
            from NhanVien nv, ChucVu cv, PhongBan pb,BangLuong bl, TrinhDoHocVan hv
            where nv.maNV=cv.maNV and nv.maNV=pb.maNV and nv.maNV=bl.maNV and nv.maNV=hv.maNV and nv.maNV like '%' + ? + '%'
            '''
        params=(employeeFind)
        try:
            return self.dataQuery.execute(query,params)
        except ValueError as error:
            print('Log Error',error)
    def uploadIMG(self,image):
        query="update NhanVien set avatar=%s where maNV='2'"
        params=(image)
        try:
            self.dataQuery.execute(query,params)
            return self.dataQuery.commit()
        except ValueError as error:
            print('Log Error',error)
    def checkTypeAvatar(self,maNV):
        query="select avatar From NhanVien where maNV=?"
        params=(maNV)
        try:
            self.dataQuery.execute(query,maNV)
            return self.dataQuery.fetchone()
        except ValueError as error:
            print("Log Error",error)
    def checkLoginNhanVien(self,email):
        query="select email,password,role from NhanVien where email=?"
        params=(email)
        try:
            self.dataQuery.execute(query,params)
            return self.dataQuery.fetchall()
        except ValueError as error:
            print("Log Error",error)
    def changePasswordEmployee(self,password,maNV):
        query="update NhanVien set password=? where maNV=?"
        params=(password,maNV)
        try:
            self.dataQuery.execute(query,params)
            return self.dataQuery.commit()
        except ValueError as error:
            print('Log Error',error)
class ChucVu(NhanVien):
    def __init__(self):
        NhanVien.__init__(self)
    def __del__(self):
        NhanVien.__del__(self)
    def showDataName(self):
        query="select tenCV from ChucVu"
        try:
            self.dataQuery.execute(query)
            return self.dataQuery.fetchall()
        except ValueError as error:
            print('Log Error',error)
    def insertPosition(self,deparment,maNV):
        query="insert into ChucVu(tenCV,maNV) VALUES (?,?)"
        parrams=(deparment,maNV)
        try:
            self.dataQuery.execute(query,parrams)
            return self.dataQuery.commit()
        except ValueError as error:
            print('Log Error',error)
    def updateEmployeePosition(self,position,manv):
        query="update ChucVu set tenCV=? where maNV=?"
        params=(position,manv)
        try:
            self.dataQuery.execute(query,params)
            return self.dataQuery.commit()
        except ValueError as error:
            print('Log Error',error)
    def optionAddPosition(self,tenCV):
        query="insert into ChucVu(tenCV) values(?)"
        params=(tenCV)
        try:
            self.dataQuery.execute(query,params)
            return self.dataQuery.commit()
        except ValueError as error:
            print("Log Error",error)
    def checkIsExitPosition(self,tenCV):
        query="select tenCV from ChucVu where tenCV=?"
        params=(tenCV)
        try:
            self.dataQuery.execute(query,params)
            return self.dataQuery.fetchone()
        except ValueError as error:
            print('Log Error',error)
class PhongBan(NhanVien):
    def __init__(self):
        NhanVien.__init__(self)
    def __del__(self):
        NhanVien(self)
    def insertDeparment(self,tenPB,maNV):
        query="insert into PhongBan(tenPB,maNV) VALUES (?,?)"
        parrams=(tenPB,maNV)
        try:
            self.dataQuery.execute(query,parrams)
            return self.dataQuery.commit()
        except ValueError as error:
            print('Log Error',error)
    def updateEmployeeDeparment(self,deparment,manv):
        query="update PhongBan set tenPB=? where maNV=?"
        params=(deparment,manv)
        try:
            self.dataQuery.execute(query,params)
            return self.dataQuery.commit()
        except ValueError as error:
            print('Log Error',error)
    def checkNameDeparment(self,tenPB):
        query="select tenPB from PhongBan where tenPB=?"
        params=(tenPB)
        try:
            self.dataQuery.execute(query,params)
            return self.dataQuery.fetchone()
        except ValueError as error:
            print('Log Error',error)
    def addOptionDeparment(self,tenPB,diaChi,sdt):
        query="insert into PhongBan(tenPB,diaChi,sdt) values(?,?,?)"
        params=(tenPB,diaChi,sdt)
        try:
            self.dataQuery.execute(query,params)
            return self.dataQuery.commit()
        except ValueError as error:
            print('Log Error',error)
    def loadDataDeparment(self):
        query="select tenPB from PhongBan"
        try:
            self.dataQuery.execute(query)
            return self.dataQuery.fetchall()
        except ValueError as error:
            print("Log Error",error)

class BangLuong(NhanVien):
    def __init__(self):
        NhanVien.__init__(self)
    def __del__(self):
        NhanVien.__del__(self)
    def insertSalary(self,luongCoban,maNV):
        query="insert into BangLuong(luongCoban,maNV) VALUES (?,?)"
        parrams=(luongCoban,maNV)
        try:
            self.dataQuery.execute(query,parrams)
            return self.dataQuery.commit()
        except ValueError as error:
            print('Log Error',error)
    def updateEmployeeSalary(self,luongCoban,manv):
        query="update BangLuong set luongCoban=? where maNV=?"
        params=(luongCoban,manv)
        try:
            self.dataQuery.execute(query,params)
            return self.dataQuery.commit()
        except ValueError as error:
            print('Log Error',error)
    def updateResultSalary(self,salary,hesoluong,bacluong,maNV):

        query='''
        update BangLuong set luongThucNhan=?,heSoLuong=?,bacLuong=? where maNV=? 
        '''
        params=(salary,hesoluong,bacluong,maNV)
        try:
            self.dataQuery.execute(query,params)
            return self.dataQuery.commit()
        except ValueError as error:
            print('Log Error',error)
    def loadDataSalary(self):
        query="select luongCoban from BangLuong"
        try:
            self.dataQuery.execute(query)
            return self.dataQuery.fetchall()
        except ValueError as error:
            print('Log Error',error)
    def showTotalSalary(self,maNV):
        query="select bl.luongThucNhan from NhanVien nv, BangLuong bl where nv.maNV=bl.maNV and nv.maNV=?"
        try:
            self.dataQuery.execute(query,maNV)
            return self.dataQuery.fetchone()
        except ValueError as error:
            print('Log Error',error)
    def saveNumTimeWork(self,dayWork,maNV):
        query=" update BangLuong set ngayCong=? where maNV=? "
        params=(dayWork,maNV)
        try:
            self.dataQuery.execute(query,params)
            return self.dataQuery.commit()
        except ValueError as error:
            print('Log Error',error)
    def showDataNumTimeWork(self,maNV):
        query="select ngayCong from BangLuong bl, NhanVien nv where nv.maNV=bl.maNV and nv.maNV=?"
        params=(maNV)
        try:
            self.dataQuery.execute(query,params)
            return self.dataQuery.fetchone()
        except ValueError as error:
            print('Log Error',error)
class TrinhDoHocVan(NhanVien):
    def __init__(self):
        NhanVien.__init__(self)
    def __del__(self):
        NhanVien.__del__(self)
    def insertLevelLearn(self,tenTrinhDo,maNV):
        query="insert into TrinhDoHocVan(tenTrinhDo,maNV) VALUES (?,?)"
        parrams=(tenTrinhDo,maNV)
        try:
            self.dataQuery.execute(query,parrams)
            return self.dataQuery.commit()
        except ValueError as error:
            print('Log Error',error)
    def updateEmployeeLevelLearn(self,tenTrinhDo,manv):
        query="update TrinhDoHocVan set tenTrinhDo=? where maNV=?"
        params=(tenTrinhDo,manv)
        try:
            self.dataQuery.execute(query,params)
            return self.dataQuery.commit()
        except ValueError as error:
            print('Log Error',error)
    def checkDataNameMajor(self,nameLevel):
        query="select tenTrinhDo from TrinhDoHocVan where tenTrinhDo=?"
        params=(nameLevel)
        try:
            self.dataQuery.execute(query,params)
            return self.dataQuery.fetchone()
        except ValueError as error:
            print('Log Error',error)
    def addMajorLevelLearn(self,nameLevel,major):
        query="insert into TrinhDoHocVan(tenTrinhDo,chuyenNghanh) values(?,?)"
        params=(nameLevel,major)
        try:
            self.dataQuery.execute(query,params)
            return self.dataQuery.commit()
        except ValueError as error:
            print('Log Error',error)
    def loadDataLevelMajor(self):
        query="select tenTrinhDo from TrinhDoHocVan"
        try:
            self.dataQuery.execute(query)
            return self.dataQuery.fetchall()
        except ValueError as error:
            print('Log Error',error)
class ChamCong(NhanVien):
    def __init__(self):
        NhanVien.__init__(self)
    def __del__(self):
        NhanVien.__del__(self)
    def showDataTimeKeeping(self,maNV,email):
        query="select nv.maNV,nv.name,GioVao,GioRa,ThoiGianLamViec,NgayLamViec,SoCong from NhanVien nv, ChamCong cc where nv.maNV=cc.maNV and nv.maNV=? or nv.email=?"
        params=(maNV,email)
        try:
            self.dataQuery.execute(query,params)
            return self.dataQuery.fetchall()
        except ValueError as error:
            print('Log Error',error)
    def insertDataTimeKeeping(self,timeIn,timeWork,dateWork,manv):
        query="insert into ChamCong(GioVao,ThoiGianLamViec,NgayLamViec,maNV) values(?,?,?,?)"
        params=(timeIn,timeWork,dateWork,manv)
        try:
            self.dataQuery.execute(query,params)
            return self.dataQuery.commit()
        except ValueError as error:
            print('Log Error',error)
    def updateTimeOut(self,timeOut,timeWork,numTimeKeeping,dayLockOut,maNV,ID):
        query="update ChamCong set GioRa=?,ThoiGianLamViec=?,SoCong=?,NgayLamViec=? where maNV=? and ID=?"
        params=(timeOut,timeWork,numTimeKeeping,dayLockOut,maNV,ID)
        try:
            self.dataQuery.execute(query,params)
            return self.dataQuery.commit()
        except ValueError as error:
            print('Log Error',error)
    def findUserByEmail(self,email):
        query="select maNV,name,password from NhanVien where email=?"
        params=(email)
        try:
            self.dataQuery.execute(query,params)
            return self.dataQuery.fetchone()
        except ValueError as error:
            print('Log Error',error)
    def checkClockIn(self,daywork,email):
        query="select nv.maNV,nv.name,GioVao,NgayLamViec from ChamCong cc, NhanVien nv where NgayLamViec=? and nv.email=? and nv.maNV=cc.maNV"
        params=(daywork,email)
        try:
            self.dataQuery.execute(query,params)
            return self.dataQuery.fetchall()
        except ValueError as error:
            print('Log Error',error)
    def checkClockOut(self,email,dateWork,timeWork):
        query='''
        select nv.maNV,nv.name,ThoiGianLamViec,NgayLamViec,GioRa
        from ChamCong cc, NhanVien nv 
        where nv.email=? and NgayLamViec=? and nv.maNV=cc.maNV or ThoiGianLamViec=?
        '''
        params=(email,dateWork,timeWork)
        try:
            self.dataQuery.execute(query,params)
            return self.dataQuery.fetchone()
        except ValueError as error:
            print('Log Error',error)
    def showDataTimeWorking(self,dateWork,maNV):
        query="select ID,GioVao,GioRa,NgayLamViec from ChamCong where NgayLamViec=? and maNV=?"
        params=(dateWork,maNV)
        try:
            self.dataQuery.execute(query,params)
            return self.dataQuery.fetchone()
        except ValueError as error:
            print('Log Error',error)
    def sumNumberTimeWorking(self,maNV):
        query="select COUNT(cc.SoCong) as 'Số ngày công'  from ChamCong  cc, NhanVien nv where nv.maNV=cc.maNV and nv.maNV=?"
        params=(maNV)
        try:
            self.dataQuery.execute(query,params)
            return self.dataQuery.fetchone()
        except ValueError as error:
            print('Log Error',error)


