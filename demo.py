#-*- coding = utf-8 -*- 
#@TIme: 2021/5/31 18:55
#@Author: Celine
#@File: demo.py
#@Software: PyCharm
import requests
import re
import jieba
import wordcloud
import json
url = "https://api.bilibili.com/x/v1/dm/list.so?oid=286148586"
urllz="https://api.bilibili.com/x/v1/dm/list.so?oid=260735136"
urlslz="https://api.bilibili.com/x/v1/dm/list.so?oid=315981126"
urlnt="https://api.bilibili.com/x/v1/dm/list.so?oid=271686211"
urltlj="https://api.bilibili.com/x/v1/dm/list.so?oid=271730941"
urltest = 'https://api.bilibili.com/x/v2/dm/web/seg.so?type=1&oid=286148586&pid=373842509&segment_index=1'

headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.37'
    }
def getCID(bvid):
    url = "https://api.bilibili.com/x/player/pagelist?bvid=" + str(bvid) + "&jsonp=jsonp"
    response = requests.get(url,headers=headers)
    dirt = json.loads(response.text)
    cid = dirt['data'][0]['cid']
    return cid

def getOID(cid):
    url = "https://api.bilibili.com/x/v1/dm/list.so?oid="+str(cid)
    return url

def get_danmu(url,png):

    response = requests.get(url, headers=headers)
    response = response.content.decode('utf-8')
    # 正则获取弹幕
    data = re.compile('<d.*?>(.*?)</d>')
    danmu = data.findall(response)
    # print(danmu)
    # 分词，并用空格连接
    danmu_word = jieba.lcut(" ".join(danmu))
    # print(danmu_word)
    danmu_str = " ".join(danmu_word) #转为字符串形式
    # print(danmu_str)
    # 构造词云对象，设置默认字体为微软雅黑
    w = wordcloud.WordCloud(font_path='msyh.ttc',background_color='white', width=1000,height=500)
    w.generate(danmu_str)
    w.to_file(png)


# get_danmu(urltlj)
def main():
    print("请输入BV号：（只支持单个视频）")
    bvid = str(input())
    cid = getCID(bvid)
    url = getOID(cid)
    print("输入保存词云图片名称：（png格式）")
    png = str(input())
    get_danmu(url,png)

main()