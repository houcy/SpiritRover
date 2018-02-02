''' This program is to explore the i2c bus on the SpiritRover Kit.

Original Source:  http://forum.plumgeek.com/viewtopic.php?f=18&t=6575

The SpiritRover i2c bus looks like:

pi@spirit_rover:~ $ sudo i2cdetect -y 1
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- 1c -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- 32 -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- 6b -- -- -- --
70: -- -- -- -- -- -- -- --

0x32 is the PIC microprocessor.

'''
from __future__ import print_function
import smbus
import time

bus = smbus.SMBus(1)
address = 0x32
reg_buzzer = 41
serv_def_value = 90
serv_values = [150, 150, 150]
reg_serv_values = [52, 53, 54]
serv_inc_value = 10
x = 0
direction = 1  # 0 for dec and 1 for inc


def writeBytes(value, reg_val):
    bus.write_i2c_block_data(address, reg_val, value)
    return -1


def writeByte(value, reg_val):
    bus.write_byte_data(address, reg_val, value)
    return -1


def readNumber(reg_val):
    number = bus.read_byte_data(address, reg_val)
    return number


def highbyte(num):
    hex_num = hex(num >> 8)
    dec_num = int(hex_num, 16)
    return dec_num


def lowbyte(num):
    hex_num = hex(num & 0xFF)
    dec_num = int(hex_num, 16)
    return dec_num


def playbuzzer(freq):
    data = [highbyte(freq), lowbyte(freq)]
    writeBytes(data, reg_buzzer)


while False:
    time.sleep(1)
#   playbuzzer(1000)
#   time.sleep(1)
#   playbuzzer(0)
    if(direction == 1):
        serv_values[x % 3] = serv_values[x % 3] + serv_inc_value
    else:
        serv_values[x % 3] = serv_values[x % 3] - serv_inc_value
    if(serv_values[2] >= 180):
        direction = 0
    elif(serv_values[2] <= 1):
        direction = 1
    writeByte(serv_values[x % 3], reg_serv_values[x % 3])
    print(serv_values)
    x = x + 1
