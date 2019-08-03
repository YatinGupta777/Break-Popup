import time
from win32api import GetSystemMetrics
import schedule
import pyglet
from win32api import GetMonitorInfo, MonitorFromPoint
import os
import ctypes
import win32gui
import win32api
from win32con import SWP_NOMOVE 
from win32con import SWP_NOSIZE 
from win32con import SW_HIDE
from win32con import SW_SHOW
from win32con import HWND_TOPMOST
from win32con import GWL_EXSTYLE 
from win32con import WS_EX_TOOLWINDOW

'''Functions to remove window from taskbar and keep it on top'''

def find_window(name):
    try:
        return win32gui.FindWindow(None, name)
    except win32gui.error:
        print("Error while finding the window")
        return None
#Remove python icon script from taskbar
def hide_from_taskbar(hw):
    try:
        win32gui.ShowWindow(hw, SW_HIDE)
        win32gui.SetWindowLong(hw, GWL_EXSTYLE,win32gui.GetWindowLong(hw, GWL_EXSTYLE)| WS_EX_TOOLWINDOW);
        win32gui.ShowWindow(hw, SW_SHOW);
    except win32gui.error:
        return None
#Keep screen on top
def set_topmost(hw):
    try:
        win32gui.SetWindowPos(hw, HWND_TOPMOST, 0,0,0,0, SWP_NOMOVE | SWP_NOSIZE)
    except win32gui.error:
       	return None


# To show program has started
print("Task Scheduled")

#Getting Taskbar Height
monitor_info = GetMonitorInfo(MonitorFromPoint((0, 0)))
monitor_area = monitor_info.get("Monitor")
work_area = monitor_info.get("Work")
taskbar_height = monitor_area[3]-work_area[3]

'''Getting screen dimensions'''
Width = GetSystemMetrics(0)
Height = GetSystemMetrics(1)

'''Assigning popup width'''
percentage_width = Width * 10/100
percentage_height = Height * 10/100
popup_width = int(percentage_width)
popup_height = int(percentage_height)
text_width = popup_width

'''Customising popups'''
eye_interval = 2/6
eye_message = " Keep Blinking "

water_drinking_interval = 1/6
water_drinking_message = " Stay Hydrated "

# loads the icons
icon_location = 'C:/Documents/Github/Break-Popup/icon.jpg'
gif_location = 'C:/Documents/Github/Break-Popup/'

icons = [
    # for the title bar
    pyglet.image.load(icon_location),

    # for the taskbar
    pyglet.image.load(icon_location),

    # Mac only
    pyglet.image.load(icon_location),

    # Mac only
    pyglet.image.load(icon_location)
]

'''Reading gifs from text file'''
f = open("C:/Documents/Github/Break-Popup/gifs.txt", "r")

'''Drinking water variables'''
water_gif_name = f.readline()
water_gif_name = water_gif_name.split("=", 1)[1]
water_gif_name = water_gif_name.strip()

water_animation = pyglet.image.load_animation(gif_location + water_gif_name)
# ANimation object that is used on window
water_animSprite = pyglet.sprite.Sprite(water_animation)
	 
scale_x = min(popup_width, water_animSprite.width)/max(popup_width, water_animSprite.width)
scale_y = min(popup_height, water_animSprite.height)/max(popup_height, water_animSprite.height)

water_animSprite.scale = max(scale_x, scale_y)

'''Eye Movement'''
eye_gif_name = f.readline()
eye_gif_name = eye_gif_name.split("=", 1)[1]
eye_gif_name = eye_gif_name.strip()

blinking_animation = pyglet.image.load_animation(gif_location + eye_gif_name)
blink_animSprite = pyglet.sprite.Sprite(blinking_animation)
	 
scale_x =  min(popup_width, blink_animSprite.width)/max(popup_width, blink_animSprite.width)
scale_y = min(popup_height, blink_animSprite.height)/max(popup_height, blink_animSprite.height)

blink_animSprite.scale = max(scale_x, scale_y)

animation_distance = 180 # Also can be seen as time taken for window to come up in (1/60) seconds

window_movement = 0
upwards = 0
stay = 0

def initialise_global_variables():
	global window_movement 
	global upwards
	global stay
	window_movement = 1
	upwards = True
	stay = 4 * 60 # Specify number of seconds for popup to stay before * sign
	return window_movement, upwards ,stay

window_movement, upwards ,stay= initialise_global_variables()
time_to_destroy_popup = 2*(animation_distance/60) + stay/60 + 2 # animation_distance and stay needs to be divided by 60 to
																# convert into seconds. +2 for proper functioning
def drinking_popupmsg(msg):
	
	global window_movement 
	global upwards
	global stay

	#Total window width and height
	w = water_animSprite.width + text_width
	h = water_animSprite.height
	 
	#Calculating position of popup where it will stay
	popup_position_width = Width - w 
	popup_position_height = Height - h - taskbar_height

	#water_animSprite is the gif animation
	water_animSprite.position = (water_animSprite.width,0) # Position is relative to window

	window = pyglet.window.Window(width=w, height=h)
	 
	#Background of window 
	r,g,b,alpha = 0, 0, 0, 0
	 
	#The text label 
	label = pyglet.text.Label(msg,color=(0,255,0,255),
	                          font_name='Arial',
	                          font_size=13,
	                          x=window.width//2, y=window.height//2,
	                          anchor_x='right', anchor_y='center', bold=True)

	label.width = text_width
	label.multiline = True
	# label = pyglet.text.HTMLLabel(
	#     '<font face="Times New Roman" size="4" style="background-color: #FFFF00">{msg}</font>'.format(msg=msg),
	#     x=window.width//2, y=window.height//2,
	#     anchor_x='center', anchor_y='center') 
	 
	pyglet.gl.glClearColor(r, g, b, alpha)

	#Keeping animation_distance from required popup height
	window.set_location(popup_position_width, popup_position_height + animation_distance) 

	#Icon and title of window
	window.set_icon(*icons)
	window.set_caption(msg)
	
	#Making window icon hidden from taskbar and keeping it on top of other windows
	hide_from_taskbar(find_window(msg))
	set_topmost(find_window(msg))

	window_movement, upwards, stay = initialise_global_variables()

	@window.event
	def on_draw():
	    window.clear()
	    water_animSprite.draw()
	    label.draw()

	#This function keep updating the window
	#Responsible for moving the window up and down    
	def update(dt):
		# Move  per second
		global window_movement 
		global upwards
		global stay
		window_y = popup_position_height + animation_distance - window_movement

		if (window_y == popup_position_height):
			upwards = False
			stay -=1
		#print(stay)
		if upwards:
			window.set_location(popup_position_width, window_y) 
			window_movement = window_movement + 1 #Printing this shows time in ((1/60)seconds) to come up
			#print (window_movement)
		elif stay == 0:
			window.set_location(popup_position_width, window_y) 
			window_movement = window_movement - 1
			#print (window_movement)
		#water_animSprite.x -=dt*10
		#water_animSprite.y -=dt*10
		#label.x -= dt*10

	def close(event):
	    window.close()
	    pyglet.clock.unschedule(update)
	# Call update 60 times a second
	
	pyglet.clock.schedule_interval(update, 1/60.)
	pyglet.clock.schedule_once(close, time_to_destroy_popup)
	pyglet.app.run()

def blinking_popupmsg(msg):
	
	global window_movement 
	global upwards
	global stay

	#Total window width and height
	w = blink_animSprite.width + text_width
	h = blink_animSprite.height
	 
	#Calculating position of popup where it will stay
	popup_position_width = Width - w 
	popup_position_height = Height - h - taskbar_height

	#water_animSprite is the gif animation
	blink_animSprite.position = (blink_animSprite.width,0) # Position is relative to window

	window = pyglet.window.Window(width=w, height=h)
	 
	#Background of window 
	r,g,b,alpha = 0, 0, 0, 0
	 
	#The text label 
	label = pyglet.text.Label(msg,color=(0,255,0,255),
	                          font_name='Arial',
	                          font_size=13,
	                          x=window.width//2, y=window.height//2,
	                          anchor_x='right', anchor_y='center', bold=True)

	# label = pyglet.text.HTMLLabel(
	#     '<font face="Times New Roman" size="4" style="background-color: #FFFF00">{msg}</font>'.format(msg=msg),
	#     x=window.width//2, y=window.height//2,
	#     anchor_x='center', anchor_y='center') 
	 
	pyglet.gl.glClearColor(r, g, b, alpha)

	#Keeping animation_distance from required popup height
	window.set_location(popup_position_width, popup_position_height + animation_distance) 

	#Icon and title of window
	window.set_icon(*icons)
	window.set_caption(msg)
	
	#Making window icon hidden from taskbar and keeping it on top of other windows
	hide_from_taskbar(find_window(msg))
	set_topmost(find_window(msg))

	window_movement, upwards, stay = initialise_global_variables()

	@window.event
	def on_draw():
	    window.clear()
	    blink_animSprite.draw()
	    label.draw()

	#This function keep updating the window
	#Responsible for moving the window up and down    
	def update(dt):
		# Move  per second
		global window_movement 
		global upwards
		global stay
		window_y = popup_position_height + animation_distance - window_movement

		if (window_y == popup_position_height):
			upwards = False
			stay -=1
		#print(stay)
		if upwards:
			window.set_location(popup_position_width, window_y) 
			window_movement = window_movement + 1 #Printing this shows time in ((1/60)seconds) to come up
			#print (window_movement)
		elif stay == 0:
			window.set_location(popup_position_width, window_y) 
			window_movement = window_movement - 1
			#print (window_movement)
		#water_animSprite.x -=dt*10
		#water_animSprite.y -=dt*10
		#label.x -= dt*10

	def close(event):
	    window.close()
	    pyglet.clock.unschedule(update)
	# Call update 60 times a second
	
	pyglet.clock.schedule_interval(update, 1/60.)
	pyglet.clock.schedule_once(close, time_to_destroy_popup)
	pyglet.app.run()

''' Task Scheduling'''
#schedule.every(eye_interval).minutes.do(blinking_popupmsg,eye_message)
#schedule.every(water_drinking_interval).minutes.do(drinking_popupmsg,water_drinking_message)

drinking_popupmsg(water_drinking_message)
#blinking_popupmsg(eye_message)
'''Keeping script running'''
#while True:
 #   schedule.run_pending()
  #  time.sleep(1)
