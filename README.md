# motivation

Sometimes we are not able to find the target data from the internet directly or sometimes the existing data cannot totally satisfy our needs. For example, when I prepared the final project for 5702 and 5293 this semester, I planned to analyze Chinese films. However, I cannot find data which has enough details from the internet. Therefore, I write a crawler script frame and a runnable example based on this frame to crawl the data from internet directly. I hope it will help others who also have the need to crawl data from the internet.

# multithreading-crawler-frame

The script provides a general frame to crawl data from websites. It needs the version of urllib3 to be 1.25.11, so you can run pip install urllib3==1.25.11 before running the code.

It's provides three ways to handle the anti-crawler mechanism.
First, it uses fake user agent. 
Second, it uses fake cookie.
Third, it uses high anonymous proxy ip.
If the crawler is detected by the target website, the script will aotumatically update the request header by update user agent, cookie and proxy ip.

Besides, I use multithreading to increase the speed since this is an I/O bound task. 

Since most proxy ip sellers have restrictions on the frequency of extracting ip, I use block queue to realize multithreading communication. Each request to get a new proxy ip has to line up in order to aviod any time interval between two requests being less than then the given time interval.

# multithreading-crawler-douban

The script uses the above frame to crawl film data from Douban, one of the biggest film websites in China.

I have bought 10000 proxy ip for the account in this script, so you can test the efficieny on your own computer. Since the ips are valid for only one month, so you can do that before 2021/11/27. If you want to test after 2021/11/27, please contact me and I will refill the account. 

# my own evaluation

First, I uses three ways to handle the anti-crawler mechanism, which is enough for many websites. 

Most importantly, I increase the speed of crawler a lot. If I want to crawl all Chinese film related information by traditional crawler, I may have to spend 60 days and 24 hours per day, which is totaly unacceptable. By this script, I just need to spend less than 2 days. Depending on different computers' performance, the increase of the speed is different. Usually, the speed can be increased at least 30 times than before. Theoretically, when the proxy ips are of high quality and the server of target website is not very weak, this script can crawl nearly 2.5 million times per day.

I have spent more than 30 hours to finish this script, and I have crwaled nearly 4 GB data by this script recently for GR5291, so I believe it is runnable. If you have any questions, please contact me and I will be very happy answer them. Thank you very much for your time!

# further improvements 

There are still some further improvements can be made in the future.

First, I can add more measures to handle some more complicated anti-crawler mechanisms. 

Second, just as I esitimate above, the theoretical speed is nearly 2.5 million times per day, but it can still be improved. The ip seller who I current buy proxy ip from requires me that I cannot extract two ips less than one second. So if I can find another ip seller who has less or even no restritions on the extracting frequency and then I have a computer with higher performance, the speed can be improved further. Theoretically, it can reach the limitation of any server.
