import imp
import time
import math
import RPi.GPIO as GPIO
import random
import minecraft
import block
import vec3

LED_ENABLE = 0
LED_DISABLE = 1
RGB_ENABLE = 1
RGB_DISABLE = 0

LED1 = 12
LED2 = 16
LED3 = 18
LED4 = 22
LED5 = 7
LED = [LED1,LED2,LED3,LED4,LED5]
RGB_RED = 11
RGB_GREEN = 13
RGB_BLUE = 15
RGB = [RGB_RED,RGB_GREEN,RGB_BLUE]
RANGE_GAP = 30

def led_setup():
	GPIO.setmode(GPIO.BOARD)
	for val in LED:
		GPIO.setup(val,GPIO.OUT)
	for val in RGB:
		GPIO.setup(val,GPIO.OUT)
	GPIO.output(RGB_RED,RGB_ENABLE)
def led_activate(led,colour):
	GPIO.output(led,LED_ENABLE)
def led_deactivate(led,colour):
	GPIO.output(led,LED_DISABLE)
def led_clear():
	for val in LED:
		GPIO.output(val,LED_DISABLE)
	for val in RGB:
		GPIO.output(val,RGB_DISABLE)
	GPIO.output(RGB_RED, RGB_ENABLE)
def placeTreasure():
	tb = vec3.Vec3(random.randint(-128,128), 80, random.randint(-128,128))
	tb.y = mc.getHeight(tb.x, tb.z)
	return tb
def distanceToTreasure(tb):
	p = mc.player.getPos();
	xd = tb.x - p.x
	zd = tb.z - p.z
	d = math.sqrt((xd**2) + (zd**2))
	return math.floor(d)
	
mc = minecraft.Minecraft.create()

mc.postToChat("Treasure Hunt starting!")
        
tl2 = placeTreasure()
mc.setBlock(tl2.x,tl2.y,tl2.z,block.CHEST)

print tl2.x
print tl2.y
print tl2.z
led_setup()
led_clear()
play = 0
timeStart = time.time()
while (play == 0):
	d2 = distanceToTreasure(tl2)
	print d2, tl2
	# Quick treasure check
	if d2 <= 2:
		# Is the chest still there?
		if mc.getBlock(tl2.x, tl2.y, tl2.z) == block.AIR:
			# replace it with Diamonds
			mc.setBlock(tl2.x, tl2.y, tl2.z, block.DIAMOND_BLOCK)
			elapsed = time.time() - timeStart
			mc.postToChat("Well done, you took " +str(elapsed) +" seconds")
			play = 1
	for i in range(0,5):
		iRange = (i) * RANGE_GAP
		if d2 <= iRange:
			led_activate(LED[i], RGB_RED)
		else:
			if d2 <= (iRange + RANGE_GAP):
				# flash this one
				delta = (d2-iRange) 
				led_activate(LED[i], RGB_RED)
				time.sleep (delta/100.0)		
				led_deactivate(LED[i], RGB_RED)
				time.sleep (delta/100.0)		
			else:
				led_deactivate(LED[i], RGB_RED)
