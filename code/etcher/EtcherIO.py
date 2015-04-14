# -*- coding: utf-8 -*- 

import serial
import time
import socket
import select
import threading
import os

# status constants
OFF =  0
ON =  1
CLOSED =   1
OPEN =   0
# RTU command for 深圳昶为科技有限公司
# for MR D 0808 or MR DO16
READ_COIL   = 1
READ_DI     = 2     # not for MR DO 16
SINGLE_WRITE_DO = 5
MULTI_WRITE_DO = 15

# for MR AI 08
# 1. command
READ_AI_INPUT   =  4
READ_AI_HOLD    =  3
WRITE_AI_HOLD   = 16
# 2. register address
INPUT_REG   = 30340
FILTER_REG  = 30341
# 3. Parameters
SIGNAL_TYPE     = 0   # 1: 1~5V; 0: 0~5V;
FILTER_METHOD   = 0   # 0: No filter; 1: Average; 2: Low pass

# for MR AO 08
SINGLE_WRITE_AO =  6
MULTI_WRITE_AO  = 16
SINGLE_READ_AO  =  3


# RS485 address
DO1_Addr = 0x03   # MR DO 16 KN
DO2_Addr = 0x04   # MR M0808 D
DI1_Addr = 0x04   # MR M0808 KN

AI1_Addr = 0x02   # MR AI08
AO1_Addr = 0x01   # MR AO08

MotorDrv1_Addr = 11 # M4505 for throttle valve
MotorDrv2_Addr = 12 # M6505 for robot arm

RF_Addr = 21    # RF power generator


MFC_FULL_SCALE = 5.0
MFC_ADC_WIDTH = 4095.0

FlushTime = 20    # in ms, time to flush loadlock
PumpTime = 60    # in ms, time to pump down loadlock
RobotTime = 5    # in ms, robot traval time from cvd to ll or reversed.


ValveList = {
    "Ar":   "V00",
    "CO2":  "V01",
    "O2":   "V02",
    "CF4":  "V03",
    "SF6":  "V04",
    "Feed": "V10",
    "Leak": "V13",
    "Angl": "V14",
    "Vacu": "V15",
    "Film": "V16",
    "Isol": "V09",
    "TPVa": "V05",
    "Gate": "V0B",
    "Pins": "V0A"
    }

Valve_Addr = {
    'V00':   [DO1_Addr,0x00],
    'V01':   [DO1_Addr,0x01],
    'V02':   [DO1_Addr,0x02],
    'V03':   [DO1_Addr,0x03],
    'V04':   [DO1_Addr,0x04],
    'V05':   [DO1_Addr,0x05],
    'V06':   [DO1_Addr,0x06],
    'V07':   [DO1_Addr,0x07],
    'V08':   [DO1_Addr,0x08],
    'V09':   [DO1_Addr,0x09],
    'V0A':   [DO1_Addr,0x0A],
    'V0B':   [DO1_Addr,0x0B],
    'V0C':   [DO1_Addr,0x0C],
    'V0D':   [DO1_Addr,0x0D],
    'V0E':   [DO1_Addr,0x0E],
    'V0F':   [DO1_Addr,0x0F],
    'V10':   [DO1_Addr,0x10], # no real valve connected
    'V11':   [DO2_Addr,0x00],
    'V12':   [DO2_Addr,0x01],
    'V13':   [DO2_Addr,0x02],
    'V14':   [DO2_Addr,0x03],
    'V15':   [DO2_Addr,0x04],
    'V16':   [DO2_Addr,0x05],
    'V17':   [DO2_Addr,0x06], # no real valve connected
    'V18':   [DO2_Addr,0x07], # no real valve connected
}

MFC_Addr = {
    'Ar':   [AO1_Addr,AI1_Addr,0,100.0,30100],
    'CO2':  [AO1_Addr,AI1_Addr,1,100.0,30140],
    'O2':   [AO1_Addr,AI1_Addr,5,100.0,30180],
    'CF4':  [AO1_Addr,AI1_Addr,3,100.0,30220],
    'SF6':  [AO1_Addr,AI1_Addr,4,100.0,30260],
    'Film':    [AO1_Addr,AI1_Addr,7,100,30300],
    'Loadlock':[AO1_Addr,AI1_Addr,5,100,30340],
    'CVD_High':[AO1_Addr,AI1_Addr,2,100,30380],
    'CVD_Low': [AO1_Addr,AI1_Addr,2,100,30420]
}

Gauge_Addr = {
    
}
Motor_Addr = {
    'Throttle': [MotorDrv1_Addr],
    'Robot':    [MotorDrv2_Addr]
}

# CRC16 function
table =[  0x0000, 0xC0C1, 0xC181, 0x0140, 0xC301, 0x03C0, 0x0280, 0xC241,
          0xC601, 0x06C0, 0x0780, 0xC741, 0x0500, 0xC5C1, 0xC481, 0x0440,
          0xCC01, 0x0CC0, 0x0D80, 0xCD41, 0x0F00, 0xCFC1, 0xCE81, 0x0E40,
          0x0A00, 0xCAC1, 0xCB81, 0x0B40, 0xC901, 0x09C0, 0x0880, 0xC841,
          0xD801, 0x18C0, 0x1980, 0xD941, 0x1B00, 0xDBC1, 0xDA81, 0x1A40,
          0x1E00, 0xDEC1, 0xDF81, 0x1F40, 0xDD01, 0x1DC0, 0x1C80, 0xDC41,
          0x1400, 0xD4C1, 0xD581, 0x1540, 0xD701, 0x17C0, 0x1680, 0xD641,
          0xD201, 0x12C0, 0x1380, 0xD341, 0x1100, 0xD1C1, 0xD081, 0x1040,
          0xF001, 0x30C0, 0x3180, 0xF141, 0x3300, 0xF3C1, 0xF281, 0x3240,
          0x3600, 0xF6C1, 0xF781, 0x3740, 0xF501, 0x35C0, 0x3480, 0xF441,
          0x3C00, 0xFCC1, 0xFD81, 0x3D40, 0xFF01, 0x3FC0, 0x3E80, 0xFE41,
          0xFA01, 0x3AC0, 0x3B80, 0xFB41, 0x3900, 0xF9C1, 0xF881, 0x3840,
          0x2800, 0xE8C1, 0xE981, 0x2940, 0xEB01, 0x2BC0, 0x2A80, 0xEA41,
          0xEE01, 0x2EC0, 0x2F80, 0xEF41, 0x2D00, 0xEDC1, 0xEC81, 0x2C40,
          0xE401, 0x24C0, 0x2580, 0xE541, 0x2700, 0xE7C1, 0xE681, 0x2640,
          0x2200, 0xE2C1, 0xE381, 0x2340, 0xE101, 0x21C0, 0x2080, 0xE041,
          0xA001, 0x60C0, 0x6180, 0xA141, 0x6300, 0xA3C1, 0xA281, 0x6240,
          0x6600, 0xA6C1, 0xA781, 0x6740, 0xA501, 0x65C0, 0x6480, 0xA441,
          0x6C00, 0xACC1, 0xAD81, 0x6D40, 0xAF01, 0x6FC0, 0x6E80, 0xAE41,
          0xAA01, 0x6AC0, 0x6B80, 0xAB41, 0x6900, 0xA9C1, 0xA881, 0x6840,
          0x7800, 0xB8C1, 0xB981, 0x7940, 0xBB01, 0x7BC0, 0x7A80, 0xBA41,
          0xBE01, 0x7EC0, 0x7F80, 0xBF41, 0x7D00, 0xBDC1, 0xBC81, 0x7C40,
          0xB401, 0x74C0, 0x7580, 0xB541, 0x7700, 0xB7C1, 0xB681, 0x7640,
          0x7200, 0xB2C1, 0xB381, 0x7340, 0xB101, 0x71C0, 0x7080, 0xB041,
          0x5000, 0x90C1, 0x9181, 0x5140, 0x9301, 0x53C0, 0x5280, 0x9241,
          0x9601, 0x56C0, 0x5780, 0x9741, 0x5500, 0x95C1, 0x9481, 0x5440,
          0x9C01, 0x5CC0, 0x5D80, 0x9D41, 0x5F00, 0x9FC1, 0x9E81, 0x5E40,
          0x5A00, 0x9AC1, 0x9B81, 0x5B40, 0x9901, 0x59C0, 0x5880, 0x9841,
          0x8801, 0x48C0, 0x4980, 0x8941, 0x4B00, 0x8BC1, 0x8A81, 0x4A40,
          0x4E00, 0x8EC1, 0x8F81, 0x4F40, 0x8D01, 0x4DC0, 0x4C80, 0x8C41,
          0x4400, 0x84C1, 0x8581, 0x4540, 0x8701, 0x47C0, 0x4680, 0x8641,
          0x8201, 0x42C0, 0x4380, 0x8341, 0x4100, 0x81C1, 0x8081, 0x4040,]

def tcrchware(data,accum):
    crc = ( (accum >> 8 ) & 0x00ff ) ^ table[ ( accum ^ data ) & 0x00ff ]
    return crc


class PID:
    """
    Discrete PID control
    """

    def __init__(self, P=2.0, I=0.0, D=1.0, Derivator=0, Integrator=0, Integrator_max=500, Integrator_min=-500):

        self.Kp=P
        self.Ki=I
        self.Kd=D
        self.Derivator=Derivator
        self.Integrator=Integrator
        self.Integrator_max=Integrator_max
        self.Integrator_min=Integrator_min

        self.set_point=0.0
        self.error=0.0

    def update(self,current_value):
        """
        Calculate PID output value for given reference input and feedback
        """

        self.error = self.set_point - current_value

        self.P_value = self.Kp * self.error
        self.D_value = self.Kd * ( self.error - self.Derivator)
        self.Derivator = self.error

        self.Integrator = self.Integrator + self.error

        if self.Integrator > self.Integrator_max:
            self.Integrator = self.Integrator_max
        elif self.Integrator < self.Integrator_min:
            self.Integrator = self.Integrator_min

        self.I_value = self.Integrator * self.Ki

        PID = self.P_value + self.I_value + self.D_value

        return PID

    def setPoint(self,set_point):
        """
        Initilize the setpoint of PID
        """
        self.set_point = set_point
        self.Integrator=0
        self.Derivator=0

    def setIntegrator(self, Integrator):
        self.Integrator = Integrator

    def setDerivator(self, Derivator):
        self.Derivator = Derivator

    def setKp(self,P):
        self.Kp=P

    def setKi(self,I):
        self.Ki=I

    def setKd(self,D):
        self.Kd=D

    def getPoint(self):
        return self.set_point

    def getError(self):
        return self.error

    def getIntegrator(self):
        return self.Integrator

    def getDerivator(self):
        return self.Derivator
    
class COMOperator(object):  

    def __init__(self,log, portname = '/dev/ttyUSB1', baudrate = 9600,timeout = 0.1):
        #foundport = self.findport()
        #if foundport <> '':
        i = 0
        while True:
            portname = '/dev/ttyUSB%s'%i
            try:
                self.port = serial.Serial(portname, baudrate, timeout =   1)
                break
            except Exception as ex:
                if i > 9:
                    log.warn('COM error:%s'%ex)
                    quit()
                else:
                    i += 1
                    continue
        self.readReady= threading.Event()
        self.readReady.set()
        self.isbusy = threading.Event()
        self.log = log
        self.log.info('COM %s is initilized, opened?%s'%(self.port.name,self.port.isOpen()))
        self.ComEnabled = False
        self.isbusy.clear()
    def get_crc(self,s):
        '''Function to do CRC16 by table index

        come from :
        input : [byte1,byte2,byte3,byte4]
        return:[byte1,byte2,byte3,byte4,CRC16_Low,CRC16_High]
        '''
        remainder = -1
        slen = len(s)
        for i in range(slen):
            remainder = ( (remainder >> 8 ) & 0x00ff ) ^ \
                table[ ( remainder ^ s[i] ) & 0x00ff ]

        s.append(remainder & 0x00ff)
        s.append(remainder >>   8 & 0xff)
        for i in range(len(s)):
            s[i]=chr(s[i])
        buf=''.join(s)
        return buf  

    def findport(self):
        ports = list(serial.tools.listports.comports())
        pp = ''
        for p in ports:
            if 'ttyUSB' in p[ 1 ]:
                return p[ 0 ]

    def dRead( self,device_addr,io_addr ):
        buf = self.readCOM()
        return buf

    def writeCOM(self,databytes):        
        
        while self.isbusy.isSet():
            time.sleep(0.02)
        
        self.isbusy.set()
        buf = self.get_crc(databytes)
        self.port.write(buf)
        
        data = ''
        for i in buf:
            data += ' %X' % ord(i)
        self.log.debug('Sent %s bytes: %s' % (len(buf),data))
        self.isbusy.clear()
        return True

    def readCOM(self, size=100):
        """Read size bytes from the serial port. If a timeout is set it may
           return less characters as requested. With no timeout it will block
           until the requested number of bytes is read."""

        self.log.debug('Going to read bytes' )
        i = 0
        x = 0
        while not self.readReady.isSet():
            time.sleep(0.02)
            i += 1
            if i > 50 : 
                self.log.debug('Read bytes timeout' )
                return False,[]
        self.readReady.clear()
        self.isbusy.set()
        read = ''
        read_data = []
        inp = None
        validdata = False
        if size > 0:
            x = self.port.inWaiting()
            self.log.debug('%s bytes in buffer' % x)
            while x > 0:# if there is bytes already in input bufffer, read it first
                read_data.append(ord(self.port.read(1)))
                if len(read_data) > 2:
                    crc = read_data
                    crcl = crc[-2]
                    crch = crc[-1]
                    crc = self.get_crc( crc[0:-2] )
                
                    if crch  == ord(crc[ -1 ]) and crcl == ord(crc[ -2 ]): # return if valid data
                        self.log.debug('Valid %s bytes data' % len(crc))
                        self.isbusy.clear()
                        self.readReady.set()
                        return True,crc
                x = self.port.inWaiting()
                self.log.debug('%s bytes in buffer' % x)
                
            while len(read_data) < size:
                
                ready,_,_ = select.select([self.port.fd],[],[], self.port.timeout)

                if not ready:
                    self.log.debug('Reading timeout by select')
                    self.isbusy.clear()
                    self.readReady.set()
                    return False,[]# timeout
                buf = os.read(self.port.fd, size-len(read))

                read += buf
                self.log.debug('Read %s bytes data by select' % (len(buf)))

                for i in buf:
                    read_data.append(ord(i))
                    if len(read_data) > 2: # if the read bytes is valid, just return
                        crc = read_data
                        crcl = crc[-2]
                        crch = crc[-1]
                        crc = self.get_crc( crc[0:-2] )
                    
                        if crch  == ord(crc[ -1 ]) and crcl == ord(crc[ -2 ]):
                            self.log.debug('Valid %s bytes data' % len(crc))
                            self.isbusy.clear()
                            self.readReady.set()
                            return True, crc
                
                if self.port.timeout >= 0 and not buf:
                    self.isbusy.clear()
                    self.readReady.set()
                    return False,[]

            self.readReady.set()
            self.isbusy.clear()
            ret_str = ''
            if len(crc) == 0:
                ret_str = 'None'
            else:
                for i in crc:
                    ret_str = ret_str + '%X' % ord( i )
            self.log.warn('Recieved %s bytes data: %s (Invalid)' % (len(read_data),ret_str))
            return False,read_data
'''
            if len(read_data) < 5 :
                self.log.warn('Read %s failed' % self.port.name  )
                return False,None

##            crc = []
##            
##            for i in read_data:
##                crc.append(ord(i))
            #self.log.debug('Recieved %s bytes data: %s ' % (len(read_data),read_data))
            crc = read_data
            crcl = crc[-2]
            crch = crc[-1]
            crc = self.get_crc( crc[0:-2] )

            if crch  == ord(crc[ -1 ]) and crcl == ord(crc[ -2 ]):
                ret_data = []
                for i in crc:
                    ret_data.append(str(i))  
                return True,ret_data
            else:
                ret_str = ''
                for i in crc:
                    ret_str = ret_str + %X' % i
                self.log.warn('Recieved %s bytes data: %s (Invalid)' % (len(read_data),ret_str))
                return False,read_data
           
'''

class Gauge(object):
    def __init__(self,id,port):

        self.id = id
        self.rAddr = Gauge_Addr[id][0]
        self.ch =    Gauge_Addr[id][1]
        self.port = port

        #self.configAIMode()

        self.port.log.info("Gauge %s is initilized !"%self.id)

    def configAIMode(self):
        for i in Gauge_Addr.keys():
            s = [self.rAddr,WRITE_AI_HOLD,(Gauge_Addr[i][3] >> 8 ) % 256, \
                 Gauge_Addr[i][3] % 256,0,1,2,0,SIGNAL_TYPE]
            if not self.port.writeCOM(s):
                self.port.log.warn('Failed to configure MFC %s !'%(self.id))

    def updateData(self):
        ret =  0
        s = [self.rAddr,READ_AI_INPUT,0, 5,0,3]
        self.port.writeCOM(s)
        ret,data = self.port.readCOM(15)
        if ret and len(data) > 5:
            if ord( data[1] ) == 4:
                keys = Gauge_Addr.keys()
                vals = {}
                for i in keys:
                    hb = ord(data[(Gauge_Addr[i][1] - 5 )*2 + 3] )
                    lb = ord(data[(Gauge_Addr[i][1] - 5 )*2 + 4] )
                    vals[i] =  ( hb *256 + lb )/4095.0 
                    self.port.log.info("Gauge %s data %s:%s"% (i,hb,lb))
                return True,vals
        elif ret and len(data) == 5:
            self.port.log.warn("Gauges COM error, code: %X"% ord(data[2]))
        else:
            self.port.log.warn("COM timeout error!")
        return False, None

class Valve(object):

    def __init__(self,id,port,init2closed = True):

        self.id = id
        self.addr = Valve_Addr[id][0]
        self.bit = Valve_Addr[id][1]
        self.port = port

        #if init2closed :
        self.close()
        #else:
            #self.open()
        self.port.log.info("Valve %s is initilized AS IS!"% (self.id))
    def open(self):
        s=[self.addr, SINGLE_WRITE_DO, 0x00, self.bit, 0xFF, 0x00]
        if self.port.writeCOM( s ):
            ret,buf = self.port.readCOM()
            if ret and len(buf) > 5:
                if ord(buf[ 4 ]) > 0:
                    self.port.log.info('Open valve %s SUCCESSFULLY'%self.id)
                    return True
                else:
                    self.port.log.warn('Try to open valve % FAILED'%self.id)
                    return False

    def close(self,ret = False):
        s=[self.addr, SINGLE_WRITE_DO, 0x00, self.bit, 0x00, 0x00]
        if self.port.writeCOM( s ):
            ret,buf = self.port.readCOM()
            if ret and len(buf) >   5:
                if ord(buf[ 4 ]) > 0:
                    self.port.log.warn('Try to close valve % FAILED'%self.id)
                    return False
                else:
                    self.port.log.info('Close valve %s SUCCESSFULLY'%self.id)
                    return True           

    def isOpen(self):
        s=[self.addr, READ_COIL, 0x00, self.bit, 0x00,   1]
        if self.port.writeCOM(s):
            ret,buf = self.port.readCOM()
            if ret and len(buf) >   5:
                if ord(buf[ 3 ]) > 0:
                    self.port.log.info('VALVE:%s is OPENED'%self.id)
                    return True
                else:
                    self.port.log.info('VALVE:%s is CLOSEED'%self.id)
                    return False
            self.port.log.warn('Error while reading valve %s'%self.id)
        return False


class MFC(object):
    def __init__(self,id, port):
        self.id = id
        self.wAddr = MFC_Addr[id][0]
        self.rAddr = MFC_Addr[id][1]
        self.ch = MFC_Addr[id][2]
        self.port = port
        #self.readParas()
        #self.configAOMode()
        #self.configAIMode()
        #self.setFlow(0)
        self.zeroinit()
    def zeroinit(self):
        s = [self.wAddr,MULTI_WRITE_AO,0,0,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.port.writeCOM(s)
        ret,retData = self.port.readCOM()
        retStr = []
        try:
            for i in retData:
                retStr.append ('%X'%ord(i))
            self.port.log.debug('Zeroinit AO returned %s'% (retStr))
        except Exception as ex:
            self.port.log.warn('Zeroinit AO error: %s' %(ex))      
            
    def readParas(self):
        s = [self.rAddr,3,(MFC_Addr[self.id][4] >> 8 ) % 256, \
             MFC_Addr[self.id][4] % 256, 0,8]
        #01 03 75 94 00 05
        #01 03 0A 00 01 00 00 00 00  3f 80 00 00
        #01 10 75 94 00 05 0A 00 00 00 00 00 00  3f 80 00 00
        self.port.writeCOM(s)
        ret,retData = self.port.readCOM()
        retStr = []
        try:
            for i in retData:
                retStr.append ('%x'%ord(i))
            self.port.log.debug('Reading %s AI parameters %s'% (self.id,retStr))
        except Exception as ex:
            self.port.log.warn('Reading %s AI parameters error: %s' %(self.id,ex))
        
    def configAOMode(self):
        s = [self.wAddr,WRITE_AI_HOLD,(MFC_Addr[self.id][4] >> 8 ) % 256, \
             MFC_Addr[self.id][4] % 256, 0, 5,0x0A,0,0,0,0,0,0,0x3f,0x80,0,0]
        self.port.writeCOM(s)
        self.port.log.debug('config AO %s'% self.port.readCOM()[1])
#        self.port.log.warn('Failed to configure MFC %s !'%(self.id))
    def configAIMode(self):
        s = [self.rAddr,WRITE_AI_HOLD,(MFC_Addr[self.id][4] >> 8 ) % 256, \
             MFC_Addr[self.id][4] % 256,0,8,0x10,0,1,0x0C,0,0x3F,0x80,0,0,0,0,0,0,0x3F,0x80,0,0x0]
        #s = [self.rAddr,WRITE_AI_HOLD,(MFC_Addr[self.id][4] >> 8 ) % 256, \
        #     MFC_Addr[self.id][4] % 256,0,1,2,0,0]
        self.port.writeCOM(s)
        ret,retData = self.port.readCOM()
        retStr = []
        try:
            for i in retData:
                retStr.append ('%x'%ord(i))
            self.port.log.debug('Configure %s AI parameters %s'% (self.id,retStr))        
        #self.port.log.debug('cofig %s AI %s'% (self.id,self.port.readCOM()[1]))
        #    self.port.log.warn('Failed to configure MFC %s !'%(self.id))
        except Exception as ex:
            self.port.log.warn('Configure %s AI parameters error: %s' %(self.id,ex))        
    def setFlow(self,flowValue):
        # 设定AO模块的对应通道的输出电压
        
        # 输入： 流量值
        # 输出： 成功，返回 (True, 实际流量值）；失败，返回 （False, -1）
        
##        try:
        self.flow = flowValue
        flowValue = int( flowValue * MFC_ADC_WIDTH / MFC_Addr[self.id][3] )
        ret =  0            
        s = [self.wAddr,SINGLE_WRITE_AO,0,self.ch,(flowValue >> 8 ) % 256, flowValue % 256]
        t0 = time.time()
        if self.port.writeCOM(s):
            
            ret,data = self.port.readCOM()
            str_data = ''
            for i in data:
                str_data += '%X ' % ord(i)
            self.port.log.debug('Returned data: %s' %str_data)
            if ret:
                if len(data) > 5:
                    retFlow = ( ord( data[4] ) << 8  + ord( data[5] ) )
                    self.port.log.info('MFC %s is adjusted to %s'%(self.id, retFlow))
                    return True,retFlow
            else:
                self.port.log.warn('Error while trying to adjust MFC %s!'%(self.id))
                return False, -1
        else:
            self.port.log.warn('Error to adjust MFC %s time' % (self.id))
            return False, -1
##        except Exception as ex:
##            self.port.log.error('MFC:%s set error %s'%(self.ch,ex))
##            return False

    def getFlow(self):
        # 从AI模块读取当前流量
        
        # 输入：无
        # 返回：当前的流量mfc_flow
        t0 = time.time()
        ret =  0
        s = [self.rAddr,READ_AI_INPUT,0, self.ch,0,1]
        self.port.writeCOM(s)
        ret,data = self.port.readCOM(7)
        self.port.log.debug('Read %s of %s bytes time: %s' % (self.id,data, time.time() - t0 ))
        if ret and len(data) > 5:
            
            if ord( data[1] ) == READ_AI_INPUT:
                
                val = ( ord(data[3] ) << 8 + ord(data[4]) ) / MFC_ADC_WIDTH * MFC_Addr[self.id][3]
                self.port.log.debug('Read MFC %s flow is %s!'%(self.id,val))
                return True, val
        elif ret and len(data) == 5:
            self.port.log.warn("Invalid MFCs data, error code: %X"% ord(data[2]))
        else:
            self.port.log.warn("Unknown COM error!")
        return False, -1


    def getAll(self):
        # 读取当前所有流量计的流量
        
        # 输入：无
        # 返回：所有通道的流量（flow1,flow2,flow3,flow4,flow5）
        ret =  0
        s = [self.rAddr,READ_AI_INPUT,0, 0, 0, 5]#MFC_Addr[MFC_Addr.keys()[0]][2],0,5]
        self.port.writeCOM(s)
        ret,data = self.port.readCOM()
        if ret and len(data) > 5:
            if ord( data[1] ) == 4:
                mfckeys = MFC_Addr.keys()
                mfcval = {}
                for i in MFC_Addr.keys():
                    retVal = ord(data[MFC_Addr[i][2]*2 + 3] )  * 256 + ord(data[MFC_Addr[i][2]*2 + 4])
                    retStr = '%s:%s' %(ord(data[MFC_Addr[i][2]*2 + 3]) , ord(data[MFC_Addr[i][2]*2 + 4]))
                    mfcval[i] = float(retVal) / MFC_ADC_WIDTH# * MFC_Addr[self.id][3]
                self.port.log.debug("MFCs %s data %s"% (i,mfcval))
                return True,mfcval
        elif ret and len(data) == 5:
            self.port.log.warn("MFCs COM error, code: %X"% ord(data[2]))
        #else:
        #    self.port.log.warn("Unknown COM error!")
        return False, None

class Motor(object):

    def __init__(self,id,port,maxRange = 100000000):
        self.id = id
        self.addr = Motor_Addr[id][0]
        self.port = port
        self.location = 0
        self.maxRange = maxRange
        self.minRange = 0
        self.zero = 0
        self.LL = 0
        self.RL = 0
        self.stepsize = 1000
        self.steptime = 0.2

        self.findLimit()


        self.port.log.info("Motor %s is initilized !"%self.id)

    def findLimit(self):
        self.gotoLimit()
        self.maxRange = 0
        while self.zero == 0:
            self.move(self.stepsize,True)
            self.readStatus()
            self.maxRange += self.stepsize

    def move(self,pulses,isBackward = False):

        s=[self.addr,0x32,0x04,0x00,0x00,0x00,0x00]

        s[4] = (pulses >> 16) % 256
        s[5] = (pulses >> 8 ) % 256
        s[6] = pulses % 256

        if isBackward :
            pulses = - pulses
            s[3] = 1

        if not self.port.writeCOM(s):
            return False
        self.location += pulses
        return True

    def stop(self):
        
        s=[self.addr,0x3c,0x00]
        if not self.port.writeCOM(s):
            return False
        return True

    def gotoZero(self):
        self.pause = False
        while self.zero == 0:
            if self.location <= self.minRange :
                break
            self.move(self.location - self.minRange, True)
            self.readStatus()
            if self.pause:
                break
            self.port.log.debug('%s location is %s'%(self.id,self.location))


    def gotoLimit(self):
        self.pause = False
        while self.RL == 0:
            if self.location >= self.maxRange:
                break
            self.move(self.maxRange - self.location, False)
            self.readStatus()
            if self.pause :
                break
            self.port.log.debug('%s location is %s'%(self.id,self.location))

    def readStatus(self):
        s = [self.addr, 0x3B, 0 ]
        if not self.port.writeCOM(s):
            return False,None        
        ret,data = self.port.readCOM()
        if ret:
            self.running,self.LL,self.zero,self.RL = \
                                            ( ord( data[3] ), ord( data[4] ),\
                                            ord( data[5] ),ord( data[6] ) )
            return True,( ord( data[3] ), ord( data[4] ),\
                          ord( data[5] ),ord( data[6] ) )
        else:
            return False, None
class RFPower(object):
    def __init__(self,ID,port):
        self.ID = ID
        self.addr = RF_Addr
        self.port = port
    def powerON(self):
        
        s = [01, 05, 00, 00, 0xFF, 00]
        if not self.port.writeCOM(s):
            return False
        ret,data = self.port.readCOM()
        self.port.log.debug('Power on returned %s'% data )
        
    def powerOFF(self):
        
        s = [01, 05, 00, 00, 0, 00]
        if not self.port.writeCOM(s):
            return False
        ret,data = self.port.readCOM()
        self.port.log.debug('Power off returned %s'% data )
    def setPowerLevel(self,pwrVal):
        s = [01, 06, 00, 00, ( pwrVal >> 8 ) % 256, pwrVal % 256]
        if not self.port.writeCOM(s):
            return False
        ret,data = self.port.readCOM()
        self.port.log.debug('Power off returned %s'% data )        
    def readPower(self):
        s = [01,04,00,00,00,03]
        if not self.port.writeCOM(s):
            return False,None
        ret,data = self.port.readCOM()
        if ret:
            dcBias = ord( data[8] ) - 256
            forPwr = ord( data[3] ) << 8 + ord( data[4] )
            retPwr = ord( data[5] ) << 8 + ord( data[6] )
            return True,{'DCBias':dcBias,'ForPwr':forPwr,'RetPwr':retPwr}
        else:
            return False,None
class Pump(object):
    def __init__(self,ID):
        self.ID = ID
        self.running = False
    def powerOff(self):
        self.running = False
        return True
    def powerOn(self):
        self.running = True
        return True
    def isRunning(self):
        return self.running

if __name__ == "__main__":
    import logging
    # logging parameters
    LOGFILE = "/var/log/EtcherIO.log"
    MAXLOGSIZE = 2*1024*1024    #Bytes
    BACKUPCOUNT = 2
    FORMAT = \
        "%(asctime)s %(levelname)-8s[%(filename)s:%(lineno)d(%(funcName)s)] %(message)s"
    LOGLVL = logging.DEBUG

    formatter = logging.Formatter(FORMAT)
    # create console handler with a higher log level  
    ch = logging.StreamHandler()  
    ch.setLevel(logging.DEBUG)  
    # create formatter and add it to the handlers  
    ch.setFormatter(formatter)  

    LOG = logging.getLogger()
    # add the handlers to logger  
    LOG.addHandler(ch)
    LOG.setLevel(LOGLVL)
##    LOG.debug("logging init")

    s = COMOperator(LOG)
    if s.port.isOpen():
        s.log.info('Open %s successfully !'% s.port.name)
    else:
        s.log.warn('Open %s failed !' % s.port.name)

