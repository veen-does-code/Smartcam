import customtkinter as ctk
from PIL import Image
import cv2 as cv
import os
import mediapipe as mp
import sys
import math

app =ctk.CTk()
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")
app.geometry("1536x864") 
app.title("SmartCam")

app.grid_columnconfigure(0,weight=3)
app.grid_columnconfigure(1,weight=1)
app.grid_rowconfigure(0,weight=1)

left_frame=ctk.CTkFrame(master=app, fg_color="black")
left_frame.grid(row=0,column=0,sticky='nsew')

right_frame=ctk.CTkFrame(master=app,fg_color="white")
right_frame.grid(row=0,column=1,sticky='nsew')

camera_label = ctk.CTkLabel(left_frame,text="")
camera_label.pack(fill='both',expand=True)

web_cam=cv.VideoCapture(0)
face_mesh=mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)

latest_frame = None
x1,x2,x3,x4,y1,y2,y3,y4=0,0,0,0,0,0,0,0

def updat_cam():
    global latest_frame
    _,image=web_cam.read()
    image=cv.flip(image,1)
    image=cv.cvtColor(image,cv.COLOR_BGR2RGB)
    fh,fw,_=image.shape
    # cv.imshow("cam",image)
    # key=cv.waitKey(100)
    # if key==27:
    #     break 
    img = Image.fromarray(image)
    output = face_mesh.process(image)
    landmark_points = output.multi_face_landmarks
    if landmark_points:
        landmarks = landmark_points[0].landmark
        for id,landmark in enumerate(landmarks):
            x = int(landmark.x * fw)
            y = int(landmark.y * fh)
            if id==159:
                x1=x
                y1=y
            if id==145:
                x2=x
                y2=y
            if id==386:
                x3=x
                y3=y
            if id==374:
                x4=x
                y4=y
        distl = math.sqrt((x2-x1)**2+(y2-y1)**2)
        distr = math.sqrt((x4-x3)**2+(y4-y3)**2)
        distl = int(distl)
        distr = int(distr)
        print(distl,distr)
        if distl < 10 or distr < 10 :
            capt()
        

    
    ctk_img = ctk.CTkImage(light_image=img,dark_image=img,size=(800, 600))
    camera_label.configure(image=ctk_img)
    camera_label.image = ctk_img
    latest_frame = image.copy()
    app.after(10,updat_cam)

def on_close():
    web_cam.release()
    app.destroy()

x=1

def capt():
    global latest_frame
    global x
    if latest_frame is not None:
        cv.imwrite(f"captures/photo{x}.png",latest_frame)
        x+=1
        print("saved")

def view_images():
    files=os.listdir("captures")
    if not files:
        print("No images")

    window = ctk.CTkToplevel(app)
    window.geometry("600x600")
    window.title("Captured Images")

    scroll = ctk.CTkScrollableFrame(window)
    scroll.pack(expand=True,fill="both")

    row,column=0,0
    
    for file in files:
        card = ctk.CTkFrame(scroll)
        card.grid(row=row,column=column,padx=20,pady=20)

        img = Image.open(f"captures/{file}")
        img = ctk.CTkImage(light_image=img, dark_image=img, size=(200, 150))

        label = ctk.CTkLabel(card, text="", image=img)
        label.image = img
        label.pack(pady=20)

        delete_btn = ctk.CTkButton(card,text="Delete 🗑️",text_color="black",fg_color="red",font=("Arial",15,"bold"),command=lambda f=file,c=card:delete(f,c))
        delete_btn.pack(pady=10)

        column+=1
        if column==3:
            column=0
            row+=1

def delete(file,frame):
    os.remove(f"captures/{file}")
    frame.destroy()


capture_btn = ctk.CTkButton(right_frame,text="🔴",text_color="black",width=50,height=50,font=("Arial",15,"bold"),corner_radius=100,fg_color="black",command=capt)
capture_btn.pack(pady=(300,20))

view_btn = ctk.CTkButton(right_frame,text="View Images 📷",text_color="black",width=180,height=50,font=("Arial",15,"bold"),command=view_images)
view_btn.pack(pady=20)

app.protocol("WM_DELETE_WINDOW", on_close)
updat_cam()
app.mainloop()
