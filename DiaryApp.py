from tkinter import *
import datetime as dt
from tkinter import messagebox as mb
import mysql.connector as msc

def db_creation():

    con = msc.connect(host = "localhost", username = "root", password = "")
    
    if con.is_connected():
        our_database = 'diaryapp'
        cur = con.cursor(buffered = True)
        cur.execute("show databases like '%s'"%our_database)
        row = cur.fetchone()

        if row == None:
            cur.execute("create database %s"%our_database)
            cur.execute('''create table %s.user_info (
                            userID integer auto_increment primary key,
                            username text,
                            password text 
            )'''%our_database)
            cur.execute('''create table %s.workspace (
                            userID integer,
                            user_text text,
                            text_date text
            )'''%our_database)
            con.close()

        login_window()

    else:
        mb.showerror("Error", "Could not Connect to Database !")

def login_user():
    
    global conn, connecting_ID

    name = logname.get()
    passwd = logpass.get()

    if name == "":
        mb.showinfo("Alert", "Enter Username !")

    elif passwd == "":
        mb.showinfo("Alert", "Enter Password !")
    
    else:
        conn = msc.connect(host = "localhost", username = "root", password = "", database = "diaryapp")

        if conn.is_connected():
            cur = conn.cursor()
            cur.execute(''' select * from user_info
                            where username = %s and password = %s''', (name, passwd))

            row = cur.fetchone()

            if row == None:
                mb.showerror("Login", "Account does not exist ! create one through Register.")
                logn.delete(0, END)
                logp.delete(0, END)
                
            else:
                connecting_ID = row[0]
                mb.showinfo("Login", "Login Successful !")
                login.destroy()
                workspace()    

        else:
            mb.showerror("Error", "Could not Connect to Database !")

def register_user():
    name = regname.get()
    passwd = regpass.get()

    if name == "":
        mb.showinfo("Alert", "Enter Username !")

    elif passwd == "":
        mb.showinfo("Alert", "Enter Password !")
    
    else:
        con = msc.connect(host = "localhost", username = "root", password = "", database = "diaryapp")

        if con.is_connected():
            cur = con.cursor(buffered = True)
            cur.execute(''' select * from user_info
                            where username = %s and password = %s''', (name, passwd))

            row = cur.fetchone()

            if row == None:
                response = mb.askquestion("Alert", "Are you sure about your credentials")
                if response == 'yes':
                    cur.execute(''' insert into user_info (username, password)
                                    values (%s, %s)''', (name, passwd))
                    con.commit()

                    cur.execute(''' select * from user_info
                                where username = %s and password = %s''', (name, passwd))

                    data = cur.fetchone()
                    con.close()

                    if data == None:
                        mb.showerror("Register", "Could Not Register Try Again !")
                        regn.delete(0, END)
                        regp.delete(0, END)

                    else:
                        mb.showinfo("Register", "Registered Successfuly !")
                        regn.delete(0, END)
                        regp.delete(0, END)
                
            else:
                mb.showerror("Register", "Account Already Exist, Try Login !")
                regn.delete(0, END)
                regp.delete(0, END)    

        else:
            mb.showerror("Error", "Could not Connect to Database !")

def login_window():

    def close():
        login.destroy()

    global logname, logpass, login, logn, logp
    

    login = Tk()
    window_width = 500
    window_height = 500
    screen_width = login.winfo_screenwidth()
    screen_height = login.winfo_screenheight()
    x_center = int((screen_width/2)-(window_width/2))
    y_center = int((screen_height/2)-(window_height/2))

    login.geometry(f"{window_width}x{window_height}+{x_center}+{y_center}")
    login.minsize(500, 500)
    login.configure(bg="#23799e")
    login.title("DiaryApp - Login")

    f2 = Frame(login, width=575, height=575, background="#23799e")
    f2.place(anchor="c", relx=.5, rely=.6)

    Label(login, text="Login", width = 5, font=("Calibri", 70), bg = "#23799e", fg="peachpuff").place(in_=f2, x=43, y=10)
    Label(login, text="Username", width = 10, font=("Calibri", 25), bg = "#23799e", fg="peachpuff").place(in_=f2, x=48, y=130)
    Label(login, text="Password", width = 10, font=("Calibri", 24), bg = "#23799e", fg="peachpuff").place(in_=f2, x=48, y=200)
    Label(login, text="Already Account - Login", font=("Calibri", 15), bg = "#23799e", fg="peachpuff").place(in_=f2, x=68, y=350)
    Label(login, text="New User - Register", font=("Calibri", 15), bg = "#23799e", fg="peachpuff").place(in_=f2, x=68, y=380)

    logname = StringVar()
    logpass = StringVar()

    logn = Entry(login, textvariable = logname, width = 25, font=("Calibri", 15))
    logn.place(in_=f2, x=250, y=140)
    logp = Entry(login, textvariable = logpass, width = 25, font=("Calibri", 15), show='*')
    logp.place(in_=f2, x=250, y=210)

    Button(login, text = 'Login', width = 20, font=("Calibri", 15), bg="peachpuff", command = login_user).place(in_=f2, x=68, y=280)
    Button(login, text = 'Register Here', width = 20, font=("Calibri", 15), bg="peachpuff", command = lambda:[close(), register_window()]).place(in_=f2, x=295, y=280)

    login.mainloop()

def register_window():

    def close():
        register.destroy()

    global register, regname, regpass, regn, regp

    register = Tk()
    window_width = 500
    window_height = 500
    screen_width = register.winfo_screenwidth()
    screen_height = register.winfo_screenheight()
    x_center = int((screen_width/2)-(window_width/2))
    y_center = int((screen_height/2)-(window_height/2))

    register.geometry(f"{window_width}x{window_height}+{x_center}+{y_center}")
    register.minsize(500, 500)
    register.configure(bg="#23799e")
    register.title("DiaryApp - Register")
    
    f2 = Frame(register, width=575, height=575, background="#23799e")
    f2.place(anchor="c", relx=.5, rely=.6)

    Label(register, text="Register", font=("Calibri", 60), bg = "#23799e", fg="peachpuff").place(in_=f2, x=60, y=10)
    Label(register, text="Username", width = 10, font=("Calibri", 25), bg = "#23799e", fg="peachpuff").place(in_=f2, x=48, y=130)
    Label(register, text="Password", width = 10, font=("Calibri", 24), bg = "#23799e", fg="peachpuff").place(in_=f2, x=48, y=200)

    regname = StringVar()
    regpass = StringVar()

    regn = Entry(register, textvariable = regname, width = 25, font=("Calibri", 15))
    regn.place(in_=f2, x=250, y=140)
    regp = Entry(register, textvariable = regpass, width = 25, font=("Calibri", 15), show='*')
    regp.place(in_=f2, x=250, y=210)

    Button(register, text = 'Register', width = 20, font=("Calibri", 15), bg="peachpuff", command=register_user).place(in_=f2, x=68, y=280)
    Button(register, text = 'Back To Login', width = 20, font=("Calibri", 15), bg="peachpuff", command=lambda:[close(), login_window()]).place(in_=f2, x=295, y=280)

    Label(register, text="Account created - Back To Login", font=("Calibri", 15), bg = "#23799e", fg="peachpuff").place(in_=f2, x=68, y=350)

    register.mainloop()

def workspace():

    def logout():
        conn.close()
        mb.showinfo("Logout", "Logout Successfuly")
        window.destroy()
        login_window()

    def save_entry():
        content = text.get('1.0', END)

        if len(content) == 1:
            mb.showinfo("Save", "Can't Save Empty Text !")
        
        elif text['state'] == DISABLED:
            mb.showinfo("Save", "Already Saved !")

        else:
            cur = conn.cursor()
            cur.execute("insert into workspace values(%s, %s, %s)",(connecting_ID, content, Date))
            conn.commit()
            mb.showinfo("Save", "Saved Successfuly !")
            listbox.delete(0,END)

            cur.execute("select text_date from workspace where userID = %s"%connecting_ID)
            row = cur.fetchall()

            for i in range(len(row)):
                listbox.insert(0, row[i])
            
            text.delete('1.0', END)

    def clear_entry():
        text.configure(state=NORMAL)
        date_label['text'] = Date
        text.delete('1.0', END)
        
    def select_from_list(e):
        text.configure(state=NORMAL)

        selected_date = listbox.get(ANCHOR)

        cur.execute("select user_text from workspace where userID = %s and text_date = %s", (connecting_ID, selected_date[0]))
        row = cur.fetchone()
        
        text.delete('1.0', END)
        text.insert(END, row[0])
        date_label['text'] = selected_date[0]
        text.configure(state=DISABLED)

    window = Tk()
    window_width = 1100
    window_height = 700
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_center = int((screen_width/2)-(window_width/2))
    y_center = int((screen_height/2)-(window_height/2))


    window.geometry(f"{window_width}x{window_height}+{x_center}+{y_center}")
    window.minsize(1100, 700)
    window.configure(bg="#23799e")
    window.title("DiaryApp - Workspace")

    f2 = Frame(window, background="#23799e", width=1075, height=700)
    f2.place(anchor="c", relx=0.5, rely=0.5)

    date = dt.datetime.now()
    Date = format(date, "%d-%m-%Y")

    date_label = Label(window, text=Date, font=("Calibri", 15), bg="#23799e", fg="peachpuff")
    date_label.place(in_=f2, x=20, y=10)

    Label(window, text="Older Entries", font=("Calibri", 15), bg="#23799e", fg="peachpuff").place(in_=f2, x=850, y=10)

    text = Text(window, height = 26, font=("Calibri", 15), bg="peachpuff")
    text.place(in_=f2, x=20, y=50)

    listbox = Listbox(window, height = 20, font=("Calibri", 15), bg="peachpuff")
    listbox.place(in_=f2, x=850, y=50)

    cur = conn.cursor()
    cur.execute("select text_date from workspace where userID = %s"%connecting_ID)
    row = cur.fetchall()

    for i in range(len(row)):
        listbox.insert(0, row[i])

    listbox.bind('<<ListboxSelect>>', select_from_list)

    Button(window, text="Clear", width = 28, font=("Calibri", 10), bg="peachpuff", command=clear_entry).place(in_=f2, x=850, y=570)
    Button(window, text="Save", width = 28, font=("Calibri", 10), bg="peachpuff", command=save_entry).place(in_=f2, x=850, y=610)
    Button(window, text="LogOut", width = 28, font=("Calibri", 10), bg="peachpuff", command=logout).place(in_=f2, x=850, y=650)

    window.mainloop()
    
db_creation()
