from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from sqlite3 import *

import requests
import bs4

import matplotlib.pyplot as plt

def f1():
	add_window.deiconify()
	main_window.withdraw()


def f2():
    main_window.deiconify()
    add_window.withdraw()

def f3():
    view_window.deiconify()
    main_window.withdraw()

    view_window_st_data.delete(1.0, END)
    info = ""
    con = None
    try:
        con = connect('intern.db')
        cursor = con.cursor()
        sql = "select * from student"
        cursor.execute(sql)
        data = cursor.fetchall()
        for d in data:
            info = info + " Rno = " + str(d[0]) + " Name = " + str(d[1]) +"  Marks="+str(d[2])+ "\n"
        view_window_st_data.insert(INSERT, info)
    except Exception as e:
        showerror('Failure', e)

    finally:
        if con is not None:
            con.close()

def f4():
    main_window.deiconify()
    view_window.withdraw()
def f5():
    update_window.deiconify()
    main_window.withdraw()

def f6():
    main_window.deiconify()
    update_window.withdraw()

def f7():
    delete_window.deiconify()
    main_window.withdraw()

def f8():
    main_window.deiconify()
    delete_window.withdraw()

def f9():
    con=connect('intern.db')
    c=con.cursor()
    c.execute('select name,marks from student')
    data=c.fetchall()
    name=[]
    marks=[]
    for row in data:
        name.append(row[0])
        marks.append(row[1])

    plt.bar(name,marks,color=['red','green','blue'])
    plt.xlabel("Name")
    plt.ylabel("Marks")
    plt.title("Batch Performance ")
    con.commit()

    # close connection
    con.close()
    plt.show()


def sf1():
    con = None
    try:
        con = connect('intern.db')
        cursor = con.cursor()

        sql = "insert into student values('%d','%s','%d')"
        rno = int(add_window_ent_no.get())
        name = add_window_ent_name.get()
        marks = int(add_window_ent_marks.get())
        if rno>0 and 0<=marks<100 and len(name)>=2 and name.isalpha():

            cursor.execute(sql % (rno, name,marks))
            con.commit()
            showinfo('Success', 'record added')

        elif name.isalpha()==False:
            showwarning("Warning", "Enter only chararcters")

        elif rno<0:
            showwarning("Warning","Rno shud be +ve")
    #
        elif marks<0:
            showwarning("Warning", "Marks greater be less than 0")

        elif marks > 100:
            showwarning("Warning", "Marks shud be less than 100")

        elif len(name)<2:
            showwarning("Warning","Letter should be minimum 2")
        #
        # elif rno.isalnum():
        #     showwarning("Warning", "Rno shud be in digits only")
        # else:
        #     showwarning("Exists","Record Already exits")

    except IntegrityError:
        showerror("Exists","Record Already exits")

    except ValueError:
        showerror("Failure", "Enter Integers")

    except Exception as e:
        showerror('Failure', e)

    finally:
        if con is not None:
            con.close()
        view_window_st_data.focus()

def sf2():
    con = None
    try:
        con = connect('intern.db')
        cursor = con.cursor()
        sql = "update student set name = '%s',marks ='%d' where rno = '%d'"
        rno = int(update_window_ent_no.get())
        name = update_window_ent_name.get()
        marks = int(update_window_ent_marks.get())
        cursor.execute(sql % (name, marks, rno))
        con.commit()

        # if cursor.rowcount > 0:
        #     showinfo('Success ','Record Updated ')
        #     con.commit()
        if rno > 0 and 0<=marks < 100 and len(name)>=2 and name.isalpha() and cursor.rowcount > 0:

            cursor.execute(sql % (name, marks, rno))
            con.commit()
            showinfo('Success', 'record Updated')

        # if cursor.rowcount > 0:
        #     showinfo('Success ','Record Updated ')
        #     con.commit()
        elif marks<0:
            showwarning("Warning", "Marks should be greater  than 0")

        elif name.isalpha()==False:
            showwarning("Warning", "Enter only chararcters")

        elif rno < 0:
            showwarning("Warning", "Rno shud be +ve")
        #
        elif marks>100:
            showwarning("Warning", "Marks shud be less than 100")

        elif len(name)<2:
            showwarning("Warning","Letter should be minimum 2")

        # elif cursor.rowcount > 0:
        #     showinfo('Success ','Record Updated ')
        #     con.commit()
        else:
            showwarning('Warning',"Record doesn't exist")

    #

    except ValueError:
        showerror("Failure", "Enter Integers")
    except Exception as e:
        showerror('Failure', e)


    

    finally:
        if con is not None:
            con.close()
        view_window_st_data.focus()


def sf3():
    con = None

    try:
        con = connect("intern.db")
        cursor = con.cursor()
        sql = "delete from student where rno='%d'"
        rno = int(delete_window_ent_no.get())
        cursor.execute(sql % (rno))
        if cursor.rowcount > 0:
            showinfo('Success',"record deleted")
            con.commit()
        else:
            showwarning('Failure',"Record doesn't exist")

    except ValueError:
        showerror("Failure", "Enter Integers")

    except Exception as e:
        print("issue", e)
        con.rollback()
    finally:
        if con is not None:
            con.close()
            print("Closed")



main_window=Tk()
main_window.title("S.M.S")
main_window.geometry("1020x700+380+10")

f =('Arial',20,'bold')
main_window_btn_add = Button(main_window,text="Add",font=f,width=10,command=f1)
main_window_btn_view = Button(main_window,text="View",font=f,width=10,command=f3)
main_window_btn_update = Button(main_window,text="Update",font=f,width=10,command=f5)
main_window_btn_delete = Button(main_window,text="Delete",font=f,width=10,command=f7)
main_window_btn_charts = Button(main_window,text="Charts",font=f,width=10,command=f9)

main_window_Location = Label(main_window,text="Location : ",font=f)

try:
    wa = "https://ipinfo.io/"
    res = requests.get(wa)

    data = res.json()

    city = data['city']

except Exception as e:
	print("issue",e)
main_window_Location_displaylabel = Label(main_window, text=city , font=f)


main_window_quotd_label = Label(main_window,text="QUOTD : ",font=f)
try:
    wa = "https://www.brainyquote.com/quote_of_the_day"
    res = requests.get(wa)

    data = bs4.BeautifulSoup(res.text, 'html.parser')

    info = data.find('img', {'class': 'p-qotd'})

    msg = info['alt']
    main_window_quotd_displaylabel = Label(main_window, text=msg , font=f)


except Exception as e:
    print('issue', e)




main_window_btn_add.pack(pady=10)
main_window_btn_view.pack(pady=10)
main_window_btn_update.pack(pady=10)
main_window_btn_delete.pack(pady=10)
main_window_btn_charts.pack(pady=10)
main_window_Location.place(x=10,y=400)
main_window_Location_displaylabel.place(x=150,y=400)
main_window_quotd_label.place(x=10,y=450)

main_window_quotd_displaylabel .place(x=150,y=450)


add_window = Toplevel(main_window)
add_window.title("Add St.")
add_window.geometry("500x500+400+100")

add_window_lbl_rno = Label(add_window,text="Enter Roll No :",font=f)
add_window_ent_no = Entry(add_window,bd=5,font=f)
add_window_lbl_name = Label(add_window,text="Enter Name :",font=f)
add_window_ent_name = Entry(add_window,bd=5,font=f)
add_window_lbl_marks = Label(add_window,text="Enter Marks :",font=f)
add_window_ent_marks = Entry(add_window,bd=5,font=f)
add_window_btn_save = Button(add_window,text="Save",font=f,command=sf1)
add_window_btn_back = Button(add_window,text="Back",font=f,command=f2)

add_window_btn_save.focus()
add_window_btn_back.focus()


add_window_lbl_rno.pack(pady=10)
add_window_ent_no.pack(pady=10)
add_window_lbl_name.pack(pady=10)
add_window_ent_name.pack(pady=10)
add_window_lbl_marks.pack(pady=10)
add_window_ent_marks.pack(pady=10)
add_window_btn_save.pack(pady=10)
add_window_btn_back.pack(pady=10)
add_window.withdraw()

view_window = Toplevel(main_window)
view_window.title("View St.")
view_window.geometry("500x500+400+100")

view_window_st_data = ScrolledText(view_window,width=35,height=10,font=('Arial',20,'bold'))
view_window_btn_back = Button(view_window,text="Back",font=('Arial',20,'bold'),command=f4)
view_window_st_data.pack(pady=10)
view_window_btn_back.pack(pady=10)
view_window.withdraw()

update_window=Toplevel(main_window)
update_window.title("Update St")
update_window.geometry("500x500+400+100")

update_window_lbl_rno = Label(update_window,text="Enter Roll No :",font=f)
update_window_ent_no = Entry(update_window,bd=5,font=f)
update_window_lbl_name = Label(update_window,text="Enter Name :",font=f)
update_window_ent_name = Entry(update_window,bd=5,font=f)
update_window_lbl_marks = Label(update_window,text="Enter Marks :",font=f)
update_window_ent_marks = Entry(update_window,bd=5,font=f)
update_window_btn_save = Button(update_window,text="Save",font=f,command=sf2)
update_window_btn_back = Button(update_window,text="Back",font=f,command=f6)

update_window_lbl_rno.pack(pady=10)
update_window_ent_no.pack(pady=10)
update_window_lbl_name.pack(pady=10)
update_window_ent_name.pack(pady=10)
update_window_lbl_marks.pack(pady=10)
update_window_ent_marks.pack(pady=10)
update_window_btn_save.pack(pady=10)
update_window_btn_back.pack(pady=10)
update_window.withdraw()

delete_window=Toplevel(main_window)
delete_window.title("Delete St")
delete_window.geometry("500x500+400+100")
delete_window_lbl_rno = Label(delete_window,text="Enter Roll No :",font=f)
delete_window_ent_no = Entry(delete_window,bd=5,font=f)
delete_window_btn_save = Button(delete_window,text="Save",font=f,command=sf3)
delete_window_btn_back = Button(delete_window,text="Back",font=f,command=f8)


delete_window_lbl_rno.pack(pady=10)
delete_window_ent_no.pack(pady=10)
delete_window_btn_save.pack(pady=10)
delete_window_btn_back.pack(pady=10)
delete_window.withdraw()



main_window.mainloop()