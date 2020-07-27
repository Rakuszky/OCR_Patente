import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

placa = []
image = cv2.imread('imagenes/patente1.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.blur(gray,(3,3))
canny = cv2.Canny(gray,150,200)
canny = cv2.dilate(canny,None,iterations=2)

cnts,_ = cv2.findContours(canny,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
#cv2.drawContours(image,cnts,-1,(0,0,255),2)

for c in cnts:
    area = cv2.contourArea(c)
    x,y,w,h = cv2.boundingRect(c)
    epsilon = 0.03*cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c,epsilon,True)
    
    if len(approx)==4 and area > 5000:
        print('area', area)
        #cv2.drawContours(image,[c],0,(0,0,255),2)
        aspect_ratio = float(w)/h
        if aspect_ratio > 2.0:
            placa = gray[y:y+h, x:x+w]
            text = pytesseract.image_to_string(placa, config='--psm 9')
            str = ':?}°"- /°|*)'
            for quitar in str:
                text = text.replace(quitar,'')
            print('text=', text)
            cv2.imshow('placa',placa)
            cv2.moveWindow('placa',780,10)
            cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),0)
            cv2.putText(image,text,(x+10,y-10),1,2.2,(0,0,255),3)

#cv2.imshow('Canny', canny)
cv2.imshow('Image', image)
cv2.moveWindow('Image',45,10)
cv2.waitKey(0)