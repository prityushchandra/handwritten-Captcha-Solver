import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import Image
from PIL import ImageTk
import create_menu
import time
from tkinter.filedialog import askopenfile
from tkinter import filedialog as tkFileDialog
import cv2
import numpy as np

def f(x): return x
class FullScreenApp(object):
	def __init__(self, master, **kwargs):
		self.master=master
		padx=145
		pady=720
		self._geom='200x200+0+0'
		#master.geometry("{0}x{1}+0+0".format(master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
		master.geometry("{0}x{1}+360+40".format(master.winfo_screenwidth() - pady, master.winfo_screenheight() - padx))
		master.bind('<Escape>',self.toggle_geom)
	def toggle_geom(self,event):
		geom=self.master.winfo_geometry()
		print(geom,self._geom)
		self.master.geometry(self._geom)
		self._geom=geom

def run_progressbar():
	progress_bar['maximum']=100
	for i in range(101):
		time.sleep(0.01)
		progress_bar['value']=i
		progress_bar.update()


root = tk.Tk(className='Captcha Solver')
app=FullScreenApp(root)

image = Image.open("logimages/covid.jpeg")
photo = ImageTk.PhotoImage(image)
# create_menu.icon_background(root,photo)
canvas = Canvas(root, width = 850, height = 600)
canvas.pack()
canvas.create_image(0,0, anchor=NW, image=photo)
Label(root,text='Loading MODEL Have Patience....',font='Didot',bg='AntiqueWhite1',fg='RED').pack()

progress_bar=ttk.Progressbar(root,orient='horizontal',length=500,mode='determinate')
progress_bar.pack(padx=20,pady=10,ipadx=10,ipady=1)
Label(root,text="",font='Didot',bg='AntiqueWhite1',fg='RED',command=run_progressbar())#.pack(padx=20,pady=10,ipadx=10,ipady=10)

for i in range(10):
	time.sleep(.01)
Label(root,text="Welcome to Captcha Solver",font='Didot',bg='AntiqueWhite1',fg='black').pack(padx=20,pady=10,ipadx=10,ipady=10)

root.after(2300,lambda: root.destroy())
root.mainloop()

main_window=tk.Tk(className='Captcha Solver')
main_window.resizable(False,False)
create_menu.create_menu_bar(main_window)


Label(main_window,text="NOTE: Hey Become Sure That Final Background of Image Must Be White with black text",font='Didot',bg='AntiqueWhite1',fg='black').grid(row=0,column=0,padx=10,pady=5,ipadx=10,ipady=0)
Label(main_window,text="NOTE: If somehow u don't get white bg try to adjust bg slider",font='Didot',bg='AntiqueWhite1',fg='black').grid(row=1,column=0,padx=10,pady=5,ipadx=10,ipady=0)
Label(main_window,text="NOTE: Adjust the adjust_me slider to get good thresholding if default ones don't work",font='Didot',bg='AntiqueWhite1',fg='black').grid(row=2,column=0,padx=10,pady=5,ipadx=10,ipady=0)
Label(main_window,text="NOTE: Use erosion and dilation slider to remove bg noise",font='Didot',bg='AntiqueWhite1',fg='black').grid(row=3,column=0,padx=10,pady=5,ipadx=10,ipady=0)
Label(main_window,text="NOTE: After adjusting sliders press s to predict the output",font='Didot',bg='AntiqueWhite1',fg='black').grid(row=4,column=0,padx=10,pady=5,ipadx=10,ipady=0)

# Label(main_window,text="Change background either 0 or 1 to achieve above",font='Didot',bg='AntiqueWhite1',fg='black').grid(row=2,column=0,padx=20,pady=10,ipadx=10,ipady=0)
def highlight(text):
	img=np.zeros((300,900,3),np.uint8)
	cv2.putText(img,text,(20,120),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),2)
	cv2.putText(img,"U can also predict text written with colored",(1,230),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),1)
	cv2.putText(img,"ink but for that adjust sliders accordingly to",(1,260),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),1)
	cv2.putText(img,"get good threshold reverse bg slider if bg comes black",(1,290),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),1)

	cv2.imshow('predict',img)

def take_from_gallery():

	path = tkFileDialog.askopenfilename()
		# ensure a file path was selected
	if len(path) > 0:

		cv2.namedWindow('tune')
		cv2.moveWindow('tune',20,300)

		cv2.createTrackbar('lowH', 'tune', 0, 179, f)
		cv2.createTrackbar('upH', 'tune', 179, 179, f)
		cv2.createTrackbar('lowS', 'tune', 0, 255, f)
		cv2.createTrackbar('upS', 'tune', 255, 255, f)
		cv2.createTrackbar('adjust_me', 'tune', 180, 255, f)
		cv2.createTrackbar('upV', 'tune', 255, 255, f)
		cv2.createTrackbar('erosion', 'tune', 0, 50, f)
		cv2.createTrackbar('dilation', 'tune', 0, 50, f)
		cv2.createTrackbar('bg', 'tune', 1, 1, f)

		while(1):
			img=cv2.resize(cv2.imread(path),(400,200))

			hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
			ilowH=cv2.getTrackbarPos('lowH','tune')
			iupH=cv2.getTrackbarPos('upH','tune')
			ilowS=cv2.getTrackbarPos('lowS','tune')
			iupS=cv2.getTrackbarPos('upS','tune')
			ilowV=cv2.getTrackbarPos('adjust_me','tune')
			iupV=cv2.getTrackbarPos('upV','tune')
			eros=cv2.getTrackbarPos('erosion','tune')
			dil=cv2.getTrackbarPos('dilation','tune')
			background=cv2.getTrackbarPos('bg','tune')

			lower=np.array([ilowH,ilowS,ilowV])
			upper=np.array([iupH,iupS,iupV])


			mask=cv2.inRange(hsv,lower,upper)

			kernel=np.ones((2,2),np.uint8)

			mask=cv2.dilate(mask, kernel, iterations=dil)#use this to remove bg noise from text

			mask=cv2.erode(mask, kernel, iterations=eros)#use this to focus on text`
			if background==1:
				mask=mask
			else:
				mask=255-mask
			cv2.imshow('mask',mask)



			k=cv2.waitKey(1)
			##########__Above code is just for GUI development___######
			##########__here is our final program__############
			if k==ord('s'):
				cv2.destroyAllWindows()
				mask=cv2.resize(mask,(2400,800))
				cv2.imwrite('logimages/mask.png',mask)
				from main import final_pred as fp
				text=fp('logimages/mask.png')
				highlight(text)
				print text
				break
			#########__if u want to see all functions used open main.py__#######
			if k==ord('q'):
				cv2.destroyAllWindows()
				break



main_window.configure(background='AntiqueWhite1')
plot_detail=tk.LabelFrame(main_window,text='Captcha prediction',font='Didot',width=450,highlightcolor='pink',highlightbackground='pink',bd=30,bg='green')
plot_detail.grid(row=5,column=0,padx=20,pady=10)
Label(plot_detail,text='Take captcha image',bg='green',fg='RED',font='Didot').grid(row=0,column=0,pady=10,padx=10)
button=tk.Button(plot_detail,bg='black',command=take_from_gallery,font='courier',activebackground='blue',activeforeground='red',text='TAKE FROM GALLERY',width=30,height=2).grid(row=2,column=0,padx=5,pady=5)
main_window.mainloop()
