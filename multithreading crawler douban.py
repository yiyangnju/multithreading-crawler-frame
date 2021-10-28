# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 13:25:54 2021

@author: YI YANG
"""
import requests    
from bs4 import BeautifulSoup        
import pandas as pd
import re
import time
import random
import string
import threading
import queue
import traceback
import json
import pypinyin
       

class douban():
    def __init__(self,start_number,end_number,region):
        print('initialization')
        global all_film_url
        self.start_number = start_number
        self.end_number = end_number
        self.film_url = all_film_url[start_number:end_number]
        self.region = region
        self.proxy_url = 'http://http.9vps.com/getip.asp?username=853455788&pwd=cf7c710425d6fd266c7fc9df3dbb3c3f&geshi=1&fenge=1&fengefu=&getnum=1'
        self.ua_position = 1
        self.ua_pool = pd.read_table('ua_pool.txt',header = None)[0]
        self.current_header = None
        self.current_cookie =None
        self.current_proxy = None
        self.update_request()
        self.data = {}
        self.special_cases = {}
        
    def reset_cookie(self):
        self.current_cookie = {"Cookie": "bid=%s" % "".join(random.sample(string.ascii_letters + string.digits, 11))}
    
    def reset_header(self):
        self.ua_position += 1
        if self.ua_position >= self.ua_pool.shape[0]:
            self.ua_position = 0
        self.current_header = {'User-agent': self.ua_pool[self.ua_position]}
    
    def reset_proxy(self):
        global proxy_request_queue 
        code = 403
        while(code!=200):
            try:
                proxy_request_queue.join() 
                temp = proxy_request_queue.put(1)
                response = requests.get(url=self.proxy_url,headers=self.current_header,timeout=3)
                code = response.status_code
                time.sleep(1.1)
                temp = proxy_request_queue.get()
                proxy_request_queue.task_done()
                ip = response.text
                self.current_proxy = {'https': 'https://'+ip}
                print(code)
                print(ip)
                if(code!=200):
                    self.reset_proxy()
            except:
                time.sleep(1.1)
                temp = proxy_request_queue.get()
                proxy_request_queue.task_done()
                self.reset_proxy()
        
    
    def update_request(self):
        self.reset_cookie()
        self.reset_header()
        self.reset_proxy()
    
    def get_html(self,url):
        code = 403
        while(code!=200):
            try:
                response = requests.get(url=url,headers=self.current_header,cookies = self.current_cookie,proxies = self.current_proxy,timeout=3)
                code = response.status_code
                if(code!=200):
                    self.update_request()
                    print('update request')
            except:
                self.update_request()
                print('update request')
        return response
    
    def crawl_data(self):
        for i in range(self.start_number,self.end_number):
            url = self.film_url['film_url'][i]
            film_number = self.film_url['film_number'][i]
            print((film_number,i))
            try:
                film_info = self.get_film_info(url)
                self.data[url] = film_info
                print('crawl film'+str(film_number)+'successfully')
            except:
                print('meet error, record')
                error = traceback.format_exc()
                special_case = {'film_url':url,'error':error}
                self.special_cases[url] = special_case
                continue

    def get_film_info(self,url): 
        html = self.get_html(url)       
        soup = BeautifulSoup(html.content, "html.parser")
        film_pattern=re.compile(r'.*subject/(.*)/')
        film_id = film_pattern.findall(url)[0]
        film_name = soup.find(property="v:itemreviewed").string
        origin_film_name = film_name
        film_name = pypinyin.slug(film_name, separator=' ')
        initialReleaseDate = soup.find(property="v:initialReleaseDate")
        if(initialReleaseDate==None):
            initialReleaseDate = 'null'
        else:
            initialReleaseDate = pypinyin.slug(initialReleaseDate.string, separator=' ')
        runtime = soup.find(property="v:runtime")
        if(runtime==None):
            runtime = 'null'
        else:
            runtime = pypinyin.slug(runtime.string.replace('分钟','minutes'), separator=' ')
        rating = soup.find(class_="ll rating_num", property="v:average").string 
        if(rating==None):
                rating = 'null'
         
        rating_number = soup.find(property="v:votes")
        if(rating_number==None):
            rating_number = 'null'
        else: 
            rating_number = rating_number.string
        try:
            rating_distribution = []
            for i in soup.find_all(class_="rating_per"):
                rating_distribution.append(i.string)
        except:
            rating_distribution = ['null','null','null','null','null']
        try:
            genre = soup.find(property="v:genre").string
            genre_dict = {'喜剧':'comedy', '动作':'action', '剧情':'drama', '爱情':'affectional', '科幻':'fiction',
                          '奇幻':'fantasy', '动画':'cartoon', '悬疑':'suspense', '音乐':'musicals', '脱口秀':'talk show', 
                          '歌舞':'song and dance','真人秀':'reality show', '战争':'war', '传记':'biography', '惊悚':'thriller', 
                          '武侠':'swordsman', '历史':'history', '犯罪':'crime', '运动':'sport', '冒险':'adventure', '儿童':'childrem', 
                          '恐怖':'horror','家庭':'family', '戏曲':'opera', '古装':'ancient costume', '同性':'isosexual'}
            genre = genre_dict[genre]
        except:
            genre = 'null'
        imdb_pattern = re.compile(r'IMDb:</span>\s(.*?)<br>',re.DOTALL)
        imdb = imdb_pattern.findall(str(html.content))
        imdb = self.whether_has_value(imdb)
        other_names_pattern = re.compile(r'又名:</span>\s(.*?)<br/>',re.DOTALL)
        other_names = other_names_pattern.findall(str(soup))
        other_names = self.whether_has_value(other_names)
        info = {
                'film_name' : film_name,
                'origin_film_name' : origin_film_name,
                'film_id':film_id,
                'film_url':url,
                'release_date' : initialReleaseDate,
                'runtime' : runtime,
                'rating' : rating,
                'rating_number': rating_number,
                'rating_distribution' : rating_distribution,
                'genre' : genre,
                'imdb' : imdb,
                'other_names' : other_names
                }
        return info
 
    def whether_has_value(self,result):
        if len(result)==0:
            return 'null'
        else:
            return result[0]
    
    def is_alphabet(self,uchar):
        if (uchar >= u'\u0041' and uchar<=u'\u005a') or (uchar >= u'\u0061' and uchar<=u'\u007a'):
            return True
        else:
            return False

    def delete_chinese(self,content):
        content_str = ''
        for i in content:
            if self.is_alphabet(i):
                content_str += i
        if len(content_str) == 0:
            return 'null'
        return content_str        

        
if __name__ == '__main__':
    thread_loop_n = 1
    thread_n = 10
    film_n_per_thread = 20
    start_n = 0
    region = '中国大陆'
    all_film_url = pd.read_hdf('all_film_url',key='s')
    proxy_request_queue =queue.Queue()
    for i in range(thread_loop_n):
        temp_data = {}
        temp_special_data = {}
        for j in range(thread_n):
            current_start = start_n + film_n_per_thread*j + i*thread_n*film_n_per_thread
            current_end = current_start + film_n_per_thread
            exec('Douban{} = douban({},{},\'{}\')'.format(j,current_start,current_end,region))
            exec('t{}=threading.Thread(target=Douban{}.crawl_data, args=())'.format(j,j))
            exec('t{}.start()'.format(j))
            time.sleep(1.1)
        for k in range(thread_n):
            exec('t{}.join()'.format(k))
            exec('temp_data.update(Douban{}.data)'.format(k))
            exec('temp_special_data.update(Douban{}.special_cases)'.format(k))
        #save data
        filename = 'data.json'
        with open(filename) as f_ojb:
            data = json.load(f_ojb)
        data.update(temp_data)
        with open(filename, 'w') as f_ojb:  
            json.dump(data, f_ojb) 
        #save special cases
        filename = 'special_cases.json'
        with open(filename) as f_ojb:
            special_cases = json.load(f_ojb)
        special_cases.update(temp_special_data)
        with open(filename, 'w') as f_ojb:  
            json.dump(special_cases, f_ojb)      
    end_n = start_n + thread_loop_n*thread_n*film_n_per_thread
    print('finish, current position is'+str(end_n))
    
    
