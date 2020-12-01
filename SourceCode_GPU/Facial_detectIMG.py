import face_recognition
import pickle
import cv2
import os
import draft
import tkinter
import time
import globals
import operator
import numpy as np
import datetime
import operator
# import draft
import dlib

def run():

    time_start = time.time()
    classes = [f for f in os.listdir("face_recog/dataset")]
    dictNames = dict.fromkeys(classes)
    for key in dictNames.keys():
        dictNames[key] = 0
    totalIn = 0
    global lbl1, lbl2, lbl3, lbl4, check
    check = False
    # Xóa thành phần đang có trong bảng Bảng thông tin
    for widget in globals.listCam.winfo_children():
        widget.destroy()

    tkinter.Label(globals.listCam, text='Cam IP', width= 20).grid(row=0, column=0,padx=1,pady=1)
    tkinter.Label(globals.listCam, text='Name', width= 20).grid(row=0, column=1,padx=1,pady=1)
    tkinter.Label(globals.listCam, text='Time', width= 30).grid(row=0, column=2,padx=1,pady=1)
    tkinter.Label(globals.listCam, text='Date', width= 30).grid(row=0, column=3,padx=1,pady=1)
    
    # Đọc file encodings.pickle
    data = pickle.loads(open("face_recog/encodings.pickle", "rb").read())
    
    # load the input image and convert it from BGR to RGB
    path = 'ToAPI/imgN_V'
    images = [f for f in os.listdir("ToAPI/imgN_V")]
    
    # Tạo thanh tiến độ
    t = tkinter.Toplevel()
    t.geometry('{}x{}+{}+{}'.format(300, 50, 500, 300))   
    t.wm_title('Process Detect')
    progress = tkinter.ttk.Progressbar(t, orient=tkinter.HORIZONTAL, length=300, mode='determinate')
    progress.pack()
    lb1 = tkinter.Label(t, text="")
    lb1.pack()

    # Ghi ra file detect_face.txt 
    with open("detect_face.txt", "w") as d:
        for index, name_pic in enumerate(images):
            progress['value'] = int((index+1)/len(images) * 100)
            lb1.configure(text="[INFO] processing image {}/{}".format(index+1, len(images)))
            t.update()
            # time.sleep(1)

            
            link = os.path.join(path, name_pic)
            image = cv2.imread(link)
            image=cv2.resize(image,(500,500))
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            boxes = face_recognition.face_locations(rgb,model='cnn',number_of_times_to_upsample=0)
            print(len(boxes))
            if len(boxes) > 0:
                encodings = face_recognition.face_encodings(rgb, boxes)
            
                # initialize the list of names for each face detected
                names = []
                
                # loop over the facial embeddings
                for encoding in encodings:
                    matches = face_recognition.compare_faces(data["encodings"], encoding, tolerance=0.45)
                    name = "Unknown"
                    
                    if True in matches:
                        matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                        counts = {}
                        
                        for i in matchedIdxs:
                            name = data["names"][i]
                            counts[name] = counts.get(name, 0) + 1
                        count_sort = sorted(counts.items(), key=operator.itemgetter(1), reverse=True)
                        for i in range (len(count_sort)):
                            names.append(count_sort[i][0])
                   
                        if len(names) == 1:
                            print("Kết luận: {}".format(names[0]))
                        elif len(names) == 2:
                            print("Kết luận: {}, {}".format(names[0], names[1]))
                        else:
                            print("Kết luận: {}, {}, {}".format(names[0], names[1], names[2]))
                            #Nếu chưa đi qua lần nào thì đếm
                        if dictNames[names[0]] == 0:
                            totalIn += 1
                        
                        dictNames[names[0]] += 1
                        print("{} đã đi qua {} lần".format(names[0], dictNames[names[0]]))
                        strName = names[0]                            
                        name = max(counts, key=counts.get)
                    else:
                        print("Kết luận: Unknown")
                        totalIn += 1
                        strName = "Unknown"
                    names.append(name)

                    # Điền vào bảng thông tin
                    tkinter.Label(globals.listCam, text=name, width=20).grid(row=index+1, column=1,padx=1,pady=1)
                
                # Cắt chuỗi lấy thông tin
                strPic_name = name_pic[0:2] + "_" + name_pic[2:4] + "_" + name_pic[4:8] + "|" + name_pic[8:10] + ":" + name_pic[10:12] + ":" + name_pic[12:14]
                d.write(str(index+1) + "/ " + strPic_name + "\t" + names[0] + "\n")

                datePic = name_pic[0:2] + "_" + name_pic[2:4] + "_" + name_pic[4:8]
                timePic = name_pic[8:10] + ":" + name_pic[10:12] + ":" + name_pic[12:14]

                # Điền vào bảng thông tin
                tkinter.Label(globals.listCam, text=str(index+1), width= 20).grid(row=index+1, column=0,padx=1,pady=1)
                tkinter.Label(globals.listCam, text=datePic, width= 30).grid(row=index+1, column=3,padx=1,pady=1)
                tkinter.Label(globals.listCam, text=timePic, width= 30).grid(row=index+1, column=2,padx=1,pady=1)
                res = draft.uploadImgN_VToAPI(name_pic)
                print(res)
            #end if

            # Tạo thêm dòng mới để sửa bug không hiển thị dữ liệu cuối cùng
            if index == len(images) - 2:
                lbl1 = tkinter.Label(globals.listCam, text='', width= 20)
                lbl1.grid(row=index+2, column=0)
                lbl2 = tkinter.Label(globals.listCam, text='', width= 20)
                lbl2.grid(row=index+2, column=1)
                lbl3 = tkinter.Label(globals.listCam, text='', width= 30)
                lbl3.grid(row=index+2, column=2)
                lbl4 = tkinter.Label(globals.listCam, text='', width= 30)
                lbl4.grid(row=index+2, column=3)
                check = True
            
            # Nếu có tạo thêm dòng mới mà không có khuôn mặt sau đó thì xóa dòng mới đó đi
            if len(boxes) == 0 and index == len(images) - 1 and check==True:
                lbl1.destroy()
                lbl2.destroy()
                lbl3.destroy()
                lbl4.destroy()
        #end for
    # Xác định độ dài thông tin để cho phép scrollbar
    globals.canvasFrame.configure(scrollregion=globals.canvasFrame.bbox('all'))

    print("Done!")

    t.destroy()
    tkinter.messagebox.showinfo("Thông báo", "Đã nhận diện và ghi xong dữ liệu!")

    time_end = time.time()
    tkinter.messagebox.showinfo("Tông thơi gian chạy",time_end-time_start)
if __name__ == "__main__":
    run()