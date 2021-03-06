# intro notes here
# created by, etc...


# instead of tweet, email or post value incase of power outage or reboot and a way to add to total
# add temp, date, time to bottom


# Imports ======================================================================================================================
import os
import time
import math
import logging
import pygame, sys
from pygame.locals import *
import RPi.GPIO as GPIO
from flowmeter import *
from beerinfo import *


# GPIO Setup ===================================================================================================================
GPIO.setmode(GPIO.BCM) # use real GPIO numbering
GPIO.setup(23,GPIO.IN, pull_up_down=GPIO.PUD_UP) # Left Tap
GPIO.setup(24,GPIO.IN, pull_up_down=GPIO.PUD_UP) # Middle Tap
GPIO.setup(25,GPIO.IN, pull_up_down=GPIO.PUD_UP) # Right Tap
# Flow Meter Wiring: Red = 5-24VDC, Black = Ground, Yellow = GPIO Pin


# Initialize Pygame ============================================================================================================
pygame.init()


# Display Window Setup =========================================================================================================
VIEW_WIDTH = 800 # my numbers 800, original number 1024
VIEW_HEIGHT = 600 # my numbers 600, original number 576
pygame.display.set_caption('KayserSosa Kegberry')


# Hide the Mouse ===============================================================================================================
pygame.mouse.set_visible(False) # only use with pi


# Flow Meters Setup ============================================================================================================
flowMeter1 = FlowMeter('gallon', ["beer"]) # Left Tap
flowMeter2 = FlowMeter('gallon', ["beer"]) # Middle Tap
flowMeter3 = FlowMeter('gallon', ["beer"]) # Right Tap
# Change input to one of the following for different readings: liter, gallon, pint


# Colors Setup =================================================================================================================
BLACK = (0,0,0)
WHITE = (255,255,255)
TGREEN = (80, 200, 100) # PC Terminal Green

# Text Color for each beer
BEER1Text = TGREEN
BEER2Text = WHITE
BEER3Text = WHITE

# Text Backgroud Color for each beer
BEER1Bg = BLACK
BEER2Bg = BLACK
BEER3Bg = BLACK


# Window Surface Setup =========================================================================================================
screen = pygame.display.set_mode((VIEW_WIDTH,VIEW_HEIGHT), FULLSCREEN, 32) # use fullscreen for pi only
windowInfo = pygame.display.Info()

#screen = pygame.display.set_mode((VIEW_WIDTH,VIEW_HEIGHT)) # use for windows testing only
FONTSIZE = 48 # may not be needed
LINEHEIGHT = 28 # may not be needed
screenfont = pygame.font.SysFont(None, FONTSIZE) # may not be needed


# Backgrounds Setup ============================================================================================================
background = pygame.image.load('Beer-Background.jpg')
#maybe rotating backgrounds? if possible


# Word Wrap ====================================================================================================================
# draw some text into an area of a surface, automatically wraps words, returns any text that didn't get blitted

# may not need, or need to review
#def drawText(surface, text, color, rect, font, aa=False, bkg=None):
#	rect = Rect(rect)
#	y = rect.top
#	lineSpacing = -2
 
	# get the height of the font
#	fontHeight = font.size("Tg")[1]
 
#	while text:
#		i = 1
 
		# determine if the row of text will be outside our area
 #       if y + fontHeight > rect.bottom:
#			break
 
        # determine maximum width of line
#       while font.size(text[:i])[0] < rect.width and i < len(text):
#			i += 1
 
        # if we've wrapped the text, then adjust the wrap to the last word      
#       if i < len(text): 
#			i = text.rfind(" ", 0, i) + 1
 
        # render the line and blit it to the surface
#        if bkg:
#			image = font.render(text[:i], 1, color, bkg)
#			image.set_colorkey(bkg)
#        else:
#			image = font.render(text[:i], aa, color)
 
#        surface.blit(image, (rect.left, y))
#        y += fontHeight + lineSpacing
 
        # remove the text we just blitted
#        text = text[i:]
 
#return text


# Rendering ====================================================================================================================
def renderThings(flowMeter1, flowMeter2, flowMeter3, screen, screenfont, 
	pint, mug, pilsner, weizen, flute, tulip, snifter, goblet,
	beer1name, beer1style, beer1OG, beer1ibu, beer1abv, beer1glass, beer1glasspic,
	beer2name, beer2style, beer2OG, beer2ibu, beer2abv, beer2glass, beer2glasspic,
	beer3name, beer3style, beer3OG, beer3ibu, beer3abv, beer3glass, beer3glasspic):

	# Clear the screen
	screen.blit(background,(0,0))

	#text edits
	#https://pygame-zero.readthedocs.io/en/latest/ptext.html
	
	# Beer 1 Details - Left Tap ================================================================================================
	
	# Beer 1 Tap
	screenfont = pygame.font.SysFont(None, 60)
	screenfont.set_underline(1)
	rendered = screenfont.render("Left Tap", True, BEER1Text, BEER1Bg)
	screen.blit(rendered, (0, 0))
	
	# Beer 1 Poured
	if flowMeter1.enabled:
		text = screenfont.render(flowMeter1.getFormattedTotalPour(), True, BEER1Text, BEER1Bg)
		textRect = text.get_rect()
		screen.blit(text, (0, 60))
				
	# Beer 1 Name
	screenfont = pygame.font.SysFont(None, 40)
	rendered = screenfont.render(beer1name, True, BEER1Text, BEER1Bg)
	screen.blit(rendered, (0, 120))
		
	# Beer 1 Separator Line
	screenfont = pygame.font.SysFont(None, 20)
	rendered = screenfont.render('================================', True, BEER1Text, BEER1Bg)
	screen.blit(rendered, (0, 160))
		
	# Beer 1 Style
	screenfont = pygame.font.SysFont(None, 35)
	rendered = screenfont.render(beer1style, True, BEER1Text, BEER1Bg)
	screen.blit(rendered, (0, 185))
	
	# Beer 1 Original Gravity (OG)
	screenfont = pygame.font.SysFont(None, 35)
	rendered = screenfont.render(beer1OG, True, BEER1Text, BEER1Bg)
	screen.blit(rendered, (0, 220))
	
	# Beer 1 International Bittering Units (IBU)
	screenfont = pygame.font.SysFont(None, 35)
	rendered = screenfont.render(beer1ibu, True, BEER1Text, BEER1Bg)
	screen.blit(rendered, (0, 255))
	
	# Beer 1 Alcohol / Volume (ABV)
	screenfont = pygame.font.SysFont(None, 35)
	rendered = screenfont.render(beer1abv, True, BEER1Text, BEER1Bg)
	screen.blit(rendered, (0, 290))
	
	# Beer 1 Glass
	screenfont = pygame.font.SysFont(None, 35)
	rendered = screenfont.render(beer1glass, True, BEER1Text, BEER1Bg)
	screen.blit(rendered, (0, 325))
	screen.blit(beer1glasspic, (0, 360))

	
	# Beer 2 Details - Middle Tap ==============================================================================================
	
	#https://stackoverflow.com/questions/34013119/pygame-text-anchor-right
	# justify center
	
	# Beer 2 Tap
	screenfont = pygame.font.SysFont(None, 60)
	screenfont.set_underline(1)
	rendered = screenfont.render("Middle Tap", True, BEER2Text, BEER2Bg)
	screen.blit(rendered, (266, 0))

	# Beer 2 Poured
	if flowMeter2.enabled:
		text = screenfont.render(flowMeter2.getFormattedTotalPour(), True, BEER2Text, BEER2Bg)
		textRect = text.get_rect()
		screen.blit(text, (266, 60))
				
	# Beer 2 Name
	screenfont = pygame.font.SysFont(None, 40)
	rendered = screenfont.render(beer2name, True, BEER2Text, BEER2Bg)
	screen.blit(rendered, (266, 120))
		
	# Beer 2 Separator Line
	screenfont = pygame.font.SysFont(None, 20)
	rendered = screenfont.render('================================', True, BEER2Text, BEER2Bg)
	screen.blit(rendered, (266, 160))
		
	# Beer 2 Style
	screenfont = pygame.font.SysFont(None, 35)
	rendered = screenfont.render(beer2style, True, BEER2Text, BEER2Bg)
	screen.blit(rendered, (266, 185))
	
	# Beer 2 Original Gravity (OG)
	screenfont = pygame.font.SysFont(None, 35)
	rendered = screenfont.render(beer2OG, True, BEER2Text, BEER2Bg)
	screen.blit(rendered, (266, 220))
	
	# Beer 2 International Bittering Units (IBU)
	screenfont = pygame.font.SysFont(None, 35)
	rendered = screenfont.render(beer2ibu, True, BEER2Text, BEER2Bg)
	screen.blit(rendered, (266, 255))
	
	# Beer 2 Alcohol / Volume (ABV)
	screenfont = pygame.font.SysFont(None, 35)
	rendered = screenfont.render(beer2abv, True, BEER2Text, BEER2Bg)
	screen.blit(rendered, (266, 290))
	
	# Beer 2 Glass
	screenfont = pygame.font.SysFont(None, 35)
	rendered = screenfont.render(beer2glass, True, BEER2Text, BEER2Bg)
	screen.blit(rendered, (266, 325))
	screen.blit(beer2glasspic, (266, 360))
	
	# Beer 3 Details - Right Tap ===============================================================================================
	
	#https://stackoverflow.com/questions/34013119/pygame-text-anchor-right
	#justify right
	
	# Beer 3 Tap
	screenfont = pygame.font.SysFont(None, 60)
	screenfont.set_underline(1)
	rendered = screenfont.render("Right Tap", True, BEER3Text, BEER3Bg)
	screen.blit(rendered, (532, 0))

	# Beer 3 Poured
	if flowMeter3.enabled:
		text = screenfont.render(flowMeter3.getFormattedTotalPour(), True, BEER3Text, BEER3Bg)
		textRect = text.get_rect()
		screen.blit(text, (532, 60))
				
	# Beer 3 Name
	screenfont = pygame.font.SysFont(None, 40)
	rendered = screenfont.render(beer3name, True, BEER3Text, BEER3Bg)
	screen.blit(rendered, (532, 120))
		
	# Beer 3 Separator Line
	screenfont = pygame.font.SysFont(None, 20)
	rendered = screenfont.render('================================', True, BEER3Text, BEER3Bg)
	screen.blit(rendered, (532, 160))
		
	# Beer 3 Style
	screenfont = pygame.font.SysFont(None, 35)
	rendered = screenfont.render(beer3style, True, BEER3Text, BEER3Bg)
	screen.blit(rendered, (532, 185))
	
	# Beer 3 Original Gravity (OG)
	screenfont = pygame.font.SysFont(None, 35)
	rendered = screenfont.render(beer3OG, True, BEER3Text, BEER3Bg)
	screen.blit(rendered, (532, 220))
	
	# Beer 3 International Bittering Units (IBU)
	screenfont = pygame.font.SysFont(None, 35)
	rendered = screenfont.render(beer3ibu, True, BEER3Text, BEER3Bg)
	screen.blit(rendered, (532, 255))
	
	# Beer 3 Alcohol / Volume (ABV)
	screenfont = pygame.font.SysFont(None, 35)
	rendered = screenfont.render(beer3abv, True, BEER3Text, BEER3Bg)
	screen.blit(rendered, (532, 290))
	
	# Beer 3 Glass
	screenfont = pygame.font.SysFont(None, 35)
	rendered = screenfont.render(beer3glass, True, BEER3Text, BEER3Bg)
	screen.blit(rendered, (532, 325))
	screen.blit(beer2glasspic, (532, 360))

	#https://stackoverflow.com/questions/34013119/pygame-text-anchor-right
	#justiry right testing
	
	screenfont = pygame.font.SysFont(None, 35)
	rendered = screenfont.render("right justified?", True, BEER3Text, BEER3Bg)
	newrendered = rendered.get_rect(right=(532, 600)
	#newrendered.right = 500
	screen.blit(rendered, newrendered)
	
	
	
	
	

	
	# Kegerator Temp ===========================================================================================================
	# right justified temp
	
	# Date / Time ==============================================================================================================
	screenfont = pygame.font.SysFont(None, 35)
	rendered = screenfont.render(time.strftime("%I:%M:%S %p - %Y/%m/%d"), True, WHITE, BLACK)
	screen.blit(rendered, (0, 575))
	# may be wrong due to internet blocking, unblock and try
	
	
	# Display everything
	pygame.display.flip()

    
#what is this doing? =======================================================================================================
  
# Beer, on Pin 23.
def doAClick1(channel):
  currentTime = int(time.time() * FlowMeter.MS_IN_A_SECOND)
  if flowMeter1.enabled == True:
    flowMeter1.update(currentTime)

# Beer, on Pin 24.
def doAClick2(channel):
  currentTime = int(time.time() * FlowMeter.MS_IN_A_SECOND)
  if flowMeter2.enabled == True:
    flowMeter2.update(currentTime)

# Beer, on Pin 25.
def doAClick3(channel):
  currentTime = int(time.time() * FlowMeter.MS_IN_A_SECOND)
  if flowMeter3.enabled == True:
    flowMeter3.update(currentTime)

GPIO.add_event_detect(23, GPIO.RISING, callback=doAClick1, bouncetime=20) # Beer, on Pin 23
GPIO.add_event_detect(24, GPIO.RISING, callback=doAClick2, bouncetime=20) # Beer, on Pin 24
GPIO.add_event_detect(25, GPIO.RISING, callback=doAClick3, bouncetime=20) # Beer, on Pin 24


# Main Never Ending Loop =======================================================================================================
while True:
	# Handle keyboard events
	for event in pygame.event.get():
		if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
			GPIO.cleanup()
			pygame.quit()
			sys.exit()
		elif event.type == KEYUP and event.key == K_1:
			flowMeter1.enabled = not(flowMeter1.enabled)
		elif event.type == KEYUP and event.key == K_2:
			flowMeter2.enabled = not(flowMeter2.enabled)
		elif event.type == KEYUP and event.key == K_3:
			flowMeter3.enabled = not(flowMeter3.enabled)
		elif event.type == KEYUP and event.key == K_8:
			flowMeter1.clear()
		elif event.type == KEYUP and event.key == K_9:
			flowMeter2.clear()
		elif event.type == KEYUP and event.key == K_0:
			flowMeter3.clear()
  
	currentTime = int(time.time() * FlowMeter.MS_IN_A_SECOND)
  
	# reset flow meter after each pour (2 secs of inactivity)
	if (flowMeter1.thisPour <= 0.23 and currentTime - flowMeter1.lastClick > 2000):
		flowMeter1.thisPour = 0.0
    
	if (flowMeter2.thisPour <= 0.23 and currentTime - flowMeter2.lastClick > 2000):
		flowMeter2.thisPour = 0.0
		
	if (flowMeter3.thisPour <= 0.23 and currentTime - flowMeter3.lastClick > 2000):
		flowMeter3.thisPour = 0.0

	# Update the screen
	renderThings(flowMeter1, flowMeter2, flowMeter3, screen, screenfont, 
		pint, mug, pilsner, weizen, flute, tulip, snifter, goblet,
		beer1name, beer1style, beer1OG, beer1ibu, beer1abv, beer1glass, beer1glasspic,
		beer2name, beer2style, beer2OG, beer2ibu, beer2abv, beer2glass, beer2glasspic,
		beer3name, beer3style, beer3OG, beer3ibu, beer3abv, beer3glass, beer3glasspic)
