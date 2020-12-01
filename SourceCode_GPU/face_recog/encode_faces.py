from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os
import tkinter
import time
from shutil import copyfile
from tkinter import W, N, E, S, filedialog
from tkinter.ttk import Button, Label
import face_recog.folder_processing as fp

def initUI():
    # Tạo UI
    t = tkinter.Toplevel()
    t.title("Add Face")
    t.grab_set()

    lbl1 = Label(t,text="Name Face:")
    lbl1.grid(sticky=W+S, padx=5)

    name = tkinter.Entry(t)
    name.grid(row=0,column=1,columnspan=2,padx=5)

    # Tạo button
    abtn = Button(t,text="Image", command= lambda: browser_file(name,t))
    abtn.grid(row=1, column=0, pady=5, padx=5)

    cbtn = Button(t, text="Close", command=t.destroy)
    cbtn.grid(row=1, column=2, pady=5, padx=5)

def browser_file(name,t):
    # lệnh browser
    currdir = os.getcwd()
    filename= filedialog.askopenfilenames(initialdir=currdir, title='Select images', filetype=(('jpge','*.jpg'),('png','*.png')))
    lenght=len(filename)
    if lenght != 0:
        if not os.path.exists("face_recog/dataset_train/"+name.get()):
            os.makedirs("face_recog/dataset_train/"+name.get())
        for i in filename:
            copyfile(i,"face_recog/dataset_train/"+name.get()+"/"+(i.split("/")[-1]))
        tkinter.messagebox.showinfo("Thông báo", "Đã thêm ảnh của "+name.get()+" vào dữ liệu!")

def trainNewFaces():
    # folder chứa ảnh muốn được train thêm
    super_path_new_data = "face_recog/dataset_train/"
    if len(os.listdir(super_path_new_data)) != 0:
        
        # folder chứa ảnh đã train
        super_path_data = "face_recog/dataset/"

        # lưu trữ dữ liệu được encode mới
        encodes = []

        # tên tương ứng với các ảnh được encode
        names = []

        # Tạo frame hiển thị tiến độ
        t = tkinter.Toplevel()
        t.geometry('{}x{}+{}+{}'.format(300, 50, 500, 300))   
        t.wm_title('Process Train')
        
        progress = tkinter.ttk.Progressbar(t, orient=tkinter.HORIZONTAL, length=300, mode='determinate')
        progress.pack()
        lb1 = tkinter.Label(t, text="aaa")
        lb1.pack()  
        # đọc các ảnh trong folder new_image và encode
        for f in os.listdir(super_path_new_data):
            name = f
            sub_path_new_data = super_path_new_data + name + '/'
            length=len(os.listdir(sub_path_new_data))
            i=0
            for img in os.listdir(sub_path_new_data):
                img_path = sub_path_new_data + img
                image = cv2.imread(img_path)
                progress['value'] = int(((i+1)/length) * 100)
                lb1.configure(text="Processing image of "+name+" {}/{}".format(i + 1, length))
                t.update()
                i+=1

                # chỉnh sửa thông số cho ảnh dữ liệu
                cv2.resize(image,(100,100))
                img_y_cr_cb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
                y, cr, cb = cv2.split(img_y_cr_cb)
                y_eq = cv2.equalizeHist(y)
                img_y_cr_cb_eq = cv2.merge((y_eq, cr, cb))
                rgb = cv2.cvtColor(img_y_cr_cb_eq, cv2.COLOR_YCR_CB2RGB)

                # trả 
                boxes = face_recognition.face_locations(rgb, model='cnn',number_of_times_to_upsample=0)

                # encode mặt người vừa nhận được
                encodings = face_recognition.face_encodings(rgb, boxes)

                # loop over the encodings
                for encoding in encodings:
                    # add each encoding + name to our set of known names and
                    # encodings
                    encodes.append(encoding)
                    names.append(name)

        # kiểm tra có file data.pickle không
        # if not os.path.exists('data.pickle'):
        #     file = open('data.pickle', 'wb')
        #     file.close()

        # đọc dữ liệu đã được encode trong file data.pickle
        # nếu file data rỗng thì tạo 1 đối tượng data 
        try:
            data = pickle.load(open("face_recog/encodings.pickle","rb"))
        except:
            data = {'encodings':[], 'names': []}
        
        if len(encodes) == 0 or len(names) == 0:
            print('data folder is empty')
        else:
            # append dữ liệu vừa encode từ folder new_image vào data
            for (encode, name) in zip(encodes, names):
                data['encodings'].append(encode)
                data['names'].append(name)
            # lưu lại data vào file data.pickle
            with open('face_recog/encodings.pickle', 'wb') as handle:
                pickle.dump(data, handle)
            t.destroy()
            fp.move_folder2folder(super_path_new_data,super_path_data)
            tkinter.messagebox.showinfo("Thông báo", "Đã train xong dữ liệu!")
    else: tkinter.messagebox.showinfo("Thông báo", "Không có dữ liệu mới!")

def trainAll():
    pathdata="face_recog/dataset"
    if len(os.listdir(pathdata)) != 0:
        pathpickle="face_recog/encodings.pickle"

        # grab the paths to the input images in our dataset
        imagePaths = list(paths.list_images(pathdata))
        
        # initialize the list of known encodings and known names
        knownEncodings = []
        knownNames = []
        
        # Tạo frame hiển thị tiến độ
        t = tkinter.Toplevel()
        t.geometry('{}x{}+{}+{}'.format(300, 50, 500, 300))   
        t.wm_title('Process Train')
        
        progress = tkinter.ttk.Progressbar(t, orient=tkinter.HORIZONTAL, length=300, mode='determinate')
        progress.pack()
        lb1 = tkinter.Label(t, text="aaa")
        lb1.pack()
        
        # loop over the image paths
        for (i, imagePath) in enumerate(imagePaths):

            name = imagePath.split(os.path.sep)[-2]

            # extract the person name from the image path
            progress['value'] = int((i+1)/len(imagePaths) * 100)
            lb1.configure(text="Processing image of "+name+" {}/{}".format(i + 1, len(imagePaths)))
            t.update()
            time.sleep(1)
            
            # load the input image and convert it from RGB (OpenCV ordering)
            image = cv2.imread(imagePath)
            
            img_y_cr_cb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
            y, cr, cb = cv2.split(img_y_cr_cb)
            y_eq = cv2.equalizeHist(y)
            img_y_cr_cb_eq = cv2.merge((y_eq, cr, cb))
            rgb = cv2.cvtColor(img_y_cr_cb_eq, cv2.COLOR_YCR_CB2RGB)
        
            # detect the (x, y)-coordinates of the bounding boxes
            # corresponding to each face in the input image
            boxes = face_recognition.face_locations(rgb, model='cnn',number_of_times_to_upsample=0)
        
            # compute the facial embedding for the face
            encodings = face_recognition.face_encodings(rgb, boxes)
        
            # loop over the encodings
            for encoding in encodings:
                # add each encoding + name to our set of known names and
                # encodings
                knownEncodings.append(encoding)
                knownNames.append(name)
        
        # dump the facial encodings + names to disk
        data = {"encodings": knownEncodings, "names": knownNames}
        f = open(pathpickle, "wb")
        f.write(pickle.dumps(data))
        f.close()
        t.destroy()
        tkinter.messagebox.showinfo("Thông báo", "Đã train xong dữ liệu!")
    else: tkinter.messagebox.showinfo("Thông báo", "Không có dữ liệu!")