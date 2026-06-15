import os
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image
from tkinter import PhotoImage
import numpy as np
import cv2
import pytesseract

# On Windows, Tesseract is usually not on PATH, so point pytesseract at the
# default install location if it exists. On macOS/Linux the `tesseract` binary
# is normally on PATH (Homebrew / apt), so we leave pytesseract's default.
_windows_tesseract = "C:/Program Files/Tesseract-OCR/tesseract.exe"
if os.path.exists(_windows_tesseract):
    pytesseract.pytesseract.tesseract_cmd = _windows_tesseract

cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_russian_plate_number.xml")
states = {"AN": "Andaman and Nicobar", "AP": "Andhra Pradesh", "AR": "Arunachal Pradesh", "AS": "Assam", "BH": "India", "BR": "Bihar", "CH": "Chandigarh",
          "DN": "Dadra and Nagar Haveli", "DD": "Daman and Diu", "DL": "Delhi", "GA": "Goa", "GJ": "Gujarat", "HR": "Haryana", "HP": "Himachal Pradesh",
          "JK": "Jammu and Kashmir", "KA": "Karnataka", "KL": "Kerala", "LD": "Lakshadweep", "MP": "Madhya Pradesh", "MH": "Maharashtra", "MN": "Manipur", "ML": "Meghalaya",
          "MZ": "Mizoram", "NL": "Nagaland", "OD": "Odissa", "PY": "Pondicherry", "PN": "Punjab", "RJ": "Rajasthan", "SK": "Sikkim", "TN": "Tamil Nadu", "TR": "Tripura",
          "UP": "Uttar Pradesh", "WB": "West Bengal", "CG": "Chhattisgarh", "TS": "Telangana", "JH": "Jharkhand", "UK": "Uttarakhand"}

top = tk.Tk()
top.geometry('1280x720')
top.title('Number Plate Recognition')

top.configure(background='#CDCDCD')
label = Label(top, background='#CDCDCD', font=('arial', 35, 'bold'))
sign_image = Label(top, bd=10)
plate_image = Label(top, bd=10)


def classify(file_path):
    res_text = [0]
    res_img = [0]
    img = cv2.imread(file_path)
    #cv2.imshow("plate", img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("plate", gray)
    ################################################
    nplate = cascade.detectMultiScale(gray, 1.1, 4)
    if len(nplate) == 0:
        # No plate detected: show a message and stop instead of crashing on a
        # missing "Number Plate.jpg" further down.
        label.configure(foreground='#011638', text='No number plate detected.')
        plate_image.configure(image='')
        plate_image.image = None
        return
    for (x, y, w, h) in nplate:
        # Cropping a portion of the number plate
        a, b = (int(0.02*img.shape[0]), int(0.025*img.shape[1]))
        # Making the image more darker to identify the LPR
        plate = img[y+a:y+h-a, x+b:x+w-b, :]
        # Image Processing
        kernel = np.ones((1, 1), np.uint8)
        plate = cv2.dilate(plate, kernel, iterations=1)
        plate = cv2.erode(plate, kernel, iterations=1)
        plate_gray = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY)
        (thresh, plate) = cv2.threshold(plate_gray, 127, 255, cv2.THRESH_BINARY)
        # Feeding the image into the OCR engine
        read = pytesseract.image_to_string(plate)
        read = ''.join(e for e in read if e.isalnum())
        # print(read)
        stat = read[0:2]
        try:
            # Fetching the information of the state to which the car belongs
            print('Car belongs to:', states[stat])
            temp = "\nCar belongs to:"
            temp += states[stat]
        except:
            print('Image not clear.')
            temp = "Image not clear!!!"
        print(read)
        cv2.rectangle(img, (x, y), (x+w, y+h), (51, 51, 255), 2)
        cv2.rectangle(img, (x, y - 40), (x + w, y), (51, 51, 255), -1)
        cv2.putText(img, read, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        #cv2.imshow('Plate', plate)
        # Saving & displaying the result
        cv2.imwrite('Number Plate.jpg', plate)

    ################################################

        # cv2.imwrite("result.png",plate)
        #read = pytesseract.image_to_string(plate)
        res_img[0] = plate
        #cv2.imshow("plate", res_img)
        #res_img[0].resize((1000, 500))
        res_text[0] = read
        res_text[0] += temp
        """if(temp!="Image not clear!!!"):
            res_text[0]+=temp
        else:
            res_text[0]=temp"""
        if read:
            break

    #######################################################
    label.configure(foreground='#011638', text=res_text[0])
    # label.configure(foreground='#011638', text=temp)
    uploaded = Image.open("Number Plate.jpg")
    im = ImageTk.PhotoImage(uploaded)
    plate_image.configure(image=im)
    plate_image.image = im
    plate_image.pack()
    plate_image.place(x=900, y=400)


def show_classify_button(file_path):
    classify_b = Button(top, text="Classify Image",
                        command=lambda: classify(file_path), padx=10, pady=5)
    classify_b.configure(background='#364156',
                         foreground='white', font=('arial', 15, 'bold'))
    classify_b.place(x=800, y=600)


def upload_image():
    try:
        file_path = filedialog.askopenfilename()
        uploaded = Image.open(file_path)
        uploaded.thumbnail(
            ((top.winfo_width()/2.25), (top.winfo_height()/2.25)))
        im = ImageTk.PhotoImage(uploaded)
        sign_image.configure(image=im)
        sign_image.image = im
        label.configure(text='')
        show_classify_button(file_path)
    except:
        pass


upload = Button(top, text="Upload an image",
                command=upload_image, padx=10, pady=5)
upload.configure(background='#364156', foreground='white',
                 font=('arial', 15, 'bold'))
upload.pack()
upload.place(x=410, y=600)
# sign_image.pack(side=BOTTOM,expand=True)
sign_image.pack()
sign_image.place(x=170, y=200)

# label.pack(side=BOTTOM,expand=True)
label.pack()
label.place(x=800, y=220)
#heading = Label(top,image=img)
# heading.configure(background='#CDCDCD',foreground='#364156')
# heading.pack()
top.mainloop()
