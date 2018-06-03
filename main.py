import gc
gc.collect()
import board
gc.collect()
import busio as io
gc.collect()
import adafruit_ssd1306
gc.collect()
import bitmapfont
gc.collect()
import time
gc.collect()
import adafruit_bmp280
gc.collect()
#import gfx
#gc.collect()
# needed?
#import framebuf
#gc.collect()0
import pulseio
gc.collect()

# debug mode
debug = False

# init I2c on board
i2c = io.I2C(board.SCL, board.SDA)
gc.collect()

## BMP280 ##
sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
gc.collect()

## OLED/ssd1306 ##
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=0x3c)
gc.collect()

## Piezo
# tones to play
TONE_FREQ = [ 262,  # C4
              294,  # D4
              330,  # E4
              #349,  # F4
              #392,  # G4
              440,  # A4
              #494,  # B4
              262,  # C3
              530, ] # C4

buzzer = pulseio.PWMOut(board.D4, variable_frequency=True)
buzzer.frequency = 440

DUTY_OFF = 0
DUTY_ON = 2**15

# pressure at sea level in San Jose, CA
# https://aviationweather.gov/adds/metars/index?submit=1&station_ids=KSJC&chk_metars=on&hoursStr=8&std_trans=translated
sensor.sea_level_pressure = 1019.40
gc.collect()

# for console output
if debug:
    print('\nTemperature: {} degrees C'.format(sensor.temperature)) 
    print('Pressure: {}hPa'.format(sensor.pressure))
    print('Altitude: {} meters'.format(sensor.altitude))
    gc.collect()
    ### OLED bounds - bottom left/right, top left/right
    oled.pixel(0, 31, 100)
    oled.pixel(127, 31, 100)
    oled.pixel(0, 0, 100)
    oled.pixel(127, 0, 100)
    gc.collect()
    # free mem
    print("\nfree mem:", gc.mem_free())

bf = bitmapfont.BitmapFont(128, 32, oled.pixel)
bf.init()

def welcome():
    oled.fill(0)
    bf.text("   - MicroVario - ", 0, 0, 100)
    bf.text("version 0.1", 0, 12, 100)
    bf.text("bmosley - 2018", 0, 22, 100)
    oled.show()
    # Startup tune
    buzzer.duty_cycle = DUTY_ON

    for i in range(len(TONE_FREQ)):
        buzzer.frequency = TONE_FREQ[i]
        time.sleep(.1)

    buzzer.duty_cycle = DUTY_OFF
    
    time.sleep(3)
    gc.collect
    return

# welcome to your doom
welcome()

# set timer to 0
oled_timer = 0

def data_display():
    global oled_timer
    oled_timer = 0
    # BMP280 stores current value in mem. for more accurate readings, read once to dump to console
    #sensor_dump = sensor.altitude

    # meters to feet
    altitude_feet = sensor.altitude / .3048
    
    altitude_oled = 'Alt: {0:.3f} ft'.format(altitude_feet)
    temp_oled = 'Tmp: {0:.2f} C'.format(sensor.temperature)
    pressure_oled = 'Prs: {0:.0f} hPa'.format(sensor.pressure)
    oled.fill(0)
    bf.text(altitude_oled, 0, 0, 100)
    bf.text(temp_oled, 0, 13, 100)
    bf.text(pressure_oled, 0, 25, 100)
    oled.show()
    gc.collect
    
    return


# Init display first
data_display()

current_alt = sensor.altitude
TONE = TONE_FREQ[3]

while True:
    print(TONE)
    while sensor.altitude > (current_alt + 0.2):
        TONE = TONE + 2
        buzzer.duty_cycle = DUTY_ON
        buzzer.frequency = TONE
        current_alt = sensor.altitude
        lift = True
        
    while sensor.altitude < (current_alt - 0.2):
        TONE = TONE - 2
        buzzer.duty_cycle = DUTY_ON
        buzzer.frequency = TONE
        current_alt = sensor.altitude
        
    while (sensor.altitude - .1) <= sensor.altitude <= (sensor.altitude + .1):
        buzzer.duty_cycle = DUTY_OFF
    
    
'''
while True:
    oled_timer = oled_timer + 1
    if oled_timer == 60:
        data_display()
    
    if (sensor.altitude) > (current_alt):
        print("{}------UP".format(current_alt))

    elif (sensor.altitude) < (current_alt):
        print("{}------DOWN".format(current_alt))

    else:
        print("{}~".format(current_alt))
    
    current_alt = round(sensor.altitude, 1)
   
    #print(oled_timer)
    #print(sensor.altitude)
'''

# free mem
print("\nfree mem:", gc.mem_free())