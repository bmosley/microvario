import gc
gc.collect()
import micropython
gc.collect()
import board
gc.collect()
import busio as io
gc.collect()
import adafruit_ssd1306
gc.collect()
import framebuf
gc.collect()
import bitmapfont
gc.collect()
import digitalio
gc.collect()
import time
gc.collect()
import adafruit_bmp280
gc.collect()
#import gfx
#gc.collect()

# init I2c on board
i2c = io.I2C(board.SCL, board.SDA)

## BMP280 ##
sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)

## OLED/ssd1306 ##
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=0x3c)

# pressure at sea level in San Jose, CA
# https://aviationweather.gov/adds/metars/index?submit=1&station_ids=KSJC&chk_metars=on&hoursStr=8&std_trans=translated
sensor.sea_level_pressure = 1019.40

# for console output
print('\nTemperature: {} degrees C'.format(sensor.temperature)) 
print('Pressure: {}hPa'.format(sensor.pressure))
print('Altitude: {} meters'.format(sensor.altitude))

# meters to feet
altitude_feet = sensor.altitude / .3048

altitude_oled = 'Alt: {} ft'.format(altitude_feet)
temp_oled = 'Tmp: {0:.2f} C'.format(sensor.temperature)
pressure_oled = 'Prs: {0:.0f} hPa'.format(sensor.pressure)

bf = bitmapfont.BitmapFont(128, 32, oled.pixel)
bf.init()

bf.text(altitude_oled, 0, 0, 100)
bf.text(temp_oled, 0, 10, 100)
bf.text(pressure_oled, 0, 20, 100)

#bf.text(line, 0, 28, 100)
oled.invert(False)
oled.show()

print("\nfree mem:", gc.mem_free())