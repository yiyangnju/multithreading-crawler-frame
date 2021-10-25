# multithreading-crawler-frame

We need data .However, sometimes we cannot find ..or existing data does not satisfy your need. For example, we I prepare the data for the final project of 5702 and 5293 this semester, I plan to analyze chinese film data. However, I cannot find ... data from the internet. Therefore, I want write a crawler script to crawl the data from internet directly. 

The script: , provides a general frame to crawl data from websites.

It's provides three ways to handle the anti-crawler mechanism.
First, it uses fake user agent information. 
Second, it uses fake cookie.
Third, it uses high anonymous proxy ip.

Since this is an I/O bound task, I use multithreading to increase the speed. 
Depending on the computer's performance, the speed can be increased at least 30 times than before.

Since most proxy ip sellers have restrictions on the frequency of extracting ip, 
I use block queue to realize multithreading communication.

The script: use the above frame to crawl film date from Douban, one of the biggest film websites in China.

I have bought 20000 for the proxy ip account, you just need to put data.json, special...

