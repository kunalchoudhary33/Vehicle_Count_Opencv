import cv2
import numpy as np

upCarCount = 0
downCarCount = 0

upTwoWheelerCount = 0
downTwoWheelerCount = 0

def get_centroid(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return (cx, cy)

cap = cv2.VideoCapture("input.mp4")

_, frame1 = cap.read()
_, frame2 = cap.read()

while(True):
    
    # Background difference and apply filters
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    
    # Get contours
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Draw Vehicle upwards line
    cv2.line(frame1, (10,300), (600,300),(0,0,255), 2)
    cv2.line(frame1, (10,310), (600,310),(0,0, 255), 2)
    
    # Draw Vehicle downwards Line
    cv2.line(frame1, (730,340), (1200,340),(0,0,255), 2)
    cv2.line(frame1, (730,330), (1200,330),(0,0,255), 2)
   
    for contour in contours:
        (x,y,w,h) = cv2.boundingRect(contour)
        area = (cv2.contourArea(contour)) 
        
        if (cv2.contourArea(contour) < 700):
            continue
        if (w<40):
            (tx, ty) = get_centroid(x,y,w,h)
            cv2.rectangle(frame1, (x,y), (x+w, y+h), (255,0,0), 2)
            if(tx>300 and tx < 600 and ty > 300 and ty<305):
                upTwoWheelerCount = upTwoWheelerCount +1
            if(tx>730 and tx < 1100 and ty > 330 and ty<335):
                downTwoWheelerCount = downTwoWheelerCount +1
            
        if (w>40 and h<100):
            (cx, cy) = get_centroid(x,y,w,h)
            cv2.rectangle(frame1, (x,y), (x+w, y+h), (255,0,0), 2)
            if(cx>300 and cx < 600 and cy > 300 and cy<305):
                upCarCount = upCarCount + 1
            if(cx>730 and cx < 1100 and cy > 330 and cy<335):
                downCarCount = downCarCount +1
        
        carUpText =("Car Count Up : "+str(upCarCount))
        cv2.putText(frame1, carUpText, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0 ,255), 2)
        twoWheelUpText =("Two Wheelers Counter Up :"+str(upTwoWheelerCount))
        cv2.putText(frame1, twoWheelUpText, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0 ,255), 2)
        
        carDownText =("Car Count Down : "+str(downCarCount))
        cv2.putText(frame1, carDownText, (900, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0 ,255), 2)
        twoWheelDownText =("Two Wheelers Counter Down :"+str(downTwoWheelerCount))
        cv2.putText(frame1, twoWheelDownText, (900, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0 ,255), 2)
         
    cv2.imshow("Frame", frame1)
    #cv2.imshow("dilated", dilated)
    frame1=frame2
    _, frame2 = cap.read()
    _, frame2 = cap.read()
    
    key = cv2.waitKey(30)
    if key ==27:
        break
        
cap.release()
cv2.destroyAllWindows()
