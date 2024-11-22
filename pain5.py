from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time
from fifo import Fifo
import math
print(math.sin(30))

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
screen_width = 128
screen_height = 64
screen = SSD1306_I2C(screen_width, screen_height, i2c)


class mover:
    def __init__(self, x, y, rot_a, rot_b):
        self.x=x
        self.y=y
        self.a = Pin(rot_a, mode = Pin.IN, pull = Pin.PULL_UP)
        self.b = Pin(rot_b, mode = Pin.IN, pull = Pin.PULL_UP)
        self.fifo = Fifo(30, typecode = 'i')
        self.a.irq(handler = self.handler, trigger = Pin.IRQ_RISING, hard = True)
        self.press = Pin(12, mode = Pin.IN, pull = Pin.PULL_UP)
        self.direction=1
        
    def handler(self, pin):
        if self.b():
            self.fifo.put(-1)
        else:
            self.fifo.put(1)
        
    def move(self):
        if self.press.value()==0:
            screen.fill(0)
            self.x=64
            self.y=32
            
        if self.fifo.has_data():
            if self.fifo.get()==1:
                screen.pixel(int(self.x), int(self.y), 1)
                screen.show()
                self.x+=math.sin(self.direction)
                self.y+=math.cos(self.direction)
                self.direction-=0.3
            else:
                screen.pixel(int(self.x), int(self.y), 1)
                screen.show()
                self.x+=math.sin(self.direction)
                self.y+=math.cos(self.direction)
                self.direction+=0.3
                
        else:
                screen.pixel(int(self.x), int(self.y), 1)
                screen.show()
                self.x+=math.sin(self.direction)
                self.y+=math.cos(self.direction)
        
    def looper(self):
        while True:
            self.move()
            
move = mover(64,32, 10, 11)
move.looper()