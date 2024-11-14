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
print(mini, maxi, len(lista))

class Encoder:
    def __init__(self, rot_a, rot_b):
        self.a = Pin(rot_a, mode = Pin.IN, pull = Pin.PULL_UP)
        self.b = Pin(rot_b, mode = Pin.IN, pull = Pin.PULL_UP)
        self.fifo = Fifo(30, typecode = 'i')
        self.a.irq(handler = self.handler, trigger = Pin.IRQ_RISING, hard = True)
        
    def handler(self, pin):
        if self.b():
            self.fifo.put(-1)
        else:
            self.fifo.put(1)

rot = Encoder(10, 11)

while True:
    while rot.fifo.has_data():
        suunta=rot.fifo.get()
        if suunta == 1 and not position>=1000:
            oled.fill(0)
            for x in range(127):
                oled.pixel(x,int(((lista[position+x]-mini)/(maxi-mini))*64),1)
            position+=1
            oled.show()
            print(position)
            
        elif suunta == -1 and not position<=0:
            oled.fill(0)
            for x in range(127):
                oled.pixel(x,int(((lista[position+x]-mini)/(maxi-mini))*64),1)
            position-=1
            oled.show()
            print(position)