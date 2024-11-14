from machine import Pin
from fifo import Fifo
from filefifo import Filefifo
from machine import UART, Pin, I2C, Timer, ADC
from ssd1306 import SSD1306_I2C
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

data = Filefifo(10, name = 'capture_250Hz_01.txt')

position=0
lista=[]
for x in range(1000):
    lista.append(data.get())
print(lista)
maxi=max(lista)
mini=min(lista)
print(mini, maxi)

"""
class testiclass:

    def testi2(self):
        oled.fill(0)
        oled.text("1", 0, 0, 1)
        oled.show()

testiob = testiclass()
testiob.testi2()

for x in range(1):
    print(data.get())
    
            #oled.fill(0)
            #oled.text("723", 0, 0, 1)
            #oled.show()
"""

class Encoder:
    def __init__(self, rot_a, rot_b):
        self.a = Pin(rot_a, mode = Pin.IN, pull = Pin.PULL_UP)
        self.b = Pin(rot_b, mode = Pin.IN, pull = Pin.PULL_UP)
        self.fifo = Fifo(30, typecode = 'i')
        self.a.irq(handler = self.handler, trigger = Pin.IRQ_RISING, hard = True)
        
    def handler(self, pin):
        if self.b():
            varis=oled.fill(1)
            self.fifo.put(-1)

        else:
            self.fifo.put(1)

rot = Encoder(10, 11)

while True:
    if rot.fifo.has_data():
        #print(rot.fifo.get())
        
        if rot.fifo.get() == 1 and not position>=100:
            oled.fill(0)
            for x in range(127):
                oled.pixel(x,int(((lista[position+x]-mini)/(maxi-mini))*64),1)
            position+=1
            oled.show()
            print(position)
            
        elif not position<=0:
            oled.fill(0)
            for x in range(127):
                oled.pixel(x,int(((lista[position+x]-mini)/(maxi-mini))*64),1)
            position-=1
            oled.show()
            print(position)

