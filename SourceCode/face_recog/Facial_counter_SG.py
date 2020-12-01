from face_recog.iiiTrackerObject.centroidtracker import CentroidTracker
from face_recog.iiiTrackerObject.trackableobject import TrackableObject
# from iiiTrackerObject.centroidtracker import CentroidTracker
# from iiiTrackerObject.trackableobject import TrackableObject
import face_recognition
import face_recognition
import numpy as np
import datetime
import operator
import pickle
# import draft
import dlib
import cv2
import os
import threading

#"rtsp://admin:ADMIN123@117.6.131.222:7979"
#Khởi tạo dic lưu số lần đã đi qua camera của mọi người trong dataset
classes = [f for f in os.listdir("face_recog/dataset")]
dictNames = dict.fromkeys(classes)
for key in dictNames.keys():
	dictNames[key] = 0
	
class Face(object):
	"""docstring for Face"""
	def __init__(self):
		# self.Frames = 0
		self.w = None
		self.h = None
		self.data = pickle.loads(open('face_recog/encodings.pickle', "rb").read())
		self.trackableObjects = {}
		self.totalIn = 0
		# self.path = os.path.dirname(os.path.abspath(__file__))
		self.ct = CentroidTracker(maxDisappeared=10, maxDistance=100)
		# self.strName = None
		
	def run(self, frame):
		if self.w is None or self.h is None:
			(self.h, self.w) = frame.shape[:2]
		# check = 0
		rects = []
		trackers = []

		rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		his_img = cv2.equalizeHist(gray)

		# Find all the faces and face encodings inframe of video
		face_locations = face_recognition.face_locations(his_img, model='hog', number_of_times_to_upsample=1)
		for face_location in face_locations:
			startY, endX, endY, startX = face_location
			tracker = dlib.correlation_tracker()
			rect = dlib.rectangle(int(startX), int(startY), int(endX), int(endY))
			tracker.start_track(rgb, rect)
			trackers.append(tracker)
		# loop over the trackers
			
		for tracker in trackers:
			# update the tracker and grab the updated position
			tracker.update(rgb)
			pos = tracker.get_position()

			# unpack the position object
			startX = int(pos.left())
			startY = int(pos.top())
			endX = int(pos.right())
			endY = int(pos.bottom())
			
			# add the bounding box coordinates to the rectangles list
			rects.append((startX, startY, endX, endY))
				
		# Update objects and counting     
		objects = self.ct.update(rects)
		
		# loop over the tracked objects
		for (objectID, centroid) in objects.items():
			# check to see if a trackable object exists for the current
			# object ID
			to = self.trackableObjects.get(objectID, None)

			# if there is no existing trackable object, create one
			if to is None:
				to = TrackableObject(objectID, centroid)

			# otherwise, there is a trackable object so we can utilize it
			# to determine direction
			else:
				# the difference between the y-coordinate of the current
				# centroid and the mean of previous centroids will tell
				# us in which direction the object is moving (negative for
				# 'up' and positive for 'down')
				y = [c[1] for c in to.centroids]
				# direction = centroid[1] - np.mean(y)
				to.centroids.append(centroid)
				
				# Đếm khi bắt được khuôn mặt đi qua
				if not to.counted:
					frame1=frame.copy()
					th = threading.Thread(target=Face.Face_cut, args=(frame1,centroid))
					to.counted = True
					th.start()
					# roi_img = frame[centroid[3] - 20:centroid[5] + 10, centroid[2] - 10:centroid[4] + 10]
					# # to.counted = True
					# 		#Lưu ảnh 
					# temp = datetime.datetime.today().strftime("%d-%m-%Y-%H-%M-%S")
					# dt = temp.split('-')
					# # img_name = "".join(dt) + "_" + str(self.totalIn) +".jpg"
					# img_name = "".join(dt) +".jpg"
					# img_dir1 = "ToAPI/imgN_V/" + img_name
					# cv2.imwrite(img_dir1, roi_img)

					# if direction > 0 and centroid[1] > self.h // 3:# đếm khi có người đi vào
					# if centroid[1] > self.h // 6:
					# if centroid[1] > self.h // 3:
						# check = 1
						# Cắt ảnh chứa khuôn mặt phát hiện được
						# size = self.w // 10
						# size = self.w // 5
						# if centroid[0] - size >= 0 and centroid[0] + size <= self.w and centroid[1] + size <= self.h:
							# roi_img = frame[centroid[3] - 20:centroid[5] + 10, centroid[2] - 10:centroid[4] + 10]
							# roi_img = frame[centroid[3] - 20:centroid[5] + 10, centroid[2] - 10:centroid[4] + 10]
							# to.counted = True
							# #Lưu ảnh 
							# temp = datetime.datetime.today().strftime("%d-%m-%Y-%H-%M-%S")
							# dt = temp.split('-')
							# # img_name = "".join(dt) + "_" + str(self.totalIn) +".jpg"
							# img_name = "".join(dt) +".jpg"
							# img_dir1 = "ToAPI/imgN_V/" + img_name
							# cv2.imwrite(img_dir1, roi_img)

#                        #Tăng độ tương phản cho ảnh màu 
# 						img_y_cr_cb = cv2.cvtColor(roi_img, cv2.COLOR_BGR2YCrCb)
# 						y, cr, cb = cv2.split(img_y_cr_cb)
# 						y_eq = cv2.equalizeHist(y)
# 						img_y_cr_cb_eq = cv2.merge((y_eq, cr, cb))
# 						rgb = cv2.cvtColor(img_y_cr_cb_eq, cv2.COLOR_YCR_CB2RGB)    

# 					   #Nhận diện khuôn mặt trong ảnh là ai
# 						boxes = face_recognition.face_locations(rgb, model='hog')
# 						encodings = face_recognition.face_encodings(rgb, boxes) 
					   
# 					   #Nếu tìm thấy khuôn mặt trong hình vừa cắt ra
# 						if(len(encodings) > 0):
# 							for encoding in encodings:
# 							# attempt to match each face in the input image to our known
# 							# encodings
# 								matches = face_recognition.compare_faces(self.data["encodings"], encoding, tolerance=0.45)
# 								print("----------------")
							
# 							   #Nếu tìm thấy khuôn mặt khớp với dữ liệu có sẵn
# 								if True in matches:
# 								# find the indexes of all matched faces then initialize a
# 								# dictionary to count the total number of times each face
# 								# was matched
# 									matchedIdxs = [i for (i, b) in enumerate(matches) if b]
# 									counts = dict()
# 									names = []
			   
# 								# loop over the matched indexes and maintain a count for
# 								# each recognized face face
# 									for i in matchedIdxs:
# 										name = self.data["names"][i]
# #                                        dist = face_recognition.face_distance(encodings, self.data["encodings"][i])
# #                                        print(dist, self.data["names"][i])
# 										counts[name] = counts.get(name, 0) + 1
								   
# 									print(counts)
								   
# 									count_sort = sorted(counts.items(), key=operator.itemgetter(1), reverse=True)
# 									for i in range (len(count_sort)):
# 										names.append(count_sort[i][0])
				   
# 									if len(names) == 1:
# 										print("Kết luận: {}".format(names[0]))
# 									elif len(names) == 2:
# 										print("Kết luận: {}, {}".format(names[0], names[1]))
# 									else:
# 										print("Kết luận: {}, {}, {}".format(names[0], names[1], names[2]))
# 									#Nếu chưa đi qua lần nào thì đếm
# 									if dictNames[names[0]] == 0:
# 										self.totalIn += 1
# 									dictNames[names[0]] += 1
# 									print("{} đã đi qua {} lần".format(names[0], dictNames[names[0]]))
# 									self.strName = names[0]
# #                                    res = draft.uploadImgN_VToAPI(img_name)
							   
# 							   #Nếu không khớp với dữ liệu các khuôn mặt có sẵn  
# 								else:
# 									print("Kết luận: Unknown")
# 									self.totalIn += 1
# 									self.strName = "Unknown"
# 					   #Không tìm được khuôn mặt trong hình cắt
# 						else:
# 							print("Không bắt được khuôn mặt trong hình")
# 							self.strName = "None"
# #            # store the trackable object in our dictionary
			self.trackableObjects[objectID] = to
			text = "ID {}".format(objectID)
			cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
		for (startX, startY, endX, endY) in rects:
			cv2.rectangle(frame, (startX, startY), (endX, endY), (0,0,255), 1)
			
		# cv2.putText(frame, 'Chạy nhận diện', (0,frame.shape[0] -10), cv2.FONT_HERSHEY_TRIPLEX, 0.5,  (0, 0, 255), 1)
		cv2.line(frame, (0, self.h//3), (self.w, self.h//3), (0,255,255), 3)

	def Face_cut(frame,centroid):
		print(1)
		roi_img = frame[centroid[3] - 20:centroid[5] + 10, centroid[2] - 10:centroid[4] + 10]
					# to.counted = True
							#Lưu ảnh 
		temp = datetime.datetime.today().strftime("%d-%m-%Y-%H-%M-%S")
		dt = temp.split('-')
					# img_name = "".join(dt) + "_" + str(self.totalIn) +".jpg"
		img_name = "".join(dt) +".jpg"
		img_dir1 = "ToAPI/imgN_V/" + img_name
		cv2.imwrite(img_dir1, roi_img)

		# self.Frames += 1
#        if check == 1:
#            return self.strName, temp
#        else:
#            return None, None