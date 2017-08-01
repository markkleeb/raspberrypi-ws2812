# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import time, threading
from time import sleep
#------sudo pip install pyOSC------------#
import OSC
from neopixel import *

# LED strip configuration:
LED_COUNT      = 75      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering



strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
strip.begin()

c = OSC.OSCServer(('192.168.0.111', 4000))
c.addDefaultHandlers()

def printing_handler(addr, tags, stuff, source):
    print "---"
    print "received new osc msg from %s" % OSC.getUrlStr(source)
    print "with addr : %s" % addr
    print "typetags %s" % tags
    print "data %s" % stuff
    print "---"
    leds = stuff[0].split('\\')
    print leds
    sleep(2)



def update_leds(addr, tags, stuff, source):
		
	#print ('update leds')
	for i in range(strip.numPixels()):
                r = stuff[i*3+0]
                g = stuff[i*3+1]
                b = stuff[i*3+2]
                #print r
                #print g
                #print b
		strip.setPixelColorRGB(i, r, g, b)
                strip.show()



c.addMsgHandler("/print", printing_handler) # adding our function
c.addMsgHandler("/leds", update_leds)



# just checking which handlers we have added
print "Registered Callback-functions are :"
for addr in c.getOSCAddressSpace():
    print addr


# Start OSCServer
print "\nStarting OSCServer. Use ctrl-C to quit."
st = threading.Thread( target = c.serve_forever )
st.start()


try :
    while 1 :
        time.sleep(5)

except KeyboardInterrupt :
    print "\nClosing OSCServer."
    c.close()
    print "Waiting for Server-thread to finish"
    st.join() ##!!!
    print "Done"

# Main program logic follows:
#if __name__ == '__main__':

	# Create NeoPixel object with appropriate configuration.
	#strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
	# Intialize the library (must be called once before other functions).
	#strip.begin()
	
	#setup your OSC receiver here

	#print ('Press Ctrl-C to quit.')
	#while True:
		#print ('update leds')
		#for i in range(strip.numPixels()):
		#r = oscMessage[0]
		#g = oscMessage[1]
		#b = oscMessage[2]
		#print r
		#print g
		#print b

			#strip.setPixelColorRGB(i, r, g, b)
    		#strip.show()
