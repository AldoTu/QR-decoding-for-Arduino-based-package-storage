import cv2
import pyqrcode
from pyzbar.pyzbar import decode
from PIL import Image
import serial
import sqlite3
import os

newData = True
oldData = ""
count = 0

conn = sqlite3.connect(os.getcwd() + r"\qr.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS product(
    name VARCHAR(255),
    path INTEGER)""")
conn.commit()

ser = serial.Serial('COM6', 9600)
print ser.name
if ser.isOpen():
    print "Serial Opened!"
else:
    ser.open()
ser.flush()


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
cap.set(3, 2048)
cap.set(4, 2048)

while True:

    _, frame = cap.read()
    if frame is not None:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        pil = Image.fromarray(gray)
        decoded = decode(pil)
        print decoded
        cv2.putText(frame, str(count), (585, 40), cv2.FONT_HERSHEY_PLAIN, 2.5, (0, 0, 255), 2)
        cv2.imshow('QR Code', frame)
        if len(decoded) != 0:
            product = cursor.execute("""SELECT path FROM product WHERE name = {}""".format("'" + decoded[0][0] + "'"))
            var = product.fetchone()
            if var is not None:
                if oldData == decoded:
                    newData = False
                else:
                    newData = True
                if newData:
                    print decoded[0][0]
                    ser.write(str(var))
                    count = count + 1
                    oldData = decoded
            else:
                continue
        else:
            oldData = ""
        ch = 0xFF & cv2.waitKey(1)
        if ch == 27:
            break

cap.release()
cv2.destroyAllWindows()
ser.close()
conn.close()
