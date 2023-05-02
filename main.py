import requests
from fastapi import FastAPI
from selenium import webdriver
import json
import re
import random
import time
import os
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

BliCreeper = FastAPI()
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.58',
    'cookie': "buvid3=A8F4D1EF-8E6F-5C53-9E5F-D57FC5EAAA1F48338infoc; i-wanna-go-back=-1; _uuid=A28D7624-AACC-FECD-82DF-10F2892E8D610E48075infoc; buvid4=26BA48C0-3339-21D3-0ACC-7433845FB12950633-022061117-17uwI6qsF9fxs6pNPkKGFw==; LIVE_BUVID=AUTO4016564939161006; blackside_state=0; CURRENT_BLACKGAP=0; nostalgia_conf=-1; buvid_fp_plain=undefined; fingerprint3=5d49c2a6462f52f817890ab7b1abd26e; b_nut=100; hit-dyn-v2=1; rpdid=|(u||uu~JuR)0J'uYYmuuJRYJ; header_theme_version=CLOSE; CURRENT_QUALITY=116; CURRENT_PID=4dcb61e0-cd47-11ed-9218-e9fcb2d66548; is-2022-channel=1; FEED_LIVE_VERSION=V8; CURRENT_FNVAL=4048; bsource=search_bing; fingerprint=a2b19b5935b9b23925b097ef1def7d29; buvid_fp=a2b19b5935b9b23925b097ef1def7d29; SESSDATA=b47533f0,1698408414,7b84b*42; bili_jct=63d2dcc49c3c57f480d6b81a3577f3fe; DedeUserID=109297473; DedeUserID__ckMd5=e8f62313d867c09e; b_ut=5; home_feed_column=4; b_lsid=331047DD4_187D2325712; PVID=6; innersign=1; sid=78c2cvj9; browser_resolution=902-768; bp_video_offset_109297473=790366616570298400"
}
@BliCreeper.get('/api/search/author/{username}')
def SearchUp(username):

    params={
        'search_type':'bili_user',
        'keyword': username
    }
    res=requests.get('https://api.bilibili.com/x/web-interface/search/type',headers=headers,params=params)
    print(res.json().get('data').get('result'))
    datas=res.json().get('data').get('result')
    data = []
    for item in datas:
        content={
            'id':item.get('mid'),
            'username':item.get('uname')
            }
        data.append(content)
    return {'ret': data}

@BliCreeper.get('/api/video/{id}/{page}')#id为上面的mid，page为页数
def getVideo(id,page):
    url='https://api.bilibili.com/x/space/wbi/arc/search'
    headers={
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.58'
    }
    params={
        'mid':id,
        'pn':page
    }
    res=requests.get(url,params=params,headers=headers)
    list=res.json().get('data').get('list').get('vlist')
    print(list)
    datas=[]
    for item in list:
        data={
            'id':item.get('bvid'),
            'time':item.get('created'),
            'timestamp': item.get('created'),
            'title': item.get('title')
        }
        datas.append(data)
    print(datas)
    return {'ret': datas}

@BliCreeper.get('/api/video/{id}')
def bliSummarize(id):
    driver=webdriver.Edge(executable_path="E:\msedgedriver.exe")
    driver.get('https://b.jimmylv.cn/video/'+str(id))
    try:
        accountinput = driver.find_element(By.XPATH,'//*[@id="email"]')
        accountinput.send_keys('835343587@qq.com')
        pswordinput = driver.find_element(By.XPATH,'//*[@id="password"]')
        pswordinput.send_keys('lyz20040812')
        loginButton = driver.find_element(By.XPATH,'//*[@id="auth-sign-in"]/div/button')
        loginButton.click()
        time.sleep(10)
        summarizeButton = driver.find_element(By.XPATH,'//*[@id="__next"]/div[1]/main/div/form/div[3]/button')
        summarizeButton.click()
        time.sleep(15)
    except:
        print('已总结过此视频')
    content=driver.find_element(By.CLASS_NAME,'mb-8')
    print(content.text)
    return content.text
#此函数只返回文本

'''
url='https://b.jimmylv.cn/api/summarize'
    headers={
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection':'keep-alive',
        'Content-Type':'application/json',
        'Cookie':'AMP_fc3722f601=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjJhYWVhZTQ3Ni1jZGYwLTRmM2ItYTNhNS03MThiZjRhMzdlMzUlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNjgyOTEwMTAzNzY0JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTY4MjkxMDExOTMwMCU3RA==; AMP_MKTG_fc3722f601=JTdCJTdE',
        'Host':'b.jimmylv.cn',
        'Origin':'https://b.jimmylv.cn',
        'Referer':'https://b.jimmylv.cn/video/BV1ip4y197X3',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0',
    }
    sessions = requests.session()

    res=sessions.post(url,headers=headers)
'''