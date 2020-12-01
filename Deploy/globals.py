# Lưu trữ các biến toàn cục
def init():
    #Biến hiển thị tên khuôn mặt
    global strName
    strName = ""
    #Biến hiển thị thời gian khuôn mặt được phát hiện và nhận diện
    global strTime
    strTime = ""
    # Biến hiển thị kết quả detect
    global listCam
    listCam = None

    global canvasFrame
    canvasFrame = None