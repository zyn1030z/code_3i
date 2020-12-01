import cv2
import os
import tkinter
import time
import globals
import math
from tkinter import * 
from tkinter.ttk import *
import PIL
import frame
import threading
import MyVideoCapture
import cut_frame
import win32api
from PIL import Image, ImageTk
import PIL.Image, PIL.ImageTk
class ExtractFrame(object):
	def __init__(self):
		#Build interface
		self.ws=globals.ws
		self.hs=globals.hs
		self.exCount=0
		self.jsonCheck=0
		self.newWindow = tkinter.Toplevel()
		self.newWindow.state('zoomed')
		self.frameExtract = Frame(self.newWindow)
		self.frameExtract.pack(fill=BOTH)

		self.leftFrame=Frame(self.frameExtract,width=((self.ws-10)/2),height=(self.hs - 100))
		self.leftFrame.pack(side=LEFT,fill=Y,anchor=NW)

		self.rightFrame=Frame(self.frameExtract,width=((self.ws-10)/2),height=(self.hs - 100))
		self.rightFrame.pack(side=TOP,fill=BOTH)		# self.rightFrame.grid(row=0,column=1)

		self.left_topFrame=Frame(self.leftFrame,height=10)
		self.left_topFrame.pack(side=TOP,anchor=NW)

		tkinter.Label(self.left_topFrame, text="Input Video:",width=10).grid(row=0, column=1, sticky=E)
		self.entryIn= tkinter.Entry(self.left_topFrame, width=40)
		self.entryIn.grid(row=0, column=2, sticky=E)
		tkinter.Button(self.left_topFrame,text='Browse',command=self.browsefucnction).grid(row=0,column=3,sticky=E)

		self.VideoFrame=Frame(self.leftFrame,width=600, height=450)
		self.VideoFrame.pack(side=TOP,fill=X)

		self.canvas = tkinter.Canvas(self.VideoFrame,width=600, height=450, bg="gray50")
		self.canvas.place(relx=0, rely=0)

		self.left_infoFrame=Frame(self.leftFrame,width=((self.ws-10)/2),borderwidth=1)
		self.canvasFrame = Canvas(self.left_infoFrame, height=300)
		self.listInfo = Frame(self.canvasFrame)
		
		self.size=StringVar()
		self.size.set('')
		self.labelSize=tkinter.Label(self.listInfo,text="Size:",width=10, borderwidth=2, relief="groove")
		self.labelSize.grid(row=0,column=0,padx=1,pady=1)
		self.labelSize1=tkinter.Label(self.listInfo,textvariable=self.size,width=10)
		self.labelSize1.grid(row=0,column=1,padx=1,pady=1)
		
		self.dur=StringVar()
		self.dur.set('')
		self.labelDuration=tkinter.Label(self.listInfo,text="Duration:",width=10, borderwidth=2, relief="groove")
		self.labelDuration.grid(row=1,column=0,padx=1,pady=1)
		self.labelDuration1=tkinter.Label(self.listInfo,textvariable=self.dur,width=10)
		self.labelDuration1.grid(row=1,column=1,padx=1,pady=1)

		self.start=StringVar()
		self.start.set('')
		self.intLabel=tkinter.Label(self.listInfo, text="From",width=10, borderwidth=2, relief="groove")
		self.intLabel.grid(row=2,column=0,padx=1,pady=1)
		self.intLabel1=tkinter.Label(self.listInfo, textvariable=self.start,width=10)
		self.intLabel1.grid(row=2,column=1,padx=1,pady=1)

		self.end=StringVar()
		self.end.set('')
		self.intLabel2=tkinter.Label(self.listInfo, text="To",width=10, borderwidth=2, relief="groove")
		self.intLabel2.grid(row=2,column=2,padx=1,pady=1)
		self.intLabel3=tkinter.Label(self.listInfo, textvariable=self.end,width=10)
		self.intLabel3.grid(row=2,column=3,padx=1,pady=1)

		self.listInfo.pack(side=TOP)
		self.canvasFrame.pack(side=TOP, fill=Y, anchor=NW)
		self.left_infoFrame.pack(side=TOP, anchor=NW)

		self.right_topFrame=Frame(self.rightFrame,height=10)
		self.right_topFrame.pack(side=TOP,fill=X)

		self.imageLabel = Label(self.right_topFrame, text=('Image'),width=7)
		self.imageLabel.grid(row=0,column=0,padx=1,pady=1)

		self.right_imageFrame=Frame(self.rightFrame,width=((self.ws-10)/2),height=210)
		self.right_imageFrame.pack(side=TOP,anchor=NW,fill=X)
		
		self.right_top_videoFrame=Frame(self.rightFrame,height=10)
		self.right_top_videoFrame.pack(side=TOP,fill=X)

		self.right_videoFrame=Frame(self.rightFrame,width=(self.ws/2),height=225)
		self.right_videoFrame.pack(side=TOP,anchor=NW)

		self.videoLabel=Label(self.right_top_videoFrame,text='Video',width=7)
		self.videoLabel.grid(row=0,column=0,padx=1,pady=1)


		self.rightcanvas1 = tkinter.Canvas(self.right_imageFrame,width=(self.ws-10)/2, height=210,bg='gray')
		img = PIL.Image.open('icons/empty.jpg')
		img = img.resize((220,200), PIL.Image.ANTIALIAS)
		self.photo = PIL.ImageTk.PhotoImage(img)
		self.rightcanvas1.create_image(5, 5, image = self.photo, anchor = tkinter.NW)
		self.rightcanvas1.create_image(230, 5, image = self.photo, anchor = tkinter.NW)
		self.rightcanvas1.create_image(455, 5, image = self.photo, anchor = tkinter.NW)
		self.rightcanvas1.place(relx=0, rely=0.01)

		self.rightcanvas2=tkinter.Canvas(self.right_videoFrame,width=(self.ws-10)/2,height=225,bg='gray85')
		self.rightcanvas2.place(relx=0, rely=0)
		
		self.right_infoFrame=Frame(self.rightFrame,width=(self.ws/2))
		self.right_infoFrame.pack(side=TOP,anchor=NW)

		self.var1=IntVar()
		tkinter.Checkbutton(self.right_infoFrame,text='JSON/Input Time',variable=self.var1,command=self.activateCheck).grid(row=1,column=0)

		tkinter.Label(self.right_infoFrame,text="From").grid(row=1,column=1)
		self.entryVidFrom=tkinter.Entry(self.right_infoFrame,width=10)
		self.entryVidFrom.grid(row=1,column=2)

		tkinter.Label(self.right_infoFrame,text="To").grid(row=2,column=1)
		self.entryVidTo=tkinter.Entry(self.right_infoFrame,width=10)
		self.entryVidTo.grid(row=2,column=2)
		
		tkinter.Label(self.right_infoFrame,text='Cutting/second').grid(row=3,column=1)
		self.entryDelta=tkinter.Entry(self.right_infoFrame,width=10)
		self.entryDelta.grid(row=3,column=2)

		self.entryVidFrom.config(state=NORMAL)
		self.entryVidTo.config(state=NORMAL)
		self.entryDelta.config(state=DISABLED)
		
		tkinter.Button(self.right_infoFrame,text="Extract Image",command=self.extract30second).grid(row=4,column=0)
		tkinter.Button(self.right_infoFrame,text="Extract Video",command=self.exportVideo).grid(row=4,column=1)
		
		

	def browsefucnction(self):
		self.entryIn.delete(0, 'end')
		filename = filedialog.askopenfilename()
		self.entryIn.insert(0,filename)
		self.displayVideo()
	
	def activateCheck(self):
		if self.var1.get() == 0:
			self.jsonCheck=0
			self.entryVidFrom.config(state=NORMAL)
			self.entryVidTo.config(state=NORMAL)
			self.entryDelta.config(state=DISABLED)
		elif self.var1.get() == 1:        #whenever unchecked
			self.jsonCheck=1
			self.entryVidFrom.config(state=DISABLED)
			self.entryVidTo.config(state=DISABLED)
			self.entryDelta.config(state=NORMAL)
	
	
	def displayVideo(self):
		self.paIn = self.entryIn.get()
		globals.extract=1
		#Read video
		self.cap = cv2.VideoCapture(self.paIn)
		
		#Calculate size of video
		vidSize = os.path.getsize(self.paIn)
		vidSize=round((vidSize/1048576),2)

		# print(vidSize)
		self.size.set(str(vidSize))
		
		#Read date of video creation                            
		self.date_record_start=time.ctime(os.path.getctime(self.paIn))
		
		#Count total frame count, self.fps,so duration
		self.fps = self.cap.get(cv2.CAP_PROP_FPS)      
		self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
		print(self.frame_count)

		self.duration = self.frame_count/self.fps

		minutes = int(self.duration/60)
		seconds = round((self.duration%60),2)

		self.dur.set(str(minutes) + ':' + str(seconds))
		self.date_record_end=time.ctime(os.path.getctime(self.paIn)+self.duration)
		#Display video
		self.th = threading.Thread(target=cut_frame.VideoShow, args=(self.cap,self.VideoFrame, self.canvas,self.ws,self.hs))
		self.th.start()
		
		#Display info video
		self.start.set(str(self.date_record_start.split()[3]))
		self.end.set(str(self.date_record_end.split()[3]))

	def extract30second(self):
		self.rightcanvas1.delete("all")
		if self.jsonCheck==0:
			self.thre=threading.Thread(target=cut_frame.ExtractFrame,args=(self.paIn, self.entryVidFrom, self.entryVidTo, self.date_record_start, self.fps,self.rightcanvas1))
			self.thre.start()

		elif self.jsonCheck==1:
			self.thre=threading.Thread(target=cut_frame.ExtractFrameJSON,args=(self.paIn,self.entryDelta,self.date_record_start,self.fps,self.rightcanvas1))
			self.thre.start()

	def exportVideo(self):
		self.ws=(globals.ws/2)
		self.hs=(globals.hs/3)
		if self.jsonCheck==0:
			th=threading.Thread(target=cut_frame.exportVideo,args=(self.paIn,
																	self.entryVidFrom,
																	self.entryVidTo,
																	self.date_record_start,
																	self.fps,self.right_videoFrame,self.rightcanvas2,
																	self.ws,self.hs))
			th.start()

		else:
			th=threading.Thread(target=cut_frame.exportVideoJSON,args=(self.paIn,
																		self.entryDelta,
																		self.date_record_start,
																		self.fps,self.right_videoFrame,self.rightcanvas2,
																		self.ws,self.hs))
			th.start()