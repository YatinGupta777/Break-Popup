import time
from win32api import GetSystemMetrics
import schedule
import time
from datetime import datetime
import pyglet
from win32api import GetMonitorInfo, MonitorFromPoint
import os

monitor_info = GetMonitorInfo(MonitorFromPoint((0, 0)))
monitor_area = monitor_info.get("Monitor")
work_area = monitor_info.get("Work")
taskbar_height = monitor_area[3]-work_area[3]

print("Tasks Scheduled")
Width = GetSystemMetrics(0)
Height = GetSystemMetrics(1)

percentage_width = Width * 10/100
percentage_height = Height * 10/100
popup_width = int(percentage_width)
popup_height = int(percentage_height)
text_width = popup_width

eye_interval = 10
eye_message = " Keep Blinking "

water_drinking_interval = 20
water_drinking_message = " Stay Hydrated "

time_to_destroy_popup = 12  # Replace with number of seconds you want

LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)

# loads the icons
icon_location = 'C:/Users/yatigupta/Documents/Arpit/Batch/icon1.jpg'
gif_location = 'C:/Users/yatigupta/Documents/Arpit/Batch/'
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
f = open("C:/Users/yatigupta/Documents/Arpit/Batch/gifs.txt", "r")

'''Drinking water variables'''
water_gif_name = f.readline()
water_gif_name = water_gif_name.split("=", 1)[1]
water_gif_name = water_gif_name.strip()


water_animation = pyglet.image.load_animation(gif_location + water_gif_name)
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

animation_distance = 200 # Also can be seen as time taken for window to come up in (1/60) seconds

'''Neck Movement'''
window_movement = 1
upwards = True
stay = 4 * 60 # Specify number of seconds for popup to stay before * sign
def drinking_popupmsg(msg):
	
	global window_movement 

	w = water_animSprite.width + text_width
	h = water_animSprite.height
	 
	popup_position_width = Width - w 
	popup_position_height = Height - h - taskbar_height

	water_animSprite.position = (water_animSprite.width,0) # Position is relative to window

	window = pyglet.window.Window(width=w, height=h)
	 
	r,g,b,alpha = 0, 0, 0, 0
	 
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

	x, y = window.get_location()
	window.set_location(popup_position_width, popup_position_height + animation_distance) 

	window.set_icon(*icons)
	window.set_caption(msg)
	@window.event
	def on_draw():
	    window.clear()
	    water_animSprite.draw()
	    label.draw()
	 
	def close(event):
	    window.close()

	
	window_movement = 1
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

	# Call update 60 times a second	
	pyglet.clock.schedule_interval(update, 1/60.)
	pyglet.clock.schedule_once(close, time_to_destroy_popup)
	pyglet.app.run()

window_movement = 1
upwards = True
stay = 4 * 60
def blinking_popupmsg(msg):
	
	w = blink_animSprite.width + text_width
	h = blink_animSprite.height
	 
	popup_position_width = Width - w 
	popup_position_height = Height - h - taskbar_height


	blink_animSprite.position = (blink_animSprite.width,0)

	window = pyglet.window.Window(width=w, height=h)
	 
	r,g,b,alpha = 100, 100, 240, 0
	 
	label = pyglet.text.Label(msg, color = (0, 90, 0, 255),
	                          font_name='Arial',
	                          font_size=13,
	                          x=window.width//2, y=window.height//2,
	                          anchor_x='right', anchor_y='center', bold=True)

	# label = pyglet.text.HTMLLabel(
	#     '<font face="Times New Roman" size="4" style="background-color: #FFFF00">{msg}</font>'.format(msg=msg),
	#     x=window.width//2, y=window.height//2,
	#     anchor_x='center', anchor_y='center') 
	 
	pyglet.gl.glClearColor(r, g, b, alpha)

	x, y = window.get_location()
	window.set_location(popup_position_width, popup_position_height) 

	window.set_icon(*icons)
	window.set_caption(msg)
	@window.event
	def on_draw():
	    window.clear()
	    blink_animSprite.draw()
	    label.draw()
	 
	def close(event):
	    window.close()

	pyglet.clock.schedule_once(close, time_to_destroy_popup)
	pyglet.app.run()


schedule.every(eye_interval).minutes.do(blinking_popupmsg,eye_message)
schedule.every(water_drinking_interval).minutes.do(drinking_popupmsg,water_drinking_message)

def neck_popupmsg(msg):
	
	w = blink_animSprite.width + text_width
	h = blink_animSprite.height
	 
	popup_position_width = Width - w 
	popup_position_height = Height - h - taskbar_height


	window = pyglet.window.Window(width=w, height=h)
	 
	r,g,b,alpha = 100, 100, 240, 0
	 
	label = pyglet.text.Label(msg, color = (0, 90, 0, 255),
	                          font_name='Arial',
	                          font_size=13,
	                          x=window.width//2, y=window.height//2,
	                          anchor_x='left', anchor_y='center', bold=True)

	# label = pyglet.text.HTMLLabel(
	#     '<font face="Times New Roman" size="4" style="background-color: #FFFF00">{msg}</font>'.format(msg=msg),
	#     x=window.width//2, y=window.height//2,
	#     anchor_x='center', anchor_y='center') 
	 
	pyglet.gl.glClearColor(r, g, b, alpha)

	x, y = window.get_location()
	window.set_location(popup_position_width, popup_position_height) 

	window.set_icon(*icons)
	window.set_caption(msg)
	@window.event
	def on_draw():
	    window.clear()
	    blink_animSprite.draw()
	    label.draw()
	 
	def close(event):
	    window.close()

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
  #  time.sleep(300)


#C:/Users/yatigupta/Documents/Arpit/Batch/giphy.gif
