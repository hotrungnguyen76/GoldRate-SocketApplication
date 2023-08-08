from calendar import c
from json.encoder import JSONEncoder
from tkinter import *
from tkinter import font as tkfont
import tkinter
import tkinter as tk
#from tkinter.ttk import *
from PIL import Image,ImageTk
import threading 
import pyodbc
import socket
#from tkinter import messagebox
import datetime
import schedule
import time
import urllib.request, json 
import urllib

HOST = "127.0.0.1"
SERVER_PORT = 55555
FORMAT = "utf8"

SERVER = 'DESKTOP-V1R4RH9\SQLEXPRESS'
DATABASE = 'socket1'
UID = 'socket'
PWD = '123456'

SIGNUP = "signup"
LOGIN = "login"
LOGOUT = "logout"
SEARCH = "search"
DATA = "data"

LARGE_FONT = ("verdana", 13,"bold")

Live_Account=[]
ID=[]
Ad=[]

def ConnectToDB():
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+SERVER+';DATABASE='+DATABASE+';UID='+UID+';PWD='+ PWD)
    cursor = cnxn.cursor()
    return cursor

def Insert_New_Account(user,password):
    cursor.execute( "insert into users values(?,?);",(user,password))
    cursor.commit()
    

def check_clientSignUp(username):
    # if username == "admin":
    #     return False
    cursor.execute("select * from users where username=(?)",(username))
    check = cursor.fetchone()
    if check is None:
        return 1
    else:
        return 0
    # for row in cursor:
    #     parse=str(row)
    #     parse_check =parse[2:]
    #     parse= parse_check.find("'")
    #     parse_check= parse_check[:parse]
    #     if parse_check == username:
    #         return 0
    # return 1
    #False: Tài khoản đã tồn tại.   #True: Đăng ký thành công

def clientSignUp(conn, addr):
    print(addr, ": SIGN UP")
    user = conn.recv(1024).decode(FORMAT)
    print("username: " + user)

    conn.sendall(user.encode(FORMAT))

    pswd = conn.recv(1024).decode(FORMAT)
    print("password: "+ pswd )

    #a = input("accepting...")
    check = check_clientSignUp(user)
    print("accept_signup:", check)
    conn.sendall(str(check).encode(FORMAT))

    if check:
        Insert_New_Account(user, pswd)

        # add client sign up address to live account
        Ad.append(str(addr))
        ID.append(user)
        account=str(Ad[Ad.__len__()-1])+"-"+str(ID[ID.__len__()-1])
        Live_Account.append(account)

    #print("end-logIn()")
    print("")
    
def Check_LiveAccount(username): #check if the account is logged in. False: logged in , True: not logged in
    for row in Live_Account:
        parse= row.find("-")
        parse_check= row[(parse+1):]
        if parse_check== username:
            return False
    return True

def Remove_LiveAccount(conn,addr):
    for row in Live_Account:
        parse= row.find("-")
        parse_check=row[:parse]
        if parse_check== str(addr):
            parse= row.find("-")
            Ad.remove(parse_check)
            username= row[(parse+1):]
            ID.remove(username)
            Live_Account.remove(row)
            #conn.sendall("True".encode(FORMAT))

def check_clientLogIn(username, password):
    
    if Check_LiveAccount(username)== False: #check if this account is logged in
        return 0
    cursor.execute("select password from users where username=(?)",(username))
    pass_list = cursor.fetchone()
    #print(pass_list[0])
    message = "" 
    if pass_list is None:
        message = "Unexist"
        print(message)
        return 2
    else:
        data_password = pass_list[0]
        # verify login
        if password == str(data_password):
            accept = 1
            RP = "OK"
        else:
            accept = 2
            RP = "FAIL"
    return accept
    #0: This account is being logged in
    #1: Ok
    #2: Invalid username or password}
    
def clientLogIn(conn, addr):
    print(addr, ": LOG IN")
    user = conn.recv(1024).decode(FORMAT)
    print("username:--" + user +"--")

    conn.sendall(user.encode(FORMAT))
    
    pswd = conn.recv(1024).decode(FORMAT)
    print("password:--" + pswd +"--")
    
    accepted = check_clientLogIn(user, pswd)
    if accepted == 1:
        ID.append(user)
        account=str(Ad[Ad.__len__()-1])+"-"+str(ID[ID.__len__()-1])
        Live_Account.append(account)
        # for i in range(len(Live_Account)):
        #     print(Live_Account[i])
    
    print("accept:", accepted)
    conn.sendall(str(accepted).encode(FORMAT))
    #print("end-logIn()")
    print("")


def sendList(conn, list):
    
    for item in list:
        conn.sendall(item.encode(FORMAT))
        #wait response
        conn.recv(1024)

    msg = "end"
    conn.send(msg.encode(FORMAT))
def recvList(conn):
    list = []
    item = conn.recv(1024).decode(FORMAT)
    while (item != "end"):
        
        list.append(item)
        #response
        conn.sendall(item.encode(FORMAT))
        item = conn.recv(1024).decode(FORMAT)     
    return list
#Gửi data qua client
def sendData(conn,addr):
    list = recvList(conn)
    cursor = ConnectToDB()
    if(list[2] == "Khác"):
        cursor.execute("SELECT type, company, brand, buy, sell, updated from TyGia where updated like "+list[0]+" and type NOT like N'AVPL%' and type NOT like N'Nữ trang%' and type NOT like N'Kim Ngưu%' and type NOT like 'SJC%'and company like "+list[1]+" and brand like "+list[3])
    else:
        cursor.execute("SELECT type, company, brand, buy, sell, updated from TyGia where updated like "+list[0]+" and company like "+list[1]+" and type like "+list[2]+" and brand like "+list[3])   
    records = cursor.fetchall()
    cursor.commit()
    records = str(records)
    conn.sendall(records.encode(FORMAT))

def handle_client(conn, addr):
    # Ở PHẢI BỔ SUNG TRY - EXCEPT
    try:
        #print("Connection: ", conn.socgetkname())
        while True:
            option = conn.recv(1024).decode(FORMAT)
            if option == LOGIN:
                Ad.append(str(addr))
                clientLogIn(conn, addr)     
            elif option == SIGNUP:
                clientSignUp(conn, addr)
            elif option == LOGOUT:
                print(addr, ": LOG OUT")
                Remove_LiveAccount(conn,addr)
            elif option == DATA:
                sendData(conn,addr)
                 
        Remove_LiveAccount(conn,addr)
        conn.close()
        #print("end-thread")
    except:
        print("error")


        


def runServer():
    try:
        print(HOST)
        print("Waiting for Client")

        while True:
            #print("enter while loop")
            conn, addr = socket.accept()
            print("Client "+ str(addr) +" connected" )
            clientThread = threading.Thread(target=handle_client, args=(conn,addr))
            clientThread.daemon = True 
            clientThread.start()
    
        
    except KeyboardInterrupt:
        print("error")
        socket.close()
    finally:
        socket.close()
        print("end")
# GUI

class Server_App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.iconbitmap('logo.ico')
        self.title("Tra cứu giá vàng")
        self.geometry("500x200")
        # self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.resizable(width=False, height=False)

        container = tk.Frame(self)
        container.pack(side="top", fill = "both", expand = True)
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage,HomePage):
            frame = F(container, self)

            self.frames[F] = frame 

            frame.grid(row=0, column=0, sticky="nsew")

        self.showFrame(StartPage)


    def showFrame(self, container):
        
        frame = self.frames[container]
        if container==HomePage:
            self.geometry("500x350")
        else:
            self.geometry("500x200")
        frame.tkraise()

    # close-programe function
    # def on_closing(self):
    #     if messagebox.askokcancel("Quit", "Do you want to quit?"):
    #         self.destroy()

    def logIn(self,curFrame):

        user = curFrame.entry_user.get()
        pswd = curFrame.entry_pswd.get()

        if pswd == "":
            curFrame.label_notice["text"] = "password cannot be empty"
            return 

        if user == "admin" and pswd == "1":
            self.showFrame(HomePage)
            curFrame.label_notice["text"] = ""
        else:
            curFrame.label_notice["text"] = "invalid username or password"

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="black")
        
        
        label_title = tk.Label(self, text="\nLOG IN FOR SEVER\n", font=LARGE_FONT,fg='white',bg="black").grid(row=0,column=1)

        label_user = tk.Label(self, text="\tUSERNAME ",fg='floral white',bg="black",font='verdana 10 bold').grid(row=1,column=0)
        label_pswd = tk.Label(self, text="\tPASSWORD ",fg='floral white',bg="black",font='verdana 10 bold').grid(row=2,column=0)

        self.label_notice = tk.Label(self,text="",bg="black",fg='red')
        self.entry_user = tk.Entry(self,width=30,bg='white')
        self.entry_pswd = tk.Entry(self,width=30, show ="*", bg='white')

        button_log = tk.Button(self,text="LOG IN",bg="#e0b64a",fg='floral white', font = "Times 13",command=lambda: controller.logIn(self))

        button_log.grid(row=4,column=1)
        button_log.configure(width=10)
        self.label_notice.grid(row=3,column=1)
        self.entry_pswd.grid(row=2,column=1)
        self.entry_user.grid(row=1,column=1)

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) 
        self.configure(bg="#0f1011")
        label_title = tk.Label(self, text="\n ACTIVE ACCOUNT ON SEVER\n", font=LARGE_FONT,fg='white',bg="#0f1011").pack()
        
        self.conent =tk.Frame(self)
        self.data = tk.Listbox(self.conent, height = 10, 
                  width = 40, 
                  bg='white',
                  activestyle = 'dotbox', 
                  font = "Helvetica",
                  fg='#20639b')
        
        button_log = tk.Button(self,text="REFRESH",bg="#e0b64a",fg='white', font="Times",command=self.Update_Client)
        button_back = tk.Button(self, text="LOG OUT",bg="#e0b64a",fg='white', font= "Times" ,command=lambda: controller.showFrame(StartPage))
        button_log.pack(side= BOTTOM)
        button_log.configure(width=10)
        button_back.pack(side=BOTTOM)
        button_back.configure(width=10)
        
        self.conent.pack_configure()
        self.scroll= tk.Scrollbar(self.conent)
        self.scroll.pack(side = RIGHT, fill= BOTH)
        self.data.config(yscrollcommand = self.scroll.set)
        
        self.scroll.config(command = self.data.yview)
        self.data.pack()
        
    def Update_Client(self):
        self.data.delete(0,len(Live_Account))
        for i in range(len(Live_Account)):
            self.data.insert(i,Live_Account[i])
        
        print ("Live Account List:")
        for i in range(len(Live_Account)):
            print(Live_Account[i])
#Register()
#login()
#test()

connection_database = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; \
                        SERVER=' + SERVER + ';Database=' + DATABASE + ';UID=' + UID + ';PWD=' + PWD)
cursor = connection_database.cursor()

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind((HOST, SERVER_PORT))
socket.listen()

sThread = threading.Thread(target=runServer)
sThread.daemon = True 
sThread.start()

#Lấy url
def get_url():
    url = "https://sjc.com.vn/xml/tygiavang.xml"
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    data = str(data)
    data =  data[87:(len(data)-99)]+"]"
    df = data.replace("'",'"')
    return(df)
#Thêm dữ liệu từ url hiện tại vào database
def newData():
    cursor = ConnectToDB()
    #Xoá data cũ
    x = datetime.datetime.now()
    x = str(x);
    x = x[:10]
    date = "'"+x+"%'"
    cursor.execute("DELETE from TyGia where updated like "+date)
    #Data mới
    df = get_url()
    cursor.execute("INSERT INTO TyGia(buy,sell,company,brand,updated,brand1,id,type,code) SELECT buy, sell, company, brand, updated, brand1, id, type, code FROM OPENJSON(N'" +df+ "') WITH (buy NVARCHAR(20), sell NVARCHAR(200), company NVARCHAR(20), brand NVARCHAR(20), updated NVARCHAR(20), brand1 NVARCHAR(20), date NVARCHAR(20), id NVARCHAR(20), type NVARCHAR(20), code NVARCHAR(20))")
    cursor.commit()
    
#Cập nhật database mỗi 30p
def UpdatePer30min():
    schedule.every(30).minutes.do(newData)
 

#Cập nhật ngày hôm nay khi vừa khởi động Server

newData()
#Cập nhật sau mỗi 30p từ khi khởi động server
#UpdatePer30min()

updateThread = threading.Thread(target=UpdatePer30min)
updateThread.daemon = True 
updateThread.start()



if __name__ == "__main__":
    app = Server_App()
    app.mainloop()
    
    

