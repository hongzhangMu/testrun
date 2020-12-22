#-*-coding:utf-8-*-
import json
from flask import make_response
import datetime,time
from math import sin, asin, cos, radians, fabs, sqrt
from testtrail.examples.allroadstime import *
from testtrail.models.trail import Trail
from testtrail.models.test_roads_name import TestRoadsName
from testtrail.models.roadname import Roadname
import numpy as np
def built_response(code, msg, data):
    """
    根据code，msg，data构造合适的返回数据
    :param code: 状态码
    :param msg: 消息
    :param data: 数据
    :return: 构造好的数据，可以直接返回
    """
    res = dict(code=code, msg=msg, data=data)
    rsp = make_response(json.dumps(res))
    rsp.headers['Access-Control-Allow-Origin'] = '*'
    rsp.headers['Access-Control-Allow-Headers'] ='Content-Type, Content-Length, Authorization, Accept, X-Requested-With , yourHeaderFeild'
    rsp.headers['Access-Control-Allow-Methods'] ='PUT,POST,GET,DELETE,OPTIONS'

    rsp.headers['Content-Type'] = 'application/json;charset=utf-8'
    return rsp
def built_resp(code, msg, data,nowspeed,speed,stopcishu,stoptime):
    """
    根据code，msg，data构造合适的返回数据
    :param code: 状态码
    :param msg: 消息
    :param data: 数据
    :return: 构造好的数据，可以直接返回
    """
    res = dict(code=code, msg=msg, data=data,nowspeed=nowspeed,speed=speed,stopcishu=stopcishu,stoptime=stoptime)
    rsp = make_response(json.dumps(res))
    rsp.headers['Access-Control-Allow-Origin'] = '*'
    rsp.headers['Access-Control-Allow-Headers'] ='Content-Type, Content-Length, Authorization, Accept, X-Requested-With , yourHeaderFeild'
    rsp.headers['Access-Control-Allow-Methods'] ='PUT,POST,GET,DELETE,OPTIONS'

    rsp.headers['Content-Type'] = 'application/json;charset=utf-8'
    return rsp
# 分割字符
def str2list(str):
    if str == '':
        return []
    else:
        return str.split(',')


def str2intList(str):
    if str == '':
        return []
    else:
        return [int(each) for each in str.split(',')]

def time2str(strtime):
    year = datetime.datetime.now().year
    mon = datetime.datetime.now().month
    day = datetime.datetime.now().day
    tss1 = str(year)+"-"+str(mon)+"-"+str(day)+" "+strtime
    timeArray = time.strptime(tss1, "%Y-%m-%d %H:%M:%S")

    timeStamp = int(time.mktime(timeArray))
    print(timeStamp)
    return timeStamp


def hav(theta):
    s = sin(theta / 2)
    return s * s

def get_distance_hav(lat0, lng0, lat1, lng1):
    try:
        EARTH_RADIUS = 6371
        distance = 0
        "用haversine公式计算球面两点间的距离。"
        # 经纬度转换成弧度
        lat0 = float(lat0)
        lat1 = float(lat1)
        lng0 = float(lng0)
        lng1 = float(lng1)
        lat0 = radians(lat0)
        lat1 = radians(lat1)
        lng0 = radians(lng0)
        lng1 = radians(lng1)
        dlng = fabs(lng0 - lng1)
        dlat = fabs(lat0 - lat1)
        h = hav(dlat) + cos(lat0) * cos(lat1) * hav(dlng)
        distance = int(2 * EARTH_RADIUS * asin(sqrt(h))*3600)
        if distance>700:
            distance = 0
        print('aaaa---11',distance)
    except:
        print('except----1')
        distance =0
    return distance
def pre_processroads(inttime,start_time,greentime,yellowtime,redtime,distance,roadname,index):
    """

    :param inttime: 当前时刻事件time.time
    :param start_time: 绿灯开始时间
    :param greentime: 绿灯间隔时间
    :param yellowtime: 黄灯间隔时间
    :param redtime: 红灯间隔时间
    :param roadname:路口名字
    :return: x轴数据和visualmap数据
    """
    # inttime = int(time.time())
    # final_lists = []
    # start_time = 1587605400000
    # miletime_now = inttime * 1000
    # greentime = 109
    # yellowtime = 4
    # redtime = 2
    miletime_now = inttime * 1000
    allroadtimes, flagleftcolor = concattimes(miletime_now, start_time, greentime, yellowtime, redtime)
    tendata = ten_minsdata(inttime,400)

    fin_list = []
    count = 0
    aaa = []
    aaa.append(0)
    # print('aa1111111time-----------',allroadtimes)
    for i in tendata:
        if i in allroadtimes:
            # print('ok')
            aaa.append(count)
            fin_list.append([i, distance])

        else:
            fin_list.append([i, ''])
        count += 1
    fin_list[0][1] = distance
    fin_list[len(fin_list) - 1][1] = distance
    serices = []
    print('-=-=-=-=-=-111111----',aaa)
    for i in range(0, len(aaa) - 3, 3):
        print('-000--------',i,aaa[i])
        if flagleftcolor == 'green':
            serices.append(dict(gt=aaa[i], lte=aaa[i + 1], color='green'))
            serices.append(dict(gt=aaa[i + 1], lte=aaa[i + 2], color='yellow'))
            serices.append(dict(gt=aaa[i + 2], lte=aaa[i + 3], color='red'))
        elif flagleftcolor == 'yellow':
            serices.append(dict(gt=aaa[i], lte=aaa[i + 1], color='yellow'))
            serices.append(dict(gt=aaa[i + 1], lte=aaa[i + 2], color='red'))
            serices.append(dict(gt=aaa[i + 2], lte=aaa[i + 3], color='green'))
        else:
            serices.append(dict(gt=aaa[i], lte=aaa[i + 1], color='red'))
            serices.append(dict(gt=aaa[i + 1], lte=aaa[i + 2], color='green'))
            serices.append(dict(gt=aaa[i + 2], lte=aaa[i + 3], color='yellow'))
    if len(aaa) % 3 == 1:
        serices.append(dict(gt=aaa[len(aaa) - 1], lte=len(fin_list), color=flagleftcolor))
    elif len(aaa) % 3 == 2:
        serices.append(dict(gt=aaa[len(aaa) - 2], lte=aaa[len(aaa) - 1], color=flagleftcolor))
        serices.append(dict(gt=aaa[len(aaa) - 1], lte=len(fin_list), color=nextcolor(flagleftcolor)))
    else:
        serices.append(dict(gt=aaa[len(aaa) - 3], lte=aaa[len(aaa) - 2], color=flagleftcolor))
        serices.append(dict(gt=aaa[len(aaa) - 2], lte=aaa[len(aaa) - 1], color=nextcolor(flagleftcolor)))
        serices.append(dict(gt=aaa[len(aaa) - 1], lte=len(fin_list), color=nextnextcolor(flagleftcolor)))
    makeseriesitems = makeseriesdict(roadname,fin_list)
    makevisualMapitems = makevisualMap(index,serices)
    return makeseriesitems,makevisualMapitems

def makeseriesdict(name,data):
    tmp = {
        "name": name,
        "type": 'line',
        "smooth": "true",
        "symbolSize": 5,
        "connectNulls": 'true',
        "data":data
    }
    return tmp
def makevisualMap(seriesIndex,data):
    tmp = {
        "hoverLink":"false",
        "show": False,
        "showSymbol": "false",
        "dimension": 0,
        "seriesIndex":seriesIndex,
        "pieces": data
    }
    return tmp
#计算下时刻的红绿灯情况
def nextcolor(flagleftcolor):
    nextcolor ='green'
    if flagleftcolor == 'green':
        nextcolor = 'yellow'
    elif flagleftcolor == 'yellow':
        nextcolor = 'red'
    else:
        nextcolor = 'green'
    return nextcolor
#计算下下时刻的红绿灯情况
def nextnextcolor(flagleftcolor):
    nextcolor ='green'
    if flagleftcolor == 'green':
        nextcolor = 'red'
    elif flagleftcolor == 'yellow':
        nextcolor = 'green'
    else:
        nextcolor = 'yellow'
    return nextcolor

#单次平均时间
# processing
def per_processing_speed(la0,la1,long1,long2,time1,time2):
    try:

        distance_tmp = get_distance_hav_dis(la0,long1,la1,long2)
        left_time = int(time2-time1)
        # left_time = getcalc_time(time1,time2)
        ave_speed  = int(distance_tmp/left_time)
    except:
        ave_speed = 0
    return ave_speed
#获取当前场景初始点
def getscenesPoint(type):
    points =[]
    try:
        first_data = TestRoadsName.query.filter(type==TestRoadsName.name).first()
        type_roadname = first_data.type
        #根据type寻找当前路段
        data_filter = Roadname.query.filter(type_roadname==Roadname.type).all()

        for i in data_filter:
            if i.distance==0:
                points=[i.latitude,i.longitude]
                break
        print('========217===',points)
    except:
        points = [40.011467, 116.406784]
    print('points----------',points)
    return points
def get_distance_hav_dis(lat0, lng0, lat1, lng1):
    try:
        EARTH_RADIUS = 6371
        distance = 0
        "用haversine公式计算球面两点间的距离。"
        # 经纬度转换成弧度
        lat0 = float(lat0)
        lat1 = float(lat1)
        lng0 = float(lng0)
        lng1 = float(lng1)
        lat0 = radians(lat0)
        lat1 = radians(lat1)
        lng0 = radians(lng0)
        lng1 = radians(lng1)
        dlng = fabs(lng0 - lng1)
        dlat = fabs(lat0 - lat1)
        h = hav(dlat) + cos(lat0) * cos(lat1) * hav(dlng)
        distance = int(2 * EARTH_RADIUS * asin(sqrt(h))*1000)
        print('a-------aaa---11',distance)
    except:
        print('except----1')
        distance =0
    return distance
#计算平均速度
def aveDisSpeed(distance,times):
    try:
        allroaddis_first = Trail.query.filter().order_by('id').limit(2)
        print('new--new1--------',allroaddis_first[0].latitude)
        print('new--new222--------',allroaddis_first[1].latitude)
        lat1 = allroaddis_first[0].latitude
        lat2 = allroaddis_first[1].latitude
        long1 = allroaddis_first[0].longitude
        long2 = allroaddis_first[1].longitude
        print('====end=====',long1,long2,lat2,lat1)
        distance = get_distance_hav_dis(lat1,long1,lat2,long2)
        print('start---------')
        speed = int(float(distance)*3.6)
        print('speed--------',speed)
    except:
        speed = 0
    return int(speed)
#获取当前时刻速度
def getallpoint_distance(imei):
    try:
        count_data = Trail.query.filter(Trail.imei == imei).all()
        tmp_len = len(count_data)
        time1 = count_data[0].date_time
        time2 = count_data[tmp_len - 1].date_time
        tmp_dis = 0
        for i in range(0, len(count_data) - 1):
            sp = get_distance_hav(count_data[i].latitude, count_data[i].longitude, count_data[i + 1].latitude,
                                  count_data[i + 1].longitude)
            print ('sp----------', sp)
            tmp_dis += sp
    except:
        tmp_dis = 0
    return tmp_dis
#获取当前时刻产生的数据
def getspeed_data(imei):
    count_data = Trail.query.filter(Trail.imei ==imei).all()
    tmp_len = len(count_data)
    time1 = count_data[0].date_time
    time2 = count_data[tmp_len - 1].date_time
    tmp_speed =0
    for i in range(0,len(count_data)-1):
        sp = get_distance_hav(count_data[i].latitude,count_data[i].longitude,count_data[i+1].latitude,count_data[i+1].longitude)
        print ('sp----------',sp)
        tmp_speed += sp
    try:
        final_speed = tmp_speed/(len(count_data)-1)
    except:
        final_speed = 0
    return final_speed

#获取当前路段的运行情况，剔除少于180秒的情况
def getSomeroadCishu(roadname):
    num = Trail.query.filter(Trail.type==roadname).distinct().values("imei")
    num_list = []
    for i in num:
        count_times = Trail.query.filter(Trail.imei==i.imei).all()
        print(type(count_times))
        tmp_len = len(count_times)
        if tmp_len>120:
            cishu,time_stop = computer_cishu_time(count_times)
            la0 = count_times[0].latitude
            la1 = count_times[tmp_len-1].latitude
            long1 = count_times[0].longitude
            long2 = count_times[tmp_len-1].longitude
            time1 = count_times[0].date_time
            time2 = count_times[tmp_len-1].date_time
            ave_speed = processing_time(la0,la1,long1,long2,time1,time2)
            if ave_speed<120 and ave_speed>1:
                num_list.append([ave_speed,cishu,time_stop])
    print(num_list)
    a = np.array(num_list)
    bb = np.mean(a,axis=0)
    print(int(bb[0]),int(bb[1]),int(bb[2]))
    return int(bb[0]),int(bb[1]),int(bb[2]),len(num_list[0])
# processing
def processing_time(la0,la1,long1,long2,time1,time2):
    distance_tmp = get_distance_hav_dis(la0,long1,la1,long2)
    left_time = getcalc_time(time1,time2)
    ave_speed  = distance_tmp/left_time
    return ave_speed
#时间差
def getcalc_time(aaa,bbb):
    aaa = aaa
    bbb = bbb
    # dd = datetime.datetime.strptime(aaa, "%Y-%m-%d %H:%M:%S")
    dd = aaa
    t = dd.timetuple()
    timeStamp1 = int(time.mktime(t))
    dd1 = bbb
    t = dd1.timetuple()
    timeStamp2 = int(time.mktime(t))
    time_cishu = timeStamp2 - timeStamp1
    return time_cishu
#计算停车次数和时间
def computer_cishu_time(items):
    sequence = []
    for i in items:
        sequence.append(i.latitude+i.longitude)
    counts = {}
    for x in sequence:
        if x in counts:
            counts[x] += 1
        else:
            counts[x] = 1
    tmp = counts
    counts = 0
    stoptime = 0
    for i in tmp:
        #停留3秒以上算停车
        if tmp[i] > 5:
            counts += 1
            stoptime += tmp[i] - 1
    return counts,int(stoptime)

def real_trackLength(imei):
    all_trail = Trail.query.filter(Trail.imei == imei).all()
    all_distance_real = 0
    first_point = []
    end_point = []
    print (type(all_trail),len(all_trail))
    tmp_all_trail = []
    for i in range(0, len(all_trail), 1):
        print (all_trail[len(all_trail)-1].longitude)
        if all_trail[i].latitude==all_trail[len(all_trail)-1].latitude and all_trail[i].longitude==all_trail[len(all_trail)-1].longitude:
            continue
        else:
            tmp_all_trail.append(all_trail[i])
    print ('----',len(all_trail),tmp_all_trail)
    all_trail = tmp_all_trail
    for i in range(0,len(all_trail),1):
        print(all_trail[i].imei)
        try:
            if i==0:
                first_point = [all_trail[i].latitude,all_trail[i].longitude]
            distance =get_distance_hav_dis(all_trail[i].latitude,all_trail[i].longitude,all_trail[i+1].latitude,all_trail[i+1].longitude)
            dat_time = getcalc_time(all_trail[i].date_time,all_trail[i+1].date_time)
            # print ('distance-----------',distance)
            real_per_distance = per_track_distance(distance,dat_time)
            # print ('--------',real_per_distance)
            all_distance_real +=real_per_distance
            end_point = [all_trail[i].latitude,all_trail[i].longitude]
        except:
            continue
    dream_distance = get_distance_hav_dis(first_point[0],first_point[1],end_point[0],end_point[1])

    return all_distance_real,dream_distance

def per_track_distance(distance,dis_time):
    dis = ((dis_time*11.11)*(dis_time*11.11) +distance*distance) **0.5
    return dis


def rate_trackLength(imei):
    try:
        real_track_length ,think_length= real_trackLength(imei=imei)
        think_length = think_length*(2**0.5)
        print (real_track_length,think_length)
        rate_real = real_track_length/think_length
        final_rate_real = round(rate_real,2)
        return final_rate_real
    except:
        return 0
