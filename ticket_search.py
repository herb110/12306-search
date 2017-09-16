#coding: utf-8

'''命令行火车票查看器

usage:
    tickets [-gdtkz] <from> <to> <date>
    
options:
    -h,--help   显示帮助菜单
    -g          高铁
    -d          动车
    -t          特快
    -k          快速
    -z          直达
    
example:
    tickets 合肥 南京 2017-9-15
    tickets -hg 合肥 南京 2017-9-15
    
    
    
'''

import requests
import ssl

from docopt import docopt
from prettytable import PrettyTable
from colorama import init,Fore
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup
#from urllib.request import urlopen

from stations import stations

init()

class TrainsCollection:
    header = '车次 车站 时间 历时 一等 二等 高级软卧 软卧 硬卧 硬座 无座'.split()

    def __init__(self,available_trains,available_place, options):
        self.available_trains = available_trains
        self.available_place = self.available_place
        self.options = options
        
    
    @property
    def trains(self):
        for raw_train in self.available_trains:
            raw_train_list = raw_train.split('|')
            train_no = raw_train_list[3]
            initial = train_no[0].lower()
            duration = raw_train_list[10]
            if initial in self.options:
                train = [
                    train_no,
                    '\n'.join([Fore.LIGHTGREEN_EX + self.available_place[raw_train_list[6]] + Fore.RESET,
                               Fore.LIGHTRED_EX + self.available_place[raw_train_list[7]] + Fore.RESET]),
                    '\n'.join([Fore.LIGHTGREEN_EX + raw_train_list[8] + Fore.RESET,
                               Fore.LIGHTRED_EX + raw_train_list[9] + Fore.RESET]),
                    duration,
                    raw_train_list[-4] if raw_train_list[-4] else '--',
                    raw_train_list[-5] if raw_train_list[-5] else '--',
                    raw_train_list[-14] if raw_train_list[-14] else '--',
                    raw_train_list[-12] if raw_train_list[-12] else '--',
                    raw_train_list[-7] if raw_train_list[-7] else '--',
                    raw_train_list[-6] if raw_train_list[-6] else '--',
                    raw_train_list[-9] if raw_train_list[-9] else '--',
                ]
                yield train



    def pretty_print(self):
        pt = PrettyTable()
        pt._set_field_names(self.header)
        for train in self.trains:
            pt.add_row(train)
        print(pt)

def click():
    #command-line interface 
    arguments = docopt(__doc__)
    from_station = stations.get(arguments['<from>'])
    to_station = stations.get(arguments['<to>'])
    date = arguments['<date>']
    #构建URL
    url = 'https://kyfw.12306.cn/otn/leftTicket/queryX?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(date,from_station,to_station)
    #url = 'https://kyfw.12306.cn/otn/leftTicket/queryX?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'
    #添加verify=False参数不验证证书
    headers = {
    "Accept": "text/html, application/xhtml+xml, image/jxr, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "Keep-Alive",
    "Accept-Language": "zh-Hans-CN, zh-Hans; q=0.5",
    "Host": "kyfw.12306.cn",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063",
    "Referer":"https://kyfw.12306.cn/otn/leftTicket/init",
    "DNT": "1",
    
   "Cookie": "JSESSIONID=C0FD250ECAA03C09DC11FF0873D5A850; fp_ver=4.5.1; RAIL_EXPIRATION=1505819118076; RAIL_DEVICEID=LssNQXKy2MXUZMHMZoqzWY9VdjXz8pa8uTVD9Kr3-1LZb1fZjTh_FUyXBycHI3DXuaV4ItLdsz9o9mN8l3-iMErRYZ1AQKvSWVYNsNuWj8_95nQLZUF-3Qszovf2znnGFAb4LjnKi6F1PZPH6MistoBhVHLPuPmz; route=c5c62a339e7744272a54643b3be5bf64; BIGipServerotn=1339621642.64545.0000; _jc_save_fromStation=%u5408%u80A5%2CHFH; _jc_save_toStation=%u5357%u4EAC%2CNJH; _jc_save_fromDate=2017-09-16; _jc_save_toDate=2017-09-16; _jc_save_wfdc_flag=dc"
   }
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    r = requests.get(url,headers = headers, verify = False)
    available_trains = r.json()['data']['result']
    available_maps = r.json()['data']['map']
    options =''.join([
        key for key, value in arguments.items() if value is True
    ])
    TrainsCollection(available_trains,available_place,options).pretty_print()
    
    

    
if __name__ =='__main__':
    click()