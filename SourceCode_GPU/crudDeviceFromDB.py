from tkinter import *
import sqlite3

BASE_DIR = 'CamAI.db'

conn = sqlite3.connect(BASE_DIR)

class Create:
    def __init__(self, master):
        self.master = master
        self.master.geometry('350x230+100+200')
        self.master.maxsize(350,230)
        self.master.title('Create data')
        self.label2 = Label(self.master, text='Welcome to the data entry menu', fg='red').grid(row=0, column=0, sticky=N)
        self.label3 = Label(self.master, text='Enter Device ID: ', fg='black').grid(row=1, column=0, sticky=NW)
        self.label4 = Label(self.master, text='Enter Device Tittle: ', fg='black').grid(row=2, column=0, sticky=NW)
        self.label5 = Label(self.master, text='Enter Vendor: ', fg='black').grid(row=3, column=0, sticky=NW)
        self.label6 = Label(self.master, text='Enter Position Device: ', fg='black').grid(row=4, column=0, sticky=NW)
        self.label7 = Label(self.master, text='Enter Account: ', fg='black').grid(row=5, column=0, sticky=NW)
        self.label8 = Label(self.master, text='Enter Describe: ', fg='black').grid(row=6, column=0, sticky=NW)
        self.label9 = Label(self.master, text='Enter Device Type: ', fg='black').grid(row=7, column=0, sticky=NW)
        self.labe20 = Label(self.master, text='Enter Status: ', fg='black').grid(row=8, column=0, sticky=NW)

        self.DeviceID = StringVar()
        self.text_entry = Entry(self.master, textvariable=self.DeviceID, width=27).grid(row=1, column=1)

        self.DeviceTittle = StringVar()
        self.text_entry = Entry(self.master, textvariable=self.DeviceTittle, width=27).grid(row=2, column=1)

        self.Vendor = StringVar()
        self.text_entry = Entry(self.master, textvariable=self.Vendor, width=27).grid(row=3, column=1)

        self.PositionDevice = StringVar()
        self.text_entry = Entry(self.master, textvariable=self.PositionDevice, width=27).grid(row=4, column=1)

        self.Account = StringVar()
        self.text_entry = Entry(self.master, textvariable=self.Account, width=27).grid(row=5, column=1)

        self.Describe = StringVar()
        self.text_entry = Entry(self.master, textvariable=self.Describe, width=27).grid(row=6, column=1)

        self.DeviceType = StringVar()
        self.text_entry = Entry(self.master, textvariable=self.DeviceType, width=27).grid(row=7, column=1)

        self.Status = IntVar()
        self.int_entry = Entry(self.master, textvariable=self.Status, width=27).grid(row=8, column=1)

        self.button4 = Button(self.master, text="Save", fg='red',
                              command=lambda :self.savedata(self.DeviceID.get(), self.DeviceTittle.get(), self.Vendor.get(),
                                                    self.PositionDevice.get(), self.Account.get(), self.Describe.get(),
                                                    self.DeviceType.get(), self.Status.get())).grid(row=9, column=0, sticky=E)


    def savedata(self, DeviceID, DeviceTittle, Vendor, PositionDevice, Account, Describe, DeviceType, Status):
        # con = pymssql.connect('Test.db')
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO OBE_LIST_DEVICE (DEVICE_ID, DEVICE_TITLE,VENDOR,POSITION_DEVICE,ACCOUNT,DESCRIBE,DEVICE_TYPE, STATUS) VALUES (?,?,?,?,?,?,?,?)',
            (DeviceID, DeviceTittle, Vendor, PositionDevice, Account, Describe, DeviceType, Status))
        conn.commit()
        # Read.readfromDatabase()
        print('Record inserted in Data')
        self.master.destroy()
class Read:
    cur = conn.cursor()

    def readfromDatabase(self):
        self.cur.execute('Select * from OBE_LIST_DEVICE')
        return self.cur.fetchall()
class UpdateDevice:
  pass