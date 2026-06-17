import customtkinter as ctk
from PIL import Image
import cv2 
import os

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

capture_btn = ctk.CTkButton(right_frame,text="Capture",text_color="black",width=180,height=50)
capture_btn.pack(pady=(300,20))

view_btn = ctk.CTkButton(right_frame,text="View Images",text_color="black",width=180,height=50)
view_btn.pack(pady=20)

delete_btn = ctk.CTkButton(right_frame,text="Delete",text_color="black",width=180,height=50,fg_color="red")
delete_btn.pack(pady=20)



app.mainloop()