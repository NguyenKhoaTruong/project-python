from tkinter import *
from tkinter.ttk import *
from time import strftime
from threading import Timer
from tkinter import messagebox as mb
from tkcalendar import Calendar,DateEntry
from tkinter import filedialog
from PIL import ImageTk,Image
import time
import imageio as iio
import pyodbc
import re
import imageio as iio
import pandas as pd
import Users as us
import NhanVien as nv
import os
import sys
import io
import json
import base64
import pickle
import matplotlib.pyplot as plt
from datetime import datetime
import time
import csv
import bcrypt
class MainMenu:
    def __init__(self,root):
        super().__init__()
        self.dataUs=us.Users()
        self.dataNv=nv.NhanVien()
        self.dataCV=nv.ChucVu()
        self.dataPB=nv.PhongBan()
        self.dataBL=nv.BangLuong()
        self.dataHV=nv.TrinhDoHocVan()
        self.dataCC=nv.ChamCong()
        self.dataTableUser=self.dataUs.showDataUser()
        self.dataTableNhanViens=self.dataNv.showDataNhanVien()
        self.reloadDataEmployee()
        self.reloadDataUser()
    def clear_frame(self):
        for widget in root.winfo_children():
            widget.destroy()
    def reloadDataEmployee(self):
        self.dataOne=self.dataNv.showDataNhanVien()
        return self.dataOne 
    def reloadDataUser(self):
        self.dataUser=self.dataUs.showDataUser()
        return self.dataUser 
    def screenMenu(self):
        self.clear_frame()
        self.reloadDataEmployee()
        #multiple variable
        self.name,self.genders,self.birthday,self.email,self.address,self.phone=(StringVar(),)*6
        def insertEmployeeIsEmpty():
            mb.showerror(title="Notification!!!",message="MaNV is Exits Please Enter New.")
        def insertSuccess():
            mb.showinfo(message="Insert Employee Success")
        def isEmptyEmployee():
            mb.showwarning(title='Notification',message='No info user. Please enter infomation')
        def notifiCheckGenDer():
            mb.showerror(title="Notification!!!",message="Inaccurate information")
        def deleteEmployeeSuccess():
            mb.showinfo(title='Notification!!!',message='Delete User Success')
        def deleteFail():
            mb.showerror(title='Notification!!!',message="User is not exits, Delete Fail")
        def updateEM():
            mb.showinfo(title="Notification",message='Update User Success')
        def addUser():
            #variable
            dataIMG=uploadImageUser()
            manv=self.inputIdUser.get()
            name=self.inputNameUser.get()
            email=self.inputLabelEmail.get()
            phone=self.inputPhoneUser.get()
            address=self.inputAddress.get()
            gender=self.genders.get()
            birthday=datePicker.get_date()
            birthdayConvert=birthday.strftime('%m/%d/%Y') #convert datetime.datee to string
            position=self.positionEm.get()
            deparment=self.deparmentEm.get()
            salary=self.salaryEm.get()
            levelLearn=self.levelAcademy.get()
            
            # ảnh chưa lưu được ảnh
            #connect data
            if  manv and email:
                dataCheckMaNv=self.dataNv.checkEmployee(manv)
                if dataCheckMaNv == None:
                    insertEmployeeIsEmpty()
                else:
                    self.dataNv.insertEmployeeMenuScreen(manv,name,email,phone,address,gender,birthdayConvert)
                    self.dataCV.insertPosition(position,manv)
                    self.dataPB.insertDeparment(deparment,manv)
                    self.dataBL.insertSalary(salary,manv)
                    self.dataHV.insertLevelLearn(levelLearn,manv)
                    insertSuccess
                    clearDataUser()
                    #reload data table
                    self.reloadDataEmployee()
                    self.screenMenu()
            else:
                isEmptyEmployee()
        def editUser():
            self.inputIdUser.delete(0,"end")
            self.inputNameUser.delete(0,'end')
            self.inputLabelEmail.delete(0,'end')
            self.inputPhoneUser.delete(0,'end')
            self.inputAddress.delete(0,'end')
            selected=self.TableUser.focus()
            values=self.TableUser.item(selected,'values')
            self.inputIdUser.insert(0,values[0])
            self.inputNameUser.insert(0,values[1])  
            self.inputLabelEmail.insert(0,values[2])
            datePicker.set_date(values[6])
            if values[5].rstrip() == 'Male':
                self.genders.set('Male')
            elif values[5].rstrip() == 'Female':
                self.genders.set('Female')
            else:
               notifiCheckGenDer()
            self.inputAddress.insert(0,values[4])
            self.inputPhoneUser.insert(0,values[3]) 
            self.positionEm.set(values[7])
            self.deparmentEm.set(values[8])
            self.salaryEm.set(values[9])
            self.levelAcademy.set(values[10])
            checkDataAvarta=self.dataNv.checkTypeAvatar(self.inputIdUser.get())
            dataAvatarByte=str(checkDataAvarta).encode()
            img = Image.frombytes('RGB', (640, 480), dataAvatarByte)
            img.show()
            # dataAvatarByteArray=bytearray(checkDataAvarta)
            # print('check type avater araybytes',dataAvatarByteArray)
            # if checkDataAvarta:
            #     byte_array=str(checkDataAvarta).encode()
            #     img = Image.frombytes('RGB', (640, 480), byte_array)
            #     img.show()
            #     mb.showerror(message="User đã có ảnh?")
            # else:
            #      mb.showerror(message="User chưa có ảnh?")
            if self.btnSave.cget("state") == "disabled":
                self.btnSave.config(state="normal")   
            else:
                self.btnSave.config(state="normal")
                self.btnEditUser.config(state="disabled")
                self.btnDelUser.config(state="disabled")
                self.labelEmail.config(state="disabled")
                self.inputLabelEmail.config(state="disabled")
                self.btnAddUser.config(state="disabled")
                self.btnClearInfoUser.config(state="disabled")
                self.btnAddImage.config(state="normal")
                self.btnBackHome.config(state="disabled")
                self.inputIdUser.config(state="disabled")
        def deleteUser():
            try:
                selected=self.TableUser.focus()
                if selected != None:
                    values=self.TableUser.item(selected,'values')
                    self.dataNv.deleteEmployee(values[0],values[0],values[0],values[0],values[0])
                    deleteEmployeeSuccess()
                    self.reloadDataEmployee()
                    self.screenMenu()
                elif selected==None:
                    deleteFail()
            except ValueError as e:
                print('Log Error',e)
        def clearDataUser():
            self.inputIdUser.delete(0,'end')
            self.inputNameUser.delete(0,'end')
            self.inputLabelEmail.delete(0,'end')
            self.inputPhoneUser.delete(0,'end')
            self.inputAddress.delete(0,'end')
            self.genders.set(None)
            self.inputIdUser.delete(0,'end')
            positionCB.current(0)
            deparmentCB.current(0)
            salaryCB.current(0)
            levelCB.current(0)
            self.inputNumSalary.delete(0,'end')
            self.inputRankSalary.delete(0,'end')
            self.inputSearchUser.delete(0,'end')

        def saveChange():
            manv=self.inputIdUser.get()
            name=self.inputNameUser.get()
            email=self.inputLabelEmail.get()
            phone=self.inputPhoneUser.get()
            address=self.inputAddress.get()
            gender=self.genders.get()
            birthday=datePicker.get_date()
            birthdayConvert=birthday.strftime('%m/%d/%Y') #convert datetime.datee to string
            position=self.positionEm.get()
            deparment=self.deparmentEm.get()
            salary=self.salaryEm.get()
            levelLearn=self.levelAcademy.get()
            self.dataNv.updateEmployee(email,name,phone,address,gender,birthdayConvert,manv)
            self.dataCV.updateEmployeePosition(position,manv)
            self.dataPB.updateEmployeeDeparment(deparment,manv)
            self.dataBL.updateEmployeeSalary(salary,manv)
            self.dataHV.updateEmployeeLevelLearn(levelLearn,manv)
            updateEM()
            if self.btnAddUser.cget("state") == "disabled" and self.btnEditUser.cget("state") == "disabled" and self.btnDelUser.cget("state") == "disabled" and self.btnBackHome.cget("state")=="disabled" and self.btnAddImage.cget("state")=="disable" and self.btnClearInfoUser.cget("state")=="disable" :
                self.btnSave.config(state="normal")             
            else:
                self.btnEditUser.config(state="normal")
                self.btnDelUser.config(state="normal")
                self.labelEmail.config(state="normal")
                self.inputLabelEmail.config(state="normal")
                self.btnAddUser.config(state="normal")
                self.btnClearInfoUser.config(state="normal")
                self.btnAddImage.config(state="normal")
                self.btnBackHome.config(state="normal")
            clearDataUser()
            self.reloadDataEmployee()
            self.screenMenu()
        def paymentEmployee():
            def calSalarySuccess():
                mb.showinfo(title="Notification",message="Caculate Success")
            def emptyID():
                mb.showwarning(title="Notification",message="MaNV is Empty Please Entern")
            def showMessageSumNumberTimeWork():
                mb.showwarning(title="Notification!!!",message="Employee Not Work Please Check.")
            try:
                numSalary=self.inputNumSalary.get()
                rankSalary=self.inputRankSalary.get()
                basicSalary=self.salaryEm.get()
                maNV=self.inputIdUser.get()
                sumNumberTimeWork=self.dataCC.sumNumberTimeWorking(maNV)
                # check khi user chưa có ngày công
                if sumNumberTimeWork[0] == 0:
                    showMessageSumNumberTimeWork()
                    clearDataUser()
                elif sumNumberTimeWork:
                    saveDataDateWork=self.dataBL.saveNumTimeWork(sumNumberTimeWork[0],maNV)
                    numberTimeDayWork=self.dataBL.showDataNumTimeWork(maNV)
                    dataCaculateSalary=int(numSalary)*int(rankSalary)*int(basicSalary)/int(numberTimeDayWork[0])
                    if maNV:
                        self.dataBL.updateResultSalary(dataCaculateSalary,numSalary,rankSalary,maNV)
                        calSalarySuccess()
                        clearDataUser()
                        #load data table
                        # self.screenMenu()
                    else:
                        emptyID()
            except ValueError as error:
                print('Log Error',error)
        def uploadImageUser():
                def showAddImageSuccess():
                    mb.showinfo(title="Notificitation",message="Upload IMG Success")
                def showAddImageFail():
                    mb.showerror(title="Notificiation",message="Upload IMG Fail")
                try:
                    maNV=self.inputIdUser.get()
                    t_types=[('*.png'),('*jpg'),('*.jpeg')] 
                    fileName= filedialog.askopenfilename(title='open',typevariable=t_types)
                    img=Image.open(fileName)
                    img=img.resize((150,190),Image.ANTIALIAS)
                    img=ImageTk.PhotoImage(img) 
                    panel=Label(root,image=img) 
                    panel.image=img 
                    panel.place(x=1000,y=75)
                    #cũ
                    # with open(fileName,"rb") as f:
                    #     dataConvernt= f.read()  
                    #     dataIMG=pyodbc.Binary(dataConvernt)
                    # data=self.dataNv.uploadIMG(dataIMG,maNV)
                    #new
                    with open(fileName,"rb") as f: 
                        # chuyển đổi file -> base64
                        dataIMG=base64.b64decode(f.read())
                    data=self.dataNv.uploadIMG(dataIMG)
                    if data:
                        mb.showinfo(message="Upload Image Success")
                    else:
                        mb.showinfo(message="Upload Image Fail")
                except ValueError as error:
                    print('Log Error',error)

        def findUser():
            def noValues():
                mb.showwarning(title="",message="No Values In DataBase")
            def noValuesInput():
                mb.showwarning(title="",message="No Values Data Input")
            valuesFind=self.inputSearchUser.get()
            dataFind=self.dataNv.findDataEmployee(valuesFind)
            if valuesFind and dataFind:
                if self.btnPayRollEm.cget("state")=="disabled":
                    self.btnPayRollEm.config(state="normal")
                    self.inputNumSalary.config(state="normal")
                    self.inputRankSalary.config(state="normal")
                    self.labelNumSalary.config(state="normal")
                    self.labelRankSalary.config(state="normal")
                else:
                    self.btnPayRollEm.config(state="normal")
                    self.inputNumSalary.config(state="normal")
                    self.inputRankSalary.config(state="normal")
                    self.labelNumSalary.config(state="normal")
                    self.labelRankSalary.config(state="normal")
                for row in self.TableUser.get_children():
                    self.TableUser.delete(row)
                for valueFind in dataFind:
                    self.TableUser.insert('',END,values=tuple(valueFind))
                    self.inputIdUser.insert(0,valueFind[0])
                    self.inputLabelEmail.insert(0,valueFind[2])
                    self.inputAddress.insert(0,valueFind[4])
                    self.inputNameUser.insert(0,valueFind[1])
                    datePicker.set_date(valueFind[6])
                    if valueFind[5].rstrip() == 'Male':
                        self.genders.set('Male')
                    elif valueFind[5].rstrip() == 'Female':
                        self.genders.set('Female')
                    else:
                        notifiCheckGenDer()
                    self.inputPhoneUser.insert(0,valueFind[3])
                    self.positionEm.set(valueFind[7])
                    self.deparmentEm.set(valueFind[8])
                    self.salaryEm.set(valueFind[9])
                    self.levelAcademy.set(valueFind[10])
            else:
                noValues()
                self.screenMenu()
        def exportData():
            def showSaveDataSuceess():
                mb.showinfo(title="Notification!!!",message="Export Data Success")
            headerColumns=['MaNV','Name','Email','Phone','Address','GenDer','Birthday','Position','Deparment','Salary','Level']
            with open('dataEmployee.csv','w',encoding='UTF8',newline='') as f:
                write=csv.writer(f)
                write.writerow(headerColumns)
                write.writerows(self.dataTableNhanViens)
                showSaveDataSuceess()
        self.titleFrameManageUser=LabelFrame(root,text='Infomation Employee',labelanchor='n')
        self.idUser=Label(self.titleFrameManageUser,text='MaNV:',font=('calibre',10)).place(x=30,y=20)
        self.inputIdUser=Entry(self.titleFrameManageUser,font=('calibre',10,'bold'))
        self.inputIdUser.place(x=80,y=20)
        self.labelEmail=Label(self.titleFrameManageUser,text="Email:",font=('calibre',10))
        self.labelEmail.place(x=30,y=70)
        self.inputLabelEmail=Entry(self.titleFrameManageUser,font=('caliber',10))
        self.inputLabelEmail.place(x=80,y=70)
        self.labelBir=Label(self.titleFrameManageUser,text="Birthday:",font=('calibre',10)).place(x=30,y=120)
        self.labelAddress=Label(self.titleFrameManageUser,text='Address',font=('calibre',10)).place(x=30,y=170)
        self.inputAddress=Entry(self.titleFrameManageUser,font=('calibre',10))
        self.inputAddress.place(x=80,y=170,width=450)
        self.labelNumSalary=Label(self.titleFrameManageUser,text="Num Salary:",state=DISABLED)
        self.labelNumSalary.place(x=30,y=210)
        self.inputNumSalary=Entry(self.titleFrameManageUser,font=("carible",10,'bold'),state=DISABLED)
        self.inputNumSalary.place(x=100,y=205)
        self.labelRankSalary=Label(self.titleFrameManageUser,text="Wage:",state=DISABLED)
        self.labelRankSalary.place(x=300,y=210)
        self.inputRankSalary=Entry(self.titleFrameManageUser,font=("calibre",10,'bold'),state=DISABLED)
        self.inputRankSalary.place(x=350,y=205)
        self.labelNameUser=Label(self.titleFrameManageUser,text='Name:',font=('calibre',10)).place(x=300,y=20)
        self.inputNameUser=Entry(self.titleFrameManageUser,font=('calibre',10,'bold'))
        self.inputNameUser.place(x=380,y=20)
        self.labelGender=Label(self.titleFrameManageUser,text='Gender:',font=('calibre',10)).place(x=300,y=70)
        self.radioMale=Radiobutton(self.titleFrameManageUser,text='Male',value="Male",variable=self.genders)
        self.radioMale.place(x=380,y=70)
        self.radioFemale=Radiobutton(self.titleFrameManageUser,text='Female',value="Female",variable=self.genders)
        self.radioFemale.place(x=450,y=70)
        self.labelPhone=Label(self.titleFrameManageUser,text='Phone',font=('calibre',10)).place(x=300,y=120)
        self.labelPosition=Label(self.titleFrameManageUser,text="Position:",font=('calibre',10)).place(x=600,y=20)
        self.positionEm=StringVar()
        positionCB=Combobox(self.titleFrameManageUser,width=27,textvariable=self.positionEm)
        if self.dataCV.showDataName():
            datafill=self.dataCV.showDataName()
            result=[''.join(list(filter(str.isalnum,line))) for line in datafill]
            while('' in result):
                result.remove('')
            positionCB['values']=result
            positionCB.current(0)
            positionCB.place(x=680,y=20)
            positionCB.config(width=20)
        else:
            positionCB['values']=('No Data')
        self.btnAddPosition=Button(self.titleFrameManageUser,text="+",command=self.menuPosition)
        self.btnAddPosition.place(x=850,y=20)
        self.labelPB=Label(self.titleFrameManageUser,text="Deparment:",font=('calibre',10))
        self.labelPB.place(x=600,y=70)
        self.deparmentEm=StringVar()
        deparmentCB=Combobox(self.titleFrameManageUser,width=27,textvariable=self.deparmentEm)
        if self.dataPB.loadDataDeparment():
            dataDeparment=self.dataPB.loadDataDeparment()
            result=["".join(list(filter(str.isalnum,line))) for line in dataDeparment]
            while('' in result):
                result.remove('')
            deparmentCB['values']=result
            deparmentCB.current(0)
            deparmentCB.place(x=680,y=70)
            deparmentCB.config(width=20)
        else:
            deparmentCB['values']=("No Data")
        self.btnAddDeparment=Button(self.titleFrameManageUser,text="+",command=self.menuDeparment)
        self.btnAddDeparment.place(x=850,y=70)
        self.labelSalary=Label(self.titleFrameManageUser,text="Salary Basic:",font=('calibre',10))
        self.labelSalary.place(x=600,y=120)
        self.salaryEm=StringVar()
        salaryCB=Combobox(self.titleFrameManageUser,width=27,textvariable=self.salaryEm)
        if self.dataBL.loadDataSalary():
            dataSalary=self.dataBL.loadDataSalary()
            result=["".join(list(filter(str.isalnum,line))) for line in str(dataSalary)]
            while('' in result):
                result.remove('')
            salaryCB['values']=result
            salaryCB.current(0)
            salaryCB.place(x=680,y=120)
            salaryCB.config(width=20)
        else:
            salaryCB['values']=("No Data")
        self.levelLearn=Label(self.titleFrameManageUser,text="Level:",font=("calibre",10))
        self.levelLearn.place(x=600,y=170)
        self.levelAcademy=StringVar()
        levelCB=Combobox(self.titleFrameManageUser,width=27,textvariable=self.levelAcademy)
        if self.dataHV.loadDataLevelMajor():
            dataLevelLearn=self.dataHV.loadDataLevelMajor()
            result=["".join(list(filter(str.isalnum,line))) for line in dataLevelLearn]
            while('' in result):
                result.remove('')
            levelCB['values']=result
            levelCB.current(0)
            levelCB.place(x=680,y=170)
            levelCB.config(width=20)
        else:
             levelCB['values']=("No Data")
        self.btnAddLevel=Button(self.titleFrameManageUser,text="+",command=self.menuLevelLearn)
        self.btnAddLevel.place(x=850,y=170)
        self.inputPhoneUser=Entry(self.titleFrameManageUser,font=('calibre',10))
        self.inputPhoneUser.place(x=380,y=120)
        self.frameImageeUser=Frame(self.titleFrameManageUser,width=150,height=180,borderwidth=2,relief="groove")
        self.frameImageeUser.place(x=1000,y=20)
        self.titleFunManageUser=Label(self.titleFrameManageUser,text='Fucntion',font=('calibre',10))
        self.titleFunManageUser.place(x=850,y=250)
        self.btnAddUser=Button(self.titleFrameManageUser,text="Add",command=addUser)
        self.btnAddUser.place(x=850,y=280)
        self.btnEditUser=Button(self.titleFrameManageUser,text="Edit",command=editUser)
        self.btnEditUser.place(x=850,y=310)
        self.btnDelUser=Button(self.titleFrameManageUser,text="Delete",command=deleteUser)
        self.btnDelUser.place(x=850,y=340)
        self.btnClearInfoUser=Button(self.titleFrameManageUser,text="Clear",command=clearDataUser)
        self.btnClearInfoUser.place(x=950,y=340)
        self.btnPayRollEm=Button(self.titleFrameManageUser,text="PayRoll",command=paymentEmployee,state=DISABLED)
        self.btnPayRollEm.place(x=1030,y=340)
        self.btnAddImage=Button(self.titleFrameManageUser,text="Upload Image",command=uploadImageUser)
        self.btnAddImage.place(x=1035,y=210)
        self.btnSave=Button(self.titleFrameManageUser,text="Save",command=saveChange,state=DISABLED)
        self.btnSave.place(x=950,y=280)
        self.labelSearchUser=Label(self.titleFrameManageUser,text="Find User By Name:",font=("calibre",10))
        self.labelSearchUser.place(x=1030,y=250)
        self.inputSearchUser=Entry(self.titleFrameManageUser,font=("calibre",10))
        self.inputSearchUser.place(x=1030,y=280)
        self.btnSearchUser=Button(self.titleFrameManageUser,text="Search",command=findUser)
        self.btnSearchUser.place(x=1030,y=310)
        self.btnExportData=Button(self.titleFrameManageUser,text="Export Data",command=exportData)
        self.btnExportData.place(x=950,y=310)
        self.titleFrameManageUser.pack(fill="both",expand="yes")
        self.TableUser=Treeview(root,selectmode="browse")
        self.TableUser.pack(side="right")
        verscrlbar=Scrollbar(root,orient="vertical",command=self.TableUser.yview)
        verscrlbar.pack(side="right",fill='x')
        self.TableUser.configure(xscrollcommand=verscrlbar.set)
        self.TableUser.place(x=30,y=300,width=800,height=200)
        self.TableUser['columns']=('MaNV','Name','Email','Phone','Address','GenDer','Birthday','Position','Deparment','Salary','Level')
        self.TableUser.column("#0",width=0,stretch=NO)
        self.TableUser.column('MaNV',anchor=CENTER,width=80)
        self.TableUser.column('Name',anchor=CENTER,width=80)
        self.TableUser.column('Email',anchor=CENTER,width=80)
        self.TableUser.column('Phone',anchor=CENTER,width=80)
        self.TableUser.column('Address',anchor=CENTER,width=80)
        self.TableUser.column('GenDer',anchor=CENTER,width=80)
        self.TableUser.column('Birthday',anchor=CENTER,width=80)
        self.TableUser.column('Position',anchor=CENTER,width=80)    
        self.TableUser.column('Deparment',anchor=CENTER,width=80)
        self.TableUser.column('Salary',anchor=CENTER,width=80)
        self.TableUser.column('Level',anchor=CENTER,width=80)
        self.TableUser.heading("#0",text="",anchor=CENTER)
        self.TableUser.heading('MaNV',text="MaNV",anchor=CENTER)
        self.TableUser.heading('Name',text="Name",anchor=CENTER)
        self.TableUser.heading('Email',text="Email",anchor=CENTER)
        self.TableUser.heading('Phone',text="Phone",anchor=CENTER)
        self.TableUser.heading('Address',text="Address",anchor=CENTER)
        self.TableUser.heading('GenDer',text="GenDer",anchor=CENTER)
        self.TableUser.heading('Address',text="Address",anchor=CENTER)
        self.TableUser.heading('Birthday',text="Birthday",anchor=CENTER)
        self.TableUser.heading('Position',text="Position",anchor=CENTER)
        self.TableUser.heading('Deparment',text="Deparment",anchor=CENTER)
        self.TableUser.heading('Salary',text="Salary",anchor=CENTER)
        self.TableUser.heading('Level',text="Level",anchor=CENTER)
        for dataTables in self.dataTableNhanViens:
             self.dataTableNhanViens
             self.TableUser.insert('',END,values=tuple(dataTables))
        table_scroll=Scrollbar()
        varDate=StringVar()
        datePicker=DateEntry(root,selectmode='day',textVariable=varDate)
        datePicker.place(x=85,y=185,width=145)
        # check phân quyền
        if self.roleUser_str=='manager':
                self.btnDelUser.config(state="disabled")
                self.btnSave.config(state="normal")  
        if self.roleUser_str=='user':
                self.btnAddUser.config(state="disabled")
                self.btnEditUser.config(state="disabled")
                self.btnDelUser.config(state="disabled")
                self.btnSearchUser.config(state="disabled")
                self.btnAddPosition.config(state="disabled")
                self.btnAddDeparment.config(state="disabled")
                self.btnAddLevel.config(state="disabled")
                self.btnSave.config(state="disabled")
root = Tk()
myWin=MainMenu(root)
root.title('Manage User')
root.geometry("1200x500")
root.iconbitmap("logoFile.ico")
root.mainloop()
