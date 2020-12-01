import os
import requests

path = os.path.dirname(os.path.abspath(__file__))
img_dir = path

def uploadImgN_VToAPI(file_path):
    img_dir = os.path.join(path,'ToAPI/imgN_V/')
    api_url = 'https://s-work.vn/MobileLogin/InsertFaceId'
    folder_code_object = "IOT.N-V"
    
    for root, _, _ in os.walk(img_dir): 
        img_valid = {'img': open((os.path.join(root, file_path)), 'rb')}
        # cv2.imshow("name",img_valid)
        values = {'folderCode': folder_code_object}
        response = requests.post(api_url, files=img_valid, data=values)
    # response =requests.get(api_url, files=files, data=values).json()
    return response.text
    
def uploadQTToAPI():
    img_dir = os.path.join(path,'/ToAPI/imgQT/')
    api_url = 'https://s-work.vn/MobileLogin/InsertFaceId'
    folder_code_monitoring = "IOT.QT"

    for root, dirs,files in os.walk(img_dir):
        for file in files:
            if file.endswith('png') or file.endswith('jpg'):
                img_valid = {'img': open((os.path.join(root,file)), 'rb')}
                print (img_valid)
                # cv2.imshow("name",img_valid)
                values = {'folderCode': folder_code_monitoring}

                response = requests.post(api_url, files=img_valid, data=values)
    # response =requests.get(api_url, files=files, data=values).json()
                print(response.text)
                
def uploadN_VToAPI():
    img_dir = os.path.join(path,'/ToAPI/imgN_V/')
    api_url = 'https://s-work.vn/MobileLogin/InsertFaceId'    
    folder_code_object = "IOT.N-V"

    for root, dirs,files in os.walk(img_dir):
        for file in files:
            if file.endswith('png') or file.endswith('jpg'):
                img_valid = {'img': open((os.path.join(root,file)), 'rb')}
                # cv2.imshow("name",img_valid)
                values = {'folderCode': folder_code_object}

                response = requests.post(api_url, files=img_valid, data=values)
    # response =requests.get(api_url, files=files, data=values).json()
                print(response.text)

def uploadCar_VToAPI(file_path,strPlate):
    img_dir = os.path.join(path, 'ToAPI/imgXE/')
    api_url = 'https://s-work.vn/MobileLogin/InsertCarLicesePlate'

    for root, _, _ in os.walk(img_dir):
        img_valid = {'img': open((os.path.join(root, file_path)), 'rb')}
        # cv2.imshow("name",img_valid)
        values = {'licensePlate': strPlate,
                  'active': 'Ra',
                  'driver': 'Lê Đức Phòng',
                  'img': img_dir,
                  'folderCode': 'IOT.XE'
                  }
        response = requests.post(api_url, files=img_valid, data=values)
        return response.text

def uploadDeviceToServer():
    api_url = 'https://s-work.vn/MobileLogin/InsertDevice'
    values = {'DeviceID': '1 ',
             'DeviceTitle': '0',
             'Vendor': '3i',
             'PositionDevice': 'Tang 4',
             'Describe': 'CameraLocal1111111',
             'Status': '0'}
    response = requests.post(api_url, data=values)
    print(response.text)