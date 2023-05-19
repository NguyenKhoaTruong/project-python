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
import re
import imageio as iio
import pandas as pd
import Users as us
import NhanVien as nv
import matplotlib.pyplot as plt
from datetime import datetime
import time
class LoginPage:
    def __init__(self):
        self.ScreenHomeMenu()
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
myWin=LoginPage(root)
root.title('Manage User')
root.geometry("1200x500")
root.iconbitmap("logoFile.ico")
root.mainloop()