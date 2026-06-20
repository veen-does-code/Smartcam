import customtkinter as ctk
from PIL import Image
import cv2 as cv
import os
import mediapipe as mp
import sys

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

latest_frame = None

def updat_cam():
    global latest_frame
    _,image=web_cam.read()
    image=cv.flip(image,1)
    image=cv.cvtColor(image,cv.COLOR_BGR2RGB)
    # cv.imshow("cam",image)
    # key=cv.waitKey(100)
    # if key==27:
    #     break 
    img = Image.fromarray(image)

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

    latest = sorted(files)[-1]
    path = os.path.join("captures", latest)

    img = Image.open(path)
    img = ctk.CTkImage(light_image=img, dark_image=img, size=(500, 400))

    window = ctk.CTkToplevel(app)
    window.geometry("600x450")
    window.title("Captured Images")

    label = ctk.CTkLabel(window, text="", image=img)
    label.image = img
    label.pack(pady=20)

capture_btn = ctk.CTkButton(right_frame,text="🔴",text_color="black",width=50,height=50,font=("Arial",15,"bold"),corner_radius=100,fg_color="black",command=capt)
capture_btn.pack(pady=(300,20))

view_btn = ctk.CTkButton(right_frame,text="View Images 📷",text_color="black",width=180,height=50,font=("Arial",15,"bold"),command=view_images)
view_btn.pack(pady=20)

delete_btn = ctk.CTkButton(right_frame,text="Delete 🗑️",text_color="black",width=180,height=50,fg_color="red",font=("Arial",15,"bold"))
delete_btn.pack(pady=20)

app.protocol("WM_DELETE_WINDOW", on_close)
updat_cam()
app.mainloop()