#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 21:58:53 2021

@author: yiyang
"""

'''

'''

class crawler():
    def __init__(self,proxy_ip_url,current_range,target_url,ua_pool_path,save_data,path,save_special_cases_path):
        self.proxy_ip_url = proxy_ip_url
        self.ua_position = 1
        self.ua_pool = pd.read_table(ua_pool_path,header = None)[0]
        self.current_header = None
        self.current_cookie =None
        self.current_proxy = None
        self.proxy_ip_url = proxy_ip_url
        self.current_range = current_range
        self.target_url = target_url
        self.data = {}
        self.special_cases = {}
        self.save_data_path = save_data_path
        self.save_special_cases_path = save_special_cases_path
        
        
    def reset_cookie(self):
        '''
        This depends on the characteristic of the cookie of the website you want to crawl
        '''
        self.current_cookie = {"Cookie": "bid=%s" % "".join(random.sample(string.ascii_letters + string.digits, 11))}
    
    def reset_header(self):
        '''
        Update the user agent information from the user agent pool
        '''
        self.ua_position += 1
        if self.ua_position >= self.ua_pool.shape[0]:
            self.ua_position = 0
        self.current_header = {'User-agent': self.ua_pool[self.ua_position]}
    
    def reset_proxy(self):
        '''
        Once the previous ip dies, it will update the ip automatically.
        '''
        global proxy_request_queue
        proxy_request_queue.join()
        temp = proxy_request_queue.put(1)
        response = requests.get(url=self.proxy_url,headers=self.current_header)
        interval = #the frequency limitation of the proxy ip website
        time.sleep(interval)
        temp = proxy_request_queue.get()
        proxy_request_queue.task_done()
        ip = response.text
        print('update ip'+ip)
        self.current_proxy = {'https': 'https://'+ip}
    
    def update_request(self):
        '''
        Once one request to the target website fails, it will update the cookie, user agent and proxy ip.
        '''
        self.reset_cookie()
        self.reset_header()
        self.reset_proxy()
    
    
    def crawl_data(self):
        '''
        Crawl date from target url.
        Save the data and each failure record in json format.
        '''
        for i in current_range:
            try:
                info = self.get_info()
                self.data[i] = info
                print('crawl successfully')
            except:
                print('meet error, record')
                error = traceback.format_exc()
                special_case = {'position':i,'error':error}
                self.special_cases[i] = special_case
                continue
            
    def get_info(self):
        '''
        Define your own function to get the target information from the website 
        by regular expression or other methods
        '''
        html = get_html(self)
        
    def get_html(self):
        '''
        Request the html from the target url. 
        If fails, it will update the request information till success request.
        '''
        code = 403
        while(code!=200):
            try:
                response = requests.get(url=self.target_url,url,headers=self.current_header,cookies = self.current_cookie,proxies = self.current_proxy,timeout=3)
                code = response.status_code
                if(code!=200):
                    self.update_request()
            except:
                self.update_request()
        return response
    
    def save_data(self):
        '''
        save the data to the target path
        '''
        with open(self.save_data_path) as f_ojb:
            data = json.load(f_ojb)
        data.update(temp_data)
        with open(self.save_data_path, 'w') as f_ojb:  
            json.dump(data, f_ojb) 
        
    def save_special_cases(self):
        '''
        save the special cases to the target path
        '''
        with open(self.save_special_cases_path) as f_ojb:
            special_cases = json.load(f_ojb)
        special_cases.update(temp_special_data)
        with open(self.save_special_cases_path, 'w') as f_ojb:  
            json.dump(special_cases, f_ojb)  


if __name__ == '__main__':
    thread_loop_n =  #set the number of loop
    thread_n =  #set the number of threads
    proxy_ip_url = #the url where you get your proxy ip
    save_data_path = #the path where you want to save the crawled data
    save_special_cases_path = #the path where you want to save the special cases
    ua_pool_path = #the path where the ua pool is located
    proxy_request_queue =queue.Queue() # initialize the queue
    for i in range(thread_loop_n):
        temp_data = {}
        temp_special_data = {}
        for j in range(thread_n):
            current_range = #the range you want to crawl in this thread
            exec('Crawler{} = crawler({},{},\'{}\',{})'.format(j,current_start,current_end,region,proxy_account))
            exec('t{}=threading.Thread(target=crawler{}.crawl_data, args=())'.format(j,j))
            exec('t{}.start()'.format(j))
        for k in range(thread_n):
            exec('t{}.join()'.format(k))
            exec('temp_data.update(Douban{}.data)'.format(k))
            exec('temp_special_data.update(Douban{}.special_cases)'.format(k))
        for l in range(thread_n):
            exec('Crawler{}.save_data()'.format(l))
            exec('Crawler{}.save_special_cases()'.format(l))
            
        
   
    