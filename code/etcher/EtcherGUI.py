# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun  6 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

wx.ID_EtcherFrame = 1000

###########################################################################
## Class EtcherFrame
###########################################################################

class EtcherFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_EtcherFrame, title = u"Welcome -Etch Process Program!", pos = wx.DefaultPosition, size = wx.Size( 1440,900 ), style = wx.CLOSE_BOX|wx.DEFAULT_FRAME_STYLE|wx.STAY_ON_TOP|wx.RAISED_BORDER|wx.TAB_TRAVERSAL, name = u"mainFrame" )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		self.SetFont( wx.Font( 9, 74, 90, 90, False, "Sans" ) )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer_title = wx.BoxSizer( wx.VERTICAL )
		
		self.lable_title = wx.StaticText( self, wx.ID_ANY, u"刻蚀工艺控制程序(Etching Process Program)", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
		self.lable_title.Wrap( -1 )
		self.lable_title.SetFont( wx.Font( 20, 70, 90, 90, False, "Impact" ) )
		
		bSizer_title.Add( self.lable_title, 1, wx.ALIGN_CENTER_HORIZONTAL, 20 )
		
		self.m_staticText22 = wx.StaticText( self, wx.ID_ANY, u"xusz@nankai.edu.cn", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText22.Wrap( -1 )
		bSizer_title.Add( self.m_staticText22, 1, wx.ALIGN_BOTTOM|wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		self.m_staticline2 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer_title.Add( self.m_staticline2, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		bSizer1.Add( bSizer_title, 1, wx.EXPAND, 5 )
		
		bSizer862 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer862.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		bSizer_left = wx.BoxSizer( wx.HORIZONTAL )
		
		sbSizer_step1 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"衬底操作区" ), wx.VERTICAL )
		
		bSizer_step1_up = wx.BoxSizer( wx.VERTICAL )
		
		
		bSizer_step1_up.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		bSizer93 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer491 = wx.BoxSizer( wx.VERTICAL )
		
		sbSizer7 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"装片室" ), wx.VERTICAL )
		
		
		sbSizer7.AddSpacer( ( 0, 0), 1, 0, 5 )
		
		bSizer64 = wx.BoxSizer( wx.VERTICAL )
		
		self.txt_llMark = wx.TextCtrl( self, wx.ID_ANY, u"Mark:", wx.DefaultPosition, wx.DefaultSize, 0|wx.SIMPLE_BORDER )
		self.txt_llMark.SetMaxLength( 0 ) 
		self.txt_llMark.SetFont( wx.Font( 12, 74, 90, 92, False, "Sans" ) )
		self.txt_llMark.SetForegroundColour( wx.Colour( 76, 65, 91 ) )
		
		bSizer64.Add( self.txt_llMark, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL|wx.EXPAND, 5 )
		
		self.btn_snSure = wx.Button( self, wx.ID_ANY, u"确定", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer64.Add( self.btn_snSure, 1, wx.ALIGN_RIGHT|wx.ALIGN_TOP|wx.ALL, 5 )
		
		
		sbSizer7.Add( bSizer64, 2, wx.EXPAND, 5 )
		
		self.label_ll_pressure = wx.StaticText( self, wx.ID_ANY, u"真空度", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_ll_pressure.Wrap( -1 )
		self.label_ll_pressure.SetFont( wx.Font( 11, 76, 90, 90, False, "Monospace" ) )
		self.label_ll_pressure.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_CAPTIONTEXT ) )
		
		sbSizer7.Add( self.label_ll_pressure, 1, wx.ALIGN_LEFT|wx.ALL, 5 )
		
		self.label_loadTime = wx.StaticText( self, wx.ID_ANY, u"装片时间:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_loadTime.Wrap( -1 )
		self.label_loadTime.SetFont( wx.Font( 11, 74, 90, 92, False, "Sans" ) )
		self.label_loadTime.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_CAPTIONTEXT ) )
		
		sbSizer7.Add( self.label_loadTime, 1, wx.ALIGN_LEFT|wx.ALL, 5 )
		
		
		bSizer491.Add( sbSizer7, 6, wx.ALIGN_CENTER|wx.EXPAND, 5 )
		
		
		bSizer93.Add( bSizer491, 2, wx.EXPAND, 5 )
		
		bSizer128 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer50 = wx.BoxSizer( wx.VERTICAL )
		
		self.btn_moveOut = wx.Button( self, wx.ID_ANY, u"<<  移出", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer50.Add( self.btn_moveOut, 1, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		self.btn_moveIn = wx.Button( self, wx.ID_ANY, u"移进 >>", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer50.Add( self.btn_moveIn, 1, wx.ALIGN_BOTTOM|wx.ALL, 5 )
		
		
		bSizer128.Add( bSizer50, 2, wx.EXPAND, 5 )
		
		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"门阀", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		bSizer128.Add( self.m_staticText3, 1, wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		bSizer79 = wx.BoxSizer( wx.VERTICAL )
		
		self.btn_gateOpen = wx.Button( self, wx.ID_ANY, u"-- 开", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer79.Add( self.btn_gateOpen, 1, wx.ALIGN_LEFT|wx.ALL, 5 )
		
		self.btn_GateClose = wx.Button( self, wx.ID_ANY, u"|| 关", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer79.Add( self.btn_GateClose, 1, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		
		bSizer128.Add( bSizer79, 2, wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		bSizer93.Add( bSizer128, 2, wx.EXPAND, 5 )
		
		
		bSizer_step1_up.Add( bSizer93, 5, wx.EXPAND, 5 )
		
		
		sbSizer_step1.Add( bSizer_step1_up, 5, wx.EXPAND, 5 )
		
		bSizer_step1_down = wx.BoxSizer( wx.VERTICAL )
		
		bSizer92 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer129 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.btn_llLoadIn = wx.Button( self, wx.ID_ANY, u"<< 装片", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer129.Add( self.btn_llLoadIn, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.btn_llLoadOut = wx.Button( self, wx.ID_ANY, u"出片 >>", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_llLoadOut.SetForegroundColour( wx.Colour( 26, 26, 26 ) )
		self.btn_llLoadOut.SetBackgroundColour( wx.Colour( 240, 240, 240 ) )
		
		bSizer129.Add( self.btn_llLoadOut, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		
		bSizer92.Add( bSizer129, 1, 0, 5 )
		
		bSizer1291 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.btn_tpOn = wx.Button( self, wx.ID_ANY, u"-- 插板阀开", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1291.Add( self.btn_tpOn, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.btn_tpOff = wx.Button( self, wx.ID_ANY, u"|| 关", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_tpOff.SetFont( wx.Font( 11, 70, 90, 90, False, "Impact" ) )
		self.btn_tpOff.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )
		
		bSizer1291.Add( self.btn_tpOff, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		
		bSizer92.Add( bSizer1291, 1, 0, 5 )
		
		bSizer12911 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.btn_leakOn = wx.Button( self, wx.ID_ANY, u"-- 放气阀开", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer12911.Add( self.btn_leakOn, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.btn_leakOff = wx.Button( self, wx.ID_ANY, u"|| 关", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_leakOff.SetFont( wx.Font( 11, 70, 90, 90, False, "Impact" ) )
		self.btn_leakOff.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )
		
		bSizer12911.Add( self.btn_leakOff, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		
		bSizer92.Add( bSizer12911, 1, 0, 5 )
		
		bSizer12923 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.btn_isoOn = wx.Button( self, wx.ID_ANY, u"-- 预抽阀开", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer12923.Add( self.btn_isoOn, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.btn_isoOff = wx.Button( self, wx.ID_ANY, u"|| 关", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer12923.Add( self.btn_isoOff, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		
		bSizer92.Add( bSizer12923, 1, 0, 5 )
		
		bSizer1292 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.btn_roughOn = wx.Button( self, wx.ID_ANY, u"-- 前级阀开", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1292.Add( self.btn_roughOn, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.btn_roughOff = wx.Button( self, wx.ID_ANY, u"|| 关", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1292.Add( self.btn_roughOff, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		
		bSizer92.Add( bSizer1292, 1, 0, 5 )
		
		bSizer12922 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.btn_llTMPOn = wx.Button( self, wx.ID_ANY, u"-- 分子泵开", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer12922.Add( self.btn_llTMPOn, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.btn_llTMPOff = wx.Button( self, wx.ID_ANY, u"|| 关", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer12922.Add( self.btn_llTMPOff, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		
		bSizer92.Add( bSizer12922, 1, 0, 5 )
		
		bSizer12921 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.btn_roughPumpOn = wx.Button( self, wx.ID_ANY, u"-- 机械泵开", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer12921.Add( self.btn_roughPumpOn, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.btn_roughPumpOff = wx.Button( self, wx.ID_ANY, u"|| 关", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer12921.Add( self.btn_roughPumpOff, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		
		bSizer92.Add( bSizer12921, 1, 0, 5 )
		
		
		bSizer_step1_down.Add( bSizer92, 7, 0, 5 )
		
		
		sbSizer_step1.Add( bSizer_step1_down, 7, 0, 5 )
		
		
		sbSizer_step1.AddSpacer( ( 0, 0), 2, wx.EXPAND, 5 )
		
		
		bSizer_left.Add( sbSizer_step1, 3, wx.EXPAND, 15 )
		
		sbSizer_step2 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"刻蚀工艺监控" ), wx.VERTICAL )
		
		bSizer_step2_up = wx.BoxSizer( wx.VERTICAL )
		
		bSizer60 = wx.BoxSizer( wx.VERTICAL )
		
		
		bSizer60.AddSpacer( ( 0, 0), 1, 0, 5 )
		
		sbSizer43 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"反应室" ), wx.VERTICAL )
		
		bSizer_PowerSwitch = wx.BoxSizer( wx.VERTICAL )
		
		bSizer55 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText9 = wx.StaticText( self, wx.ID_ANY, u"辉光控制", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9.Wrap( -1 )
		bSizer55.Add( self.m_staticText9, 0, wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		self.check_autoGD = wx.CheckBox( self, wx.ID_ANY, u"自动停止", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.check_autoGD.SetValue(True) 
		self.check_autoGD.SetFont( wx.Font( 9, 74, 90, 90, False, "Sans" ) )
		
		bSizer55.Add( self.check_autoGD, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )
		
		
		bSizer_PowerSwitch.Add( bSizer55, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_TOP|wx.ALL, 5 )
		
		bSizer56 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.btn_powerOn = wx.Button( self, wx.ID_ANY, u"开", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer56.Add( self.btn_powerOn, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_TOP|wx.ALL, 5 )
		
		self.btn_powerOff = wx.Button( self, wx.ID_ANY, u"关", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer56.Add( self.btn_powerOff, 0, wx.ALIGN_TOP|wx.ALL, 5 )
		
		
		bSizer_PowerSwitch.Add( bSizer56, 1, wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		sbSizer43.Add( bSizer_PowerSwitch, 2, wx.EXPAND, 5 )
		
		bSizer69 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer86 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer84 = wx.BoxSizer( wx.VERTICAL )
		
		self.label_cvd_pressure = wx.StaticText( self, wx.ID_ANY, u"反应气压:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_cvd_pressure.Wrap( -1 )
		self.label_cvd_pressure.SetFont( wx.Font( 11, 74, 90, 90, False, "Sans" ) )
		self.label_cvd_pressure.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_CAPTIONTEXT ) )
		
		bSizer84.Add( self.label_cvd_pressure, 1, wx.ALIGN_LEFT|wx.ALL, 5 )
		
		self.label_cvd_power = wx.StaticText( self, wx.ID_ANY, u"辉光功率:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_cvd_power.Wrap( -1 )
		self.label_cvd_power.SetFont( wx.Font( 11, 74, 90, 90, False, "Sans" ) )
		
		bSizer84.Add( self.label_cvd_power, 1, wx.ALIGN_LEFT|wx.ALL, 5 )
		
		
		bSizer86.Add( bSizer84, 1, wx.EXPAND, 5 )
		
		self.label_cvd_mark = wx.StaticText( self, wx.ID_ANY, u"样品编号:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_cvd_mark.Wrap( -1 )
		self.label_cvd_mark.SetFont( wx.Font( 12, 74, 90, 92, False, "Sans" ) )
		self.label_cvd_mark.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )
		
		bSizer86.Add( self.label_cvd_mark, 1, wx.ALIGN_LEFT|wx.ALL, 5 )
		
		bSizer85 = wx.BoxSizer( wx.VERTICAL )
		
		self.label_High = wx.StaticText( self, wx.ID_ANY, u"高真空：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_High.Wrap( -1 )
		bSizer85.Add( self.label_High, 1, wx.ALL, 5 )
		
		self.label_Low = wx.StaticText( self, wx.ID_ANY, u"低真空：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_Low.Wrap( -1 )
		bSizer85.Add( self.label_Low, 1, wx.ALL, 5 )
		
		
		bSizer86.Add( bSizer85, 1, wx.EXPAND, 5 )
		
		
		bSizer69.Add( bSizer86, 3, wx.EXPAND, 5 )
		
		
		sbSizer43.Add( bSizer69, 5, wx.EXPAND, 5 )
		
		
		bSizer60.Add( sbSizer43, 9, wx.EXPAND, 5 )
		
		
		bSizer_step2_up.Add( bSizer60, 0, wx.EXPAND, 5 )
		
		
		sbSizer_step2.Add( bSizer_step2_up, 8, wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )
		
		bSizer_step2_down = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer831 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer_CVDValves = wx.BoxSizer( wx.VERTICAL )
		
		bSizer1296 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.btn_liftDown = wx.Button( self, wx.ID_ANY, u"_ 衬底托降", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1296.Add( self.btn_liftDown, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.btn_liftUp = wx.Button( self, wx.ID_ANY, u"-- 升", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1296.Add( self.btn_liftUp, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		
		bSizer_CVDValves.Add( bSizer1296, 1, wx.EXPAND, 5 )
		
		bSizer1294 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.btn_filmOn = wx.Button( self, wx.ID_ANY, u"-- 隔离阀开", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1294.Add( self.btn_filmOn, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.btn_filmOff = wx.Button( self, wx.ID_ANY, u"|| 关", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1294.Add( self.btn_filmOff, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		
		bSizer_CVDValves.Add( bSizer1294, 1, wx.EXPAND, 5 )
		
		bSizer12941 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.btn_vacuumOn = wx.Button( self, wx.ID_ANY, u"-- 截止阀开", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer12941.Add( self.btn_vacuumOn, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.btn_vacuumOff = wx.Button( self, wx.ID_ANY, u"|| 关", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer12941.Add( self.btn_vacuumOff, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		
		bSizer_CVDValves.Add( bSizer12941, 1, wx.EXPAND, 5 )
		
		bSizer129221 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.btn_cvdTMPOn = wx.Button( self, wx.ID_ANY, u"-- 分子泵开", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer129221.Add( self.btn_cvdTMPOn, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.btn_cvdTMPOff = wx.Button( self, wx.ID_ANY, u"|| 关", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer129221.Add( self.btn_cvdTMPOff, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		
		bSizer_CVDValves.Add( bSizer129221, 1, wx.EXPAND, 5 )
		
		bSizer129222 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.btn_cvdRoughOn = wx.Button( self, wx.ID_ANY, u"-- 罗次泵开", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer129222.Add( self.btn_cvdRoughOn, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.btn_cvdRoughOff = wx.Button( self, wx.ID_ANY, u"|| 关", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer129222.Add( self.btn_cvdRoughOff, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		
		bSizer_CVDValves.Add( bSizer129222, 1, wx.EXPAND, 5 )
		
		
		bSizer831.Add( bSizer_CVDValves, 2, wx.ALIGN_TOP|wx.EXPAND, 5 )
		
		
		bSizer_step2_down.Add( bSizer831, 1, 0, 5 )
		
		bSizer841 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer_throttleValve = wx.BoxSizer( wx.VERTICAL )
		
		bSizer94 = wx.BoxSizer( wx.VERTICAL )
		
		sbSizer6 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"蝶阀控制" ), wx.VERTICAL )
		
		bSizer721 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.btn_throttleAuto = wx.ToggleButton( self, wx.ID_ANY, u"手动模式", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_throttleAuto.SetValue( True ) 
		bSizer721.Add( self.btn_throttleAuto, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		sbSizer6.Add( bSizer721, 1, wx.ALIGN_CENTER|wx.EXPAND, 5 )
		
		bSizer62 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer82 = wx.BoxSizer( wx.VERTICAL )
		
		self.btn_throttleOpen = wx.Button( self, wx.ID_ANY, u"全开", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer82.Add( self.btn_throttleOpen, 1, wx.ALIGN_LEFT|wx.ALL, 5 )
		
		self.btn_throttleClose = wx.Button( self, wx.ID_ANY, u"全关", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer82.Add( self.btn_throttleClose, 1, wx.ALIGN_LEFT|wx.ALL, 5 )
		
		
		bSizer62.Add( bSizer82, 1, wx.EXPAND, 5 )
		
		bSizer83 = wx.BoxSizer( wx.VERTICAL )
		
		self.spin_throttleValue = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 100, 0 )
		self.spin_throttleValue.SetFont( wx.Font( 12, 74, 90, 92, False, "Sans" ) )
		
		bSizer83.Add( self.spin_throttleValue, 1, wx.ALIGN_LEFT|wx.ALL, 5 )
		
		self.btn_throttleSet = wx.Button( self, wx.ID_ANY, u"设定", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer83.Add( self.btn_throttleSet, 1, wx.ALIGN_LEFT|wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer62.Add( bSizer83, 1, wx.EXPAND, 5 )
		
		
		sbSizer6.Add( bSizer62, 2, wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )
		
		
		bSizer94.Add( sbSizer6, 1, wx.EXPAND, 5 )
		
		
		bSizer_throttleValve.Add( bSizer94, 1, 0, 5 )
		
		
		bSizer_throttleValve.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		bSizer841.Add( bSizer_throttleValve, 2, wx.ALIGN_TOP|wx.EXPAND, 5 )
		
		
		bSizer_step2_down.Add( bSizer841, 1, 0, 5 )
		
		
		sbSizer_step2.Add( bSizer_step2_down, 5, 0, 5 )
		
		
		bSizer_left.Add( sbSizer_step2, 4, wx.EXPAND, 5 )
		
		sbSizer_step3 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"工艺参数控制" ), wx.VERTICAL )
		
		bSizer861 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer622 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer18 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer75 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.check_Ar = wx.CheckBox( self, wx.ID_ANY, u"Ar", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer75.Add( self.check_Ar, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )
		
		self.label_Ar = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT )
		self.label_Ar.Wrap( -1 )
		bSizer75.Add( self.label_Ar, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )
		
		
		bSizer18.Add( bSizer75, 1, wx.EXPAND, 5 )
		
		bSizer22 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.txt_Ar = wx.TextCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		self.txt_Ar.SetMaxLength( 0 ) 
		self.txt_Ar.Enable( False )
		
		bSizer22.Add( self.txt_Ar, 0, wx.ALIGN_TOP|wx.ALL, 5 )
		
		self.btn_setAr = wx.Button( self, wx.ID_ANY, u"设定", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_setAr.Enable( False )
		
		bSizer22.Add( self.btn_setAr, 0, wx.ALIGN_TOP|wx.ALL, 5 )
		
		
		bSizer18.Add( bSizer22, 1, wx.EXPAND, 5 )
		
		
		bSizer622.Add( bSizer18, 1, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		bSizer181 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer74 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.check_CO2 = wx.CheckBox( self, wx.ID_ANY, u"CO2", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer74.Add( self.check_CO2, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )
		
		self.label_CO2 = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_CO2.Wrap( -1 )
		bSizer74.Add( self.label_CO2, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )
		
		
		bSizer181.Add( bSizer74, 1, wx.EXPAND, 5 )
		
		bSizer221 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.txt_CO2 = wx.TextCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		self.txt_CO2.SetMaxLength( 0 ) 
		self.txt_CO2.Enable( False )
		
		bSizer221.Add( self.txt_CO2, 0, wx.ALIGN_TOP|wx.ALL, 5 )
		
		self.btn_setCO2 = wx.Button( self, wx.ID_ANY, u"设定", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_setCO2.Enable( False )
		
		bSizer221.Add( self.btn_setCO2, 0, wx.ALIGN_TOP|wx.ALL, 5 )
		
		
		bSizer181.Add( bSizer221, 1, wx.EXPAND, 5 )
		
		
		bSizer622.Add( bSizer181, 1, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		bSizer182 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer731 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.check_O2 = wx.CheckBox( self, wx.ID_ANY, u"O2", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer731.Add( self.check_O2, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )
		
		self.label_O2 = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_O2.Wrap( -1 )
		bSizer731.Add( self.label_O2, 0, wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		
		bSizer182.Add( bSizer731, 1, wx.EXPAND, 5 )
		
		bSizer222 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.txt_O2 = wx.TextCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		self.txt_O2.SetMaxLength( 0 ) 
		self.txt_O2.Enable( False )
		
		bSizer222.Add( self.txt_O2, 0, wx.ALIGN_TOP|wx.ALL, 5 )
		
		self.btn_setO2 = wx.Button( self, wx.ID_ANY, u"设定", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_setO2.Enable( False )
		
		bSizer222.Add( self.btn_setO2, 0, wx.ALIGN_TOP|wx.ALL, 5 )
		
		
		bSizer182.Add( bSizer222, 1, wx.EXPAND, 5 )
		
		
		bSizer622.Add( bSizer182, 1, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		bSizer183 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer76 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.check_CF4 = wx.CheckBox( self, wx.ID_ANY, u"CF4", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer76.Add( self.check_CF4, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )
		
		self.label_CF4 = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_CF4.Wrap( -1 )
		bSizer76.Add( self.label_CF4, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )
		
		
		bSizer183.Add( bSizer76, 1, wx.EXPAND, 5 )
		
		bSizer223 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.txt_CF4 = wx.TextCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		self.txt_CF4.SetMaxLength( 0 ) 
		self.txt_CF4.Enable( False )
		
		bSizer223.Add( self.txt_CF4, 0, wx.ALIGN_TOP|wx.ALL, 5 )
		
		self.btn_setCF4 = wx.Button( self, wx.ID_ANY, u"设定", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_setCF4.Enable( False )
		
		bSizer223.Add( self.btn_setCF4, 0, wx.ALIGN_TOP|wx.ALL, 5 )
		
		
		bSizer183.Add( bSizer223, 1, wx.EXPAND, 5 )
		
		
		bSizer622.Add( bSizer183, 1, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		bSizer184 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer77 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.check_SF6 = wx.CheckBox( self, wx.ID_ANY, u"SF6", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer77.Add( self.check_SF6, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )
		
		self.label_SF6 = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_SF6.Wrap( -1 )
		bSizer77.Add( self.label_SF6, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )
		
		
		bSizer184.Add( bSizer77, 1, wx.EXPAND, 5 )
		
		bSizer224 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.txt_SF6 = wx.TextCtrl( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		self.txt_SF6.SetMaxLength( 0 ) 
		self.txt_SF6.Enable( False )
		
		bSizer224.Add( self.txt_SF6, 0, wx.ALIGN_TOP|wx.ALL, 5 )
		
		self.btn_setSF6 = wx.Button( self, wx.ID_ANY, u"设定", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_setSF6.Enable( False )
		
		bSizer224.Add( self.btn_setSF6, 0, wx.ALIGN_TOP|wx.ALL, 5 )
		
		
		bSizer184.Add( bSizer224, 1, wx.EXPAND, 5 )
		
		
		bSizer622.Add( bSizer184, 1, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		
		bSizer861.Add( bSizer622, 5, wx.EXPAND, 5 )
		
		bSizer641 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer1861 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer2061 = wx.BoxSizer( wx.VERTICAL )
		
		self.check_dischargetime = wx.CheckBox( self, wx.ID_ANY, u"反应时间", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.check_dischargetime.SetValue(True) 
		self.check_dischargetime.SetFont( wx.Font( 11, 74, 90, 90, False, "Sans" ) )
		self.check_dischargetime.Enable( False )
		
		bSizer2061.Add( self.check_dischargetime, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )
		
		bSizer2261 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.txt_DiscTime = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txt_DiscTime.SetMaxLength( 0 ) 
		bSizer2261.Add( self.txt_DiscTime, 0, wx.ALIGN_TOP|wx.ALL, 5 )
		
		self.btn_setDiscTime = wx.Button( self, wx.ID_ANY, u"设定", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2261.Add( self.btn_setDiscTime, 0, wx.ALIGN_TOP|wx.ALL, 5 )
		
		
		bSizer2061.Add( bSizer2261, 1, 0, 5 )
		
		
		bSizer1861.Add( bSizer2061, 1, 0, 5 )
		
		
		bSizer641.Add( bSizer1861, 1, wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		bSizer186 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer206 = wx.BoxSizer( wx.VERTICAL )
		
		self.check_rfpower = wx.CheckBox( self, wx.ID_ANY, u"功率", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.check_rfpower.SetValue(True) 
		self.check_rfpower.Enable( False )
		
		bSizer206.Add( self.check_rfpower, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )
		
		bSizer226 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.txt_RFPower = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txt_RFPower.SetMaxLength( 0 ) 
		bSizer226.Add( self.txt_RFPower, 0, wx.ALIGN_TOP|wx.ALL, 5 )
		
		self.btn_setRFPower = wx.Button( self, wx.ID_ANY, u"设定", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer226.Add( self.btn_setRFPower, 0, wx.ALIGN_TOP|wx.ALL, 5 )
		
		
		bSizer206.Add( bSizer226, 1, 0, 5 )
		
		
		bSizer186.Add( bSizer206, 1, 0, 5 )
		
		
		bSizer641.Add( bSizer186, 1, wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		bSizer185 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer205 = wx.BoxSizer( wx.VERTICAL )
		
		self.check_pressure = wx.CheckBox( self, wx.ID_ANY, u"气压", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.check_pressure.SetValue(True) 
		self.check_pressure.Enable( False )
		
		bSizer205.Add( self.check_pressure, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )
		
		bSizer225 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.txt_Pressure = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.txt_Pressure.SetMaxLength( 0 ) 
		bSizer225.Add( self.txt_Pressure, 0, wx.ALIGN_TOP|wx.ALL, 5 )
		
		self.btn_setPressure = wx.Button( self, wx.ID_ANY, u"设定", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer225.Add( self.btn_setPressure, 0, wx.ALIGN_TOP|wx.ALL, 5 )
		
		
		bSizer205.Add( bSizer225, 1, 0, 5 )
		
		
		bSizer185.Add( bSizer205, 1, wx.ALIGN_BOTTOM, 5 )
		
		
		bSizer641.Add( bSizer185, 1, wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		bSizer861.Add( bSizer641, 3, wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )
		
		
		sbSizer_step3.Add( bSizer861, 12, wx.EXPAND, 5 )
		
		bSizer66 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer821 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.btn_add = wx.Button( self, wx.ID_ANY, u"添加", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer821.Add( self.btn_add, 0, wx.ALL, 5 )
		
		self.btn_delete = wx.Button( self, wx.ID_ANY, u"删除", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer821.Add( self.btn_delete, 0, wx.ALL, 5 )
		
		
		bSizer66.Add( bSizer821, 1, wx.EXPAND, 5 )
		
		bSizer67 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.btn_loadRecipe = wx.Button( self, wx.ID_ANY, u" 预置", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btn_loadRecipe.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )
		
		bSizer67.Add( self.btn_loadRecipe, 0, wx.ALL, 5 )
		
		self.btn_saveRecipe = wx.Button( self, wx.ID_ANY, u"保存", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer67.Add( self.btn_saveRecipe, 0, wx.ALL, 5 )
		
		
		bSizer66.Add( bSizer67, 2, wx.EXPAND, 5 )
		
		
		sbSizer_step3.Add( bSizer66, 3, wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )
		
		
		bSizer_left.Add( sbSizer_step3, 2, wx.EXPAND, 5 )
		
		
		bSizer862.Add( bSizer_left, 10, wx.EXPAND, 5 )
		
		bSizer_right = wx.BoxSizer( wx.VERTICAL )
		
		sbSizer_System = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"系统配置" ), wx.VERTICAL )
		
		self.btn_refresh = wx.Button( self, wx.ID_ANY, u"刷新", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer_System.Add( self.btn_refresh, 0, wx.ALIGN_CENTER|wx.ALL|wx.EXPAND, 5 )
		
		self.txt_status = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
		sbSizer_System.Add( self.txt_status, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer_right.Add( sbSizer_System, 3, wx.EXPAND, 5 )
		
		bSizer_left_down = wx.BoxSizer( wx.VERTICAL )
		
		sbSizer_Logger = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"操作记录" ), wx.VERTICAL )
		
		self.txt_log = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
		sbSizer_Logger.Add( self.txt_log, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer_left_down.Add( sbSizer_Logger, 1, wx.EXPAND, 5 )
		
		
		bSizer_right.Add( bSizer_left_down, 5, wx.EXPAND, 5 )
		
		
		bSizer862.Add( bSizer_right, 2, wx.EXPAND, 20 )
		
		
		bSizer862.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		bSizer1.Add( bSizer862, 10, wx.EXPAND, 5 )
		
		bSizer87 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer87.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer88 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer_login = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer1831 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer651 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText121 = wx.StaticText( self, wx.ID_ANY, u"用户名:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText121.Wrap( -1 )
		bSizer651.Add( self.m_staticText121, 0, wx.ALL, 5 )
		
		self.txt_username = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer651.Add( self.txt_username, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		
		bSizer1831.Add( bSizer651, 1, wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		bSizer65 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText12 = wx.StaticText( self, wx.ID_ANY, u"密   码:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )
		bSizer65.Add( self.m_staticText12, 0, wx.ALL, 5 )
		
		self.txt_password = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer65.Add( self.txt_password, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		
		bSizer1831.Add( bSizer65, 1, wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		bSizer_login.Add( bSizer1831, 1, wx.EXPAND, 5 )
		
		bSizer652 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.btn_logIn = wx.Button( self, wx.ID_ANY, u"登入", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer652.Add( self.btn_logIn, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		self.btn_logOut = wx.Button( self, wx.ID_ANY, u"退出", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer652.Add( self.btn_logOut, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		
		bSizer_login.Add( bSizer652, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )
		
		
		bSizer88.Add( bSizer_login, 2, 0, 5 )
		
		bSizer129211 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.label_currentTime = wx.StaticText( self, wx.ID_ANY, u"2015-03-18 20:19:40", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_currentTime.Wrap( -1 )
		self.label_currentTime.SetFont( wx.Font( 14, 74, 90, 92, False, "Sans" ) )
		self.label_currentTime.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )
		
		bSizer129211.Add( self.label_currentTime, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		
		bSizer88.Add( bSizer129211, 1, wx.ALIGN_RIGHT, 5 )
		
		
		bSizer87.Add( bSizer88, 1, wx.EXPAND, 5 )
		
		
		bSizer1.Add( bSizer87, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		self.m_timer2 = wx.Timer()
		self.m_timer2.SetOwner( self, wx.ID_ANY )
		self.m_timer2.Start( 1000 )
		
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.EtcherFrameOnClose )
		self.Bind( wx.EVT_IDLE, self.EtcherFrameOnIdle )
		self.txt_llMark.Bind( wx.EVT_TEXT_ENTER, self.txt_llMarkOnTextEnter )
		self.btn_snSure.Bind( wx.EVT_BUTTON, self.btn_snSureOnButtonClick )
		self.btn_moveOut.Bind( wx.EVT_BUTTON, self.btn_moveOutOnButtonClick )
		self.btn_moveIn.Bind( wx.EVT_BUTTON, self.btn_moveInOnButtonClick )
		self.btn_gateOpen.Bind( wx.EVT_BUTTON, self.btn_gateOpenOnButtonClick )
		self.btn_GateClose.Bind( wx.EVT_BUTTON, self.btn_GateCloseOnButtonClick )
		self.btn_llLoadIn.Bind( wx.EVT_BUTTON, self.btn_llLoadInOnButtonClick )
		self.btn_llLoadOut.Bind( wx.EVT_BUTTON, self.btn_llLoadOutOnButtonClick )
		self.btn_tpOn.Bind( wx.EVT_BUTTON, self.btn_tpOnOnButtonClick )
		self.btn_tpOff.Bind( wx.EVT_BUTTON, self.btn_tpOffOnButtonClick )
		self.btn_leakOn.Bind( wx.EVT_BUTTON, self.btn_leakOnOnButtonClick )
		self.btn_leakOff.Bind( wx.EVT_BUTTON, self.btn_leakOffOnButtonClick )
		self.btn_isoOn.Bind( wx.EVT_BUTTON, self.btn_isoOnOnButtonClick )
		self.btn_isoOff.Bind( wx.EVT_BUTTON, self.btn_isoOffOnButtonClick )
		self.btn_roughOn.Bind( wx.EVT_BUTTON, self.btn_roughOnOnButtonClick )
		self.btn_roughOff.Bind( wx.EVT_BUTTON, self.btn_roughOffOnButtonClick )
		self.btn_llTMPOn.Bind( wx.EVT_BUTTON, self.btn_llTMPOnOnButtonClick )
		self.btn_llTMPOff.Bind( wx.EVT_BUTTON, self.btn_llTMPOffOnButtonClick )
		self.btn_roughPumpOn.Bind( wx.EVT_BUTTON, self.btn_roughPumpOnOnButtonClick )
		self.btn_roughPumpOff.Bind( wx.EVT_BUTTON, self.btn_roughPumpOffOnButtonClick )
		self.check_autoGD.Bind( wx.EVT_CHECKBOX, self.check_autoGDOnCheckBox )
		self.btn_powerOn.Bind( wx.EVT_BUTTON, self.btn_powerOnOnButtonClick )
		self.btn_powerOff.Bind( wx.EVT_BUTTON, self.btn_powerOffOnButtonClick )
		self.btn_liftDown.Bind( wx.EVT_BUTTON, self.btn_liftDownOnButtonClick )
		self.btn_liftUp.Bind( wx.EVT_BUTTON, self.btn_liftUpOnButtonClick )
		self.btn_filmOn.Bind( wx.EVT_BUTTON, self.btn_filmOnOnButtonClick )
		self.btn_filmOff.Bind( wx.EVT_BUTTON, self.btn_filmOffOnButtonClick )
		self.btn_vacuumOn.Bind( wx.EVT_BUTTON, self.btn_vacuumOnOnButtonClick )
		self.btn_vacuumOff.Bind( wx.EVT_BUTTON, self.btn_vacuumOffOnButtonClick )
		self.btn_cvdTMPOn.Bind( wx.EVT_BUTTON, self.btn_cvdTMPOnOnButtonClick )
		self.btn_cvdTMPOff.Bind( wx.EVT_BUTTON, self.btn_cvdTMPOffOnButtonClick )
		self.btn_cvdRoughOn.Bind( wx.EVT_BUTTON, self.btn_cvdRoughOnOnButtonClick )
		self.btn_cvdRoughOff.Bind( wx.EVT_BUTTON, self.btn_cvdRoughOffOnButtonClick )
		self.btn_throttleAuto.Bind( wx.EVT_TOGGLEBUTTON, self.btn_throttleAutoOnToggleButton )
		self.btn_throttleOpen.Bind( wx.EVT_BUTTON, self.btn_throttleOpenOnButtonClick )
		self.btn_throttleClose.Bind( wx.EVT_BUTTON, self.btn_throttleCloseOnButtonClick )
		self.spin_throttleValue.Bind( wx.EVT_SPINCTRL, self.spin_throttleValueOnSpinCtrl )
		self.spin_throttleValue.Bind( wx.EVT_TEXT_ENTER, self.spin_throttleValueOnTextEnter )
		self.btn_throttleSet.Bind( wx.EVT_BUTTON, self.btn_throttleSetOnButtonClick )
		self.check_Ar.Bind( wx.EVT_CHECKBOX, self.check_ArOnCheckBox )
		self.txt_Ar.Bind( wx.EVT_TEXT_ENTER, self.btn_setArOnButtonClick )
		self.btn_setAr.Bind( wx.EVT_BUTTON, self.btn_setArOnButtonClick )
		self.check_CO2.Bind( wx.EVT_CHECKBOX, self.check_CO2OnCheckBox )
		self.txt_CO2.Bind( wx.EVT_TEXT_ENTER, self.btn_setCO2OnButtonClick )
		self.btn_setCO2.Bind( wx.EVT_BUTTON, self.btn_setCO2OnButtonClick )
		self.check_O2.Bind( wx.EVT_CHECKBOX, self.check_O2OnCheckBox )
		self.txt_O2.Bind( wx.EVT_TEXT_ENTER, self.btn_setO2OnButtonClick )
		self.btn_setO2.Bind( wx.EVT_BUTTON, self.btn_setO2OnButtonClick )
		self.check_CF4.Bind( wx.EVT_CHECKBOX, self.check_CF4OnCheckBox )
		self.txt_CF4.Bind( wx.EVT_TEXT_ENTER, self.btn_setCF4OnButtonClick )
		self.btn_setCF4.Bind( wx.EVT_BUTTON, self.btn_setCF4OnButtonClick )
		self.check_SF6.Bind( wx.EVT_CHECKBOX, self.check_SF6OnCheckBox )
		self.txt_SF6.Bind( wx.EVT_TEXT_ENTER, self.btn_setSF6OnButtonClick )
		self.btn_setSF6.Bind( wx.EVT_BUTTON, self.btn_setSF6OnButtonClick )
		self.btn_setDiscTime.Bind( wx.EVT_BUTTON, self.btn_setDiscTimeOnButtonClick )
		self.btn_setRFPower.Bind( wx.EVT_BUTTON, self.btn_setRFPowerOnButtonClick )
		self.txt_Pressure.Bind( wx.EVT_TEXT_ENTER, self.btn_setRFPowerOnButtonClick )
		self.btn_setPressure.Bind( wx.EVT_BUTTON, self.btn_setPressureOnButtonClick )
		self.btn_refresh.Bind( wx.EVT_BUTTON, self.btn_refreshOnButtonClick )
		self.btn_logIn.Bind( wx.EVT_BUTTON, self.btn_logInOnButtonClick )
		self.btn_logOut.Bind( wx.EVT_BUTTON, self.btn_logOutOnButtonClick )
		self.Bind( wx.EVT_TIMER, self.m_timer2OnTimer, id=wx.ID_ANY )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def EtcherFrameOnClose( self, event ):
		event.Skip()
	
	def EtcherFrameOnIdle( self, event ):
		event.Skip()
	
	def txt_llMarkOnTextEnter( self, event ):
		event.Skip()
	
	def btn_snSureOnButtonClick( self, event ):
		event.Skip()
	
	def btn_moveOutOnButtonClick( self, event ):
		event.Skip()
	
	def btn_moveInOnButtonClick( self, event ):
		event.Skip()
	
	def btn_gateOpenOnButtonClick( self, event ):
		event.Skip()
	
	def btn_GateCloseOnButtonClick( self, event ):
		event.Skip()
	
	def btn_llLoadInOnButtonClick( self, event ):
		event.Skip()
	
	def btn_llLoadOutOnButtonClick( self, event ):
		event.Skip()
	
	def btn_tpOnOnButtonClick( self, event ):
		event.Skip()
	
	def btn_tpOffOnButtonClick( self, event ):
		event.Skip()
	
	def btn_leakOnOnButtonClick( self, event ):
		event.Skip()
	
	def btn_leakOffOnButtonClick( self, event ):
		event.Skip()
	
	def btn_isoOnOnButtonClick( self, event ):
		event.Skip()
	
	def btn_isoOffOnButtonClick( self, event ):
		event.Skip()
	
	def btn_roughOnOnButtonClick( self, event ):
		event.Skip()
	
	def btn_roughOffOnButtonClick( self, event ):
		event.Skip()
	
	def btn_llTMPOnOnButtonClick( self, event ):
		event.Skip()
	
	def btn_llTMPOffOnButtonClick( self, event ):
		event.Skip()
	
	def btn_roughPumpOnOnButtonClick( self, event ):
		event.Skip()
	
	def btn_roughPumpOffOnButtonClick( self, event ):
		event.Skip()
	
	def check_autoGDOnCheckBox( self, event ):
		event.Skip()
	
	def btn_powerOnOnButtonClick( self, event ):
		event.Skip()
	
	def btn_powerOffOnButtonClick( self, event ):
		event.Skip()
	
	def btn_liftDownOnButtonClick( self, event ):
		event.Skip()
	
	def btn_liftUpOnButtonClick( self, event ):
		event.Skip()
	
	def btn_filmOnOnButtonClick( self, event ):
		event.Skip()
	
	def btn_filmOffOnButtonClick( self, event ):
		event.Skip()
	
	def btn_vacuumOnOnButtonClick( self, event ):
		event.Skip()
	
	def btn_vacuumOffOnButtonClick( self, event ):
		event.Skip()
	
	def btn_cvdTMPOnOnButtonClick( self, event ):
		event.Skip()
	
	def btn_cvdTMPOffOnButtonClick( self, event ):
		event.Skip()
	
	def btn_cvdRoughOnOnButtonClick( self, event ):
		event.Skip()
	
	def btn_cvdRoughOffOnButtonClick( self, event ):
		event.Skip()
	
	def btn_throttleAutoOnToggleButton( self, event ):
		event.Skip()
	
	def btn_throttleOpenOnButtonClick( self, event ):
		event.Skip()
	
	def btn_throttleCloseOnButtonClick( self, event ):
		event.Skip()
	
	def spin_throttleValueOnSpinCtrl( self, event ):
		event.Skip()
	
	def spin_throttleValueOnTextEnter( self, event ):
		event.Skip()
	
	def btn_throttleSetOnButtonClick( self, event ):
		event.Skip()
	
	def check_ArOnCheckBox( self, event ):
		event.Skip()
	
	def btn_setArOnButtonClick( self, event ):
		event.Skip()
	
	
	def check_CO2OnCheckBox( self, event ):
		event.Skip()
	
	def btn_setCO2OnButtonClick( self, event ):
		event.Skip()
	
	
	def check_O2OnCheckBox( self, event ):
		event.Skip()
	
	def btn_setO2OnButtonClick( self, event ):
		event.Skip()
	
	
	def check_CF4OnCheckBox( self, event ):
		event.Skip()
	
	def btn_setCF4OnButtonClick( self, event ):
		event.Skip()
	
	
	def check_SF6OnCheckBox( self, event ):
		event.Skip()
	
	def btn_setSF6OnButtonClick( self, event ):
		event.Skip()
	
	
	def btn_setDiscTimeOnButtonClick( self, event ):
		event.Skip()
	
	def btn_setRFPowerOnButtonClick( self, event ):
		event.Skip()
	
	
	def btn_setPressureOnButtonClick( self, event ):
		event.Skip()
	
	def btn_refreshOnButtonClick( self, event ):
		event.Skip()
	
	def btn_logInOnButtonClick( self, event ):
		event.Skip()
	
	def btn_logOutOnButtonClick( self, event ):
		event.Skip()
	
	def m_timer2OnTimer( self, event ):
		event.Skip()
	


