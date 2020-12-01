from tkinter import *

class settingOffset():
    def __init__(self, master):
        self.master = master
        self.master.geometry('250x120+500+500')
        self.master.maxsize(250,120)
        self.master.minsize(250,120)
        self.master.title('Add Area')

        self.frame = Frame(self.master)
        self.frame.pack(anchor=CENTER, ipadx=1, ipady=1, padx=5, pady=5)

        self.camCode = Label(self.frame,text='ID  Area: ').grid(row=1, column=0, sticky = NW)
        self.camCode = Label(self.frame,text='Cam Code: ').grid(row=2, column=0, sticky = NW)
        self.offSet = Label(self.frame,text='Off Set: ').grid(row=3, column=0, sticky=NW)
        self.areaCode = Label(self.frame,text='Area Code: ').grid(row=4, column=0,sticky=NW)
        a= StringVar()
        b= StringVar()
        c= StringVar()
        d= StringVar()
        textCheck=False

        def passText(event):
            self.text_entry1.delete(0, END)
            self.text_entry2.delete(0, END)
            self.text_entry3.delete(0, END)
            self.text_entry4.delete(0, END)
            textCheck = True

        self.text_entry1 = Entry(self.frame, textvariable=a)
        self.text_entry1.grid(row=1,column=1)
        self.text_entry1.insert(0,'-- ID Khu vuc --')

        self.text_entry2 = Entry(self.frame)
        self.text_entry2.grid(row=2,column=1)
        self.text_entry2.insert(0,'-- Ma Camera --')

        self.text_entry3 = Entry(self.frame)
        self.text_entry3.grid(row=3,column=1)
        self.text_entry3.insert(0,'-- Ten Khu Vuc --')

        self.text_entry4 = Entry(self.frame)
        self.text_entry4.grid(row=4,column=1)
        self.text_entry4.insert(0,'-- Ma Khu Vuc --')

        self.text_entry1.bind('<Button>',passText)
        self.text_entry2.bind('<Button>',passText)
        self.text_entry3.bind('<Button>',passText)
        self.text_entry4.bind('<Button>',passText)

        self.Button1 =Button(self.frame, text = 'Save', width=5).grid(row=5,column=1,sticky=NW)
        self.Button2 =Button(self.frame, text = 'Cancel', command=lambda :self.cancel()).grid(row=5,column=1,sticky=E)
    def cancel(self):
        self.master.destroy()