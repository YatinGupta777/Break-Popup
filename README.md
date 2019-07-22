# Break-Popup
import tkinter as tk
import time
from tkinter import *
import tkinter.messagebox
from win32api import GetSystemMetrics
import schedule
import time
from datetime import datetime
import pyglet
from win32api import GetMonitorInfo, MonitorFromPoint

monitor_info = GetMonitorInfo(MonitorFromPoint((0,0)))
monitor_area = monitor_info.get("Monitor")
work_area = monitor_info.get("Work")
taskbar_height = monitor_area[3]-work_area[3]
#from pyglet.window import Platform

#monitor = Platform().get_default_display().get_default_screen()
Width = GetSystemMetrics(0)
Height = GetSystemMetrics(1)
print("width" + str(Width))
print("Height" + str(Height))
percentage_width = Width * 10/100
percentage_height = Height * 10/100
popup_width = int(percentage_width)
popup_height = int(percentage_height)

print(str(popup_width) +"x" + str(popup_height) +"+" + str(popup_width) + "+" + str(popup_height))

eye_interval = 1/10
eye_message = "Blink"

water_drinking_interval = 2/10
water_drinking_message = "Stay Hydrated"

time_to_destroy_popup = 20 * 1000 # Replace 10 with number of seconds you want

LARGE_FONT= ("Verdana", 12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)

water_animation = pyglet.image.load_animation('C:/Users/yatigupta/Documents/Arpit/Batch/source.gif')
water_animSprite = pyglet.sprite.Sprite(water_animation)
	 
scale_x = min(popup_width,water_animSprite.width)/max(popup_width,water_animSprite.width)
scale_y = min(popup_height,water_animSprite.height)/max(popup_height,water_animSprite.height)

water_animSprite.scale = max(scale_x,scale_y)

print("popup_width" + str(popup_width))
print("popup_height" + str(popup_height))

print("water_animSprite width" + str(water_animSprite.width))
print("water_animSprite height" + str(water_animSprite.height))

blinking_animation = pyglet.image.load_animation('C:/Users/yatigupta/Documents/Arpit/Batch/tenor (1).gif')
blink_animSprite = pyglet.sprite.Sprite(blinking_animation)
	 
scale_x =  min(popup_width,blink_animSprite.width)/max(popup_width,blink_animSprite.width)
scale_y = min(popup_height,blink_animSprite.height)/max(popup_height,blink_animSprite.height)

blink_animSprite.scale = max(scale_x,scale_y)


def drinking_popupmsg(msg):
	
	w = water_animSprite.width
	h = water_animSprite.height
	 
	popup_position_width = Width - w
	popup_position_height = Height - h - taskbar_height

	window = pyglet.window.Window(width=w, height=h)
	 
	r,g,b,alpha = 0.5,0.5,0.8,0.5
	 
	label = pyglet.text.Label(msg,color=(0,0,0,255),
	                          font_name='Times New Roman',
	                          font_size=10,
	                          x=window.width//2, y=window.height//2,
	                          anchor_x='center', anchor_y='center',bold=True) 
	 
	pyglet.gl.glClearColor(r,g,b,alpha)

	x, y = window.get_location()
	window.set_location(popup_position_width, popup_position_height) 

	@window.event
	def on_draw():
	    window.clear()
	    water_animSprite.draw()
	    label.draw()
	 
	def close(event):
	    window.close()

	pyglet.clock.schedule_once(close, 8.0)
	pyglet.app.run()

def blinking_popupmsg(msg):
	
	w = blink_animSprite.width
	h = blink_animSprite.height

	popup_position_width = Width - w
	popup_position_height = Height - h - taskbar_height
	 
	window = pyglet.window.Window(width=w, height=h)
	 
	r,g,b,alpha = 0.5,0.5,0.8,0.5
	 
	label = pyglet.text.Label(msg,color=(0,0,0,255),
	                          font_name='Times New Roman',
	                          font_size=10,
	                          x=window.width//2, y=window.height//2,
	                          anchor_x='center', anchor_y='center',bold=True) 
	 
	pyglet.gl.glClearColor(r,g,b,alpha)

	x, y = window.get_location()
	window.set_location(popup_position_width, popup_position_height) 

	@window.event
	def on_draw():
	    window.clear()
	    blink_animSprite.draw()
	    label.draw()
	 
	def close(event):
	    window.close()

	pyglet.clock.schedule_once(close, 8.0)
	pyglet.app.run()



#schedule.every(eye_interval).minutes.do(popupmsg,eye_message)
#schedule.every(water_drinking_interval).minutes.do(popupmsg,water_drinking_message)

drinking_popupmsg(water_drinking_message)
#blinking_popupmsg(eye_message)
# while True:
#     schedule.run_pending()
#     time.sleep(1)

#C:/Users/yatigupta/Documents/Arpit/Batch/giphy.gifBreak-Popup
