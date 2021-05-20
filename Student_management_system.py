
from tkinter import *
from tkinter import Toplevel,messagebox,filedialog
from tkinter.ttk import Treeview
from tkinter import ttk
import time
import sqlite3
import pandas

root= Tk()
root.title("Student management system")
root.geometry("1200x700+200+50")
root.config(bg='gold2')
root.iconbitmap('student_1.ico')
root.resizable(False,False)

## SLIDER FUNCTION
def clockTick():
    time_string=time.strftime('%H:%M:%S %p')
    date_string=time.strftime('%d:%m:%Y')
    clock.config(text='Date: '+date_string+"\n"+'Time: '+time_string)
    clock.after(200,clockTick)

def create_db():
    con = sqlite3.connect(database=r'student.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS student(id INTEGER PRIMARY KEY  AUTOINCREMENT,name varchar(30),mobile varchar(12),email varchar(30),address varchar(120),gender varchar(10),dob varchar(50),date varchar(50),time varchar(50))")
    con.commit()


global con,mycursor
con = sqlite3.connect(database='student.db')
mycursor =con.cursor()

def show():
    try:
        mycursor.execute("Select *from student")
        rows = mycursor.fetchall()
        studenttable.delete(* studenttable.get_children())
        for row in rows:
            studenttable.insert('',END,values=row)
    except Exception as e:
        messagebox.showerror("Error",f'Error due to: {str(e)}',parent=root)

## DATA ENTRY FUNCTION
def addstudent():
    def submitadd():
        id = idval.get()
        name = nameval.get()
        mobile = mobileval.get()
        email = emailval.get()
        address = addressval.get()
        gender = genderval.get()
        dob =  dobval.get()
        addedtime = time.strftime('%H:%M:%S')
        addeddate = time.strftime('%d:%M:%Y')

        try:
            if id =="":
                messagebox.showerror("Error","Student id must be required !",parent=root)
            else:
                mycursor.execute("Select *from student where id=?",(id,))
                row = mycursor.fetchone()
            if row!= None:
                messagebox.showerror("Error","This Student is already exists,try different id !",parent=root)
            elif  name =="":
                messagebox.showerror("Error","Name must be required !",parent=root)
            elif len(mobile) < 10 or len(mobile) > 10:
                messagebox.showerror("Error","Length of mobile number must be 10 !",parent=root)
            elif  gender =="Select":
                messagebox.showerror("Error","Gender must be required !",parent=root)
            else:
                mycursor.execute("Insert into  student (id,name,mobile,email,address,gender,dob,date,time) values(?,?,?,?,?,?,?,?,?)",(
                    id,name,mobile,email,address,gender,dob,addeddate,addedtime))
                con.commit()
                messagebox.showinfo("Success","Student is added successfully. ",parent=root)
                show()
                clear()
        except:
            pass

    def clear():
        idval.set('')
        nameval.set('')
        mobileval.set('')
        emailval.set('')
        addressval.set('')
        genderval.set('Select')
        dobval.set('')

    addroot= Toplevel(master=DataEntryFrame)
    addroot.grab_set()
    addroot.resizable(False,False)
    addroot.title('Add Student')
    addroot.iconbitmap('Student_2.ico')
    addroot.geometry('750x370+240+200')
    addroot.config(bg='spring green')
    # ADD STUDENT LABEL
    idlabel = Label(addroot,text='Id:',bg='spring green',font=('Times',20,'bold'),width=12,anchor='w')
    idlabel.place(x=20,y=20)
    namelabel = Label(addroot,text='Name:',bg='spring green',font=('Times',20,'bold'),width=12,anchor='w')
    namelabel.place(x=390,y=20)
    mobilelabel = Label(addroot,text='Mobile:',bg='spring green',font=('Times',20,'bold'),width=12,anchor='w')
    mobilelabel.place(x=20,y=80)
    emaillabel = Label(addroot,text='Email:',bg='spring green',font=('Times',20,'bold'),width=12,anchor='w')
    emaillabel.place(x=390,y=80)
    addresslabel = Label(addroot,text='Address:',bg='spring green',font=('Times',20,'bold'),width=12,anchor='w')
    addresslabel.place(x=20,y=140)
    genderlabel = Label(addroot,text='Gender:',bg='spring green',font=('Times',20,'bold'),width=12,anchor='w')
    genderlabel.place(x=390,y=140)
    doblabel = Label(addroot,text='D.O.B :',bg='spring green',font=('Times',20,'bold'),width=12,anchor='w')
    doblabel.place(x=200,y=200)

    # ADD STUDENT ENTRY
    idval=StringVar()
    nameval=StringVar()
    mobileval=StringVar()
    emailval=StringVar()
    addressval=StringVar()
    genderval=StringVar()
    dobval=StringVar()

    
    identry= Entry(addroot,font=('roman',15,'bold'),bd=2,textvariable=idval)
    identry.place(x=150,y=23)
    nameentry= Entry(addroot,font=('roman',15,'bold'),bd=2,textvariable=nameval)
    nameentry.place(x=510,y=23)
    mobileentry= Entry(addroot,font=('roman',15,'bold'),bd=2,textvariable=mobileval)
    mobileentry.place(x=150,y=83)
    emailentry= Entry(addroot,font=('roman',15,'bold'),bd=2,textvariable=emailval)
    emailentry.place(x=510,y=83)
    addressentry= Entry(addroot,font=('roman',15,'bold'),bd=2,textvariable=addressval)
    addressentry.place(x=150,y=143)
    genderentry = ttk.Combobox(addroot,values=("Select","Male","Female","Other"),state="readonly",justify=CENTER,font=("times new roman",15,"bold"),textvariable=genderval)
    genderentry.place(x=510,y=143,width=207)
    genderentry.current(0)
    dobentry= Entry(addroot,font=('roman',15,'bold'),bd=2,textvariable=dobval)
    dobentry.place(x=310,y=203)

    submitbtn = Button(addroot,text='Submit',width=20,font=('goudy old style',16,'bold'),bd=3,bg='yellow',activeforeground='red',command=submitadd)
    submitbtn.place(x=275,y=270)

    addroot.mainloop()

def searchstudent():
    def submitsearch():
        txt = searchtxtval.get()
        by = searchbyval.get()

        try:
            if by =="Select":
                messagebox.showerror("Error","Search by option must be required !",parent=root)
            elif  txt =="":
                messagebox.showerror("Error","Search input should be required !",parent=root)
                mycursor.execute("select * from student")
            else:
                by = by.lower()
                mycursor.execute("select *from student where "+by+" LIKE '%"+txt+"%'")
                rows = mycursor.fetchall()
                print(rows)
                if len(rows)!=0:
                    studenttable.delete(*studenttable.get_children())
                    for row in rows:
                        studenttable.insert('',END,values=row)
                    clear()
                else:
                    messagebox.showerror("Notification","No record found !",parent=root)
        except:
            pass

    def clear():
        searchbyval.set('Select')
        searchtxtval.set('')
        
    searchroot= Toplevel(master=DataEntryFrame)
    searchroot.grab_set()
    searchroot.resizable(False,False)
    searchroot.title('Search Student')
    searchroot.iconbitmap('Student_2.ico')
    searchroot.geometry('340x270+440+400')
    searchroot.config(bg='spring green')
    
    searchbyval=StringVar()
    searchtxtval=StringVar()
    
    search_by = ttk.Combobox(searchroot,values=('Select','Id','Name','Mobile','Email','Address','Gender','DOB','Date'),state="readonly",justify=CENTER,font=("times new roman",15,"bold"),textvariable=searchbyval)
    search_by.place(x=60,y=20,width=220,height=45)
    search_by.current(0)

    searchtype= Entry(searchroot,font=('goudy',15,'bold'),justify=CENTER,bd=2,textvariable=searchtxtval)
    searchtype.place(x=60,y=90,width=220,height=45)

    
    submitbtn = Button(searchroot,text='Search',width=20,font=('goudy old style',17,'bold'),bd=3,bg='Yellow',activeforeground='white',activebackground='sea green',command=submitsearch)
    submitbtn.place(x=105,y=170,width=130)

    searchroot.mainloop()

def deletestudent():
    f = studenttable.focus()
    content = studenttable.item(f)
    id = content['values'][0]
    try:
        if id =="":
            messagebox.showerror("Error","Student id must be required !",parent=root)
        else:
            mycursor.execute("Select *from student where id=?",(id,))
            row = mycursor.fetchone()
            if row ==None:
                messagebox.showinfo("Error","Invalid Student Id !",parent=root)
            else:
                op = messagebox.askyesno('Confirm','Do you really Want to Delete the record ?',parent=root)
                if op == True:
                    mycursor.execute("delete from student where id =?",(id,))
                    con.commit()
                    messagebox.showinfo("Success",f"Student with Id: {str(id)} Deleted Successfully. ",parent=root)
                    show()
    except:
        pass

def updatestudent():
    def updatesubmit():
        id = idval.get()
        name = nameval.get()
        mobile = mobileval.get()
        email = emailval.get()
        address = addressval.get()
        gender = genderval.get()
        dob =  dobval.get()
        addeddate = dateval.get()
        addedtime = timeval.get()

        try:
            mycursor.execute("Select *from student where id=?",(id,))
            row = mycursor.fetchone()
            if row ==None:
                messagebox.showinfo("Error","Invalid Student Id !",parent=root)
            elif  name =="":
                messagebox.showerror("Error","Name must be required !",parent=root)
            elif len(mobile) < 10 or len(mobile) > 10:
                messagebox.showerror("Error","Length of mobile number must be 10 !",parent=root)
            elif  gender =="Select":
                messagebox.showerror("Error","Gender must be required !",parent=root)
            else:
                addedtime = time.strftime('%H:%M:%S')
                addeddate = time.strftime('%d:%M:%Y')
                mycursor.execute("update student set name=?,mobile=?,email=?,address=?,gender=?,dob=?,date=?,time=? where id =?",
                    (name,mobile,email,address,gender,dob,addeddate,addedtime,id))
                con.commit()
                messagebox.showinfo("Success",f"Student with Id: {str(id)} Updated Successfully.",parent=root)
                show()
                clear()              
        except:
            pass

    def clear():
        idval.set('')
        nameval.set('')
        mobileval.set('')
        emailval.set('')
        addressval.set('')
        genderval.set('Select')
        dobval.set('')

    updateroot= Toplevel(master=DataEntryFrame)
    updateroot.grab_set()
    updateroot.resizable(False,False)
    updateroot.title('Update Student')
    updateroot.iconbitmap('Student_2.ico')
    updateroot.geometry('750x370+240+200')
    updateroot.config(bg='spring green')

    # UPDATE STUDENT LABEL
    idlabel = Label(updateroot,text='Id:',bg='spring green',font=('Times',20,'bold'),width=12,anchor='w')
    idlabel.place(x=20,y=20)
    namelabel = Label(updateroot,text='Name:',bg='spring green',font=('Times',20,'bold'),width=12,anchor='w')
    namelabel.place(x=390,y=20)
    mobilelabel = Label(updateroot,text='Mobile:',bg='spring green',font=('Times',20,'bold'),width=12,anchor='w')
    mobilelabel.place(x=20,y=80)
    emaillabel = Label(updateroot,text='Email:',bg='spring green',font=('Times',20,'bold'),width=12,anchor='w')
    emaillabel.place(x=390,y=80)
    addresslabel = Label(updateroot,text='Address:',bg='spring green',font=('Times',20,'bold'),width=12,anchor='w')
    addresslabel.place(x=20,y=140)
    genderlabel = Label(updateroot,text='Gender:',bg='spring green',font=('Times',20,'bold'),width=12,anchor='w')
    genderlabel.place(x=390,y=140)
    doblabel = Label(updateroot,text='D.O.B :',bg='spring green',font=('Times',20,'bold'),width=12,anchor='w')
    doblabel.place(x=200,y=200)

    # UPDATE STUDENT ENTRY
    idval=StringVar()
    nameval=StringVar()
    mobileval=StringVar()
    emailval=StringVar()
    addressval=StringVar()
    genderval=StringVar()
    dobval=StringVar()
    dateval=StringVar()
    timeval=StringVar()

 
    identry= Entry(updateroot,font=('roman',15,'bold'),bd=2,textvariable=idval)
    identry.place(x=150,y=23)
    nameentry= Entry(updateroot,font=('roman',15,'bold'),bd=2,textvariable=nameval)
    nameentry.place(x=510,y=23)
    mobileentry= Entry(updateroot,font=('roman',15,'bold'),bd=2,textvariable=mobileval)
    mobileentry.place(x=150,y=83)
    emailentry= Entry(updateroot,font=('roman',15,'bold'),bd=2,textvariable=emailval)
    emailentry.place(x=510,y=83)
    addressentry= Entry(updateroot,font=('roman',15,'bold'),bd=2,textvariable=addressval)
    addressentry.place(x=150,y=143)
    genderentry = ttk.Combobox(updateroot,values=("Select","Male","Female","Other"),state="readonly",justify=CENTER,font=("times new roman",15,"bold"),textvariable=genderval)
    genderentry.place(x=510,y=143,width=207)
    genderentry.current(0)
    dobentry= Entry(updateroot,font=('roman',15,'bold'),bd=2,textvariable=dobval)
    dobentry.place(x=310,y=203)
   
    submitbtn = Button(updateroot,text='Update',width=20,font=('goudy old style',18,'bold'),bd=3,bg='yellow',activeforeground='red',command=updatesubmit)
    submitbtn.place(x=275,y=270,width=230)
    
    updateroot.mainloop()

def showstudent():
    try:
        mycursor.execute("Select *from student")
        rows = mycursor.fetchall()
        studenttable.delete(* studenttable.get_children())
        for row in rows:
            studenttable.insert('',END,values=row)
    except:
        pass

def exportstudent():
    ask =messagebox.askyesnocancel("Notification","Do you want to export the data in csv format ?")
    print(ask)
    if ask == True:
        file = filedialog.asksaveasfilename()
        records = studenttable.get_children()
        id,name,mobile,email,address,gender,dob,date,time=[],[],[],[],[],[],[],[],[]
        for record in records:
            content = studenttable.item(record)
            row = content['values']
            id.append(row[0]),name.append(row[1]),mobile.append(row[2]),email.append(row[3]),address.append(row[4]),gender.append(row[5]),
            dob.append(row[6]),date.append(row[7]),time.append(row[8])
        datacolumn = ['Id','Name','Mobile','Email','Address','Gender','D.O.B','Date','Time']
        dataframe = pandas.DataFrame(list(zip(id,name,mobile,email,address,gender,dob,date,time)),columns=datacolumn)
        paths = r'{}.csv'.format(file)
        dataframe.to_csv(paths,index=False)
        messagebox.showinfo('Notifications', 'Student data is Saved {}'.format(paths))

def exitstudent():
    res = messagebox.askyesnocancel('Notification','Do you want to exit ?')
    if res == True:
        root.destroy()


# S L I D E R
text_lbl =Label(root,anchor=W,font=("times new roman",30,"bold"),bg="#010CA8")
text_lbl.place(x=0,y=0,relwidth=1,height=70)

# Welcome Text
wel_text = Label(text_lbl, text='Welcome To Student Management System',anchor=W,font=("times new roman",25,"bold"),bg="#010CA8",fg='white',padx=20,justify=RIGHT)
wel_text.place(x=290,y=10)

# Clock
clock=Label(text_lbl,borderwidth=4,font=("Gintronic", 13, "bold"),bg="#010CA8",fg="white")
clock.place(x=15,y=7)
clockTick()

# ============================================= F R A M E S =============================================
# ---------------------------------------D A T A     E N T R Y     F R A M E------------------------------
DataEntryFrame=Frame(root,relief=RIDGE,borderwidth=5)
DataEntryFrame.place(x=20,y=80,width=300,height=600)

frontlabel = Label(DataEntryFrame,text='menu',bg='turquoise2',width=20,font=('arial',20,'bold'))
frontlabel.pack(side=TOP,expand=True)
addbtn = Button(DataEntryFrame,text='Add Student',width=25,font=('goudy old style',20,'bold'),relief=RIDGE,bd=3,bg='white',activeforeground='white',activebackground='sea green',command=addstudent)
addbtn.pack(side=TOP,expand=True)
searchbtn = Button(DataEntryFrame,text='Search Student',width=25,font=('goudy old style',20,'bold'),relief=RIDGE,bd=3,bg='white',activeforeground='white',activebackground='sea green',command=searchstudent)
searchbtn.pack(side=TOP,expand=True)
deletebtn = Button(DataEntryFrame,text='Delete Student',width=25,font=('goudy old style',20,'bold'),relief=RIDGE,bd=3,bg='white',activeforeground='white',activebackground='sea green',command=deletestudent)
deletebtn.pack(side=TOP,expand=True)
updatebtn = Button(DataEntryFrame,text='Update Student',width=25,font=('goudy old style',20,'bold'),relief=RIDGE,bd=3,bg='white',activeforeground='white',activebackground='sea green',command=updatestudent)
updatebtn.pack(side=TOP,expand=True)
showallbtn = Button(DataEntryFrame,text='Show all',width=25,font=('goudy old style',20,'bold'),relief=RIDGE,bd=3,bg='white',activeforeground='white',activebackground='sea green',command=showstudent)
showallbtn.pack(side=TOP,expand=True)
explorebtn = Button(DataEntryFrame,text='Export data',width=25,font=('goudy old style',20,'bold'),relief=RIDGE,bd=3,bg='white',activeforeground='white',activebackground='sea green',command=exportstudent)
explorebtn.pack(side=TOP,expand=True)
exitbtn = Button(DataEntryFrame,text='Exit',width=25,font=('goudy old style',20,'bold'),relief=RIDGE,bd=3,bg='white',activeforeground='white',activebackground='sea green',command=exitstudent)
exitbtn.pack(side=TOP,expand=True)

# --------------------------------------S H O W    D A T A    F R A M E-----------------------------------------
ShowDataFrame=Frame(root,relief=RIDGE,borderwidth=2)
ShowDataFrame.place(x=330,y=80,width=850,height=600)

style= ttk.Style()
style.configure('Treeview.Heading',font=('goudy old style',15,'bold'),foreground='red2')
style.configure('Treeview',font=('times',15,'bold'),foreground='black',background='thistle1')

scroll_x = Scrollbar(ShowDataFrame,orient=HORIZONTAL)
scroll_y = Scrollbar(ShowDataFrame,orient=VERTICAL)

studenttable = ttk.Treeview(ShowDataFrame,columns=('id','name','mobile','email','address','gender','dob','date','time'),yscrollcommand=scroll_y.set,xscrollcommand=scroll_x.set)
scroll_x.pack(side=BOTTOM,fill=X)
scroll_y.pack(side=RIGHT,fill=Y)
scroll_x.config(command=studenttable.xview)
scroll_y.config(command=studenttable.yview)

studenttable.heading('id',text='Id')
studenttable.heading('name',text='Name')
studenttable.heading('mobile',text='Mobile No')
studenttable.heading('email',text='Email')
studenttable.heading('address',text='Address')
studenttable.heading('gender',text='Gneder')
studenttable.heading('dob',text='D.O.B')
studenttable.heading('date',text='Date')
studenttable.heading('time',text='Time')

studenttable['show'] = 'headings'

studenttable.column('id',width=80)
studenttable.column('name',width=200)
studenttable.column('mobile',width=200)
studenttable.column('email',width=200)
studenttable.column('address',width=200)
studenttable.column('gender',width=80)
studenttable.column('dob',width=140)
studenttable.column('date',width=140)
studenttable.column('time',width=140) 
studenttable.pack(fill=BOTH,expand=1)
show()
create_db()

root.mainloop()