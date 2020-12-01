from pystray import MenuItem as MenuItem
from tkinter import messagebox, ttk
from PIL.ImageTk import PhotoImage
from tkinter import messagebox
from PIL import Image, ImageTk
from sqlite3 import Error
import crudDeviceFromDB
from tkinter import *
import MyVideoCapture
import PIL.ImageTk
import cut_frame
import threading
import PIL.Image
import datetime
import sqlite3
import tkinter
import atexit
import frame
import time
import cv2
import os
import globals
import Facial_detectIMG
from face_recog import encode_faces
import ExtractFrame	

# rtsp://admin:Vietnam@3i@117.6.131.222:6969
# rtsp://admin:ADMIN123@117.6.131.222:6968

BASIC_DIR = 'CamAI.db'
conn = sqlite3.connect(BASIC_DIR)
atexit.register(conn.close) 
class App(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        icon = PhotoImage(file='icons/icon-small.png')
        master.tk.call('wm', 'iconphoto', master._w, icon)
        self.connection = conn
        self.cur = conn.cursor()
        self.init_window()
        self.inforCam()
        # self.updat_info()
        
        
    def init_window(self):
        self.master.title('cam magic eye')
        self.pack(fill=BOTH, expand=True, )

        self.ws = self.winfo_screenwidth()
        self.hs = self.winfo_screenheight()
        print(self.ws)
        globals.ws = self.winfo_screenwidth()
        globals.hs = self.winfo_screenheight()
        globals.extract=0
        #self.master.maxsize()
        root.state('zoomed')

        # open video source (by default this will try to open the computer webcam)
        # Create a form template
        # Top Frame 		
        ## Header
        self.headerTOP = Frame(self)
        self.headerTOP.pack(fill=X)
        ## Menu Bar
        self.menuBar = Menu(self.master)
        self.trainMenu = Menu(self.menuBar, tearoff=0)
        self.master.config(menu=self.menuBar)
        
        self.menuBar.add_command(label="Add Face", command=encode_faces.initUI)
        self.menuBar.add_cascade(label="Train", menu=self.trainMenu)
        self.trainMenu.add_command(label="Train New Faces", command=encode_faces.trainNewFaces)
        self.trainMenu.add_command(label="Train All", command=encode_faces.trainAll)
        self.menuBar.add_command(label="Detect and Write", command=Facial_detectIMG.run)
        self.menuBar.add_command(label="Extract Frame", command=ExtractFrame.ExtractFrame)
        
        # Main frame
        # Create a canvas that can fit the above video source size
        self.frameCam = Frame(self, width=(self.ws - 200), height=(self.hs - 100))
        self.frameCam.pack(fill=X, side=LEFT)

        self.make_multip_frame()

        self.rightFrame = Frame(self, height=10, borderwidth=1, relief=FLAT)
        self.rightFrame.pack(side=TOP, anchor=NW)

        self.lbListcam = Button(self.rightFrame, text=('Device Total : 0'), relief=FLAT)
        self.lbListcam.grid(row=0, column=0, sticky=NW)
        self.btnCreateDevice = Button(self.rightFrame, text='Create A New Device', relief=GROOVE, command= lambda :self.createNewDevice())
        self.btnCreateDevice.grid(row=0, column=1, sticky=NW)
        self.btnshowinfo = Button(self.rightFrame, text='show inforCam', relief=GROOVE, command= lambda :self.showinforCamf())
        self.btnshowinfo.grid(row=0, column=2, sticky=NW)

        # --Read Device From Database---#########################
        self.frameListCam = Frame(self, borderwidth=1, relief=GROOVE)
        self.canvasFrame = Canvas(self.frameListCam, height=300)
        self.listCam = Frame(self.canvasFrame, bg='gray5')
        # self.listCam.pack(fill=X, side=TOP, anchor=NW)
        self.scrollBar = Scrollbar(self.frameListCam, orient='vertical', command=self.canvasFrame.yview)
        self.scrollBar1 = Scrollbar(self.frameListCam,orient='horizontal', command=self.canvasFrame.xview)
        # self.scrollBar = Scrollbar(self.canvasFrame, orient='vertical', command=self.canvasFrame.yview)

        self.canvasFrame.configure(yscrollcommand=self.scrollBar.set)
        self.canvasFrame.configure(xscrollcommand=self.scrollBar1.set)
        self.scrollBar.pack(side=RIGHT, fill=Y)
        self.scrollBar1.pack(side=BOTTOM, fill=X)
        self.canvasFrame.pack(side=TOP, fill=BOTH, expand=True, anchor=NW)
        self.frameListCam.pack(side=TOP, anchor=NW, fill=BOTH)

        self.canvasFrame.create_window((4, 4), window=self.listCam, anchor=NW, tags=self.listCam)
        self.canvasFrame.bind('<Configure>',
                          lambda x: self.canvasFrame.configure(scrollregion=self.canvasFrame.bbox('all')))
        self.canvasFrame.bind('<Right>', lambda x: self.canvasFrame.xview_scroll(3, 'units'))
        self.canvasFrame.bind('<Left>', lambda x: self.canvasFrame.xview_scroll(-3, 'units'))
        self.listCam.bind('<MouseWheel>', lambda x: self.canvasFrame.yview_scroll(int(-1 * (x.delta / 40)), 'units'))
        self.intLabel = Label(self.listCam, text='Device Title', width= 24)
        self.intLabel.grid(row=0, column=1,padx=1,pady=1)
        self.intLabel = Label(self.listCam, text="Position Device", width=14)
        self.intLabel.grid(row=0, column=2, padx=1, pady =1)
        self.intLabel = Label(self.listCam, text=" ", width=12)
        self.intLabel.grid(row=0, column=3,columnspan=2, padx=1, pady =1)
        self.intLabel = Label(self.listCam, text="Device Id", width=14)
        self.intLabel.grid(row=0, column=5, padx=1, pady =1)
        self.intLabel = Label(self.listCam, text="Vendor", width=14)
        self.intLabel.grid(row=0, column=6, padx=1, pady =1)
        self.intLabel = Label(self.listCam, text="Account", width=14)
        self.intLabel.grid(row=0, column=7, padx=1, pady =1)
        self.intLabel = Label(self.listCam, text="Device Type", width=14)
        self.intLabel.grid(row=0, column=8, padx=1, pady =1)
        self.intLabel = Label(self.listCam, text="Describe", width=14)
        self.intLabel.grid(row=0, column=9, padx=1, pady =1)
        self.intLabel = Label(self.listCam, text="Status", width=14)
        self.intLabel.grid(row=0, column=10, padx=1, pady =1)

        Data = self.readfromDatabase()
        self.listDb=[]
        for index, dat in enumerate(Data):
            self.deviceTitle=StringVar()
            self.deviceTitle.set(dat[2])
            self.datalbl=Label(self.listCam,width= 24, height=2,textvariable=self.deviceTitle).grid(row=index + 1, column=1, padx=1, pady=1)

            self.devicePositon=StringVar()
            self.devicePositon.set(dat[4])
            self.datalbl=Label(self.listCam, textvariable=self.devicePositon, width=14, height=2).grid(row=index + 1, column=2, padx=1, pady=1)

            self.UpdateDevice=Button(self.listCam, text='Update', height=1, command=lambda dat=dat :(self.updateDevice(dat)))
            self.UpdateDevice.grid(row=index +1, column=3,ipady=5)

            self.delDevice=Button(self.listCam, text='Delete', height=1, command= lambda dat=dat:self.deleteDevice(dat)).grid(row=index+1, column=4, ipady=5)

            self.deviceId = StringVar()
            self.deviceId.set(dat[1])
            self.datalbl=Label(self.listCam, textvariable=self.deviceId, width=14, height=2).grid(row=index + 1, column=5, padx=1, pady=1)

            self.vendor=StringVar()
            self.vendor.set(dat[3])
            self.datalbl=Label(self.listCam, textvariable=self.vendor, width=14, height=2).grid(row=index + 1, column=6, padx=1, pady=1)

            self.account = StringVar()
            self.account.set(dat[5])
            self.datalbl=Label(self.listCam, textvariable=self.account, width=14, height=2).grid(row=index + 1, column=7, padx=1, pady=1)

            self.describe = StringVar()
            self.describe.set(dat[6])
            self.datalbl=Label(self.listCam, textvariable=self.describe, width=14, height=2).grid(row=index + 1, column=8, padx=1, pady=1)

            self.deviceType=StringVar()
            self.deviceType.set(dat[7])
            self.datalbl=Label(self.listCam, textvariable=self.deviceType, width=14, height=2).grid(row=index + 1, column=9, padx=1, pady=1)

            self.status = StringVar()
            self.status.set(dat[8])
            self.datalbl=Label(self.listCam, textvariable=self.status, width=14, height=2).grid(row=index + 1, column=10, padx=1, pady=1)

            self.listDb.append(Data)
            print(len(self.listDb))

        # ----------------- End read Device From Database---------------###########################
        self.frameOffSet = Frame(self, relief = GROOVE, borderwidth=1)
        self.Area = Canvas(self.frameOffSet, height=100)
        self.listArea = Frame(self.Area, bg='gray5',)

        self.scrollBar2 = Scrollbar(self.frameOffSet, orient='vertical', command = self.Area.yview)
        self.scrollBar2.pack(side=RIGHT, fill=Y)

        self.scrollBar3 = Scrollbar(self.frameOffSet, orient='horizontal', command=self.Area.xview)
        self.scrollBar3.pack(side=BOTTOM, fill=X)

        self.Area.configure(yscrollcommand=self.scrollBar2.set)
        self.Area.configure(xscrollcommand=self.scrollBar3.set)

        self.Area.pack(side=TOP, fill=BOTH,anchor=NW, pady=5)
        self.frameOffSet.pack(side=TOP, anchor=NW, fill = BOTH, expand=True)
        self.Area.create_window((4,4),window=self.listArea,anchor=NW,tags=self.listArea)
        self.Area.bind('<Configure>',
                              lambda x: self.Area.configure(scrollregion=self.Area.bbox('all')))
        self.Area.bind('<MouseWheel>', lambda x: self.Area.yview_scroll(int(-1 * (x.delta / 40)), 'units'))

        self.intLabel = Label(self.listArea, text='ID Khu vuc', width=10)
        self.intLabel.grid(row=0, column=1, padx=1, pady=1)
        self.intLabel = Label(self.listArea, text="Ma Camera", width=14)
        self.intLabel.grid(row=0, column=2, padx=1, pady=1)
        self.intLabel = Label(self.listArea, text="Ten Khu vuc", width=24)
        self.intLabel.grid(row=0, column=3, padx=1, pady=1)
        self.intLabel = Label(self.listArea, text="Ma Khu vuc", width=14)
        self.intLabel.grid(row=0, column=4, padx=1, pady=1)

        # ----------------------------------------------------#######################
    
    def showinforCamf(self):
        self.ShowInfoCam = Toplevel(self.listCam)
        Data = self.readfromDatabase()
        self.listDb=[]
        for index, dat in enumerate(Data):
            self.deviceTitle=StringVar()
            self.deviceTitle.set(dat[2])
            self.datalbl=Label(self.ShowInfoCam,width= 24, height=2,textvariable=self.deviceTitle).grid(row=index + 1, column=1, padx=1, pady=1)

            self.devicePositon=StringVar()
            self.devicePositon.set(dat[4])
            self.datalbl=Label(self.ShowInfoCam, textvariable=self.devicePositon, width=14, height=2).grid(row=index + 1, column=2, padx=1, pady=1)

            self.deviceId = StringVar()
            self.deviceId.set(dat[1])
            self.datalbl=Label(self.ShowInfoCam, textvariable=self.deviceId, width=14, height=2).grid(row=index + 1, column=5, padx=1, pady=1)

            self.vendor=StringVar()
            self.vendor.set(dat[3])
            self.datalbl=Label(self.ShowInfoCam, textvariable=self.vendor, width=14, height=2).grid(row=index + 1, column=6, padx=1, pady=1)

            self.account = StringVar()
            self.account.set(dat[5])
            self.datalbl=Label(self.ShowInfoCam, textvariable=self.account, width=14, height=2).grid(row=index + 1, column=7, padx=1, pady=1)

            self.describe = StringVar()
            self.describe.set(dat[6])
            self.datalbl=Label(self.ShowInfoCam, textvariable=self.describe, width=14, height=2).grid(row=index + 1, column=8, padx=1, pady=1)

            self.deviceType=StringVar()
            self.deviceType.set(dat[7])
            self.datalbl=Label(self.ShowInfoCam, textvariable=self.deviceType, width=14, height=2).grid(row=index + 1, column=9, padx=1, pady=1)

            self.status = StringVar()
            self.status.set(dat[8])
            self.datalbl=Label(self.ShowInfoCam, textvariable=self.status, width=14, height=2).grid(row=index + 1, column=10, padx=1, pady=1)

            self.listDb.append(Data)
            print(len(self.listDb))
        upload_devi.uploadDataToAPI()

    def inforCam(self):
        # Tạo frame bảng thông tin
        self.bottomRightFrame = Frame(self, relief=GROOVE, bg='gray60', borderwidth=1)
        self.bottomRightFrame.pack(side=TOP, anchor=NW, padx=2, pady=1, fill=BOTH, expand=True)

        self.lblShowInfoCam = Label(self.bottomRightFrame, text='Thông tin chi tiết', bg='gray60')
        self.lblShowInfoCam.pack(side=TOP, padx=2, pady=2)
        
        self.frameListInfo = Frame(self, borderwidth=1, relief=GROOVE)
        globals.canvasFrame = Canvas(self.frameListInfo, height=300)
        globals.listCam = Frame(globals.canvasFrame, bg='gray5',padx=1, pady =1)
        self.scrollBar = Scrollbar(self.frameListInfo, orient='vertical', command=globals.canvasFrame.yview)
        self.scrollBar1 = Scrollbar(self.frameListInfo,orient='horizontal', command=globals.canvasFrame.xview)

        globals.canvasFrame.configure(yscrollcommand=self.scrollBar.set)
        globals.canvasFrame.configure(xscrollcommand=self.scrollBar1.set)
        self.scrollBar.pack(side=RIGHT, fill=Y)
        self.scrollBar1.pack(side=BOTTOM, fill=X)
        globals.canvasFrame.pack(side=TOP, fill=BOTH, anchor=NW)
        self.frameListInfo.pack(side=TOP, anchor=NW, fill=BOTH)

        globals.canvasFrame.create_window((0, 0), window=globals.listCam, anchor=NW, tags=globals.listCam)
        globals.canvasFrame.bind('<Configure>',
                          lambda x: globals.canvasFrame.configure(scrollregion=globals.canvasFrame.bbox('all')))
        self.intLabel = Label(globals.listCam, text='Cam IP', width= 20)
        self.intLabel.grid(row=0, column=0,padx=1,pady=1)
        self.intLabel = Label(globals.listCam, text="Name", width=20)
        self.intLabel.grid(row=0, column=1, padx=1, pady =1)
        self.intLabel = Label(globals.listCam, text="Time", width=30)
        self.intLabel.grid(row=0, column=2, padx=1, pady =1)
        self.intLabel = Label(globals.listCam, text="Date", width=30)
        self.intLabel.grid(row=0, column=3, padx=1, pady =1)

    def readfromDatabase(self):
        self.cur.execute('Select * from OBE_LIST_DEVICE')
        print('Read From Database')
        print(self.cur.fetchall())
        return self.cur.fetchall()

    def createNewDevice(self):
        self.formNewDevice = Toplevel(self.rightFrame)
        guiNewDevice = crudDeviceFromDB.Create(self.formNewDevice)
        self.formNewDevice.grab_set()

    def deleteDevice(self, data_valid):
        with conn:
            dele = data_valid[0]
            messDel = messagebox.askokcancel('Warning!', 'Are you sure delete device: '+data_valid[2])
            if messDel is True:
                self.cur.execute('Delete from OBE_LIST_DEVICE where ID=?',(dele,))
                print('Deleted')
                threading.Thread(target=self.reloadDb).start()
            else:
                print('Goobye')
                
    def reloadDb(self):
        self.canvasFrame.after(1000,self.reloadDb)
        self.canvasFrame.update()
        print('refresh table')

    def updateDevice(self, data_valid):
        self.updateDevi = Toplevel(self.rightFrame)
        self.updateDevi.geometry('350x230+100+200')
        self.updateDevi.maxsize(350,200)
        self.updateDevi.title('Edit Device')
        self.updateDevi.grab_set()
        deviceTitle = data_valid[2]
        deviceId = data_valid[1]
        vendor = data_valid[3]
        positionDevice = data_valid[4]
        account = data_valid[5]
        describe = data_valid[6]
        deviceType = data_valid[7]
        status = data_valid[8]

        Label(self.updateDevi,text ='Device Title: ').grid(row=0, column=0, sticky=NW)
        Entry(self.updateDevi,textvariable=StringVar(value=deviceTitle), state='readonly').grid(row=0, column=1)
        self.newDeviceTitle = Entry(self.updateDevi)
        self.newDeviceTitle.grid(row=0, column=2)
        self.newDeviceTitle.focus()

        Label(self.updateDevi,text='Position Device: ').grid(row=1, column=0, sticky=NW)
        Entry(self.updateDevi,textvariable=StringVar(value=positionDevice), state='readonly').grid(row=1, column=1)
        self.newDevicePosition = Entry(self.updateDevi)
        self.newDevicePosition.grid(row=1, column=2)

        Label(self.updateDevi, text='Device Id: ').grid(row=2, column=0, sticky=NW)
        Entry(self.updateDevi, textvariable=StringVar(value=deviceId), state='readonly').grid(row=2, column=1)
        self.newDeviceID = Entry(self.updateDevi)
        self.newDeviceID.grid(row=2, column=2)

        Label(self.updateDevi,text='Vendor: ').grid(row=3, column=0, sticky=NW)
        Entry(self.updateDevi, textvariable=StringVar(value=vendor), state='readonly').grid(row=3,column=1)
        self.newVendor= Entry(self.updateDevi)
        self.newVendor.grid(row=3, column=2)

        Label(self.updateDevi, text='Account: ').grid(row=4, column=0, sticky=NW)
        Entry(self.updateDevi,textvariable=StringVar(value=account), state='readonly').grid(row=4, column=1)
        self.newAccount = Entry(self.updateDevi)
        self.newAccount.grid(row=4, column=2)

        Label(self.updateDevi, text='Describe: ').grid(row=5, column=0, sticky=NW)
        Entry(self.updateDevi, textvariable=StringVar(value=describe), state='readonly').grid(row=5, column=1)
        self.newDescribe = Entry(self.updateDevi)
        self.newDescribe.grid(row=5, column=2)

        Label(self.updateDevi, text='Device Type: ').grid(row=6, column=0, sticky=NW)
        Entry(self.updateDevi, textvariable=StringVar(value=deviceType), state='readonly').grid(row=6, column=1)
        self.newDeviceType = Entry(self.updateDevi)
        self.newDeviceType.grid(row=6, column=2)

        Label(self.updateDevi, text='Status: ').grid(row=7, column=0, sticky=NW)
        Entry(self.updateDevi, textvariable=StringVar(value=status), state='readonly').grid(row=7, column=1)
        self.newStatus = Entry(self.updateDevi)
        self.newStatus.grid(row=7, column=2)

        self.saveButton1=Button(self.updateDevi, text='Update', command= lambda :edit_Device(self.newDeviceTitle.get(),deviceTitle, 
            self.newDevicePosition.get(),positionDevice, self.newDeviceID.get(),deviceId, self.newVendor.get(),vendor,
            self.newAccount.get(),account, self.newDescribe.get(),describe, self.newDeviceType.get(),deviceType, 
            self.newStatus.get(),status)).grid(row=8, column=1, sticky=E)
        def edit_Device(newDeviceTitle,deviceTitle, newDevicePosition,positionDevice,newDeviceID,deviceId,newVendor,vendor,
                        newAccount,account,newDescribe,describe,newDeviceType,deviceType,newStatus,status,):
            self.cur.execute('UPDATE OBE_LIST_DEVICE '
                        'set DEVICE_TITLE=?,POSITION_DEVICE=?,DEVICE_ID=?,VENDOR=?,ACCOUNT=?,DESCRIBE=?,DEVICE_TYPE=?,STATUS=?'
                        'WHERE DEVICE_TITLE=? AND POSITION_DEVICE=? AND DEVICE_ID=? AND VENDOR=? AND ACCOUNT=? '
                        'AND DESCRIBE=?AND DEVICE_TYPE=? AND STATUS=?',
                        (newDeviceTitle,newDevicePosition,newDeviceID,newVendor,
                         newAccount,newDescribe,newDeviceType,newStatus, deviceTitle,positionDevice,deviceId ,vendor,account,describe,deviceType,status))
            self.cur.fetchall()
            conn.commit()
            print('Updated')
            self.updateDevi.destroy()

    def make_multip_frame(self):
        self.vid = []
        arrange_cam = [0, 0, 0, 1, 0, 2, 0, 3, 1, 0, 1, 1, 1, 2, 1, 3, 2, 0, 2, 1, 2, 2, 2, 3, 3, 0, 3, 1, 3, 2, 3, 3]
        for x in range(0, 16):
            y = x * 2
            if x<16:
                self.vid.append(threading.Thread(target=frame.frame,
                                                 args=(None, self.frameCam, self.ws, self.hs, arrange_cam[y],arrange_cam[y + 1], x)))
                self.vid[x].start()
        else:
            self.vid.append(frame.frame(None, self.frameCam, self.ws, self.hs, arrange_cam[y], arrange_cam[y + 1], x))


    def setting(self):
        btnSettingApp = tkinter.Toplevel(self)
        # self.master.title("Setting cam")
        self.pack(fill=BOTH, expand=True)

        self.frame1 = Frame(btnSettingApp, self)
        self.frame1.pack(fill=X)

        self.lbl1 = Label(self.frame1, text="Counter", width=8)
        self.lbl1.pack(side=LEFT, padx=5, pady=5)

        self.toggle1 = Button(self.frame1, text="On", command=self.convert1)
        self.toggle1.pack(side=RIGHT, padx=10, pady=10)

        self.frame2 = Frame(btnSettingApp, self)
        self.frame2.pack(fill=X)

        self.lbl2 = Label(self.frame2, text="Recognition", width=10)
        self.lbl2.pack(side=LEFT, padx=5, pady=5)

        self.toggle2 = Button(self.frame2, text="On", command=self.convert2)
        self.toggle2.pack(side=RIGHT, padx=10, pady=10)

        self.frame3 = Frame(btnSettingApp, self)
        self.frame3.pack(fill=X)

        self.toggle3 = Button(self.frame3, text="Close cam")
        self.toggle3.pack(side=RIGHT, padx=10, pady=10)

    def convert1(self, tog=[0]):
        tog[0] = not tog[0]
        if tog[0]:
            self.toggle1.config(text='On')
        else:
            self.toggle1.config(text='Off')

    def convert2(self, tog=[0]):

        tog[0] = not tog[0]
        if tog[0]:
            self.toggle2.config(text='On')
        else:
            self.toggle2.config(text='Off')
        # -------------------------------

    def popupMenu(self, event):
        menu = Menu(self.frameCam, tearoff=0)
        menu.add_command(label='Add Camera', command=self.addCam)
        menu.add_command(label='Setting', command=self.settingApp)
        menu.add_command(label='Destroy cam', command=self.on_quitCam)

        menu.post(event.x_root, event.y_root)


    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)

    def on_quitCam(self):
        pass

    def addCamToFame(self):
        pass
        # self.vid[0] = MyVideoCapture(int(self.entry1.get()))
        if self.entry1.get() == "0" or self.entry1.get() == "1":
            self.vid[int(self.entry2.get()) - 1].set_cam(int(self.entry1.get()))
            self.time_in.set('Time in : ' + str(datetime.datetime.now()))
        else:
            self.vid[int(self.entry2.get()) - 1].set_cam(self.entry1.get())
            self.time_in.set('Time in : ' + str(datetime.datetime.now()))

    def addCam(self):
        self.btnAddCam = tkinter.Toplevel(self)
        self.pack(fill=BOTH, expand=True)
        self.btnAddCam.grab_set()

        self.frame1 = Frame(self.btnAddCam, self)
        self.frame1.pack(fill=X)

        self.lbl1 = Label(self.frame1, text="IP or Num Cam", width=15)
        self.lbl1.pack(side=LEFT, padx=5, pady=5)

        self.entry1 = Entry(self.frame1)
        self.entry1.insert(0, "0")
        self.entry1.pack(fill=X, padx=5, expand=True)

        self.frame2 = Frame(self.btnAddCam, self)
        self.frame2.pack(fill=X)

        self.lbl2 = Label(self.frame2, text="Location Display", width=15)
        self.lbl2.pack(side=LEFT, padx=5, pady=5)

        self.entry2 = Entry(self.frame2)
        self.entry2.insert(0, "1")
        self.entry2.pack(fill=X, padx=5, expand=True)

        self.frame3 = Frame(self.btnAddCam, self)
        self.frame3.pack(fill=X)

        self.lbl3 = Label(self.frame3, text="Password", width=15)
        self.lbl3.pack(side=LEFT, padx=5, pady=5)

        self.entry3 = Entry(self.frame3)
        self.entry3.pack(fill=X, padx=5, expand=True)

        self.saveButton = Button(self.btnAddCam, text="Save", command=self.addCamToFame)
        self.saveButton.pack(side=RIGHT, padx=5, pady=5)

    def get_vid(self, num):
        self.btnAddCam = tkinter.Toplevel(self)
        self.pack(fill=BOTH, expand=True)

        self.frame1 = Frame(self.btnAddCam, self)
        self.frame1.pack(fill=X)

        self.lbl1 = Label(self.frame1, text="IP or Num Cam", width=15)
        self.lbl1.pack(side=LEFT, padx=5, pady=5)

        self.entry_vid = Entry(self.frame1)
        self.entry_vid.pack(fill=X, padx=5, expand=True)

        self.saveButton = Button(self.btnAddCam, text="Save", command=self.addCamToFame)
        self.saveButton.pack(side=RIGHT, padx=5, pady=5)

    def vid(self, num):
        self.vid[int(num)].set_cam(MyVideoCapture.Capture(int(self.entry_vid.get())))
        
if __name__ == '__main__':
    globals.init()
    root = Tk()
    app = App(root)
    root.mainloop()