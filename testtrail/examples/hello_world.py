# coding=utf-8

from flask import render_template,request
from guniflask_cli.config import _template_folder
from guniflask.web import blueprint, get_route,post_route
from testtrail.examples.util import *
from testtrail.models.roadname import Roadname
from testtrail.models.trail import Trail
from testtrail.models.test_roads_name import TestRoadsName
from testtrail import db
from urllib import parse
import random
from sqlalchemy import desc
@blueprint('/hello-world', template_folder=_template_folder)
class HelloWorld:
    def __init__(self):
        self.roadname = Roadname.query.filter(Roadname.roadsection!=None,Roadname.ns_green_time!=None).all()
        self.alltimes = {}
        self.echartsdata = {}
        self.lo = 116.407628
        self.la = 39.994662
        self.firstTime_position = {}
        self.first_origin_time = {}
        self.other_lo = 0
        self.other_la = 0
    @get_route('/')
    def home_page(self):
        """
        Home page
        """
        return render_template('hello_world/index.html')

    @get_route('/test/<imei>')
    def test(self,imei):
        """
        :param:
        :return: json data
        """
        print('=111111111135555555550',imei)
        tmp_imei = imei.split(':')[0]
        typename = parse.unquote(imei.split(':')[1])
        name_type_num = TestRoadsName.query.filter(TestRoadsName.name ==typename).first()
        name_type_num = name_type_num.type
        print('mmmmmmmmmmmmm',name_type_num)
        roadnames = Roadname.query.filter(Roadname.distance!=0,Roadname.ns_green_time!=None,Roadname.type==name_type_num).all()
        roadinfos = []
        roadinfos1 = []
        index = 0
        print(imei,tmp_imei,'===--1111111111111')
        inttime = int(time.time())
        for i in roadnames:
            roadname = str(i.name)
            timeStamp = time2str(str(i.greenstart_time))
            # roadinfos.append([i.latitude,i.longitude,timeStamp,i.ns_green_time,i.ns_yellow_time,i.ns_red_time])
            start_time = timeStamp*1000
            print('1111-----',i.name,start_time)
            greentime = int(i.ns_green_time)
            yellowtime = int(i.ns_yellow_time)
            redtime = int(i.ns_red_time)
            distance = int(i.distance)
            print('------------------------')
            print('------------------------', start_time, greentime, yellowtime, redtime)
            fin_list,serices = pre_processroads(inttime,start_time,greentime,yellowtime,redtime,distance,roadname,index)
            # roadinfos.append({"series":fin_list,"visualMap":serices})
            #test

            #test
            roadinfos.append(fin_list)
            roadinfos1.append(serices)
            index+=1
        #test
        tendata = ten_minsdata(inttime, 400)
        test_data_list = []
        for i in tendata:
            test_data_list.append([i, ''])
        self.alltimes[tmp_imei] = test_data_list
        #TODO 6.8

        test = {
            "name": '用户',
            "type": 'line',
            "smooth": "true",
            "symbolSize": 5,
            "connectNulls": 'true',
            "data": test_data_list
        }
        roadinfos.append(test)
        #test
        print ('-----87------\n')
        print ('-----87------\n')
        print (roadinfos)
        items = {"series": roadinfos, "visualMap": roadinfos1}
        self.echartsdata[tmp_imei] = items
        return built_response(200,'ok',items)
    @post_route('/lalosave')
    def save_lalo(self):
        data = request.get_json()
        la = data['la']
        lo = data['lo']

        imei = data['imei']
        type = parse.unquote(data['type'])
        # print ('111111111198-----111198---\n\n')
        # print ('111111111198-----111198---',self.firstTime_position,self.first_origin_time)
        if imei not in self.firstTime_position.keys():
            self.firstTime_position[imei] =[la,lo]
            # print(type)
            self.first_origin_time[imei] = time.time()
        # print ('111111111198-----------------\n\n')
        # print ('111111111198-------------------', self.firstTime_position, self.first_origin_time)
        if type=='其他路段':
            self.other_la = la
            self.other_lo = lo
            other_point = [self.other_la,self.other_lo]
            # now_distances = get_distance_hav_dis(la, lo, self.firstTime_position[imei][0], self.firstTime_position[imei][1])
            now_distances = getallpoint_distance(imei)
            inttime = int(time.time())
            # print('--------------1111----',now_distances)
            timeArray1 = time.localtime(inttime)
            otherStyleTime1 = time.strftime("%H:%M:%S", timeArray1)
            # 判断是否超过400秒 todo
            len_alltimes = len(self.alltimes[str(imei)]) - 1
            tmplast_item = self.alltimes[str(imei)][len_alltimes][0]
            time_tmp = time2str(tmplast_item)
            # print(self.echartsdata[str(imei)])
            # if time_tmp <=inttime:
            #     self.flush_view(str(imei))
            #     return built_response(200, 'ok', self.echartsdata[imei])
            # else:
            # ,o
            distan = []
            for i in self.alltimes[str(imei)]:
                if i[1] != '':
                    distan.append(i)
                if otherStyleTime1 == i[0]:
                    i[1] = now_distances

            # self.savetrail(first_dic,second_dic,str(imei),type)
            # todo
            self.savetrail(la, lo, str(imei), type)
            aa = len(distan) - 1
            try:

                dics_left_dis = distan[aa][1] - distan[aa - 1][1]
                time_left = time2str(distan[len(distan) - 2][0])
                time_right = time2str(distan[len(distan) - 1][0])
                times_left = time_right - time_left
            except:
                dics_left_dis = 0
                times_left = 1
            # have_left_times = distan[len(distan)-1][0] - distan[0][0]
            # todo 实时速度
            nowspeedid = get_distance_hav(la, lo, self.la, self.lo)
            # print('self.firstTime__positin--------------',self.firstTime_position[imei])
            # speedid = per_processing_speed(la, self.firstTime_position[imei][0], lo, self.firstTime_position[imei][1],
            #                                self.first_origin_time[imei], time.time())
            speedid = int(getspeed_data(str(imei)))
            stopcishu = 0
            stoptime = 0
            print ('------------end---------------------------')
            print ('------------end---------------------------')
            print ('------------end---------------------------')
            stopcishu, stoptime = self.computestopcishu_time(str(imei))
            alen = len(self.echartsdata[str(imei)]["series"]) - 1
            final_list = self.echartsdata[str(imei)]["series"][alen]
            print('end')
            print ('end\n')
            print ('end\n')
            print ('end\n')
            print ('end\n')
            print ('end\n')
            print ('-------',speedid)
            self.la = la
            self.lo = lo
            return built_resp(200, 'ok', final_list, nowspeedid, speedid, stopcishu, stoptime)
        else:
            #获取当前场景point
            print('start------')
            point = getscenesPoint(type)
            #test points test 距离TODO
            # first_dic,second_dic = self.testpoints(point)
            # print(first_dic,second_dic)
            # now_distances = get_distance_hav(first_dic, second_dic, point[0], point[1])

            now_distances = get_distance_hav_dis(la, lo, point[0], point[1])
            inttime = int(time.time())
            # print('--------------1111----',now_distances)
            timeArray1 = time.localtime(inttime)
            otherStyleTime1 = time.strftime("%H:%M:%S", timeArray1)
            print(inttime)
            #判断是否超过400秒 todo
            len_alltimes = len(self.alltimes[str(imei)])-1
            tmplast_item = self.alltimes[str(imei)][len_alltimes][0]
            time_tmp = time2str(tmplast_item)
            # print(self.echartsdata[str(imei)])
            # if time_tmp <=inttime:
            #     self.flush_view(str(imei))
            #     return built_response(200, 'ok', self.echartsdata[imei])
            # else:
                # ,o
            distan = []
            for i in self.alltimes[str(imei)]:
                if i[1]!='':
                    distan.append(i)
                if otherStyleTime1 ==i[0]:
                    i[1] = now_distances

            # self.savetrail(first_dic,second_dic,str(imei),type)
            #todo
            self.savetrail(la,lo,str(imei),type)
            aa = len(distan)-1
            try:

                dics_left_dis = distan[aa][1] - distan[aa-1][1]
                time_left = time2str(distan[len(distan) - 2][0])
                time_right = time2str(distan[len(distan) - 1][0])
                times_left = time_right - time_left
            except:
                dics_left_dis = 0
                times_left = 1
            # have_left_times = distan[len(distan)-1][0] - distan[0][0]
            #todo 实时速度
            nowspeedid = get_distance_hav(la, lo, self.la,self.lo)

            # speedid = per_processing_speed(la, self.firstTime_position[imei][0], lo,self.firstTime_position[imei][1],self.first_origin_time[imei],time.time())
            # speedid = per_processing_speed(la, self.firstTime_position[imei][0], lo,self.firstTime_position[imei][1],self.first_origin_time[imei],time.time())


            speedid = int(getspeed_data(str(imei)))
            stopcishu = 0
            stoptime = 0

            stopcishu,stoptime = self.computestopcishu_time(str(imei))
            alen = len(self.echartsdata[str(imei)]["series"])-1
            final_list = self.echartsdata[str(imei)]["series"][alen]

            self.la = la
            self.lo = lo
            return built_resp(200,'ok',final_list,nowspeedid,speedid,stopcishu,stoptime)
    def savetrail(self,la,lo,imei,type):
        timeStamp = int(time.time())
        timeArray = time.localtime(timeStamp)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        trail = Trail()
        trail.date_time =otherStyleTime
        trail.latitude = la
        trail.longitude = lo
        trail.imei = imei
        trail.type = type
        db.session.add(trail)
        db.session.flush()
        db.session.commit()

    @get_route('/settingnames/type=<segnames>')
    def segnames(self, segnames):
        print(segnames)
        allroadnames = Roadname.query.filter(Roadname.type==segnames,Roadname.ns_green_time!=None).all()
        items = []
        for i in allroadnames:
            print(i.name)
            items.append(dict(id=i.id,name=i.name,greenstart_time = str(i.greenstart_time),distance =i.distance,longitude=i.longitude,latitude=i.latitude,
                              ns_green_time= i.ns_green_time,ns_yellow_time=i.ns_yellow_time,ns_red_time=i.ns_red_time))
        print(items)
        return built_response(200, 'ok', items)

    @get_route('/getlalo/type=<segnames>')
    def getlalo(self, segnames):
        print(segnames)
        allroadnames = Roadname.query.filter(Roadname.type == segnames).first()
        items = []
        items.append(allroadnames.latitude)
        items.append(allroadnames.longitude)
        return built_response(200, 'ok', items)
    @get_route('/add_settings')
    def add_settings(self):
        data =  request.args
        name = data.get('name')
        distance = data.get('distance')
        greenstart_time = data.get('greenstart_time1')
        ns_green_time = data.get('ns_green_time')
        ns_yellow_time = data.get('ns_yellow_time')
        ns_red_time = data.get('ns_red_time')
        startTime = greenstart_time.split(' ')[1]
        type = data.get('type')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        u = Roadname()
        u.greenstart_time = startTime
        u.ns_green_time = ns_green_time
        u.ns_yellow_time = ns_yellow_time
        u.ns_red_time = ns_red_time
        u.type = type
        u.distance = distance
        u.name = name
        u.latitude = latitude
        u.longitude = longitude
        db.session.add(u)
        db.session.flush()
        db.session.commit()
        return built_response(200, 'ok', [])
    @get_route('/update_settings')
    def update_settings(self):
        data = request.args
        print(data)
        id = data.get('id')
        name = data.get('name')
        greenstart_time = data.get('greenstart_time1')
        ns_green_time = data.get('ns_green_time')
        ns_yellow_time = data.get('ns_yellow_time')
        ns_red_time = data.get('ns_red_time')
        ns_long = data.get('longitude')
        ns_lagitute = data.get('latitude')
        dis = data.get('distance')
        startTime = greenstart_time.split(' ')[1]
        print(startTime)
        u = Roadname.query.filter(Roadname.id == id ).first()
        u.name = name
        u.greenstart_time = greenstart_time
        u.ns_green_time = ns_green_time
        u.ns_yellow_time = ns_yellow_time
        u.ns_red_time = ns_red_time
        u.distance = dis
        u.longitude = ns_long
        u.latitude = ns_lagitute
        db.session.flush()
        db.session.commit()
        return built_response(200, 'ok', [])


    def flush_view(self,imei):
        roadnames = Roadname.query.filter(Roadname.roadsection != None, Roadname.ns_green_time != None).all()
        roadinfos = []
        roadinfos1 = []
        index = 0
        print(imei)
        inttime = int(time.time())
        for i in roadnames:
            roadname = str(i.name)
            timeStamp = time2str(str(i.greenstart_time))
            # roadinfos.append([i.latitude,i.longitude,timeStamp,i.ns_green_time,i.ns_yellow_time,i.ns_red_time])

            start_time = timeStamp * 1000
            greentime = int(i.ns_green_time)
            yellowtime = int(i.ns_yellow_time)
            redtime = int(i.ns_red_time)
            distance = int(i.distance)
            print('------------------------')
            print('------------------------',start_time,greentime,yellowtime,redtime)
            fin_list, serices = pre_processroads(inttime, start_time, greentime, yellowtime, redtime, distance,
                                                 roadname, index)
            # roadinfos.append({"series":fin_list,"visualMap":serices})
            # test

            # test
            roadinfos.append(fin_list)
            roadinfos1.append(serices)
            index += 1
        # test
        tendata = ten_minsdata(inttime, 400)
        test_data_list = []
        for i in tendata:
            test_data_list.append([i, ''])
        self.alltimes[imei] = test_data_list
        test = {
            "name": '用户',
            "type": 'line',
            "smooth": "true",
            "symbolSize": 5,
            "connectNulls": 'true',
            "data": test_data_list
        }
        roadinfos.append(test)
        # test
        items = {"series": roadinfos, "visualMap": roadinfos1}
        self.echartsdata[imei] = items

    # todo 计算停车次数和停车时间
    def computestopcishu_time(self,imei):
        items = Trail.query.filter(Trail.imei == imei).all()
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

    #
    # def computestoptime(self,imei):
    #     stoptime = 0
    #     return stoptime
    @get_route('/get_roads_name')
    def get_roads_name(self):
        allitems = TestRoadsName.query.filter().all()
        final_list = []
        for i in allitems:
            print(i)
            final_list.append(dict(name=i.name,type=i.type))
        return built_response(200, 'ok', final_list)


    def testpoints(self,points):
        num = random.random()
        first_point = points[0]+num*0.007+0.0015
        second_point = points[1]+num*0.007+0.0015
        return first_point,second_point

    @post_route('/get_current_position')
    def get_current_position(self):
        inttime = int(time.time())
        data = request.get_json()
        imei = data['imei']
        type = parse.unquote(data['type'])

        timeArray1 = time.localtime(inttime)
        otherStyleTime1 = time.strftime("%H:%M:%S", timeArray1)
        current_lation = Trail.query.filter(imei ==Trail.imei,type==Trail.type).order_by(desc(Trail.id)).first()
        #.latitude, i.longitude
        point = getscenesPoint(type)
        print (point)
        now_distances = get_distance_hav_dis(current_lation.latitude, current_lation.longitude, point[0], point[1])
        print(current_lation.latitude,current_lation.longitude,inttime,otherStyleTime1)
        timelist = [otherStyleTime1,now_distances]
        return built_response(200,'ok',timelist)
    @post_route('/get_roadname_trail')
    def get_roadname_trail(self):
        data = request.get_json()
        type = parse.unquote(data['type'])
        imei = data['imei']
        print ('---------------===========----------/n')
        print ('---------------===========----------/n')
        print ('---------------===========----------/n')
        print ('---------------===========----------/n')
        print (imei)
        try:
            rate_real = rate_trackLength(imei)
            speed,cishu_stops,time_stops,test_cishu = getSomeroadCishu(type)
        except:
            rate_real = 0
            speed, cishu_stops, time_stops, test_cishu =0,0,0,0
        return built_response(200,'ok',[speed,cishu_stops,time_stops,test_cishu,rate_real])
    @post_route('/rate_distance')
    def rate_distance(self):
        data = request.get_json()
        imei = data['imei']
        rate_real = rate_trackLength(imei)
        getspeed_data(imei)

        return built_response(200,'ok',rate_real)