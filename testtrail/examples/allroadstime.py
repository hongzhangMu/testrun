#coding:utf-8
import os
import time


#定义每路口剩余红绿灯剩余
def lefttime_per_reads(miletime_now,start_time,greentime,yellowtime,redtime):
	"""
	miletime_now :当前时间乘以1000，为毫秒时间戳
	start_time:当前路口绿灯开始时间，如9点半直行为绿灯，毫秒时间戳
	greentime 直行路口绿灯秒数
	redtime:直行红灯秒数
	yellowtime:黄灯秒数时间
	"""
	# miletime_now = 1587609000000
	alltime = int(greentime + redtime+ yellowtime)
	green_yellow = int(greentime+yellowtime)
	delta_time = (miletime_now - start_time)/1000
	yushu = int(delta_time)%alltime
	print(int(delta_time)%alltime)
	green,yellow,red =0,0,0
	if yushu<=greentime:
		green = greentime - yushu
	elif yushu >greentime and yushu<=green_yellow:
		green = 0 
		yellow =  yellowtime-(yushu -greentime)
	elif yushu>green_yellow:
		red = redtime-( yushu -green_yellow)
	print('================================',green,yellow,red)
	return green,yellow,red

#当前时刻红绿灯情况
#向后累计十分钟
def getafter10min(inttime,greentime,yellowtime,redtime):
	"""
	
	inttime:当前时间加上剩余时间
	greentime 直行路口绿灯秒数
	redtime:直行红灯秒数
	yellowtime:黄灯秒数时间
	"""
	alltime = int(greentime + redtime+ yellowtime)
	green_yellow = int(greentime+yellowtime)
	print(inttime)
	timeArray = time.localtime(inttime)
	otherStyleTime = time.strftime("%H:%M:%S", timeArray)
	print(otherStyleTime)   # 2013--10--10 15:40:00
	print(inttime)
	contrcut = []
	timeArray = time.localtime(inttime)
	otherStyleTime = time.strftime("%H:%M:%S", timeArray)
	contrcut.append(otherStyleTime)
	couttime = 6
	try:
		counttime = 400%(greentime+yellowtime+redtime)+1
	except:
		couttime = 6
	for i in range(0,counttime):
		nexttime = (inttime+greentime+alltime*i)
		nnexttime = (inttime+green_yellow+alltime*i)
		nnnextime = (inttime+alltime+alltime*i)
		timeArray1 = time.localtime(nexttime)
		otherStyleTime1 = time.strftime("%H:%M:%S", timeArray1)
		timeArray2 = time.localtime(nnexttime)
		otherStyleTime2 = time.strftime("%H:%M:%S", timeArray2)
		timeArray3 = time.localtime(nnnextime)
		otherStyleTime3 = time.strftime("%H:%M:%S", timeArray3)
		contrcut.append(otherStyleTime1)
		contrcut.append(otherStyleTime2)
		contrcut.append(otherStyleTime3)
	# print('=============710---------===',contrcut)
	return contrcut


# #构造一条路的时刻
def concattimes(miletime_now,start_time,greentime,yellowtime,redtime):
	final_lists =[]
	print(greentime,yellowtime,redtime,'===================')
	leftgreen,leftyellow,leftred  = lefttime_per_reads(miletime_now,start_time,greentime,yellowtime,redtime)
	inttime = miletime_now/1000
	flagleftcolor = 'green'
	leftinttime = 0
	fristtime_lists = []
	if leftgreen!=0:
		leftinttime =leftgreen+inttime
		timeArray = time.localtime(leftinttime)
		otherStyleTime = time.strftime("%H:%M:%S", timeArray)
		leftinttime1 =leftgreen+inttime+yellowtime
		timeArray1 = time.localtime(leftinttime1)
		otherStyleTime1 = time.strftime("%H:%M:%S", timeArray1)
		leftinttime2 =leftgreen+inttime+yellowtime+redtime
		timeArray2 = time.localtime(leftinttime2)
		otherStyleTime2 = time.strftime("%H:%M:%S", timeArray2)
		print('444444444--------/',otherStyleTime,otherStyleTime1,otherStyleTime2)   # 2013--10--10 15:40:00
		fristtime_lists.append(otherStyleTime)
		fristtime_lists.append(otherStyleTime1)
		fristtime_lists.append(otherStyleTime2)
		leftnowtime = (inttime +leftgreen+yellowtime+redtime)
		loadtime_lists = getafter10min(leftnowtime,greentime,yellowtime,redtime)
		final_lists = fristtime_lists+(loadtime_lists)
		flagleftcolor = 'green'
	elif leftyellow!=0:
		leftinttime =leftyellow+inttime
		timeArray = time.localtime(leftinttime)
		otherStyleTime = time.strftime("%H:%M:%S", timeArray)
		leftinttime1 =leftyellow+inttime+redtime
		timeArray1 = time.localtime(leftinttime1)
		otherStyleTime1 = time.strftime("%H:%M:%S", timeArray1)
		fristtime_lists.append(otherStyleTime)
		fristtime_lists.append(otherStyleTime1)
		leftnowtime = inttime+leftyellow+redtime
		loadtime_lists = getafter10min(leftnowtime,greentime,yellowtime,redtime)
		final_lists = fristtime_lists +(loadtime_lists)
		print(otherStyleTime,otherStyleTime1)
		print('yellow')
		flagleftcolor = 'yellow'
	elif leftred !=0:
		leftinttime = leftred
		print('red')
		leftinttime =leftred+inttime
		timeArray = time.localtime(leftinttime)
		otherStyleTime = time.strftime("%H:%M:%S", timeArray)
		fristtime_lists.append(otherStyleTime)
		leftnowtime = leftred + inttime
		loadtime_lists = getafter10min(leftnowtime,greentime,yellowtime,redtime)
		final_lists = fristtime_lists +(loadtime_lists)
		flagleftcolor = 'red'
	return final_lists,flagleftcolor
#构造400秒的点。
def ten_minsdata(inttime,miaoshu):
	nowtime = []
	for i in range(1,miaoshu):
		nexttime = (inttime+i)
		timeArray1 = time.localtime(nexttime)
		otherStyleTime1 = time.strftime("%H:%M:%S", timeArray1)
		nowtime.append(otherStyleTime1)
	# print(nowtime)
	return nowtime
