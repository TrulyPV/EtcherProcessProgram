#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import serial,sys
from EtcherGUI import *
from EtcherIO import *
import logging
from logging.handlers import RotatingFileHandler
import thread
import time
import math
from pcduino import *
import traceback
Version = '1.0'

BeepPin = 1

GAS = ('Ar','CO2','O2','CF4','SF6')
BTN_COLOUR = {
    'ON_BG' : 'green',
    'ON_FG' : 'black',
    'OFF_FG': '#%X%X%X'%(  212,57, 15 ),
    'OFF_BG': '#%X%X%X'%( 0,255,0 ),
    'Unkown_FG':'black',
    'Unkown_BG':'red'
}
#BTN_FONT = {
#        'ON' : (( 11, wx.DEFAULT, wx.NORMAL, wx.BOLD, False)),
#        "OFF": (( 11, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False))
#       }
# logging parameters
LOGFILE = "etcher.log"
MAXLOGSIZE = 2*1024*1024    #Bytes
BACKUPCOUNT = 2
FORMAT = \
"%(asctime)s %(levelname)-8s[%(filename)s:%(lineno)d(%(funcName)s)] %(message)s"
LOGLVL = logging.DEBUG
# create file handler which logs even debug messages  
fh = RotatingFileHandler(LOGFILE,
                         mode='w',
                         maxBytes=MAXLOGSIZE,
                         backupCount=BACKUPCOUNT)
formatter = logging.Formatter(FORMAT)
# create console handler with a higher log level  
ch = logging.StreamHandler()  
ch.setLevel(logging.DEBUG)  
# create formatter and add it to the handlers  
ch.setFormatter(formatter)  
fh.setFormatter(formatter)

LOG = logging.getLogger()
# add the handlers to logger  
LOG.addHandler(ch)
LOG.addHandler(fh)    
LOG.setLevel(LOGLVL)
LOG.debug("logging init")

class Throttle(Motor,threading.Thread):
    def __init__(self, ID, port, maxRange=100000):
        threading.Thread.__init__(self)
        Motor.__init__(self,ID,port,maxRange)
        self.thread_stop = False
        self.manualMode = False
        self.setDaemon(True)
        self.aimPressure = 0
        self.totalFlow = 0
        self.pressure = 0
        self.accuracy = 0.01    # 1%的精度
        self.rdy = threading.Event()
    def run(self):
        self.thread_stop = False
        
        while not self.thread_stop:
            self.rdy.wait()
            if not self.manualMode:
                self.doPressureAdjust()
                
    def stop(self):
        self.thread_stop = True
        self.join()
    def initPID(self,aimPressure,totalFlow,startPressure):
        self.gotoZero()
        self.pressure = startPressure
        self.aimPressure = aimPressure
        self.totalFlow = totalFlow
        self.rdy.set()
    def doPressureAdjust(self,period = 0.5):
        # adjust the throttle valve angle to steady the pressure in CVD chamber
        nextLocation = self.doPID()
        steps = int ( nextLocation - self.location )
        if steps > 0 :
            self.move(steps,False)
        elif steps < 0:
            steps = - steps
            self.move(steps,True)
        time.sleep(period)
        
    def doPID(self):
        
        e = self.aimePressure - self.pressure        
        nextLocation = pid_P * e + pid_I * e_sum + pid_D * (e - e_pre)  + self.location       
        e_sum += e        
        e_pre = e
        
        return nextLocation
class Operator(object):
    def __init__(self,ID):
        self.ID = ID
        
    def login(self):
        LOG.info('%s logged in!' % self.ID)
        wx.MessageBox('Welcome back %s !' % self.ID,'Info',wx.OK|wx.ICON_INFORMATION)
        
    def logout(self,sampleCount):
        LOG.info('%s logged out' % self.ID)
        wx.MessageBox('Completed %s samples,Goodbye %s!' %(sampleCount, self.ID),'Info',wx.OK|wx.ICON_INFORMATION)
        
        
class Sample(object):
    Status = {
        'Mounted': 0,
        'Heated' : 1,
        'Loaded' : 2,
        'Depositing': 3,
        'Deposited' : 4,
        'Unloaded'  : 5,
        'Cooling'   : 6,
        'Waitting'  : 7,
        'Finished'  : 0
        }
    def __init__(self,ID):
        self.ID = ID
        self.recipe = {}
        self.substrate = {}
        for i in GAS:
            self.recipe[i] = {}
        self.recipe['Power'] = {}
        self.recipe['Pressure'] = {}
        self.recipe['GDTime'] = {}
        
#class BiValve(Valve):
        #def __init__(self, ID, port):
            #self.ID = ID
            #self.ONState = Valve(BiValveList[ID][0], port,False)
            #self.OFFState = Valve(BiValveList[ID][1], port)
        #def turnON(self):
            #return self.OFFState.open()# and self.ONState.open()
        #def turnOFF(self):
            #return self.ONState.close()# and self.OFFState.open()
def call_after(func):  
    def _wrapper(*args, **kwargs):  
        return wx.CallAfter(func, *args, **kwargs)  
    return _wrapper        
class Etcher(EtcherFrame, COMOperator):      

    def __init__(self):
        EtcherFrame.__init__(self, None)
        COMOperator.__init__(self, LOG)
        
        self.operator = None
        self.throttle = Throttle("Throttle", self)
        self.robot = Motor("Robot", self)
        self.rf = RFPower('Yantuo',self)
        self.pumps = {'LL':Pump('LL'),
                      'LL_TMP':Pump('LL_TMP'),
                      'CVD':Pump('CVD'),
                      'CVD_TMP':Pump('CVD_TMP')
                      }
        self.mfcs   = {}
        self.valves = {}
        self.gauges = {}
        
        self.samples = {}
        self.sampleInLoadlock = ''
        self.sampleInCVD = ''
        # MFCs
        for m in MFC_Addr.keys():
            self.mfcs[m] = MFC(m,self) 
        # Valves
        for v in ValveList.keys():
            self.valves[v] = Valve(ValveList[v],self)
        '''
        self.valves["Gate"] = BiValve('Gate',self)
        # for CVD chamber
        self.valves["Pins"] = BiValve('Pins',self)
        self.valves["Vacu"] = Valve(SValveList['Vacu'][0],self)
        self.valves["Film"] = Valve(SValveList['Film'][0],self)
        
        # for reaction gas
        self.valves["Ar"] = Valve(SValveList['Ar'][0], self)
        LOG.debug('Passed me')
        self.valves["O2"] = Valve(SValveList['O2'][0], self)
        self.valves["CO2"] = Valve(SValveList['CO2'][0], self)
        self.valves["CF4"] = Valve(SValveList['CF4'][0], self)
        self.valves["SF6"] = Valve(SValveList['SF6'][0], self)
        self.valves["Feed"] = Valve(SValveList['Feed'][0], self)
        
        # for loadlock chamber
        self.valves["Angl"] = Valve(SValveList['Angl'][0], self)
        self.valves["TPVa"] = BiValve("TPVa",self)
        self.valves["Leak"] = Valve(SValveList['Leak'][0], self)
        self.valves["Isol"] = Valve(SValveList['Isol'][0], self)
        
        #for v in Valve_Addr.keys():
        #    self.valves[v] = Valve(v,self)
        '''
        
        #for g in Gauge_Addr.keys():
        #    self.gauges[g] = Gauge(g,self)

        self.updatable = {'MFC':True,'VALVE':False,'GAUGE':False,'THROTTLE':False,'ROBOT':False}
        LOG.info('Etcher program %s is initialized !' % Version)
        
        self.gd_startTime = 0
        self.gd_totalTime = 1
        self.gd_off = False
        self.refresh()
        
        
        self.btn_moveIn.Enabled = False
        self.btn_moveOut.Enabled = False
        self.btn_llLoadIn.Enabled  = False
        self.btn_llLoadOut.Enabled = False
        
##        for i in range(13):
##            pinMode(i,OUTPUT)
##            digitalWrite(i,HIGH)
##        self.alertSound()
        
        
    def alertSound(self,N=1):
        return
        for i in range(N):
            digitalWrite(BeepPin,LOW)
            time.sleep(0.1)
            digitalWrite(BeepPin,HIGH)
            time.sleep(0.2)
    def mount(self):
        # 手动放置新衬底后，进行后续处理，包括：关闭放气阀、打开前级阀和预抽阀、确认机械泵开启的预抽过程；关闭前级阀、确认分子泵开启、打开插板阀的高真空过程
        
        #
        if wx.MessageBox('请确认装片室中的衬底已经更换 !','Question',wx.YES_NO|wx.ICON_QUESTION) == wx.NO:
            return         
        sampleID = self.txt_llMark.GetValue()
        if sampleID == '':
            sampleID = 'S%s' % time.strftime('%Y%m%d',time.localtime(time.time()))
            if wx.MessageBox('是否采用系统默认样品编号:%s ?' % sampleID,'Question',wx.YES_NO|wx.ICON_QUESTION) == wx.NO:
                return 
        self.samples[sampleID] = Sample(sampleID)
        self.samples[sampleID].satus = Sample.Status['Mounted']      
        
        if self.valves['Leak'].close():
            self.label_loadTime.SetLabel('1关闭：放气阀')
            if self.valves['Angl'].open() and self.valves['Isol'].open():
                self.label_loadTime.SetLabel('2打开：前级阀和预抽阀')
                if not self.pumps['LL'].isRunning():
                    wx.MessageBox('请手动打开装片室机械泵后确定！' ,'Info',wx.YES|wx.ICON_INFORMATION)
                    self.pumps['LL'].powerOn()
                
                self.label_loadTime.SetLabel('3等待预抽结束...')
                wx.MessageBox('请抽气完成后确定！' ,'Info',wx.YES|wx.ICON_INFORMATION)
                if self.valves['Angl'].close() and self.valves['Isol'].close():
                    self.label_loadTime.SetLabel('4关闭：前级阀和预抽阀')
                    if not self.pumps['LL_TMP'].isRunning():
                        wx.MessageBox('请手动打开分子泵后确定！' ,'Info',wx.YES|wx.ICON_INFORMATION)
                        self.pumps['LL_TMP'].powerOn()
                        self.label_loadTime.SetLabel('5打开：分子泵')
                    if self.valves['TPVa'].turnON():
                        self.label_loadTime.SetLabel('6等待真空环境准备好...')
                        #time.sleep(PumpTime)
                        wx.MessageBox('等待真空环境准备好后确定！' ,'Info',wx.YES|wx.ICON_INFORMATION)
                        self.label_loadTime.SetLabel(time.strftime('装片时间：%H:%M:%S',time.localtime(time.time())))
                        self.appendLog('%s is mounted from loadlock' % sampleID)
                        return True
                    
        else:
            self.label_loadTime.SetLabel('装片时出错!')
        
    def unmount(self):
        sampleID = self.txt_llMark.GetValue()
        if sampleID == '':
            if wx.NO == wx.MessageBox('貌似装片室里没有样品，继续?' ,'Question',wx.YES_NO|wx.ICON_QUESTION):
                return
        
        if self.valves['Gate'].isOpen():
            wx.MessageBox('请先关闭门阀!' ,'Info',wx.YES|wx.ICON_WARNING)
            return
        if self.valves['TPVa'].close():
            self.label_loadTime.SetLabel('1关闭：插板阀!')
            if self.valves['Isol'].close():#作为前级泵
                self.label_loadTime.SetLabel('2关闭：预抽阀!')
                if self.valves['Leak'].open():
                    self.label_loadTime.SetLabel('3打开：放气阀!')
                    #time.sleep(FlushTime)
                    wx.MessageBox('请稍后打开装片室，取走样品！' ,'Info',wx.YES|wx.ICON_INFORMATION)
                    self.label_loadTime.SetLabel('4取出样品!')
                    if self.samples[sampleID].status == Sample.Status['Finished']:
                        self.txt_llMark.SetValue('')
                        self.appendLog('%s is unmounted from loadlock' % sampleID)
                    return
                self.label_loadTime.SetLabel('打开放气阀时出错!')
                return
            self.label_loadTime.SetLabel('关闭前级阀时出错!')
            return
        self.label_loadTime.SetLabel('取片时出错!')        
        
    def load(self):
        sampleID = self.txt_llMark.GetValue()
        if sampleID == '' :
            wx.MessageBox('貌似装片室中没有样品 ！' ,'Info',wx.YES|wx.ICON_INFOMATION)
            return
        
        if wx.NO == wx.MessageBox('要打开门阀装片，继续?' ,'Question',wx.YES_NO|wx.ICON_QUESTION):
            return
        if self.valves['Gate'].close():
            if self.robot.gotoLimit():
                self.label_cvd_mark.SetLabel('等待装片装入!')
                wx.MessageBox('机械手停止了吗？' ,'Info',wx.YES|wx.ICON_INFOMATION)
                #time.sleep(RobotTime)
                if self.valves['Pins'].turnON():
                    self.label_cvd_mark.SetLabel('取下样品!')
                    sleep(2)
                    if self.robot.gotoZero():
                        self.label_cvd_mark.SetLabel('等待机械手回原点!')
                        time.sleep(RobotTime)
                        if self.valves['Pins'].close():
                            if self.valves['Gate'].close():
                                self.label_cvd_mark.SetLabel('等待关闭门阀!')
                                sleep(2)
                                self.label_cvd_mark.SetLabel('样品编号：%s'%sampleID)
                                self.samples[sampleID].satus = Sample.Status['Loaded']        
                                self.txt_llMark.SetValue('')
                                self.label_loadTime.SetLabel('没有样品')
                                
                                
                            
                                self.gd_startTime = 0
                                self.gd_totalTime = 0
                                self.gd_off = False
                                self.gd_gauage.SetValue(0)
                                self.appendLog('Sample %s is loaded to CVD!'% sampleID)
        
        else:
            wx.MessageBox('移片进反应室时出错！' ,'Warning',wx.YES|wx.ICON_WARNING)

    #@call_after    
    def deposite(self):
                      
        
        self.gd_off = False
        self.setFlag(self.btn_powerOn)
        self.setFlag(self.btn_powerOff,False)        
        strT = self.txt_DiscTime.GetValue()
        try:
            self.gd_totalTime = float(strT)
            if self.gd_totalTime <= 0: 
                raise ValueError
        except ValueError:
            wx.MessageBox('请设置正确的辉光时间！','Warning',wx.OK|wx.ICON_WARNING)
            self.setFlag(self.btn_powerOn,False)
            return False                        
        
        # Power on
        if not self.rf.powerON():
            wx.MessageBox('打开射频电源错误！','Warning',wx.OK|wx.ICON_WARNING)
            self.appendLog('RF error!') 
            self.setFlag(self.btn_powerOn,False)
            return False
        self.gauge_gd.SetValue(0)
        self.gauge_gd.SetRange(self.gd_totalTime)
        self.appendLog('GD started, %s to go!'% self.gd_totalTime) 
        gaugerange = int(self.gauge_gd.GetRange())
        
        dialog = wx.ProgressDialog("辉光时间", "", self.gd_totalTime,  parent = None,
                                  style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME )  
        keepGoing = True
        self.gd_startTime = time.time()
        passed = (time.time() - self.gd_startTime )
        while  keepGoing and ( passed < self.gd_totalTime ):  
            passed = (time.time() - self.gd_startTime ) 
            keepGoing,skip = dialog.Update(passed)
            if not keepGoing:
                self.appendLog('GD canceled by user after %10.1fs, Try to power off!' % passed) 
                ret = self.rf.powerOFF()
                if not ret:
                    wx.MessageBox('关闭射频电源错误，请手动关闭！','Warning',wx.OK|wx.ICON_WARNING)
                self.appendLog('GD ended after %10.1f seconds!' % (time.time() - self.gd_startTime))
            wx.Sleep(0.1)
        
        dialog.Destroy() 
        #Power off
        
        self.gd_startTime = 0     
        self.setFlag(self.btn_powerOn,False)
        self.setFlag(self.btn_powerOff,True)         
        '''
        while not self.gd_off:  # manually power off
            passed = (time.time() - self.gd_startTime )
            passed =  int( (passed / self.gd_totalTime) * gaugerange )
            self.appendLog(passed)
            if passed >= gaugerange:
                self.gauge_gd.SetValue(gaugerange)
                if self.check_autoGD.IsChecked():   # power off automatically
                    #Power off
                    ret = self.rf.powerOFF()
                    self.appendLog('GD ended after %10.1f seconds!' % (time.time() - self.gd_startTime)) 
                    if not ret:
                        wx.MessageBox('关闭射频电源错误，请手动关闭！','Warning',wx.YES_NO|wx.ICON_WARNING)
                    break
                else:
                    if wx.MessageBox(time.strftime('设定时间到了 %M:%S, 停止吗?',time.localtime(time.time())),'Warning',wx.YES_NO|wx.ICON_WARNING) == wx.YES:
                        break
            else:
                self.gauge_gd.SetValue(passed)
            
            time.sleep(1)
            '''      

    def unload(self):
        sampleID = self.txt_cvdMark.GetValue()
        if sampleID == '':
            wx.MessageBox('貌似反应室中没有样品 ！' ,'Info',wx.YES|wx.ICON_INFOMATION)
            return            
        if wx.NO == wx.MessageBox('要打开门阀装片，继续?' ,'Question',wx.YES_NO|wx.ICON_QUESTION):
            return
        
        if self.valves['Gate'].turnON():
            if self.valves['Pins'].turnON():
                self.label_cvd_mark.SetLabel('托起样品!')
                sleep(2)            
                if self.robot.gotoLimit():
                    self.label_cvd_mark.SetLabel('等待装片进来!')
                    time.sleep(RobotTime)
                
                    if self.robot.gotoZero():
                        self.label_cvd_mark.SetLabel('等待机械手取走样品!')
                        time.sleep(RobotTime)
                        if self.valves['Pins'].turnOFF():
                            if self.valves['Gate'].turnOFF():
                                self.label_cvd_mark.SetLabel('等待关闭门阀!')
                                sleep(2)
                                self.label_cvd_mark.SetLabel('没有样品')
                                self.samples[sampleID].satus = Sample.Status['Unloaded']        
                                self.txt_llMark.SetValue(sampleID)
                                self.label_loadTime.SetLabel('样品取回时间：%s'%time.strftime('%H:%M:%S',time.localtime(time.time())))
                                
                                self.appendLog('Sample %s is unloaded to loadlock!'% sampleID)
                                
        else:
            
            wx.MessageBox('移片进反应室时出错！' ,'Warning',wx.YES|wx.ICON_WARNING)
        
    def refresh(self,interval = 1):
        if self.updatable['MFC']:
            thread.start_new_thread(self.refreshMFCs,(1,))
        if self.updatable['VALVE']:
            thread.start_new_thread(self.refreshValves,(1,))
        if self.updatable['GAUGE']:
            thread.start_new_thread(self.refreshGauge,(2,))

    def refreshGauge(self,interval = 0.5):
        while True:
            ret,vals = self.gauges['Ar'].updateData()
            #LOG.debug(vals)
            if ret:
                try:
                    pressure =int( vals['CVD_Pressure'] ) / 5.0
                    wx.CallAfter(self.label_cvd_pressure.SetLabel,'薄膜计：%4.3f Torr' % pressure )
                except ValueError as ve:
                    self.appendLog('Pressure error %s'% ve)

                wx.CallAfter(self.label_High.SetLabel,'高真空：%.2e'%float(vals['CVD_High']))
                wx.CallAfter(self.label_Low.SetLabel,'低真空：%.2e'%float(vals['CVD_Low']))
                wx.CallAfter(self.label_ll_pressure.SetLabel,'气压：%.2e'%float(vals['Loadlock']))
                LOG.debug('Gauges were refreshed!')
            time.sleep(interval)


    def refreshMFCs(self,interval = 0.5):
        while True:
            ret,val = self.mfcs[MFC_Addr.keys()[0]].getAll()
            LOG.debug(val)
            if ret:
                wx.CallAfter(self.label_Ar.SetLabel,'%4.1f' % ( val["Ar"] * 100.0 ))
                wx.CallAfter(self.label_CO2.SetLabel,'%4.1f' % ( val["CO2"] * 100.0 ) )
                wx.CallAfter(self.label_O2.SetLabel,'%4.1f' % ( val["O2"] * 100.0 ) )
                wx.CallAfter(self.label_CF4.SetLabel,'%4.1f' % ( val["CF4"] * 100.0 ) )
                wx.CallAfter(self.label_SF6.SetLabel,'%4.1f' % ( val["SF6"] * 100.0 ) )
                LOG.debug('MFCs were refreshed!')
                wx.CallAfter(self.label_cvd_pressure.SetLabel,'反应气压：%5.3f'% ( val["Film"] * 1000.0 ) )
#                wx.CallAfter(self.label_High.SetLabel,'高真空：%.2e'% float(vals['CVD_High']))
#                wx.CallAfter(self.label_Low.SetLabel,'低真空：%.2e'% float(vals['CVD_Low']))
#                wx.CallAfter(self.label_ll_pressure.SetLabel,'气压：%.2e'% float(vals['Loadlock']))
            time.sleep(interval)


    def refreshValves(self,interval = 1):
        time.sleep(interval)
        pass
    
    def setFlag(self,ctrl,isOn = True, valid = True):
        if not valid:
            ctrl.SetBackgroundColour(BTN_COLOUR['Unkown_BG'])
            return
        if isOn:
            ctrl.SetBackgroundColour(BTN_COLOUR['ON_BG'])
            #ctrl.SetForegroundColour(BTN_COLOUR['ON_FG'])    
        else:
            ctrl.SetBackgroundColour(BTN_COLOUR['OFF_BG'])
            #ctrl.SetForegroundColour(BTN_COLOUR['OFF_FG'])            
    def appendLog(self,info):
        info = '%s:\n %s '% (time.strftime('%H:%M:%S',time.localtime(time.time())), info)
        self.txt_log.AppendText("\n%s"%info)

        # Virtual event handlers, overide them in your derived class
    def EtcherFrameOnClose( self, event ):
        event.Skip()
        try :
            self.port.close()
        except Exception as ex:
            LOG.warn('Error while exiting: %s' %ex)
    #def EtcherFrameOnIdle( self, event ):
        #if self.gd_startTime > 0:
            #passed = (time.time() - self.gd_startTime)
            ##if int(passed * 10) % 2 == 0 : 
            #self.gauge_gd.SetValue(passed)
            #if passed >= self.gd_totalTime:
                #self.setFlag(self.btn_powerOn,False)
                #self.setFlag(self.btn_powerOff,True)  
                #self.gd_startTime = 0
                #ret = self.rf.powerOFF()
                #if ret:
                    #self.appendLog('GD ended after %10.1f seconds!' % (time.time() - self.gd_startTime)) 
                #else:
                    #wx.MessageBox('关闭射频电源错误，请手动关闭！','Warning',wx.YES_NO|wx.ICON_WARNING) 
                    #LOG.warn('关闭射频电源错误，请手动关闭！')
                                
     
    def txt_llMarkOnTextEnter( self, event ):
        pass
    
    
    def btn_snSureOnButtonClick( self, event ):
        
        N = int(self.txt_llMark.GetValue())
        self.alertSound(N)
        pass
        
        
    def btn_moveOutOnButtonClick( self, event ):
        if not self.robot.gotoZero():
            wx.MessageBox('机械手出错!','Warning',wx.YES|wx.ICON_WARNING)
        #self.unload()

        
    def btn_moveInOnButtonClick( self, event ):    
        if not self.robot.gotoLimit():
            wx.MessageBox('机械手出错!','Warning',wx.YES|wx.ICON_WARNING)
        #self.load()
        
    def btn_gateOpenOnButtonClick( self, event ):
        if wx.NO == wx.MessageBox('要打开门阀，继续?' ,'Question',wx.YES_NO|wx.ICON_QUESTION):
            return        
        if not self.valves['Gate'].open():
            wx.MessageBox('打开门阀时出错!','Warning',wx.YES|wx.ICON_WARNING)
            self.setFlag(self.btn_gateOpen,valid = False)
            return
        self.setFlag(self.btn_gateOpen,True)
        self.setFlag(self.btn_gateClose,False)
        
    def btn_GateCloseOnButtonClick( self, event ):
        if wx.NO == wx.MessageBox('要关闭门阀，继续?', 'Question', wx.YES_NO|wx.ICON_QUESTION):
            return
        if not self.valves['Gate'].close():
            wx.MessageBox('关闭门阀时出错!', 'Warning',wx.YES|wx.ICON_WARNING)
            self.setFlag(self.btn_gateClose,valid = False)
            return
        self.setFlag(self.btn_gateOpen,False)
        self.setFlag(self.btn_gateClose,True)
    

    def btn_llLoadInOnButtonClick( self, event ):
        
        self.mount()
        self.setFlag(self.btn_llLoadOut,False)
        self.setFlag(self.btn_llLoadIn)    
     

    def btn_llLoadOutOnButtonClick( self, event ):
        self.unmount()
        self.setFlag(self.btn_llLoadOut)
        self.setFlag(self.btn_llLoadIn,False)        
        
    def btn_tpOnOnButtonClick( self, event ):
        if wx.NO == wx.MessageBox('要打开插板阀，继续?' ,'Question',wx.YES_NO|wx.ICON_QUESTION):
            return        
        if not self.valves['TPVa'].open():
            wx.MessageBox('打开插板阀时出错!','Warning',wx.YES|wx.ICON_WARNING)
            self.setFlag(self.btn_tpOn,valid = False )
            return
        self.setFlag(self.btn_tpOn)
        self.setFlag(self.btn_tpOff,False)

    def btn_tpOffOnButtonClick( self, event ):
        if wx.NO == wx.MessageBox('要关闭插板阀，继续?' ,'Question',wx.YES_NO|wx.ICON_QUESTION):
            return        
        if not self.valves['TPVa'].close():
            wx.MessageBox('关闭插板阀时出错!','Warning',wx.YES|wx.ICON_WARNING)
            self.setFlag(self.btn_tpOff,valid = False )
            return
        self.setFlag(self.btn_tpOff)
        self.setFlag(self.btn_tpOn,False)
        
    def btn_leakOnOnButtonClick( self, event ):
        if self.valves['Leak'].open():
            self.setFlag(self.btn_leakOn)
            self.setFlag(self.btn_leakOff,False)
        else:
            self.setFlag(self.btn_leakOn,valid = False)

    def btn_leakOffOnButtonClick( self, event ):
        if self.valves['Leak'].close():
            self.setFlag(self.btn_leakOff)
            self.setFlag(self.btn_leakOn,False)
        else:
            self.setFlag(self.btn_leakOff,valid = False)


    def btn_isoOnOnButtonClick( self, event ):
        
        if wx.NO == wx.MessageBox('要打开预抽阀，继续?' ,'Question',wx.YES_NO|wx.ICON_QUESTION):
            return        
        if not self.valves['Isol'].open():
            wx.MessageBox('打开预抽阀时出错!','Warning',wx.YES|wx.ICON_WARNING)
            self.setFlag(self.btn_isoOn,valid = False )
            return
        self.setFlag(self.btn_isoOn)
        self.setFlag(self.btn_isoOff,False)    
    def btn_isoOffOnButtonClick( self, event ):
        if wx.NO == wx.MessageBox('要关闭预抽阀，继续?' ,'Question',wx.YES_NO|wx.ICON_QUESTION):
            return        
        if not self.valves['Isol'].close():
            wx.MessageBox('关闭预抽阀时出错!','Warning',wx.YES|wx.ICON_WARNING)
            self.setFlag(self.btn_isoOff,valid = False )
            return
        self.setFlag(self.btn_isoOff)
        self.setFlag(self.btn_isoOn,False)
        
    def btn_roughOnOnButtonClick( self, event ):
        if wx.NO == wx.MessageBox('要打开前级阀，继续?' ,'Question',wx.YES_NO|wx.ICON_QUESTION):
            return        
        if not self.valves['Angl'].open():
            wx.MessageBox('打开前级阀时出错!','Warning',wx.YES|wx.ICON_WARNING)
            self.setFlag(self.btn_roughOn,valid = False )
            return
        self.setFlag(self.btn_roughOn)
        self.setFlag(self.btn_roughOff,False)        
    def btn_roughOffOnButtonClick( self, event ):
        if wx.NO == wx.MessageBox('要关闭前级阀，继续?' ,'Question',wx.YES_NO|wx.ICON_QUESTION):
            return        
        if not self.valves['Angl'].close():
            wx.MessageBox('关闭前级阀时出错!','Warning',wx.YES|wx.ICON_WARNING)
            self.setFlag(self.btn_roughOff, valid = False )
            return
        self.setFlag(self.btn_roughOff)
        self.setFlag(self.btn_roughOn,False)
        
    def btn_powerOnOnButtonClick( self, event ):
        
        if self.gd_startTime > 0 :# if glow discharging
            return
        
        
                 
        self.deposite()
        #t1 = threading.Thread(target = self.deposite,args = ())
        #t1.setDaemon(True)
        #t1.start()
        
        
        
        
    def btn_powerOffOnButtonClick( self, event ):
        self.gd_off = True
        self.setFlag(self.btn_powerOff)
        self.setFlag(self.btn_powerOn,False)
        
    def btn_gasFeedOnOnButtonClick( self, event ):
        if wx.NO == wx.MessageBox('要开始进气，继续?' ,'Question',wx.YES_NO|wx.ICON_QUESTION):
            return        
        if not self.valves['Feed'].open():
            wx.MessageBox('打开进气阀时出错!','Warning',wx.YES|wx.ICON_WARNING)        
            return
        self.setFlag(self.btn_gasFeedOn)
        self.setFlag(self.btn_GasFeedOff,False)        
    def btn_GasFeedOffOnButtonClick( self, event ):
        if wx.NO == wx.MessageBox('要停止进气，继续?' ,'Question',wx.YES_NO|wx.ICON_QUESTION):
            return        
        if not self.valves['Feed'].close():
            wx.MessageBox('关闭进气阀时出错!','Warning',wx.YES|wx.ICON_WARNING)
            return
        self.setFlag(self.btn_GasFeedOff)
        self.setFlag(self.btn_gasFeedOn,False)                
        
    def btn_liftDownOnButtonClick( self, event ):
        if not self.valves['Pins'].close():
            wx.MessageBox('抬起样品时出错!','Warning',wx.YES|wx.ICON_WARNING)
            self.setFlag(self.btn_liftDown,valid = False)
            return
        self.setFlag(self.btn_liftDown)
        self.setFlag(self.btn_liftUp,False)
    def btn_liftUpOnButtonClick( self, event ):
        if not self.valves['Pins'].open():
            wx.MessageBox('放下样品时出错!','Warning',wx.YES|wx.ICON_WARNING)
            self.setFlag(self.btn_liftUp,valid = False)
            return
        self.setFlag(self.btn_liftUp)
        self.setFlag(self.btn_liftDown,False)

    def btn_filmOnOnButtonClick( self, event ):
        if not self.valves['Film'].open():
            wx.MessageBox('打开薄膜计隔离阀时出错!','Warning',wx.YES|wx.ICON_WARNING)
            self.setFlag(self.btn_filmOn,valid = False)
            return
        self.setFlag(self.btn_filmOn)
        self.setFlag(self.btn_filmOff,False)

    def btn_filmOffOnButtonClick( self, event ):
        if not self.valves['Film'].close():
            wx.MessageBox('关闭薄膜计隔离阀时出错!','Warning',wx.YES|wx.ICON_WARNING)
            self.setFlag(self.btn_filmOff,valid = False)
            return
        self.setFlag(self.btn_filmOff)
        self.setFlag(self.btn_filmOn,False)

    def btn_vacuumOnOnButtonClick( self, event ):
        if not self.valves['Vacu'].open():
            wx.MessageBox('打开罗茨泵截止阀时出错!','Warning',wx.YES|wx.ICON_WARNING)
            self.setFlag(self.btn_vacuumOn,valid = False)
            return
        self.setFlag(self.btn_vacuumOn)
        self.setFlag(self.btn_vacuumOff,False) 
    def btn_vacuumOffOnButtonClick( self, event ):
        if not self.valves['Vacu'].close():
            wx.MessageBox('关闭罗茨泵截止阀时出错!','Warning',wx.YES|wx.ICON_WARNING)
            self.setFlag(self.btn_vacuumOff,vallid = False)
            return
        self.setFlag(self.btn_vacuumOff)
        self.setFlag(self.btn_vacuumOn,False)

    def btn_throttleAutoOnToggleButton( self, event ):
        self.throttle.manualMode = self.btn_throttleAuto.GetValue()

    def btn_throttleOpenOnButtonClick( self, event ):
        self.throttle.gotoLimit()
        self.spin_throttleValue.SetValue(int(self.throttle.location / self.throttle.maxRange * 100))

        self.setFlag(self.btn_throttlOpen)
        self.setFlag(self.btn_throttleClose,False)         

    def btn_throttleCloseOnButtonClick( self, event ):
        self.throttle.gotoZero()
        self.spin_throttleValue.SetValue(int(self.throttle.location / self.throttle.maxRange * 100))
        self.setFlag(self.btn_throttlClose)
        self.setFlag(self.btn_throttleOpen,False)                 

    def spin_throttleValueOnSpinCtrl( self, event ):
        self.spin_throttleValueOnTextEnter()

    def spin_throttleValueOnTextEnter( self, event ):
        locVal = self.spin_throttleValue.GetValue()
        pulses = locVal / 100 * self.throttle.maxRange - self.throttle.location
        if pulses > 0:
            self.throttle.move(pulses)
        else:
            pulses = - pulses
            self.throttle.move(pulses)


    def check_ArOnCheckBox( self, event ):
        if (self.check_Ar.IsChecked()):
            self.txt_Ar.Enable()
            self.btn_setAr.Enable()
            self.txt_Ar.SetValue("0")
        else:
            self.txt_Ar.Disable()
            self.btn_setAr.Disable()
            self.txt_Ar.SetValue("0")
            self.btn_setArOnButtonClick(None)


    def btn_setArOnButtonClick( self, event ):
        # set MFC flow, and set valve to opened( flow > 0 ) or closed( flow =0 )
        #self.testDIO(DO1_Addr,16)
        #self.testDIO(DO2_Addr,8)
        #self.testMotor(11)
        #self.testMotor(12)        
            
        gasname = 'Ar'
        flowvalue = int(self.txt_Ar.GetValue())
        if (flowvalue < 0) or (flowvalue > MFC_Addr[gasname][3]):
            wx.MessageBox('流量值 %s 错误（ 0 ~ %s ）！' % (flowvalue,MFC_Addr[gasname][3]),'错误',wx.OK|wx.ICON_INFORMATION)
            self.txt_Ar.SetValue("0")
            return
        
        if flowvalue > 0:            
            self.valves[gasname].open()
            self.btn_setAr.SetBackgroundColour(BTN_COLOUR['ON_BG'])
            self.btn_setAr.SetForegroundColour(BTN_COLOUR['ON_FG'])
#            self.btn_setAr.SetFont(wx.Font(BTN_FONT['ON']))
            self.appendLog("%s valve was OPENED"% (gasname))
        elif flowvalue == 0:
            self.valves[gasname].close()
            self.btn_setAr.SetBackgroundColour(BTN_COLOUR['OFF_BG'])
            self.btn_setAr.SetForegroundColour(BTN_COLOUR['OFF_FG'])
#            self.btn_setAr.SetFont(wx.Font(BTN_FONT['OFF']))
            self.appendLog("%s valve was CLOSED"% (gasname))
        fv = flowvalue  # * MFC_FULL_SCALE / MFC_Addr[gasname][3]  # tranlate to voltage signal
        self.mfcs[gasname].setFlow(fv)
        self.appendLog("%s was adjusted to %s SCCM"% (gasname, flowvalue))        

    def check_CO2OnCheckBox( self, event ):
        if (self.check_CO2.IsChecked()):
            self.txt_CO2.Enable()
            self.btn_setCO2.Enable()
            self.txt_CO2.SetValue("0")
        else:
            self.txt_CO2.Disable()
            self.btn_setCO2.Disable()
            self.txt_CO2.SetValue("0")
            self.btn_setCO2OnButtonClick(None)            

    def btn_setCO2OnButtonClick( self, event ):
        gasname = 'CO2'
        flowvalue = int(self.txt_CO2.GetValue())
        if (flowvalue < 0) or (flowvalue > MFC_Addr[gasname][3]):
            wx.MessageBox('流量值 %s 错误（ 0 ~ %s ）！' % (flowvalue,MFC_Addr[gasname][3]),'错误',wx.OK|wx.ICON_INFORMATION)
            self.txt_CO2.SetValue("0")
            return
        fv = flowvalue  # * MFC_FULL_SCALE / MFC_Addr[gasname][3]  # tranlate to voltage signal
        self.mfcs[gasname].setFlow(fv)
        self.appendLog("%s was adjusted to %s SCCM"% (gasname, flowvalue))
        if flowvalue > 0:            
            self.valves[gasname].open()
            self.btn_setCO2.SetBackgroundColour(BTN_COLOUR['ON_BG'])
            self.btn_setCO2.SetForegroundColour(BTN_COLOUR['ON_FG'])
    #            self.btn_setAr.SetFont(wx.Font(BTN_FONT['ON']))
            self.appendLog("%s valve was OPENED"% (gasname))
        elif flowvalue == 0:
            self.valves[gasname].close()
            self.btn_setCO2.SetBackgroundColour(BTN_COLOUR['OFF_BG'])
            self.btn_setCO2.SetForegroundColour(BTN_COLOUR['OFF_FG'])
    #            self.btn_setAr.SetFont(wx.Font(BTN_FONT['OFF']))
            self.appendLog("%s valve was CLOSED"% (gasname))

    def check_O2OnCheckBox( self, event ):
        if (self.check_O2.IsChecked()):
            self.txt_O2.Enable()
            self.btn_setO2.Enable()
            self.txt_O2.SetValue("0")
        else:
            self.txt_O2.Disable()
            self.btn_setO2.Disable()
            self.txt_CO2.SetValue("0")
            self.btn_setO2OnButtonClick(None)

    def btn_setO2OnButtonClick( self, event ):
        gasname = 'O2'
        flowvalue = int(self.txt_O2.GetValue())
        if (flowvalue < 0) or (flowvalue > MFC_Addr[gasname][3]):
            wx.MessageBox('流量值 %s 错误（ 0 ~ %s ）！' % (flowvalue,MFC_Addr[gasname][3]),'错误',wx.OK|wx.ICON_INFORMATION)
            self.txt_O2.SetValue("0")
            return
        fv = flowvalue  # * MFC_FULL_SCALE / MFC_Addr[gasname][3]  # tranlate to voltage signal
        self.mfcs[gasname].setFlow(fv)
        self.appendLog("%s was adjusted to %s SCCM"% (gasname, flowvalue))
        if flowvalue > 0:            
            self.valves[gasname].open()
            self.btn_setO2.SetBackgroundColour(BTN_COLOUR['ON_BG'])
            self.btn_setO2.SetForegroundColour(BTN_COLOUR['ON_FG'])
    #            self.btn_setAr.SetFont(wx.Font(BTN_FONT['ON']))
            self.appendLog("%s valve was OPENED"% (gasname))
        elif flowvalue == 0:
            self.valves[gasname].close()
            self.btn_setO2.SetBackgroundColour(BTN_COLOUR['OFF_BG'])
            self.btn_setO2.SetForegroundColour(BTN_COLOUR['OFF_FG'])
    #            self.btn_setAr.SetFont(wx.Font(BTN_FONT['OFF']))
            self.appendLog("%s valve was CLOSED"% (gasname))        

    def check_CF4OnCheckBox( self, event ):
        if (self.check_CF4.IsChecked()):
            self.txt_CF4.Enable()
            self.btn_setCF4.Enable()
            self.txt_CF4.SetValue("0")
        else:
            self.txt_CF4.Disable()
            self.btn_setCF4.Disable()
            self.txt_CF4.SetValue("0")
            self.btn_setCF4OnButtonClick(None)

    def btn_setCF4OnButtonClick( self, event ):
        gasname = 'CF4'
        flowvalue = int(self.txt_CF4.GetValue())
        if (flowvalue < 0) or (flowvalue > MFC_Addr[gasname][3]):
            wx.MessageBox('流量值 %s 错误（ 0 ~ %s ）！' % (flowvalue,MFC_Addr[gasname][3]),'错误',wx.OK|wx.ICON_INFORMATION)
            self.txt_CF4.SetValue("0")
            return
        fv = flowvalue  # * MFC_FULL_SCALE / MFC_Addr[gasname][3]  # tranlate to voltage signal
        self.mfcs[gasname].setFlow(fv)
        self.appendLog("%s was adjusted to %s SCCM"% (gasname, flowvalue))
        if flowvalue > 0:            
            self.valves[gasname].open()
            self.btn_setCF4.SetBackgroundColour(BTN_COLOUR['ON_BG'])
            self.btn_setCF4.SetForegroundColour(BTN_COLOUR['ON_FG'])
    #            self.btn_setAr.SetFont(wx.Font(BTN_FONT['ON']))
            self.appendLog("%s valve was OPENED"% (gasname))
        elif flowvalue == 0:
            self.valves[gasname].close()
            self.btn_setCF4.SetBackgroundColour(BTN_COLOUR['OFF_BG'])
            self.btn_setCF4.SetForegroundColour(BTN_COLOUR['OFF_FG'])
    #            self.btn_setAr.SetFont(wx.Font(BTN_FONT['OFF']))
            self.appendLog("%s valve was CLOSED"% (gasname))        

    def check_SF6OnCheckBox( self, event ):
        if (self.check_SF6.IsChecked()):
            self.txt_SF6.Enable()
            self.btn_setSF6.Enable()
            self.txt_SF6.SetValue("0")
        else:
            self.txt_SF6.Disable()
            self.btn_setSF6.Disable()
            self.txt_SF6.SetValue("0")
            self.btn_setSF6OnButtonClick(None)
    def btn_setSF6OnButtonClick( self, event ):
        gasname = 'SF6'
        flowvalue = int(self.txt_SF6.GetValue())
        if (flowvalue < 0) or (flowvalue > MFC_Addr[gasname][3]):
            wx.MessageBox('流量值 %s 错误（ 0 ~ %s ）！' % (flowvalue,MFC_Addr[gasname][3]),'错误',wx.OK|wx.ICON_INFORMATION)
            self.txt_SF6.SetValue("0")
            return
        fv = flowvalue  # * MFC_FULL_SCALE / MFC_Addr[gasname][3]  # tranlate to voltage signal
        self.mfcs[gasname].setFlow(fv)
        self.appendLog("%s was adjusted to %s SCCM"% (gasname, flowvalue))
        if flowvalue > 0:            
            self.valves[gasname].open()
            self.btn_setSF6.SetBackgroundColour(BTN_COLOUR['ON_BG'])
            self.btn_setSF6.SetForegroundColour(BTN_COLOUR['ON_FG'])
        #            self.btn_setAr.SetFont(wx.Font(BTN_FONT['ON']))
            self.appendLog("%s valve was OPENED"% (gasname))
        elif flowvalue == 0:
            self.valves[gasname].close()
            self.btn_setSF6.SetBackgroundColour(BTN_COLOUR['OFF_BG'])
            self.btn_setSF6.SetForegroundColour(BTN_COLOUR['OFF_FG'])
        #            self.btn_setAr.SetFont(wx.Font(BTN_FONT['OFF']))
            self.appendLog("%s valve was CLOSED"% (gasname))  

    def btn_setDiscTimeOnButtonClick( self, event ):
        self.samples[self.sampleInCVD].GDTime = int(self.txt_DiscTime.GetValue())
        event.Skip()

    def btn_setRFPowerOnButtonClick( self, event ):
        
        pwrVal = int(self.txt_RFPower.GetValue())
        self.rf.setPowerLevel(pwrVal)
        event.Skip()


    def btn_setPressureOnButtonClick( self, event ):
        event.Skip()

    def btn_logInOnButtonClick( self, event ):
        username = self.txt_username.GetValue()
        if username == '':
            username = 'Anoymous'
        self.operator = Operator(username)
        self.operator.login()
        
    def btn_logOutOnButtonClick( self, event ):
        self.operator.logout()
        self.operator = None
        
        self.COMOperator.ComEnabled = False
        
    def btn_refreshOnButtonClick( self, event ):
        self.txt_status.AppendText(self.testPort() + '\n')
        portStatus = self.testDIO(3,16)
        k = 0
        for i in portStatus:
            self.txt_status.AppendText('DO%s:%s'%(k,i) + '\n')
            k += 1
        portStatus = self.testDIO(4,8)
        for i in portStatus:
            self.txt_status.AppendText('DO%s:%s'%(k,i) + '\n')
            k += 1

        
    def testPort( self ):
        ret = ''
        try:
            if not self.port.isOpen():
                self.port.open()
            ret = self.port.name

        except Exception as ex:
            ret = 'Found no port '
            LOG.warn('Error: %s' % ex)
        return ret

    def testDIO( self, addr = 1, bitcount = 1 ):
        s=[addr, READ_COIL, 0, 0, 0, bitcount]
        if self.writeCOM(s):
            ret,data = self.readCOM()            
            if ret:
                status = []
                for i in data:
                    status.append(ord(i))
                
                self.appendLog('Read DIO %s, returned:%s' % (addr,status))
#                for k in range(bitcount):
#                    s=[addr, SINGLE_WRITE_DO, 0, k, 0xFF, 0]
#                    self.writeCOM(s)
#                    time.sleep(2)
#                    s=[addr, SINGLE_WRITE_DO, 0, k, 0x00, 0]
#                    self.writeCOM(s) 
#                    time.sleep(1)
            else:
                status = None
            return ret,status
        else:
            return False,'Write DO error.'


    def testMotor( self, addr ):
        

        s = [ addr, 0x3B, 0 ]
        if self.writeCOM(s):
            ret,data = self.readCOM()
            if ret:
                self.appendLog( 'Motor %s status: %s LL:%s Orig:%s RL:%s' % \
                                             (addr,ord( data[3] ), ord( data[4] ),\
                                              ord( data[5] ),ord( data[6] )))
            else:
                self.appendLog( 'Test motor %s error'%addr)
        else:
            wx.MessageBox('Write motor %s error '%addr,'Info',wx.OK|wx.ICON_INFORMATION)
            return        
    def m_timer2OnTimer( self, event ):
        self.label_currentTime.SetLabel(time.strftime('%H:%M:%S \n%Y-%m-%d',time.localtime(time.time())))
        #LOG.debug('time updated')

if __name__ == "__main__":

    app = wx.App()
    try:
        frame = Etcher()
        frame.Show()#FullScreen(True)
        app.MainLoop()
    except IOError as ier:
        sys.exc_clear()
    except Exception as ex:
        traceback.print_exc()  
        sys.exit(1)
    
    

