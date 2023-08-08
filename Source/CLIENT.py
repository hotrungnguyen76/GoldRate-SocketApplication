from json.decoder import JSONDecoder
from tkinter import *
from tkinter import font as tkfont
#import tkinter
import tkinter as tk
from tkinter import ttk 
from PIL import Image,ImageTk
import threading 
#import pyodbc
import socket
from tkinter import messagebox
#import time
from tkcalendar import DateEntry
import tkinter.ttk as Ttk
#import urllib.request, json 
#import urllib
import datetime
import schedule


HOST = ""
SERVER_PORT = 0
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
DISCONNECT = "Disconnect"

LARGE_FONT = ("verdana", 13,"bold")
username_key = ""


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        
        self.title('Tra cuu gia vang')
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        #self.geometry("400x622")
        self.iconbitmap('..\\images\\logo.ico')
        #self.resizable(width = False, height = False)
        

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (ConnectToServer,LogInPage, HomePage, SignUpPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("ConnectToServer")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        if page_name == "LogInPage":
            self.geometry("400x622") 
        if page_name == "HomePage":
            self.geometry("1000x700")
        if page_name == "ConnectToServer":
            self.geometry("500x200")    
        frame.tkraise()
    
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()
            try:
                option = LOGOUT
                client.sendall(option.encode(FORMAT))
            except:
                pass
    
class ConnectToServer(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        print("Waiting for connecting to server...")
        self.configure(bg="#0f1011")
        label_title = tk.Label(self, text="\nCONNECT TO SEVER\n", font=LARGE_FONT,fg='white',bg="#0f1011").grid(row=0,column=1)

        label_host = tk.Label(self, text="\tSERVER HOST ",fg='floral white',bg="#0f1011",font='verdana 10 bold').grid(row=1,column=0)
        label_port = tk.Label(self, text="\tSERVER PORT ",fg='floral white',bg="#0f1011",font='verdana 10 bold').grid(row=2,column=0)

        self.label_notice = tk.Label(self,text="",bg="#0f1011",fg='red')
        self.entry_host = tk.Entry(self,width=30,bg='white')
        self.entry_port = tk.Entry(self,width=30, bg='white')

        button_connect = tk.Button(self,text="START",bg="#e0b64a",fg='floral white', font = "Times 13", command = self.connect)

        button_connect.grid(row=4,column=1)
        button_connect.configure(width=10)
        self.label_notice.grid(row=3,column=1)
        self.entry_port.grid(row=2,column=1)
        self.entry_host.grid(row=1,column=1)
    def connect(self):
        if self.entry_host.get() == "" or self.entry_port.get() == "":
            self.label_notice.config(text= "Host or port cannot be empty!!!")
        else:
            global HOST, SERVER_PORT
            HOST = self.entry_host.get()
            SERVER_PORT = int(self.entry_port.get())

            global client
            try:
                client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                client.connect((HOST,SERVER_PORT))
                print("Connected to ("+ HOST + ", " + str(SERVER_PORT) + ")") 
                self.controller.show_frame("LogInPage")
            except:
                self.label_notice.config(text= "Error!!!")

class LogInPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        def toggle_password():
            if (x.get() == 0):
                self.password_entry.config(show='*')
            else:
                self.password_entry.config(show='')
        
        canvas_for_image = Canvas(self, bg='green', height=622, width=450, borderwidth=0, highlightthickness=0)
        canvas_for_image.place(x=0,y=0)

        image = Image.open('..\\images\\background.png')
        canvas_for_image.image = ImageTk.PhotoImage(image)
        canvas_for_image.create_image(0, 0, image=canvas_for_image.image, anchor='nw')

        frame = Frame(self,bg = '#0f1011')
        frame.pack(pady = 40)
        
        name = Label(frame, text ="Tra cứu giá vàng", fg = 'white', bg = '#0f1011', font = "Times 25")
        name.grid(row = 0, pady = 55)
        

        #Label(win,text="",bg = '#0f1011' ).pack()
        Label(frame, text = "Tên đăng nhập", font= 'Times 18', fg = '#8C8685', bg = '#0f1011' ).grid(row=1, column =0, sticky = W, pady = 10)
        self.username_entry = Entry(frame, font = 'Times 20 ', fg = 'black')
        self.username_entry.focus()
        self.username_entry.grid(row=2, column= 0)
        
        Label(frame, text = "Mật khẩu", font= 'Times 18', fg = '#8C8685', bg = '#0f1011' ).grid(row=3, column =0, sticky = W, pady = 10)
        self.password_entry = Entry(frame, show="*", font = 'Times 20 ', fg = 'black')
        self.password_entry.grid(row=4, column= 0)
        
        x= IntVar() 
        check_button = Checkbutton(frame, text = "Hiện mật khẩu", fg ='white', bg = '#0f1011', selectcolor='black', variable =x, onvalue= 1, offvalue= 0, command = toggle_password)
        check_button.grid(row=5, column= 0, sticky= W, pady = 3)

        self.notice = Label(frame, text="", font ="Times 13", fg = 'red', bg = '#0f1011')
        self.notice.grid(row = 6, column= 0, sticky = W, pady =2)
        
        #Label(win,text="",bg = '#0f1011' ).pack(pady = 20)
        loginBtn = Button(frame, text = "Đăng nhập", bg='#e0b64a', fg = 'white', font = 'Times 20', padx = 73, command= self.checkLogIn)
        loginBtn.grid(row=7, column= 0, pady = 10)

        registerBtn = Button(frame, text = "Tạo tài khoản", bg='#0f1011', fg = 'white', font = 'Times 13', padx = 92, command=lambda: controller.show_frame("SignUpPage"))
        registerBtn.grid(row=8, column= 0)
    
        
    def checkLogIn(self):
        print("ĐĂNG NHẬP")
        username = self.username_entry.get()
        password = self.password_entry.get()
        print("Username: "+username)
        print("Password: "+ password)
        global username_key
        username_key = username
        
        if username == "" or password == "":
            self.notice.config(text = "Chưa điền đủ thông tin đăng nhập")

        client.sendall(LOGIN.encode(FORMAT))
        client.sendall(username.encode(FORMAT))
        client.recv(1024).decode(FORMAT)
        client.sendall(password.encode(FORMAT))
        
        returned_result = client.recv(1024).decode(FORMAT)
        if returned_result == "0":
            print("Tài khoản này đang được đăng nhập ở một nơi khác!")
            self.notice.config(text = "Tài khoản này đang được đăng nhập ở một nơi khác!")
        elif returned_result == "2":
            print("Tài khoản hoặc mật khẩu không hợp lệ")
            self.notice.config(text = "Tài khoản hoặc mật khẩu không hợp lệ")
        elif returned_result == "1":
            print("Đăng nhập thành công!")
            self.controller.show_frame("HomePage")

        #returned_result = 0 ~ Tài khoản đang đăng nhập
        #returned_result = 1 ~ Đăng nhập thành công
        #returned_result = 2 ~ Tài khoản và mật khẩu không hợp lệ
    
class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        frame1 = Frame(self,width=950, height=100, bg = "light blue",borderwidth=2, relief="solid")
        Label(frame1, text = ("Xin chào"), bg = "light blue", font= "Times 15").place(x= 30, y =30)
        Button(frame1, text = "Đăng xuất", bg = "dark blue", fg = "white", font = "Times 13", command= self.log_out).place(x=840, y=50)

        canvas_logout = Canvas(frame1, bg='light blue', height=50, width=50, borderwidth=0, highlightthickness=0)
        canvas_logout.place(x=860,y=0)
        img= (Image.open("..\\images\\logout.png"))
        resized_image= img.resize((50,50), Image.ANTIALIAS)
        canvas_logout.image= ImageTk.PhotoImage(resized_image)
        canvas_logout.create_image(0, 0, image=canvas_logout.image, anchor='nw')

        canvas_hcmus = Canvas(frame1, bg='light blue', height=95, width=100, borderwidth=0, highlightthickness=0)
        canvas_hcmus.place(x=427,y=0)
        img= (Image.open("..\\images\\hcmus.png"))
        resized_image= img.resize((100,100), Image.ANTIALIAS)
        canvas_hcmus.image= ImageTk.PhotoImage(resized_image)
        canvas_hcmus.create_image(0, 0, image=canvas_hcmus.image, anchor='nw')

        frame2 = Frame(self,width=950, height=100, bg = "light blue",borderwidth=2, relief="solid")
        Label(frame2,text = "Ngày", font = "Gulim 15 bold", bg = "light blue", fg = "black", width = 7).place(x= 10, y = 10)
        self.cal = DateEntry(frame2, selectmode= 'day')
        self.cal.place(x=20, y=40)

        Label(frame2,text = "Thương hiệu", font = "Gulim 15 bold", bg = "light blue", fg = "black").place(x=180, y = 10)
        self.cmb_brand = Ttk.Combobox(frame2)
        self.cmb_brand['values']= ("Default", "DOJI", "3BANKS","2GROUP","1OTHER","1Coin")
        self.cmb_brand.current(0)
        self.cmb_brand.place(x=180,y=40)

        Label(frame2,text = "Loại", font = "Gulim 15 bold", bg = "light blue", fg = "black").place(x= 400, y = 10)
        self.cmb_type = Ttk.Combobox(frame2)
        self.cmb_type['values']= ("Default", "AVPL", "Nữ trang","Kim Ngưu","SJC","Khác")
        self.cmb_type.current(0)
        self.cmb_type.place(x=400,y=40)

        Label(frame2,text = "Vị trí", font = "Gulim 15 bold", bg = "light blue", fg = "black").place(x= 600, y = 10)
        self.cmb_location = Ttk.Combobox(frame2)
        self.cmb_location['values']= ("Default", "Hồ Chí Minh", "Hà Nội","Nhẫn DOJI Hưng Thịnh","Mi Hồng")
        self.cmb_location.current(0)
        self.cmb_location.place(x=600,y=40)

        Button(frame2, text = "Hiện kết quả", fg = "white", bg = "dark blue",command = lambda: self.Search(client)).place(x= 800,y=37)
        

        frame3 = Frame(self,width=950, height=480, bg = "light blue",borderwidth=2, relief="solid")

        style = ttk.Style()

        style.theme_use('default')

        style.configure("Treeview", bg = "#D3D3D3", fg ="black", rowheight =25, fieldbackground= "#D3D3D3")

        style.map('Treeview', bg= [('selected',"#347083")])

        tree_scroll = Scrollbar(frame3)
        tree_scroll.pack(side=RIGHT, fill = Y)

        self.my_tree= Ttk.Treeview(frame3, yscrollcommand=tree_scroll.set, height= 17)

        self.my_tree.pack()

        tree_scroll.config(command=self.my_tree.yview)

        self.my_tree['columns']= ("type","brand", "area", "buy","sell", "date")

        self.my_tree.heading("#0", text="", anchor=W)
        self.my_tree.heading("type", text = "Type", anchor = W)
        self.my_tree.heading("brand", text ="Brand", anchor=W)
        self.my_tree.heading("area", text ="Area", anchor = CENTER)
        self.my_tree.heading("buy", text = "Buy", anchor = CENTER)
        self.my_tree.heading("sell", text = "Sell", anchor = CENTER)
        self.my_tree.heading("date",text = "Updated", anchor = W)

        self.my_tree.column("#0", width = 0, stretch = NO)
        self.my_tree.column("type",width =191, anchor =W,minwidth =191)
        self.my_tree.column("brand",anchor = W, width = 172, minwidth=172)
        self.my_tree.column("area",anchor = W, width = 120, minwidth=100)
        self.my_tree.column("buy",anchor = CENTER, width =140, minwidth= 120)
        self.my_tree.column("sell", anchor= CENTER, width =140, minwidth= 120)
        self.my_tree.column("date", anchor= W, width=163, minwidth = 163)

        self.my_tree.tag_configure('oddrow',background= "white")
        self.my_tree.tag_configure('evenrow',background= "lightblue")

        frame1.pack(pady = 5)
        frame2.pack(pady = 2)
        frame3.pack()
        
    def log_out(self):
        print("ĐĂNG XUẤT")
        client.sendall(LOGOUT.encode(FORMAT))
        self.controller.show_frame("LogInPage")

    def Search(self,sck):
        #Xoá bảng
        try:
            for record in self.my_tree.get_children():
                self.my_tree.delete(record)
            sck.sendall(DATA.encode(FORMAT))
            #Gửi yêu cầu cho Server
            date = "'" + str(self.cal.get_date())+"%" + "'"
            if self.cmb_brand.get() == 'Default':
                brand = "N'%'"
            else:
                brand = "N'" + self.cmb_brand.get()+"%" + "'"
            if self.cmb_location.get() == 'Default':
                location = "N'%'"
            else:
                location = "N'" + self.cmb_location.get()+"%" + "'"
            if self.cmb_type.get() == 'Khác':                    
                list = [date,brand,"Khác",location]
                sendList(sck,list)
                
            else:
                if self.cmb_type.get() == 'Default':
                    type = "N'%'"
                else:
                    type = "N'" + self.cmb_type.get()+"%" + "'"
                list = [date,brand,type,location]
                sendList(sck,list)

            records = client.recv(1024*700).decode(FORMAT)
            records = eval(records)
        
            count = 0
            for record in records:
                if count%2 == 0:
                    self.my_tree.insert(parent = '', index = 'end', iid= count, text = '', values=(record[0],record[1],record[2],record[3],record[4],record[5] ), tag = ('evenrow',))
                else:
                    self.my_tree.insert(parent = '', index = 'end', iid= count, text = '', values=(record[0],record[1],record[2],record[3],record[4],record[5] ), tag = ('oddrow',))
                count += 1
        except:
            print("Error")

        
class SignUpPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        
        #bg='#e0b64a', fg = 'white', bg ='0f1011
        self.configure(bg="#0f1011")
                
        name = tk.Label(self, text ="Đăng ký", fg = 'red', font = "Times 25 bold",bg ="#0f1011")
        name.pack(pady = 60)

        tk.Label(self, text = "Tên truy cập", font= 'Times 18', fg = 'white', bg="#0f1011").pack()
        self.username_entry = tk.Entry(self, font = 'Times 20 ', fg = 'black')
        self.username_entry.focus()
        self.username_entry.pack(pady = 5)

        tk.Label(self, text = "Mật khẩu", font= 'Times 18', fg = 'white', bg="#0f1011").pack()
        self.password_entry = tk.Entry(self, show= "*", font = 'Times 20 ', fg = 'black')
        self.password_entry.pack(pady = 5)

        tk.Label(self, text = "Nhập lại mật khẩu", font= 'Times 18', fg = 'white', bg="#0f1011").pack()
        self.password_confirm_entry = tk.Entry(self, show = "*" ,font = 'Times 20 ', fg = 'black')
        self.password_confirm_entry.pack(pady = 5)
        
        self.notice = Label(self, text="", font ="Times 13", fg = 'red', bg = '#0f1011')
        self.notice.pack(pady = 3)
        
    
        registerBtn = tk.Button(self, text = "Đăng ký", fg= 'black', bg= '#e0b64a', font = 'Times 25 bold', command= self.check_register)
        registerBtn.pack(pady = 10)
        
        backBtn = tk.Button(self, text = "Quay lại", fg= 'white', bg= '#e0b64a', font = 'Times 13 bold', command=lambda: controller.show_frame("LogInPage"))
        backBtn.pack()
    
    def check_register(self):  
        print("ĐĂNG KÝ")
        username = self.username_entry.get()
        password = self.password_entry.get()
        password_confirm = self.password_confirm_entry.get()
        print("Username: "+username)
        print("Password: "+ password)
        
        if (not username or not password or not password_confirm):
            print("Chưa điền đủ thông tin!")
            self.notice.config(text = "Chưa điền đủ thông tin!")
        elif (password !=  password_confirm):
            print("Mật khẩu không khớp!")
            self.notice.config(text = "Mật khẩu không khớp!")
        else:  
            client.sendall(SIGNUP.encode(FORMAT))
            client.sendall(username.encode(FORMAT))
            client.recv(1024).decode(FORMAT)
            client.sendall(password.encode(FORMAT))
            
            returned_result = client.recv(1024).decode(FORMAT)
            if (returned_result == "1"):
                print("Đăng ký thành công!")
                self.notice.config(text = "Đăng ký thành công!")
                #time.sleep(2)
                self.controller.show_frame("HomePage")
            if (returned_result == "0"):
                print("Tên đăng nhập đã được sử dụng!")
                self.notice.config(text= "Tên đăng nhập đã được sử dụng!")
        

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


app = App()
#main
try:
    app.mainloop()
except:
    print("Error: server is not responding")
    client.close()

# finally:
#     client.close()