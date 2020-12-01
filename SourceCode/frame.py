import MyVideoCapture
import tkinter
import cv2
import PIL
import cut_frame
import threading
from face_recog.Facial_counter_SG import *
import win32api

check = False
class frame(object):
    def __init__(self, vid, frameCam, ws, hs, x, y, num):
        self.frameCam = frameCam
        self.ws = ws
        self.hs = hs
        self.x = x
        self.y = y
        self.vid = vid
        self.num = num
        self.face = Face()
        self.width=((self.ws - 780) / 4)
        self.height=((self.hs - 100) / 4)

        self.cam = tkinter.Canvas(self.frameCam, width=((self.ws - 780) / 4), 
            height=((self.hs - 100) / 4), bg="black")
        self.cam.place(x=0, y=0)
        self.test=0

        img = PIL.Image.open('icons/icon-cam.png')
        img = img.resize((50,50), PIL.Image.ANTIALIAS)
        self.photo = PIL.ImageTk.PhotoImage(img)
        self.cam.create_image(((self.ws - 780) / 8) - (50 / 2), ((self.hs - 100) / 8) - (50 / 2), 
            image = self.photo, anchor = tkinter.NW)
        
        self.double_click_flag = False
        self.checkshown = 0
        self.face_recogizer_acti=0

        try:
            self.iconShowCam = PIL.ImageTk.PhotoImage(file='icons/showCam.png')
            self.iconSettingCam = PIL.ImageTk.PhotoImage(file='icons/off-icon.png')
            self.iconDestroyCam = PIL.ImageTk.PhotoImage(file='icons/destroyCam.png')
            self.iconAddCam = PIL.ImageTk.PhotoImage(file='icons/on-addCam.png')
        except:
            print("Error : Do not read the file Image *.png on class frame")

        self.menuCam = tkinter.Menu(self.cam, tearoff=0)
        self.menuCam.add_command(label='Add Cam', command=lambda: 
            self.addcam(), underline=0, compound='left', image=self.iconAddCam)
        self.menuCam.add_command(label='Show', underline=0, command=lambda: 
            self.example_show(), compound='left', image=self.iconShowCam)
        self.menuCam.add_command(label='Edit', underline=0, command=lambda: 
            self.edit(), compound='left', image=self.iconShowCam)
        self.menuCam.add_command(label='Setting Camera', command=lambda: 
            self.settingApp(),compound='left', image=self.iconSettingCam)
        self.menuCam.add_command(label='Đếm số lượng người', command=lambda: 
            self.face_recognizer(), compound='left', image=self.iconSettingCam)
        self.menuCam.add_command(label='Nhận Diện Biển số xe ', command=lambda: 
            self.license_plate_recognizer(), underline=0, compound='left', image=self.iconSettingCam)
        self.menuCam.add_command(label='Tắt Cam', command=lambda: 
            self.destroy_Cam(), underline=0, compound='left', image=self.iconDestroyCam)    

        self.cam.bind('<Button-1>', self.mouse_click) # bind left mouse click
        self.cam.bind('<Double-1>', self.double_click) # bind double left clicks
        self.cam.bind('<Button-3>', self.popup)         #bind right clicks
        self.cam.grid(row=self.x, column=self.y)

    def popup(self, event):
        self.menuCam.post(event.x_root, event.y_root)

    def mouse_click(self, event):
        self.cam.after(300, self.mouse_action, event)

    def double_click(self, event):
        self.double_click_flag = True

    def mouse_action(self, event):
        # global double_click_flag
        if self.double_click_flag:
            print('double mouse click event')
            # self.show()
            self.double_click_flag = False
        else:
            print('single mouse click event')

    def edit(self):
        pass

    def set_cam(self):
        if self.entry.get().isdigit():
            self.vid = MyVideoCapture.Capture(int(self.entry.get()))
        else:
            self.vid = MyVideoCapture.Capture(self.entry.get())
        self.update()
        self.AddCam.destroy()

    def addcam(self):
        self.AddCam = tkinter.Toplevel()
        L1 = tkinter.Label(self.AddCam, text="IP CAM")
        L1.pack( side = tkinter.LEFT)
        self.entry = tkinter.Entry(self.AddCam, bd =5)
        self.entry.insert(0,"0")
        self.entry.pack(side = tkinter.LEFT)
        tkinter.Button(self.AddCam, text="Save", command=self.set_cam).pack()

    def example_show(self):
        self.th = threading.Thread(target=cut_frame.ExampleApp, args=(self.vid, self.frameCam, self.ws, self.hs))
        self.th.start()
    
    def face_recognizer(self):
        self.face_recogizer_acti=not(self.face_recogizer_acti)

    def license_plate_recognizer(self):
        self.th = threading.Thread(target=cut_frame.ShowLicensePlateRecognition, args=(self.vid, self.frameCam, self.ws, self.hs))
        self.th.start()

    def settingApp(self):
        cut_frame.control(self.vid)
        pass

    def update(self):
        if self.vid != None:
            if check:
                self.cam.after(10, self.update)
            else:
                frame = self.vid.get_frame()
                if self.face_recogizer_acti==1:
                    self.face.run(frame)
                
                frame1 = cv2.resize(frame, (int(((self.ws - 780) / 4)),int(((self.hs - 100) / 4))))  
                frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
                self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame1))
                self.cam.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
                self.cam.after(10, self.update)
        else:
            img = PIL.Image.open('icons/icon-cam.png')
            img = img.resize((50,50), PIL.Image.ANTIALIAS)
            self.photo = PIL.ImageTk.PhotoImage(img)
            self.cam.create_image(((self.ws - 780) / 8) - (50 / 2), ((self.hs - 100) / 8) - (50 / 2), image = self.photo, anchor = tkinter.NW)

    def destroy_Cam (self):
        # message box display
        if tkinter.messagebox.askokcancel("Close", "Do you want to close Camera?"):
            if self.vid != None:
                self.vid = None
                cv2.destroyAllWindows()
                self.face_recogizer_acti=0
                self.checkshown = 0