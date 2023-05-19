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
        self.ScreenHomeMenu()
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
    def roleUserMenu(self):
        self.clear_frame()
        self.reloadDataUser()
        self.selectRoleUser=StringVar()
        def insertUserSuccess():
             mb.showinfo(title="Notification!!!",message="Add User Success!")
        def checkEmailInsert():
            mb.showwarning(title="Notification!!!",message="User Is Exits. Please Enter New Email")
        def updateSuccess():
            mb.showinfo(title="Notification!!!",message="Update User Success")
        def deleteUserSuccess():
            mb.showinfo(title="Notification",message="Delete User Success")
        def userNotDefine():
            mb.showwarning(title="Notification",message="User Is Not Define")
        # show all user Table

        #Fun : Add, Update , Delete
        def addUserInRoleMenu():
            email=self.inputValuesEmailUser.get()   
            password=self.inputValuesPasswordUser.get()
            role=self.selectRoleUser.get()
            dataEmailCheck=self.dataUs.checkEmail(email)
            emailIsExit=''
            for values in dataEmailCheck:
                emailIsExit=values[1]
            if email == emailIsExit.rstrip():
                checkEmailInsert()
            else:
                self.dataUs.insertUserRoleMenu(email,password,role)
                insertUserSuccess()
                self.inputValuesEmailUser.delete(0,"end")
                self.inputValuesPasswordUser.delete(0,"end")
                userRole.current(2)
                self.reloadDataUser()
                time.sleep(0.2)
        def chooseItemUser():
            self.inputValuesEmailUser.delete(0,"end")
            self.inputValuesPasswordUser.delete(0,"end")
            selected=self.TableRoleUser.focus()
            values=self.TableRoleUser.item(selected,"values")
            self.inputValuesEmailUser.insert(0,values[1])
            self.inputValuesPasswordUser.insert(0,values[2])
            userRole.set(values[3])
        def updateUserInRoleMenu():
            emailUpdate=self.inputValuesEmailUser.get()
            passwordUpdate=self.inputValuesPasswordUser.get()
            roleUpdate=self.selectRoleUser.get()
            self.dataUs.updateUserRoleMenu(passwordUpdate,roleUpdate,emailUpdate)
            updateSuccess()
            self.inputValuesEmailUser.delete(0,"end")
            self.inputValuesPasswordUser.delete(0,"end")
            userRole.current(2)
            #Fun Reload Table
            self.reloadDataUser()
            self.roleUserMenu()
        def delUserInRoleMenu():
            selected=self.TableRoleUser.focus()
            if selected != None:
                values=self.TableRoleUser.item(selected,'values')
                self.dataUs.deleteUserRoleMenu(values[1])
                deleteUserSuccess()
                # Fun reload data
                self.reloadDataUser()
                self.roleUserMenu()
            else:
                userNotDefine()
        def clearDataRoleMenu():
            self.inputValuesEmailUser.delete(0,"end")
            self.inputValuesPasswordUser.delete(0,"end")
            userRole.current(2)
        self.titleLabelRoleUser=Label(root,text="USER AUTHORAZETION",font=("carible",25,"bold")).place(x=450,y=100)
        self.inputLabelEmailUser=Label(root,text="Email:",font=("carible",10,"bold")).place(x=450,y=150)
        self.inputValuesEmailUser=Entry(root,font=("carible",10,"bold"))
        self.inputValuesEmailUser.place(x=520,y=150)
        self.inputLabelPasswordUser=Label(root,text="Password:",font=("carible",10,"bold")).place(x=450,y=200)
        self.inputValuesPasswordUser=Entry(root,font=("carible",10,"bold"),show="*")
        self.inputValuesPasswordUser.place(x=520,y=200)
        self.btnAddUser=Button(root,text="ADD",command=addUserInRoleMenu).place(x=700,y=150)
        self.btnUpUser=Button(root,text="UPDATE",command=updateUserInRoleMenu).place(x=700,y=200)
        self.btnDelUser=Button(root,text="DELETE",command=delUserInRoleMenu).place(x=700,y=250)
        self.btnBackMenu=Button(root,text="BACK",command=self.optionHomeMenu).place(x=800,y=150)
        self.btnClearDataMenu=Button(root,text="CLEAR",command=clearDataRoleMenu).place(x=800,y=200)
        self.btnChooseItemUser=Button(root,text="EDIT",command=chooseItemUser).place(x=800,y=250)
        # Combobox
        self.labelRole=Label(root,text="Role:",font=("carible",10,"bold"))
        self.labelRole.place(x=450,y=250)
        userRole=Combobox(root,width=27,textvariable=self.selectRoleUser)
        dataRoleUser=self.dataUs.showValueRoleUser()  
        # # map phân quyền dựa trên data base
        # if dataRoleUser:
        #     result=[''.join(list(filter(str.isalnum,line))) for line in dataRoleUser]
        #     while('' in result):
        #         result.remove('')
        #     userRole['values']=dataRoleUser
        #     userRole.current(2)
        #     userRole.place(x=520,y=250)
        #     userRole.config(width=20)
        # else:
        #     userRole['values']=('No Data')
        # Table
        userRole['values']=('admin','manager','user')
        userRole.current(2)
        userRole.place(x=520,y=250)
        userRole.config(width=20)
        self.TableRoleUser=Treeview(root,selectmode="browse")
        self.TableRoleUser.pack(side="right") 
        verscrlbar=Scrollbar(root,orient="vertical",command=self.TableRoleUser.yview)
        verscrlbar.pack(side="right",fill='x')  
        self.TableRoleUser.configure(xscrollcommand=verscrlbar.set)
        self.TableRoleUser.place(x=200,y=300,width=800,height=200)
        self.TableRoleUser['columns']=('ID','Email','Password','Role')
        self.TableRoleUser.column("#0",width=0,stretch=NO)
        self.TableRoleUser.column('ID',anchor=CENTER,width=80)
        self.TableRoleUser.column('Email',anchor=CENTER,width=80)
        self.TableRoleUser.column('Password',anchor=CENTER,width=80)
        self.TableRoleUser.column('Role',anchor=CENTER,width=80)
        self.TableRoleUser.heading("#0",text="",anchor=CENTER)
        self.TableRoleUser.heading('ID',text="ID",anchor=CENTER)
        self.TableRoleUser.heading('Email',text="Email",anchor=CENTER)
        self.TableRoleUser.heading('Password',text="Password",anchor=CENTER)
        self.TableRoleUser.heading('Role',text="Role",anchor=CENTER)
        data=self.dataUs.showDataUser()
        if data:
            for dataTab in data:
                self.TableRoleUser.insert('',END,values=(tuple(dataTab)))
        else:
            print('Error')
    def menuChart(self):
        self.timeWorkClockIn=0
        self.dateCheck=datetime.now().strftime("%d/%m/%Y")
        self.timeCheck=datetime.now().strftime("%H:%M:%S")
        self.dataClockIn=self.dataCC.checkClockIn(self.dateCheck,self.userName_str)
        self.dataClockOut=self.dataCC.checkClockOut(self.userName_str,self.dateCheck,'')
        self.numberWorK=1
        def showFindNoData():
            mb.showinfo(title="Notification!!!",message="No Data")
        def showDataClockInIsExit():
            mb.showwarning(title="Notification!!!",message="You Have Clock In, Please Check Again ")
        def showDataClockOutIsExit():
            mb.showwarning(title="Notification!!!",message="You Have Clock In, Please Check Again ")
        def loadDataFail():
            mb.showwarning(title="Notification!!!",message="Load Data Fail")
        def reloadDataTable():
            try:
                for item in self.TableTimeKeeping.get_children():
                    self.TableTimeKeeping.delete(item)
                dataCheck=self.dataCC.findUserByEmail(self.inputUser.get())
                if dataCheck:
                    dataTableTimeKeeping=self.dataCC.showDataTimeKeeping(dataCheck[0],'')
                    for dataTables in dataTableTimeKeeping:
                        self.TableTimeKeeping.insert('',END,values=tuple(dataTables))
                    self.inputUser.delete(0,'end')
                else:
                    loadDataFail()
            except ValueError as error:
                print('Log Error',error)
        def findUserByName():
            try:
                for item in self.TableTimeKeeping.get_children():
                    self.TableTimeKeeping.delete(item)
                dataCheck=self.dataCC.findUserByEmail(self.inputUser.get())
                # self.idUserMenu=dataCheck[0]
                if dataCheck:
                    dataTableTimeKeeping=self.dataCC.showDataTimeKeeping(dataCheck[0],'')
                    for dataTables in dataTableTimeKeeping:
                        self.TableTimeKeeping.insert('',END,values=tuple(dataTables))
                    self.inputUser.delete(0,'end')
                else:
                    showFindNoData()
            except ValueError as error:
                print('Log Error',error)
        def funClockIn():
            def clockInSuccess():
                mb.showinfo(title="Notification!!!",message="Clock In Success")
            dataUserImport=self.dataCC.findUserByEmail(self.userName_str)            
            if dataUserImport:
                self.dataCC.insertDataTimeKeeping(self.timeCheck,self.timeWorkClockIn,self.dateCheck,dataUserImport[0])
                clockInSuccess()
                self.btnClockIn.config(state="disabled")
            else:
                showFindNoData()
        def funClockOut():
            def clockOutSuccess():
                mb.showinfo(title="Notification!!!",message="Clock Out Success")
            dataUserImport=self.dataCC.findUserByEmail(self.userName_str)
            caculatorTimeWork=self.dataCC.showDataTimeWorking(self.dateCheck,dataUserImport[0])
            timeIn=caculatorTimeWork[1]
            timeOut=caculatorTimeWork[2]
            timeFormat="%H:%M:%S"
            timeInConvert=datetime.now().strptime(timeIn,timeFormat)
            timeCheckConvert=datetime.now().strptime(self.timeCheck,timeFormat)
            timeWork=timeCheckConvert-timeInConvert
            if dataUserImport:
                self.dataCC.updateTimeOut(self.timeCheck,str(timeWork),self.numberWorK,self.dateCheck,dataUserImport[0],caculatorTimeWork[0])
                clockOutSuccess()
                self.btnClockOut.config(state="disabled")
            else:
                showFindNoData()
        def exitProgram():
            root.destroy()
        def savePassword():
            def showSavePasswordSuccess():
                mb.showinfo(title="Notificitation!!!",message="Change Password Success")
            def showSavePasswordFail():
                mb.showinfo(title="Notificitation!!!",message="Change Password Fail")
            dataUser=self.dataCC.findUserByEmail(self.userName_str)
            self.inputCurrentPassword.get()
            self.inputNewPassword.get()
            if dataUser[2] == self.inputCurrentPassword.get() and self.inputNewPassword.get():
                self.dataNv.changePasswordEmployee(self.inputNewPassword.get(),dataUser[0])
                showSavePasswordSuccess()
            else:
                showSavePasswordFail()
            self.labelCurrentPassword.config(state="disabled")
            self.labelNewPassword.config(state="disabled")
            self.inputCurrentPassword.config(state="disabled")
            self.inputNewPassword.config(state="disabled")
            self.btnSavePassword.config(state="disabled")
            self.btnChangePassword.config(state="normal")
        def changePassword():
            self.labelCurrentPassword.config(state="normal")
            self.labelNewPassword.config(state="normal")
            self.inputCurrentPassword.config(state="normal")
            self.inputNewPassword.config(state="normal")
            self.btnSavePassword.config(state="normal")
            self.btnChangePassword.config(state="disabled")
        self.tabControl = Notebook(root)
        self.tabTimeKeeping = Frame(self.tabControl)
        self.tabInforUser = Frame(self.tabControl)
        self.tabControl.add(self.tabTimeKeeping, text ='Time Keeping')
        self.tabControl.add(self.tabInforUser, text ='Information User')
        self.tabControl.pack(expand = 1, fill ="both")
        self.labelFrameTimeKeeping=LabelFrame(self.tabTimeKeeping,text="Function Time Keeping",labelanchor="n")
        self.labelFrameTimeKeeping.place(x=20,y=20)
        self.labelFindUser=Label(self.labelFrameTimeKeeping,text="Find User By Email").place(x=10,y=20)
        self.inputUser=Entry(self.labelFrameTimeKeeping,font=("calibre",10,"bold"))
        self.inputUser.place(x=10,y=40)
        self.btnFindUserName=Button(self.labelFrameTimeKeeping,text="Find",command=findUserByName)
        self.btnFindUserName.place(x=40,y=80)
        self.btnClockIn=Button(self.labelFrameTimeKeeping,text="Clock In",command=funClockIn)
        self.btnClockIn.place(x=40,y=120)
        self.btnClockOut=Button(self.labelFrameTimeKeeping,text="Clock Out",command=funClockOut)
        self.btnClockOut.place(x=40,y=160)
        self.labelTimer=Label(self.labelFrameTimeKeeping,text="Timer",font=("Digital-7",10,'bold'),foreground='green')
        self.labelTimer.place(x=40,y=200)
        self.btnLoadData=Button(self.labelFrameTimeKeeping,text="Load Data",command=reloadDataTable)
        self.btnLoadData.place(x=40,y=240)
        self.btnExit=Button(self.labelFrameTimeKeeping,text="Exit",command=exitProgram)
        self.btnExit.place(x=40,y=280)
        self.labelTotalSalary=Label(self.labelFrameTimeKeeping,text="Total Salary:")
        self.labelTotalSalary.place(x=20,y=320)
        # Tính tổng lương
        # self.valuesTotalSalary=Label(self.labelFrameTimeKeeping,textvariable=self.dataShowTotal)
        # self.valuesTotalSalary.place(x=90,y=320)
        # table
        self.TableTimeKeeping=Treeview(self.labelFrameTimeKeeping,selectmode="browse")
        self.TableTimeKeeping.pack(side="right")
        verscrlbar=Scrollbar(self.labelFrameTimeKeeping,orient="vertical",command=self.TableTimeKeeping.yview)
        verscrlbar.pack(side="right",fill='x')
        self.TableTimeKeeping.configure(xscrollcommand=verscrlbar.set)
        self.TableTimeKeeping.place(x=200,y=20,width=950,height=1000)
        self.TableTimeKeeping['columns']=('MaNV','Name','Time In',"Time Out","Time Work","Date Work")
        self.TableTimeKeeping.column("#0",width=0,stretch=NO)
        self.TableTimeKeeping.column('MaNV',anchor=CENTER,width=80)
        self.TableTimeKeeping.column('Name',anchor=CENTER,width=80)
        self.TableTimeKeeping.column('Time In',anchor=CENTER,width=80)
        self.TableTimeKeeping.column('Time Out',anchor=CENTER,width=80)
        self.TableTimeKeeping.column('Time Work',anchor=CENTER,width=80)
        self.TableTimeKeeping.column("Date Work",anchor=CENTER,width=80)
        self.TableTimeKeeping.heading("#0",text="",anchor=CENTER)
        self.TableTimeKeeping.heading('MaNV',text="MaNV",anchor=CENTER)
        self.TableTimeKeeping.heading('Name',text="Name",anchor=CENTER)
        self.TableTimeKeeping.heading('Time In',text="Time In",anchor=CENTER)
        self.TableTimeKeeping.heading('Time Out',text="Time Out",anchor=CENTER)
        self.TableTimeKeeping.heading('Time Work',text="Time Work",anchor=CENTER)
        self.TableTimeKeeping.heading('Date Work',text="Date Work",anchor=CENTER)
        self.labelFrameTimeKeeping.pack(fill="both",expand="yes")
        self.labelFrameInfoUser=LabelFrame(self.tabInforUser,text="Profile User",labelanchor="n")
        self.labelFrameInfoUser.place(x=20,y=20)
        #profile user 
        self.labelNameUser=Label(self.labelFrameInfoUser,text="Name:",font=('Comic Sans MS',10,'bold'))
        self.labelNameUser.place(x=350,y=60)
        self.inputNameUser=Entry(self.labelFrameInfoUser)
        self.inputNameUser.place(x=440,y=60)
        self.labelEmailUser=Label(self.labelFrameInfoUser,text="Email:",font=('Comic Sans MS',10,'bold'))
        self.labelEmailUser.place(x=650,y=60)
        self.inputEmailUser=Entry(self.labelFrameInfoUser)
        self.inputEmailUser.place(x=740,y=60)
        self.labelPhoneUser=Label(self.labelFrameInfoUser,text="Phone:",font=('Comic Sans MS',10,'bold'))
        self.labelPhoneUser.place(x=350,y=120)
        self.inputPhoneUser=Entry(self.labelFrameInfoUser)
        self.inputPhoneUser.place(x=440,y=120)
        self.labelAddressUser=Label(self.labelFrameInfoUser,text="Address:",font=('Comic Sans MS',10,'bold'))
        self.labelAddressUser.place(x=650,y=120)
        self.inputAddressUser=Entry(self.labelFrameInfoUser)
        self.inputAddressUser.place(x=740,y=120)
        self.labelGenderUser=Label(self.labelFrameInfoUser,text="Gender:",font=('Comic Sans MS',10,'bold'))
        self.labelGenderUser.place(x=350,y=180)
        self.inputGenderUser=Entry(self.labelFrameInfoUser)
        self.inputGenderUser.place(x=440,y=180)
        self.labelPositionUser=Label(self.labelFrameInfoUser,text="Position:",font=('Comic Sans MS',10,'bold'))
        self.labelPositionUser.place(x=650,y=180)
        self.inputPositionUser=Entry(self.labelFrameInfoUser)
        self.inputPositionUser.place(x=740,y=180)
        self.labelDeparmentUser=Label(self.labelFrameInfoUser,text="Deparment:",font=('Comic Sans MS',10,'bold'))
        self.labelDeparmentUser.place(x=350,y=240)
        self.inputDeparmentUser=Entry(self.labelFrameInfoUser)
        self.inputDeparmentUser.place(x=440,y=240)
        self.labelMajorUser=Label(self.labelFrameInfoUser,text="Major:",font=('Comic Sans MS',10,'bold'))
        self.labelMajorUser.place(x=650 ,y=240)
        self.inputMajorUser=Entry(self.labelFrameInfoUser)
        self.inputMajorUser.place(x=740,y=240)
        self.btnChangePassword=Button(self.labelFrameInfoUser,text="Change Password",command=changePassword)
        self.btnChangePassword.place(x=40,y=20)
        self.labelCurrentPassword=Label(self.labelFrameInfoUser,text="Current Password:",state=DISABLED)
        self.labelCurrentPassword.place(x=35,y=60)
        self.inputCurrentPassword=Entry(self.labelFrameInfoUser,state=DISABLED,show='*',justify='center')
        self.inputCurrentPassword.place(x=20,y=100)
        self.labelNewPassword=Label(self.labelFrameInfoUser,text="New Password:",state=DISABLED)
        self.labelNewPassword.place(x=40,y=140)
        self.inputNewPassword=Entry(self.labelFrameInfoUser,state=DISABLED,show='*',justify='center')
        self.inputNewPassword.place(x=20,y=180)
        self.btnSavePassword=Button(self.labelFrameInfoUser,text="Save Password",state=DISABLED,command=savePassword)
        self.btnSavePassword.place(x=40,y=220)
        self.btnExit=Button(self.labelFrameInfoUser,text="Exit",command=exitProgram)
        self.btnExit.place(x=45,y=260)
        self.labelFrameInfoUser.pack(fill="both",expand="yes")
        def showProfileData():
            emailCheck=self.dataCC.findUserByEmail(self.userName_str)
            infoProFile=self.dataNv.showDataProfile(emailCheck[0])
            self.inputNameUser.insert(0,infoProFile[1])
            self.inputEmailUser.insert(0,infoProFile[2])
            self.inputPhoneUser.insert(0,infoProFile[3])
            self.inputAddressUser.insert(0,infoProFile[4])
            self.inputGenderUser.insert(0,infoProFile[5])
            self.inputPositionUser.insert(0,infoProFile[7])
            self.inputDeparmentUser.insert(0,infoProFile[8])
            self.inputMajorUser.insert(0,infoProFile[10])
        def clock():
            timeString=time.strftime('%H:%M:%S:%p')
            self.labelTimer.config(text=timeString)
            self.labelTimer.after(1000,clock)
        def showTotal():
            checkTotalByUser=self.dataCC.findUserByEmail(self.userName_str)
            totalSalary=self.dataBL.showTotalSalary(checkTotalByUser[0])
            return totalSalary[0]
        clock()
        showProfileData()
        self.checkClockInAndOut()
        self.dataShowTotal=showTotal()
        print('check data',self.dataShowTotal,type(self.dataShowTotal))
    def checkClockInAndOut(self):
        timeCurrent=datetime.now().strftime("%H:%M:%S")
        timeLockAM=datetime.fromtimestamp(1684461600).strftime('%H:%M:%S')
        timeLockPM=datetime.fromtimestamp(1684490400).strftime('%H:%M:%S')
        def converntTime(dataTime):
            timeFormat="%H:%M:%S"
            valuesConvert=datetime.now().strptime(dataTime,timeFormat)
            return valuesConvert
        try:
            if converntTime(timeCurrent)>=converntTime(timeLockAM):
                self.btnClockIn.config(state="disabled")
            if converntTime(timeCurrent)<converntTime(timeLockPM):
                self.btnClockOut.config(state="disabled")
            if len(self.dataClockIn)>0:
                self.btnClockIn.config(state="disabled")
            if self.dataClockOut[4]==None:
                self.btnClockOut.config(state="normal")
            else:
                self.btnClockOut.config(state="disabled")
        except ValueError as error:
            print('Log Error',error)
    def optionHomeMenu(self):
        self.clear_frame()
        def loadingDataScreenMenu():
            self.screenMenu()
        def loadingDataManageUser():
            self.roleUserMenu()
        def loadingDataSalary():
            self.menuChart()
        self.titleOptionMenu=Label(root,text="OPTION MENU",font=('carible',20,'bold'))
        self.titleOptionMenu.place(x=500,y=150)
        self.btnFuAddUser=Button(root,text="Add New Customer",command=loadingDataScreenMenu)
        self.btnFuAddUser.place(x=450,y=200)
        self.btnGoManageUser=Button(root,text="Role User",command=loadingDataManageUser)
        self.btnGoManageUser.place(x=580,y=200)
        self.btnStatictical=Button(root,text="Caculator Salary",command=loadingDataSalary)
        self.btnStatictical.place(x=660,y=200)
        # role user
        if self.roleUser_str=='manager':
            if self.btnFuAddUser.cget("state")=="normal":
                self.btnGoManageUser.config(state="disabled")
                self.btnStatictical.config(state='disabled')
            else:
                self.btnGoManageUser.config(state="disabled")
                self.btnStatictical.config(state='disabled')
        if self.roleUser_str=='user':
                self.screenMenu()
    def menuMoreOption(self):
        self.clear_frame()
        self.titleMenuMoreOption=Label(root,text="MORE OPTION",font=('calibre',20,'bold')).place(x=400,y=150)
        self.btnPosition=Button(root,text="Position",command=self.menuPosition).place(x=400,y=200)
        self.btnDeparment=Button(root,text="Deparment",command=self.menuDeparment).place(x=500,y=200)
        self.btnLevel=Button(root,text="Level").place(x=700,y=200)
        self.btnBack=Button(root,text="Back",command=self.screenMenu).place(x=1100,y=5)
    def addPosition(self):
        def showAddSuccess():
            mb.showinfo(title="Notification",message="Add Positon Success")
        def showEmty():
            mb.showerror(title="Notification",message="Position Is Empty")
        def showPositionExits():
            mb.showwarning(title="Notification",message="Position Is Exits")
        namePosition=self.inputPosition.get()
        if namePosition:
            dataCheckPosition=self.dataCV.checkIsExitPosition(namePosition)
            if dataCheckPosition:
                showPositionExits()
                self.inputPosition.delete(0,'end')
            else:
                self.dataCV.optionAddPosition(namePosition)
                showAddSuccess()
                self.inputPosition.delete(0,'end')
        else:
            showEmty()
            self.inputPosition.delete(0,'end')
    def addDeparment(self):
        def showDeparmentIsExit():
            mb.showwarning(title="Notification",message="Deparment Is Exits")
        def showDeparmentEmpty():
            mb.showwarning(title="Notification",message="Infomation Is Empty")
        def showAddDeparmentSuccess():
            mb.showinfo(title="",message="Add Deparment Success")
        def clearDataInput():
            self.inputDeparment.delete(0,'end')
            self.inputDeparmentAddress.delete(0,'end')
            self.inputDeparmentPhone.delete(0,'end')
        nameDeparment=self.inputDeparment.get()
        addressDeparment=self.inputDeparmentAddress.get()
        phoneDeparment=self.inputDeparmentPhone.get()
        if nameDeparment and addressDeparment and phoneDeparment:
            dataCheckDeparment=self.dataPB.checkNameDeparment(nameDeparment)
            if dataCheckDeparment:
                showDeparmentIsExit()
                clearDataInput()
            else:
                self.dataPB.addOptionDeparment(nameDeparment,addressDeparment,phoneDeparment)
                showAddDeparmentSuccess()
                clearDataInput()
        else:
            showDeparmentEmpty()
    def addMajorLevel(self):
        def addSuccess():
            mb.showinfo(title="Notification",message="Add Major Success")
        def showEmptyLevelLearn():
            mb.showwarning(title="Notification",message="Data Is Empty")
        def showDataIsExits():
            mb.showwarning(title="Notification",message="Data Is Exits")
        def clearData():
            self.inputMajor.delete(0,'end')
            self.inputNameLevel.delete(0,'end')
        nameLevel=self.inputNameLevel.get()
        major=self.inputMajor.get()
        if nameLevel and major:
            dataCheckMajor=self.dataHV.checkDataNameMajor(nameLevel)
            if dataCheckMajor:
                showDataIsExits()
                clearData()
            else:
                self.dataHV.addMajorLevelLearn(nameLevel,major)
                addSuccess()
                clearData()
        else:
            showEmptyLevelLearn()
    def menuPosition(self):
        # self.clear_frame() lỗi ở đây
        top=Toplevel(root)
        top.title('Position Option')
        top.geometry("1200x500")
        self.titleMenuMoreOption=Label(top,text="MORE OPTION POSITION",font=('calibre',20,'bold')).place(x=400,y=150)
        self.labelPositionMore=Label(top,text="Position:").place(x=450,y=200)
        self.inputPosition=Entry(top,font=("calibre",10,"bold"))
        self.inputPosition.place(x=520,y=200)
        self.btnPosition=Button(top,text="Add",command=self.addPosition).place(x=520,y=250)
        #tạm ẩn
        # self.btnBack=Button(top,text="Back")
        # self.btnBack.place(x=1100,y=5)
    def menuDeparment(self):
        top=Toplevel(root)
        top.title('Deparment Option')
        top.geometry("1200x500")
        self.btnDeparment=Label(top,text="MORE OPTION DEPARMENT",font=('calibre',20,'bold')).place(x=400,y=150)
        self.labelDeparment=Label(top,text="Name Deparment:").place(x=450,y=200)
        self.inputDeparment=Entry(top,font=("calibre",10,'bold'))
        self.inputDeparment.place(x=580,y=200)
        self.labelDeparmentAddress=Label(top,text="Address Deparment:").place(x=450,y=250)
        self.inputDeparmentAddress=Entry(top,font=("calibre",10,'bold'))
        self.inputDeparmentAddress.place(x=580,y=250)
        self.labelDeparmentPhone=Label(top,text="Phone:").place(x=450,y=300)
        self.inputDeparmentPhone=Entry(top,font=("calibre",10,'bold'))
        self.inputDeparmentPhone.place(x=580,y=300)
        self.btnDeparment=Button(top,text="Add",command=self.addDeparment).place(x=580,y=350)
        #tạm ẩn
        # self.btnBack=Button(top,text="Back").place(x=1100,y=5)
    def menuLevelLearn(self):
        top=Toplevel(root)
        top.title('Level Option')
        top.geometry("1200x500")
        self.titleMenuMorelevelLear=Label(root,text="MORE OPTION LEVEL",font=('calibre',20,'bold')).place(x=400,y=150)
        self.labelNameLevel=Label(root,text="Name Level:").place(x=450,y=200)
        self.inputNameLevel=Entry(root,font=("calibre",10,'bold'))
        self.inputNameLevel.place(x=580,y=200)
        self.labelMajor=Label(root,text="Major:").place(x=450,y=250)
        self.inputMajor=Entry(root,font=("calibre",10,'bold'))
        self.inputMajor.place(x=580,y=250)
        self.titleMenuMorelevelLear=Button(root,text="Add",command=self.addMajorLevel).place(x=400,y=200)
        # tạm ẩn
        # self.btnBack=Button(root,text="Back",command=lambda : self.screenMenu()).place(x=1100,y=5)
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
        def goHomeMenu():
            self.ScreenHomeMenu()
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
        # tạm ẩn
        self.btnBackHome=Button(root,text='Back',command=goHomeMenu)
        self.btnBackHome.place(x=1100,y=5)
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
    def ScreenHomeMenu(self):
        self.clear_frame()
        self.userName_str=StringVar()
        self.passWord_str=StringVar()
        self.roleUser_str=StringVar()
        def exitProgram():
            mb.showwarning(title='Notification!!!',message='Do you want exit program')
            root.destroy()
        def loginSuccess():
            # import process bar khi thực hiện đăng nhập
            # progbar =Progressbar(root, orient=HORIZONTAL, length=220, mode="indeterminate",max=50.0)
            # progbar.place(x=500,y=500)
            # progbar.start()
            # progbar.stop()
            time.sleep(0.5)
            mb.showinfo(title='Notification!!!',message='Login Success')
            self.optionHomeMenu()
        def loginFalseEmpty():
            mb.showerror(title='Notification!!!',message='Login Fail, Email Or Password Is Emty')
        def resFalseEmpty():
            mb.showerror(title='Notification!!!',message='Register Fail, Email Or Password Is Emty')
        def loginFail():
            mb.showerror(title='Notification!!!',message='Login Fail')
        def resSuccess():
            mb.showinfo(title='Notification!!!',message='Register Success')
        def resFalse():
            mb.showwarning(title='Notification!!!',message='Register Fail')
        def infoIsEmty():
            mb.showwarning(title='Notification!!!',message='User is exits !!! Please entern new accoutt')
        def regexEmail():
            mb.showwarning(title='Notification!!!',message="Email is exits or invalidate Email Ex:a@gmail.com")
        def checkPassIsExit():
            mb.showerror(title='Notification!!!',message="Password wrong")
        def checkEmaiAndPassIsExit():
             mb.showerror(title='Notification!!!',message="Email and Password is not exits")
        def emptyRes():
            mb.showwarning(title="Notification!!!",message="Email or PassWord is empty")
        def checkLogin():
                self.userName_str = self.textInputUserName.get()
                self.passWord_str= self.textInputPassword.get()

                if self.userName_str and self.passWord_str:
                    dataLogin=self.dataUs.checkLogin(self.userName_str)
                    dataNVLogin=self.dataNv.checkLoginNhanVien(self.userName_str)
                    # check login with User
                    if dataLogin:
                        for row in dataLogin:
                            self.roleUser_str=row[2]
                            if row[0].rstrip() == self.userName_str and row[1].rstrip() == self.passWord_str:
                                loginSuccess()
                            elif row[0].rstrip() == self.userName_str and row[1].rstrip() != self.passWord_str:
                                checkPassIsExit()
                            elif row[0].rstrip() != self.userName_str or row[1].rstrip() != self.passWord_str:
                                checkEmaiAndPassIsExit()
                    # check login with NhanVien
                    if dataNVLogin:
                        for row in dataNVLogin:
                            self.roleUser_str=row[2]
                            if row[0].rstrip() == self.userName_str and row[1].rstrip() == self.passWord_str:
                                loginSuccess()
                            elif row[0].rstrip() == self.userName_str and row[1].rstrip() != self.passWord_str:
                                checkPassIsExit()
                            elif row[0].rstrip() != self.userName_str or row[1].rstrip() != self.passWord_str:
                                checkEmaiAndPassIsExit()
                elif self.userName_str or self.passWord_str:
                    loginFalseEmpty()
                else:
                    loginFail()
        def checkRes():
            self.userName_str=self.textInputUserName.get()
            self.passWord_str=self.textInputPassword.get()
            validEmailUser=re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
            # validPasswordUser=checkValidPassword(self.passWord_str)
            if self.userName_str and self.passWord_str:
                if re.fullmatch(validEmailUser,self.userName_str):
                    dataCheckRes=self.dataUs.checkRegister(self.userName_str)
                    userName_convert=''
                    for row in dataCheckRes:
                        userName_convert=row[0]
                    if userName_convert.rstrip() == self.userName_str:
                        infoIsEmty()
                    elif self.userName_str or self.passWord_str:
                        emptyRes()
                    else:
                            self.dataUs.insertUserScreenLog(self.userName_str,self.passWord_str)
                            resSuccess()
                            self.screenMenu()
                else:
                    regexEmail()
            elif self.userName_str==None or self.passWord_str == None:
                resFalseEmpty()
            else:
                resFalse()
        def checkValidPassword(dataPassword):
            special_symbols =['$', '@', '#', '%']
            if len(dataPassword) < 6:
                mb.showwarning(message='Password must have atleast 6 characters.')
                return
            if len(dataPassword) > 20:
                mb.showwarning(message='Password cannot have more than 20 characters.')
                return
            if not any(characters.isdigit() for characters in dataPassword):
                mb.showwarning(message='Password must have at least one numeric character.')
                return
            if not any(characters.isupper() for characters in dataPassword):
                mb.showwarning(message='Password must have at least one uppercase character')
                return
            if not any(characters.islower() for characters in dataPassword):
                mb.showwarning(message='Password must have at least one lowercase character')
                return
            if not any(characters in special_symbols for characters in dataPassword):
                mb.showwarning(message='Password should have at least one of the symbols $@#%')
                return dataPassword
            else:
                print("Pasword is Valid.")
        self.textTitleProgram=Label(root,text='Manager User',font=('calibre',20,'bold')).pack(side="top")
        self.textUserName=Label(root,text='UserName:',font=('calibre',10,'bold')).place(x=450,y=150)
        self.textInputUserName=Entry(root,font=('calibre',10,'bold'))
        self.textInputUserName.place(x=530,y=145)
        self.textPassword=Label(root,text='Password:',font=('calibre',10,'bold')).place(x=450,y=190)
        self.textInputPassword=Entry(root,font=('calibre',10,'bold'),show='*')
        self.textInputPassword.place(x=530,y=185)
        self.buttonLogin=Button(root,text='Login.',command=checkLogin).place(x=530,y=250)
        self.buttonRegister=Button(root,text='Register.',command=checkRes).place(x=620,y=250)
        self.buttonExitProgram=Button(text='Exit.',command=exitProgram).place(x=1000,y=400)
root = Tk()
myWin=MainMenu(root)
root.title('Manage User')
root.geometry("1200x500")
root.iconbitmap("logoFile.ico")
root.mainloop()
