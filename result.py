from tkinter import*
from PIL import Image,ImageTk  
from tkinter import ttk,messagebox
import sqlite3
class ResultClass:
    def __init__(self,home):
        self.home=home
        self.home.title("Student Result Management System")
        self.home.geometry("1200x500+80+170")
        self.home.config(bg="lightsteelblue")
        self.home.focus_force()

    #Title of result
        title=Label(self.home,text="Manage Student Results",font=("times new roman",20,"bold"),bg="black",fg="white").place(x=0,y=0,relwidth=1,height=50)

    
    #Variables
        self.var_roll=StringVar()
        self.var_name=StringVar()
        self.var_course=StringVar()
        self.var_marks=StringVar()
        self.var_full_marks=StringVar()
        self.roll_list=[]
    # Function calling from fetch
        self.fetch_roll()

    #Sections
        lbl_select = Label(self.home,text="Select Student",font=("times new roman",20,"bold"),bg="lightsteelblue").place(x=500,y=150)
        lbl_name = Label(self.home,text="Name",font=("times new roman",20,"bold"),bg="lightsteelblue").place(x=500,y=210)
        lbl_course = Label(self.home,text="Course",font=("times new roman",20,"bold"),bg="lightsteelblue").place(x=500,y=260)
        lbl_marks = Label(self.home,text="Marks Obtained",font=("times new roman",20,"bold"),bg="lightsteelblue").place(x=500,y=310)
        lbl_full_marks = Label(self.home,text="Full Marks",font=("times new roman",20,"bold"),bg="lightsteelblue").place(x=500,y=360)

        self.student1 = ttk.Combobox(self.home,textvariable=self.var_roll,values=self.roll_list,font=("times new roman",15,"bold"),state="readonly",justify=CENTER)
        self.student1.place(x=750,y=150,width=200)
        self.student1.set("Select")
        
        btn_search=Button(self.home,text="Search",font=("times new roman",15,"bold"),bg="blue",fg="white",cursor="hand2",command=self.search).place(x=980,y=150,width=100,height=28)

        txt_name = Entry(self.home,textvariable=self.var_name,font=("times new roman",20,"bold"),bg="lightyellow",state="readonly").place(x=750,y=210,width=320,height=30)
        txt_course = Entry(self.home,textvariable=self.var_course,font=("times new roman",20,"bold"),bg="lightyellow",state="readonly").place(x=750,y=260,width=320,height=30)
        txt_marks = Entry(self.home,textvariable=self.var_marks,font=("times new roman",20,"bold"),bg="lightyellow").place(x=750,y=310,width=330,height=30)
        txt_full_marks = Entry(self.home,textvariable=self.var_full_marks,font=("times new roman",20,"bold"),bg="lightyellow").place(x=750,y=360,width=320,height=30)

    #Buttons
        self.add=Button(self.home,text="Submit",font=("times new roman",15,"bold"),bg="violet",activebackground="lightblue",cursor="hand2",command=self.add)
        self.add.place(x=630,y=450,width=120,height=35)
        self.clear=Button(self.home,text="Clear",font=("times new roman",15,"bold"),bg="gold",activebackground="lightgreen",cursor="hand2",command=self.clear).place(x=810,y=450,width=120,height=35)

    #Image
        # self.bgImage=Image.open("Images/Result.png")
        # self.bgImage=self.bgImage.resize((920,800),Image.ANTIALIAS)
        # self.bgImage=ImageTk.PhotoImage(self.bgImage)

        # self.lbl_bg=Label(self.home,image=self.bgImage).place(x=625,y=50,width=920,height=800)

# Fetch to show roll no. in select student tab
    def fetch_roll(self):
        conn=sqlite3.connect(database="ResultManagementSystem.db")
        cur=conn.cursor()     
        try:
            cur.execute("Select roll no from student")
            rows=cur.fetchall()
            if len(rows)>0:
                for row in rows:
                    self.roll_list.append(row[0])
                
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")

#For Search tab functioning
    def search(self):
        conn=sqlite3.connect(database="ResultManagementSystem.db")
        cur=conn.cursor()     
        try:
            cur.execute("Select name,course from student where roll=?",(self.var_roll.get(),))
            row=cur.fetchone()
            if row !=None:
                self.var_name.set(row[0])
                self.var_course.set(row[1])
            else:
                messagebox.showerror("Error","No record Found",parent=self.home)    
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")


    def add(self):
        conn=sqlite3.connect(database="ResultManagementSystem.db")
        cur=conn.cursor()     
        try:
            if self.var_name.get()=="":
                messagebox.showerror("Error","Please First Search Student Record",parent=self.home)
            else:
                cur.execute("Select * from result where roll=? and course=?",(self.var_roll.get(),self.var_course.get())) #Due to tupple we added , at last
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error, Result already Present",parent=self.home)
                else:
                    percentage=(int(self.var_marks.get())*100)/int(self.var_full_marks.get())
                    cur.execute("Insert into result(roll,name,course,marks_obtain,full_marks,percentage) values(?,?,?,?,?,?)",(
                        self.var_roll.get(),
                        self.var_name.get(),
                        self.var_course.get(),
                        self.var_marks.get(),
                        self.var_full_marks.get(),
                        str(percentage)
                        
                    ) )
                    conn.commit()
                    messagebox.showinfo("Great","Result Added Successfully",parent=self.home)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")
    
    def clear(self):
        self.var_roll.set("Select"),
        self.var_name.set(""),
        self.var_course.set(""),
        self.var_marks.set(""),
        self.var_full_marks.set("")



if __name__=="__main__":
    home=Tk()
    obj=ResultClass(home)
    home.mainloop()