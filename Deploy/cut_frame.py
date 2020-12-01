from license_plate_recognition.Plate import *
from face_recog.Facial_counter_SG import *
# import Facial_counter_SG
# from Facial_counter_SG import *
import addFrameOffSet
import PIL
import tkinter
import cv2
import frame
import time
import os
import moviepy
from moviepy.video.io.VideoFileClip import VideoFileClip
import threading
import globals
import json

class Show(object):
    
    def __init__(self, vid, frameCam, ws, hs):
        self.frameCam = frameCam
        self.ws = ws
        self.hs = hs
        self.canvas = tkinter.Canvas(self.frameCam, width=self.ws, height=self.hs, bg="black")
        self.lmain=tkinter.Label(self.frameCam)
        self.lmain.grid(row=0, column=0)
        self.x = self.y = 0
        self.x_mouse = self.y_mouse = 0
        self.adress = []
        self.vid = vid

        self.canvas.place(x=0, y=0)
        self.Display_frame = False

        self.menuCam = tkinter.Menu(self.canvas, tearoff=0)
        self.menuCam.add_command(label='Add', command=lambda: self.add(), underline=0, compound='left')

        self.menuCam.add_command(label='Display frame', command=lambda: self.Display_framef(), underline=0, compound='left')

        self.menuCam.add_command(label='Delete All', command=lambda: self.Delete_Allf(), underline=0, compound='left')

        self.menuCam.add_command(label='Back', command=lambda: self.back_home(), underline=0, compound='left')

        self.canvas.bind('<Motion>', self.motion)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind('<Button-3>', self.popup)

        self.double_click_flag = False

        self.a = [0, 0, 0, 0]

        self.rect = None
        self.start_x = None
        self.start_y = None

    def rectang(self, rec1, rec2):
        
        if  not self.check_in_box(rec1[0], rec1[1], rec2[0], rec2[1], rec2[2], rec2[3]):
            if not self.check_in_box(rec1[0], rec1[3], rec2[0], rec2[1], rec2[2], rec2[3]):
                if not self.check_in_box(rec1[2], rec1[1], rec2[0], rec2[1], rec2[2], rec2[3]):
                    if not self.check_in_box(rec1[2], rec1[3], rec2[0], rec2[1], rec2[2], rec2[3]):
                        if not self.check_in_box(rec2[0], rec2[1], rec1[0], rec1[1], rec1[2], rec1[3]):
                            if not self.check_in_box(rec2[0], rec2[3], rec1[0], rec1[1], rec1[2], rec1[3]):
                                if not self.check_in_box(rec2[2], rec2[1], rec1[0], rec1[1], rec1[2], rec1[3]):
                                    if not self.check_in_box(rec2[2], rec2[3], rec1[0], rec1[1], rec1[2], rec1[3]):
                                        return False
        return True

    def check_in_box(self, x_m, y_m, x1, y1, x2, y2):
        if (x_m > x1 and x_m < x2 and y_m > y1 and y_m < y2):
            return True
        else:
            return False

    def motion(self, event):
        self.x_mouse, self.y_mouse = event.x, event.y

    def Delete_Allf(self):
        self.adress = []
        cv2.destroyAllWindows()

    def Display_framef(self):
        if self.Display_frame == False:
            self.Display_frame = True
            pass
        else:
            cv2.destroyAllWindows()
            self.Display_frame = False

    def add(self):
        self.name_frame = addFrameOffSet.settingOffset(Toplevel(self.canvas))
        self.adress.append(self.a[0])
        self.adress.append(self.a[1])
        self.adress.append(self.a[2])
        self.adress.append(self.a[3])

    def popup(self, event):
        i = 0
        for x in range(1,int((len(self.adress) / 4) + 1)):
            if self.check_in_box(self.x_mouse, self.y_mouse, self.adress[(x * 4) - 4], self.adress[(x * 4) - 3], self.adress[(x * 4) - 2], self.adress[(x * 4) - 1]):
                i=1
                break
        if i == 1:
            self.setting(event.x_root, event.y_root)
        else:
            self.menuCam.post(event.x_root, event.y_root)

    def on_button_press(self, event):
        # save mouse drag start position
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)

        # create rectangle if not yet exist
        if not self.rect:
            self.rect = self.canvas.create_rectangle(0, 0, 1, 1, outline='red')

    def on_move_press(self, event):
        self.curX = self.canvas.canvasx(event.x)
        self.curY = self.canvas.canvasy(event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, self.curX, self.curY)

        if len(self.adress) == 0:
            self.a.append(int(self.start_x))
            self.a.append(int(self.start_y))
            self.a.append(int(self.curX))
            self.a.append(int(self.curY))
        else:
            for x in range(1,int((len(self.adress) / 4) + 1)):
                if not self.check_in_box(self.curX, self.curY, self.adress[(x * 4) - 4], self.adress[(x * 4) - 3], 
                    self.adress[(x * 4) - 2], self.adress[(x * 4) - 1]) and not self.check_in_box(self.start_x, self.start_y, self.adress[(x * 4) - 4], self.adress[(x * 4) - 3], 
                    self.adress[(x * 4) - 2], self.adress[(x * 4) - 1]) and not self.check_in_box(self.curX, self.start_y, self.adress[(x * 4) - 4], self.adress[(x * 4) - 3], 
                    self.adress[(x * 4) - 2], self.adress[(x * 4) - 1]) and not self.check_in_box(self.start_x, self.curY, self.adress[(x * 4) - 4], self.adress[(x * 4) - 3], 
                    self.adress[(x * 4) - 2], self.adress[(x * 4) - 1]):
                    if not self.check_in_box(self.adress[(x * 4) - 4], self.adress[(x * 4) - 3], self.start_x, self.start_y, 
                        self.curX, self.curY) and not self.check_in_box(self.adress[(x * 4) - 2], self.adress[(x * 4) - 1], self.start_x, self.start_y, 
                        self.curX, self.curY) and not self.check_in_box(self.adress[(x * 4) - 4], self.adress[(x * 4) - 1], self.start_x, self.start_y, 
                        self.curX, self.curY) and not self.check_in_box(self.adress[(x * 4) - 2], self.adress[(x * 4) - 3], self.start_x, self.start_y, self.curX, self.curY):
                        self.a.append(int(self.start_x))
                        self.a.append(int(self.start_y))
                        self.a.append(int(self.curX))
                        self.a.append(int(self.curY))

        if len(self.a) > 3:
            self.a = self.a[-4:]
            pass

    def setting(self, x_root, y_root):
        self.btnSettingApp = tkinter.Toplevel()
        self.btnSettingApp.geometry('%dx%d+%d+%d' % (150, 150, x_root, y_root))

        self.name_frame = Label(self.btnSettingApp, text="name", width=8)
        self.name_frame.grid(row=0, column=0)

        self.entry = Entry(self.btnSettingApp, bd =5)
        self.entry.grid(row=0 ,column=1)

        self.lbl1 = Label(self.btnSettingApp, text="Counter", width=8)
        self.lbl1.grid(row=1, column=0)

        self.toggle1 = Button(self.btnSettingApp, text="Off", command=self.convert1, width=5)
        self.toggle1.grid(row=1, column=1)

        self.lbl2 = Label(self.btnSettingApp, text="Recognition", width=10)
        self.lbl2.grid(row=2, column=0)

        self.toggle2 = Button(self.btnSettingApp, text="Off", command=self.Recognitionf, width=5)
        self.toggle2.grid(row=2, column=1)

        self.toggle3 = Button(self.btnSettingApp, text="back")
        self.toggle3.grid(row=3, column=1)

    def convert1(self, tog=[0]):
        tog[0] = not tog[0]
        if tog[0]:
            self.toggle1.config(text='On')
        else:
            self.toggle1.config(text='Off')

    def back_home(self):
        self.canvas.destroy()
        frame.check = not frame.check

    def Recognitionf(self, tog=[0]):

        tog[0] = not tog[0]
        if tog[0]:
            self.toggle2.config(text='On')

        else:
            self.toggle2.config(text='Off')


class ShowFaceRecognition(Show):
    
    def __init__(self, vid, frameCam, ws, hs):
        super().__init__(vid, frameCam, ws, hs)
        frame.check = not frame.check
        self.face = Face()
        self.update_face()

    def update_face(self):
        if self.vid != None:
            frame = self.vid.get_frame()
            self.face.run(frame)
            # frame = imutils.resize(frame, width=600)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0,0, image = self.photo, anchor = tkinter.NW)
            self.canvas.after(10, self.update_face)


class ShowLicensePlateRecognition(Show):
    def __init__(self, vid, frameCam, ws, hs):
        super().__init__(vid, frameCam, ws, hs)
        frame.check = not frame.check
        self.update_license()

    def update_license(self):
        if self.vid != None:
            self.frame = self.vid.get_frame()
            run(self.frame)
            # frame = imutils.resize(frame, width=600)
            self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.frame))
            self.canvas.create_image(0,0, image = self.photo, anchor = tkinter.NW)
            self.canvas.after(10, self.update_license) 


class ExampleApp(Show):
    def __init__(self, vid, frameCam, ws, hs):
        super().__init__(vid, frameCam, ws, hs)
        frame.check = not frame.check
        self.updatef()

    def updatef(self):
        if self.vid != None:
            self.frame = self.vid.get_frame()
            # self.frame = imutils.resize(self.frame, width=1000)
            try:
                self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.frame))
                self.canvas.create_image(0,0, image = self.photo, anchor = tkinter.NW)
                self.canvas.after(100, self.updatef)
            except:
                pass
class exportVideo(object):
    """docstring for ClassName"""
    def __init__(self, paIn, entryVidFrom, entryVidTo, date_create, fps,right_videoFrame,rightcanvas2,ws, hs):
        self.paIn, self.entryVidFrom, self.entryVidTo,self.date_create,self.fps,self.right_videoFrame=paIn, entryVidFrom, entryVidTo, date_create, fps,right_videoFrame
        self.ws=ws
        self.hs=hs
        self.rightcanvas2=rightcanvas2

        paVid=os.path.normpath(self.paIn+os.sep+os.pardir)
        paVid=os.path.join(paVid,"Extracted video")
        if not os.path.exists(paVid):
            os.makedirs(paVid)
        else:
            for f in os.listdir(paVid):
                os.remove(os.path.join(paVid, f))

        if self.entryVidFrom.get().isdigit():      #Entry form 1: 20 (in second of duration)
            startFrom=int(self.entryVidFrom.get()) #Get the corresponding index of frame
        else:                                   #Entry form 2: 11:20:30 (in hour:minute:second)
            entrylistFrom=(self.entryVidFrom.get()).split(":")
            if len(entrylistFrom)==2:
                entrylistFrom.append("0")
                #Convert to form 1
            temp=self.date_create.split()
            for value in temp:
                if len(value)==8:
                    temp=value
            
            temp=temp.split(":")
            a=[0]*len(temp)
            for i in range(0,len(temp)):
                a[i]=-int(temp[i])+int(entrylistFrom[i])
            startFrom=a[0]*3600+a[1]*60+a[2]

        if self.entryVidTo.get().isdigit():      #Entry form 1: 20 (in second of duration)
            endTo=int(self.entryVidTo.get()) #Get the corresponding index of frame
        else:                                   #Entry form 2: 11:20:30 (in hour:minute:second)
            entrylistTo=(self.entryVidTo.get()).split(":")
            if len(entrylistTo)==2:
                entrylistTo.append("0")
            #Convert to form 1
            temp=self.date_create.split()
            for value in temp:
                if len(value)==8:
                    temp=value
            
            temp=temp.split(":")

            b=[0]*len(temp)
            for i in range(0,len(temp)):
                b[i]=-int(temp[i])+int(entrylistTo[i])
            endTo=b[0]*3600+b[1]*60+b[2]

        video = VideoFileClip(self.paIn).subclip(startFrom,endTo)
        # result = CompositeVideoClip([video]) # Overlay text on video
        owd = os.getcwd()
        os.chdir(paVid)
        video.write_videofile("extracted_video.mp4".format(startFrom,endTo),fps=self.fps)
        os.chdir(owd)
        paVid= os.path.join(paVid,"extracted_video.mp4")
        self.cap = cv2.VideoCapture(paVid)
        
        self.th = threading.Thread(target=extractVideoShow, args=(self.cap, self.right_videoFrame,self.rightcanvas2,self.ws,self.hs))
        self.th.start()

class exportVideoJSON(object):
    """docstring for ClassName"""
    def __init__(self, paIn, entryDelta, date_create, fps,right_videoFrame,rightcanvas2,ws, hs):
        self.paIn,self.entryDelta,self.date_create,self.fps,self.right_videoFrame,self.ws,self.hs=paIn, entryDelta, date_create, fps,right_videoFrame,ws, hs
        self.rightcanvas2=rightcanvas2
        #Create path to save video
        paVid=os.path.normpath(self.paIn+os.sep+os.pardir)
        paVid=os.path.join(paVid,"Extracted video")        
        if not os.path.exists(paVid):
            os.makedirs(paVid)
        else:
            for f in os.listdir(paVid):
                os.remove(os.path.join(paVid, f))

        temp=self.date_create.split()
        for value in temp:
            if len(value)==8:
                temp=value
            
        temp=temp.split(":")
        
        if self.entryDelta.get().isdigit():
            self.Delta=int(self.entryDelta.get())

        self.Id,self.Time=self.jsonAnalyze()

        for i in range(0,len(self.Time)):
            time=self.Time[i]
            time=time.split(':')
            b=[0]*len(temp)
            for u in range(0,len(temp)):
                b[u]=int(time[u])-int(temp[u])
            timeSECOND=b[0]*3600+b[1]*60+b[2]

            start=int((timeSECOND-self.Delta))
            end=int((timeSECOND+self.Delta))

            video = VideoFileClip(self.paIn).subclip(start,end)
            
            owd = os.getcwd()
            os.chdir(paVid)
            vidName="id{}_{}_{}.mp4".format(self.Id[i],start,end)
            video.write_videofile(vidName,fps=self.fps)
            os.chdir(owd)
            paVid= os.path.join(paVid,vidName)
            self.cap = cv2.VideoCapture(paVid)
            
            self.th = threading.Thread(target=extractVideoShow, args=(self.cap, self.right_videoFrame,self.rightcanvas2,self.ws,self.hs))
            self.th.start()


    def jsonAnalyze(self):
        with open("test.json", "r") as read_file:
            # data = read_file.read()
            data=json.load(read_file)
        Id=[]
        Time=[]
        for i in range(0,len(data)):
            if data[i]['Speed']==0:
                Id.append(data[i]['id'])
                Time.append(data[i]['Time'][-8:])
        return(Id,Time)


class ExtractFrame(object):
    """docstring for ExtractFrame30s"""
    def __init__(self, paIn, entryFrom, entryTo,date_create, fps,rightcanvas1):
        # super().__init__(paIn, entryFrom, entryTo, date_create, fps)
        self.paIn,self.entryFrom,self.entryTo,self.date_create,self.fps,self.rightcanvas1 = paIn, entryFrom, entryTo, date_create, fps,rightcanvas1

        pa30=os.path.normpath(self.paIn + os.sep + os.pardir)    
        pa30= os.path.join(pa30,"ExtractFrame")
        if not os.path.exists(pa30):
            os.makedirs(pa30)
        else:
            for f in os.listdir(pa30):
                os.remove(os.path.join(pa30, f))

        if self.entryFrom.get().isdigit():      #Entry form 1: 20 (in second of duration)
            startFrom=int(self.entryFrom.get()) #Get the corresponding index of frame
        else:                                   #Entry form 2: 11:20:30 (in hour:minute:second)
            entrylistFrom=(self.entryFrom.get()).split(":")
            if len(entrylistFrom)==2:
                entrylistFrom.append("0")
                    #Convert to form 1
        temp=self.date_create.split()
        for value in temp:
            if len(value)==8:
                temp=value
            
        temp=temp.split(":")
        a=[0]*len(temp)
        for i in range(0,len(temp)):
            a[i]=-int(temp[i])+int(entrylistFrom[i])
            startFrom=a[0]*3600+a[1]*60+a[2]

        if self.entryTo.get().isdigit():      #Entry form 1: 20 (in second of duration)
            endTo=int(self.entryTo.get()) #Get the corresponding index of frame
        else:                                   #Entry form 2: 11:20:30 (in hour:minute:second)
            entrylistTo=(self.entryTo.get()).split(":")
            if len(entrylistTo)==2:
                entrylistTo.append("0")
                #Convert to form 1
        temp=self.date_create.split()
        for value in temp:
            if len(value)==8:
                temp=value
            
        temp=temp.split(":")
        b=[0]*len(temp)
        for i in range(0,len(temp)):
            b[i]=-int(temp[i])+int(entrylistTo[i])
        endTo=b[0]*3600+b[1]*60+b[2]
        
        startFrame=int(self.fps*startFrom)
        endFrame=int(self.fps*endTo)
        
        cap = cv2.VideoCapture(self.paIn)
        count = -1
        a=0
        while (cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:
                count += 1
                if count in range(startFrame,endFrame+1):
                    pa30Im=os.path.join(pa30, "frame{:d}.jpg".format(count))
                    cv2.imwrite(pa30Im, frame)
                    if count==startFrame:
                        img = PIL.Image.open(pa30Im)
                        img = img.resize((220,200), PIL.Image.ANTIALIAS)
                        self.photo = PIL.ImageTk.PhotoImage(img)
                        self.rightcanvas1.create_image(5, 5, image = self.photo, anchor = tkinter.NW)
                    if count==int(0.5*(startFrame+endFrame)):
                        img1 = PIL.Image.open(pa30Im)
                        img1 = img1.resize((220,200), PIL.Image.ANTIALIAS)
                        self.photo1 = PIL.ImageTk.PhotoImage(img1)
                        self.rightcanvas1.create_image(230, 5, image = self.photo1, anchor = tkinter.NW)
                    if count==endFrame:
                        img2 = PIL.Image.open(pa30Im)
                        img2 = img2.resize((220,200), PIL.Image.ANTIALIAS)
                        self.photo2 = PIL.ImageTk.PhotoImage(img2)
                        self.rightcanvas1.create_image(455, 5, image = self.photo2, anchor = tkinter.NW)
        cap.release()

class ExtractFrameJSON(object):
    """docstring for ExtractFrame30s"""
    def __init__(self, paIn,entryDelta,date_create, fps,rightcanvas1):
        self.paIn,self.entryDelta,self.date_create,self.fps,self.rightcanvas1=paIn,entryDelta,date_create, fps,rightcanvas1

        #Creat path to save image
        pa30=os.path.normpath(self.paIn + os.sep + os.pardir)
        pa30= os.path.join(pa30,"30second")
        if not os.path.exists(pa30):
            os.makedirs(pa30)
        else:
            for f in os.listdir(pa30):
                os.remove(os.path.join(pa30, f))

        temp=self.date_create.split()
        for value in temp:
            if len(value)==8:
                temp=value
            
        temp=temp.split(":")
        
        if self.entryDelta.get().isdigit():
            self.Delta=int(self.entryDelta.get())

        self.Id,self.Time=self.jsonAnalyze()

        for i in range(0,len(self.Time)):
            time=self.Time[i]
            time=time.split(':')
            b=[0]*len(temp)
            for u in range(0,len(temp)):
                b[u]=int(time[u])-int(temp[u])
            timeSECOND=b[0]*3600+b[1]*60+b[2]

            startFrame=int(self.fps*(timeSECOND-self.Delta))
            endFrame=int(self.fps*(timeSECOND+self.Delta))

            print(startFrame,endFrame)
            
            cap = cv2.VideoCapture(self.paIn)
            count=-1

            while (cap.isOpened()):
                ret, frame = cap.read()
                if ret == True:
                    count += 1
                    if count in range(startFrame,endFrame+1):
                        pa30Im=os.path.join(pa30, "id{:d}_frame{:d}.jpg".format(self.Id[i],count))
                        cv2.imwrite(pa30Im, frame)
                        if count==startFrame:
                            img = PIL.Image.open(pa30Im)
                            img = img.resize((220,200), PIL.Image.ANTIALIAS)
                            self.photo = PIL.ImageTk.PhotoImage(img)
                            self.rightcanvas1.create_image(5, 5, image = self.photo, anchor = tkinter.NW)
                        if count==int(0.5*(startFrame+endFrame)):
                            img1 = PIL.Image.open(pa30Im)
                            img1 = img1.resize((220,200), PIL.Image.ANTIALIAS)
                            self.photo1 = PIL.ImageTk.PhotoImage(img1)
                            self.rightcanvas1.create_image(230, 5, image = self.photo1, anchor = tkinter.NW)
                        if count==endFrame:
                            img2 = PIL.Image.open(pa30Im)
                            img2 = img2.resize((220,200), PIL.Image.ANTIALIAS)
                            self.photo2 = PIL.ImageTk.PhotoImage(img2)
                            self.rightcanvas1.create_image(455, 5, image = self.photo2, anchor = tkinter.NW)
            cap.release()

    def jsonAnalyze(self):
        with open("test.json", "r") as read_file:
            # data = read_file.read()
            data=json.load(read_file)
        Id=[]
        Time=[]
        for i in range(0,len(data)):
            if data[i]['Speed']==0:
                Id.append(data[i]['id'])
                Time.append(data[i]['Time'][-8:])
        return(Id,Time)

class VideoShow(object):
    def __init__(self, cap,VideoFrame,canvas,ws,hs):
        self.cap=cap
        self.canvas=canvas
        self.VideoFrame=VideoFrame
        self.ws=ws
        self.hs=hs
        # self.canvas = tkinter.Canvas(self.VideoFrame, width=self.ws, height=self.hs, bg="black")
        self.lmain=tkinter.Label(self.VideoFrame)
        self.lmain.grid(row=0, column=0)
        
        self.show_frame()
    def show_frame(self):
        ret, frame = self.cap.read()
        try:
            frame = cv2.resize(frame,(600,450))
        except:
            pass
        if ret:
            try:
                cv2image   = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                img   = PIL.Image.fromarray(cv2image)
                imgtk = PIL.ImageTk.PhotoImage(image = img)
                self.lmain.imgtk = imgtk
                self.lmain.configure(image=imgtk)
                self.lmain.after(24, self.show_frame) 
            except:
                pass
        else:
            self.cap.release()
            
class extractVideoShow(object):
    def __init__(self, cap,VideoFrame,canvas,ws,hs):
        self.cap=cap
        self.canvas=canvas
        self.VideoFrame=VideoFrame
        self.ws=ws
        self.hs=hs
        # self.canvas = tkinter.Canvas(self.VideoFrame, width=self.ws, height=self.hs, bg="black")
        self.lmain=tkinter.Label(self.VideoFrame)
        self.lmain.grid(row=0, column=0)
        
        self.show_frame()
    def show_frame(self):
        ret, frame = self.cap.read()
        try:
            frame = cv2.resize(frame, (275,225))
        except:
            pass
        if ret:
            try:
                cv2image   = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                img   = PIL.Image.fromarray(cv2image)
                imgtk = PIL.ImageTk.PhotoImage(image = img)
                self.lmain.imgtk = imgtk
                self.lmain.configure(image=imgtk)
                self.lmain.after(24, self.show_frame) 
            except:
                pass
        else:
            self.cap.release()