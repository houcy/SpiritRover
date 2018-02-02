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


class ServoCal(object):

    def __init__(self, minVal=45, center=90, maxVal=135):
        self.min = minVal
        self.center = center
        self.max = maxVal

    def setCalArray(self, cal_array):
        self.min = cal_array[0]
        self.center = cal_array[1]
        self.max = cal_array[2]


class Servo(object):

    def __init__(self, register, i2c_bus=1, PIC_address=0x32):
        self.i2c_bus = smbus.SMBus(i2c_bus)
        self.PIC_address = PIC_address
        self.cal = ServoCal()
        self.register = register
        self.state = None
        self.write_err_count = 0
        self.read_err_count = 0

    def writeByte(self, value):
        try:
            self.i2c_bus.write_byte_data(self.PIC_address,
                                         self.register, value)
            return 0
        except:
            self.write_err_count += 1
            self.writeByte(value)
            return self.write_err_count * -1

    def limitCheck(self, cmd):
        ''' clamp specified location value to limit
        if outside specified axis limits '''

        if cmd > self.cal.max:
            cmd = self.cal.max
        elif cmd < self.cal.min:
            cmd = self.cal.min
        return cmd

    def moveAbsolute(self, cmd):
        ''' Move to specific value w/ limit check '''
        cmd = self.limitCheck(cmd)
        self.writeByte(cmd)
        self.state = cmd
        return 0

    def moveTo(self, cmd):
        ''' Move to cal-center-relative position '''
        cmd = self.cal.center + cmd
        self.moveAbsolute(cmd)
        return 0

    def moveDelta(self, delta):
        ''' Move relative to current position'''
        self.moveAbsolute(self.state + delta)
        return 0

    def center(self):
        ''' Center specified axis to cal value'''
        self.moveTo(0)
        return 0


class PanTilt(object):

    def __init__(self):
        self.pan = Servo(53)
        self.pan.cal.setCalArray([30, 90, 150])
        self.tilt = Servo(52)
        self.tilt.cal.setCalArray([20, 110, 150])
        self.center()

    def vecMoveAbsolute(self, cmd_vec):
        ''' move both axes to specified locations '''
        self.pan.moveAbsolute(cmd_vec[0])
        self.tilt.moveAbsolute(cmd_vec[1])
        return 0

    def vecMoveTo(self, cmd_vec):
        ''' move both axes to cal-center-relative positions '''
        self.pan.moveTo(cmd_vec[0])
        self.tilt.moveTo(cmd_vec[1])
        return 0

    def vecMoveDelta(self, cmd_vec):
        ''' Move both axes relative to current position'''
        self.pan.moveDelta(cmd_vec[0])
        self.tilt.moveDelta(cmd_vec[1])
        return 0

    def center(self, axis='both'):
        ''' Center all axes to cal center values'''
        if axis == 'both':
            self.pan.center()
            self.tilt.center()
        else:
            getattr(self, axis).center()
        return 0

    def fullScan(self, pan_delta=15, tilt_delta=15, pause=0.5):
        self.pan.moveAbsolute(self.pan.cal.min)
        self.tilt.moveAbsolute(self.tilt.cal.min)

        while True:
            if (self.pan.state <= self.pan.cal.min) or \
                    (self.pan.state >= self.pan.cal.max):
                pan_delta = -pan_delta
            if (self.tilt.state >= self.tilt.cal.max) and \
               (self.pan.state >= self.pan.cal.max):
                self.center()
                break
            elif (self.pan.state >= self.pan.cal.max) or \
                 (self.pan.state <= self.pan.cal.min):
                self.tilt.moveDelta(tilt_delta)
                self.pan.moveDelta(pan_delta)
            else:
                self.pan.moveDelta(pan_delta)
                time.sleep(pause)


if __name__ == "__main__":
    pt = PanTilt()
    pt.fullScan()
