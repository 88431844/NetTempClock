#!/user/bin/env python 
#coding:utf-8

import smbus
import time
import commands
import sys
import LCD1602 as LCD
import requests
import json

if __name__ == '__main__':  
        LCD.init_lcd()
        time.sleep(2)
        # 需要填自己申请到的yeelink api Key 以及你的数据的url
        apiheaders = {'U-ApiKey': '0683ad06d356171965e282b238f1362d', 'content-type': 'application/json'}
        apiurl_cpu = 'http://api.yeelink.net/v1.0/device/350082/sensor/392560/datapoints'
        ds18b20_in = 'http://api.yeelink.net/v1.0/device/350082/sensor/393293/datapoints'
        ds18b20_out = 'http://api.yeelink.net/v1.0/device/350082/sensor/393292/datapoints'
        LCD.turn_light(1)
        isLight = 1
        time.sleep(2)
        while True:

                nowtime = time.strftime('%m-%d %H:%M %a',time.localtime(time.time()))
                hourtime = time.strftime('%H',time.localtime(time.time()))
                mintime = time.strftime('%M',time.localtime(time.time()))
                secondtime = time.strftime('%S',time.localtime(time.time()))
                hourtimeint = int(hourtime)
                if hourtimeint in[0,1,2,3,4,5,6,23]:
                #如果是在0点到6点，则判断lcd背景灯标志位状态；如果是1 则表示现在亮着 0则是灭着
                 if isLight == 1:#如果lcd背景灯亮着，则熄灭
                  LCD.turn_light(0)
                  isLight = 0                          
                else:#如果是在应该亮着的时间，则判断标志位

                 if isLight == 0:#如果lcd背景灯灭着，则点亮

                  LCD.turn_light(1)
                  isLight = 1

                try:
                 # 查看室内DS18B20温度

                 file=open("/sys/bus/w1/devices/28-000003084046/w1_slave")

                 text=file.read()

                 file.close()

                 secondline = text.split("\n")[1]

                 temperaturedata = secondline.split(" ")[9]

                 temperature = float(temperaturedata[2:])

                 temperature = (temperature / 1000)

                 intemp = str(temperature)

                 payload_ds18b20in = {'value': intemp}                 

                 # 查看室外DS18B20温度

                 file=open("/sys/bus/w1/devices/28-000003083029/w1_slave")

                 #read temprature

                 text=file.read()

                 #close file

                 file.close()

                 secondline = text.split("\n")[1]

                 temperaturedata = secondline.split(" ")[9]

                 temperature = float(temperaturedata[2:])

                 temperature = (temperature / 1000)

                 outtemp = str(temperature)
				 
                 payload_ds18b20out = {'value': outtemp}
				 
				 # 查看CPU温度
                 file = open("/sys/class/thermal/thermal_zone0/temp")
                 cputemp = float(file.read()) / 1000
                 file.close()
                 payload_cpu = {'value': cputemp}
                 				 
                except IOError:
                #如果在try部份引发了'name'异常
                 LCD.print_lcd(0,0,"---temp error--")
                else:
                 LCD.print_lcd(0,0,"o:"+outtemp[0:5]+ " i:"+intemp[0:5])
                 LCD.print_lcd(0,1,nowtime+"*")
                 requests.post(ds18b20_in, headers=apiheaders, data=json.dumps(payload_ds18b20in))
                 requests.post(ds18b20_out, headers=apiheaders, data=json.dumps(payload_ds18b20out))
                 requests.post(apiurl_cpu, headers=apiheaders, data=json.dumps(payload_cpu))

