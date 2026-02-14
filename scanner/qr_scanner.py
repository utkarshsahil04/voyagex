import cv2
def qr_scanner():
    cam=cv2.VideoCapture(0)
    detector=cv2.QRCodeDetector()
    print("Scanning Qr code...... press q for exit")
    while True :
    
        ret,frame=cam.read()
        frame=cv2.flip(frame,1)
        data,bbox,_=detector.detectAndDecode(frame)
        print(frame.shape)
        if not data:
            print("Can't receive frame (stream end?). Exiting ...")
        else:
            print("data recieved")
            cam.release()
            cv2.destroyAllWindows()
            return data
   
        cv2.imshow('QR_scanner',frame)
        if cv2.waitKey(1) == ord('q'):
            break
    

    cam.release()
    cv2.destroyAllWindows()

cam=qr_scanner()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         