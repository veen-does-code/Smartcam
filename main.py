import customtkinter as ctk
from PIL import Image
import cv2 
import os

app =ctk.CTk()
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
app.geometry("1536x864") 
app.title("SmartCam")
capture_btn = ctk.CTkButton(app,text="capture",text_color="black")
capture_btn.pack(pady=20)

view_btn = ctk.CTkButton(app,text="View Images",text_color="black")
view_btn.pack(pady=20)

delete_btn = ctk.CTkButton(app,text="Delete",text_color="black")
delete_btn.pack(pady=20)





app.mainloop()