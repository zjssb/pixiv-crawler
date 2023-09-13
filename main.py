import json
import os
import random
import time
import re
import requests as req

# 作家 uid
uid = ''
# 模拟浏览器header
header = {
    'Referer':'https://www.pixiv.net/',
    'User-Agent': ',
    'Cookie': '',
}

def img(urls):
    imgStr = re.findall('img/(.*?)_p0', urls['url'])
    gb = urls['url'][-1:-5:-1]  # 提取后缀
    gb = gb[::-1]  # 翻转
    url = f'https://i.pximg.net/img-original/img/{imgStr[0]}_p0{gb}'
    name = urls['title']  # 获取作品名
    # 去除作品名中的非法字符
    name = re.sub(r'[<>?/\\|":*]', ' ', name)
    imgId = urls['id']  # 获取作品id
    print(url)
    try:
        html = req.get(url, headers=header)
    except:
        print('图片下载失败')
        error(imgId, name)
        return
    if html.ok:
        ans = 0
        ansStr = ''
        while True:
            if os.path.exists(f'./png/{uid}/{name}{ansStr}{gb}'):
                ans += 1
                ansStr = '_' + str(ans)
            else:
                break
        with open(f'./png/{uid}/{name}{ansStr}{gb}', 'wb') as f:
            f.write(html.content)#成功下载
            f.close()
            deltime(1)
    else:
        print(html.status_code)
        error(imgId, name)

# 下载错误时，向图片文件夹中创建txt文件，写入下载错误的图片id和名称（为获取到名称按xxx处理）
def error(id, name):
    with open(f'./png/{uid}/' + '下载失败.txt', 'a+', encoding='utf-8') as f:
        f.write(f'{id}:{name}' + '\n')
        f.close()
    # 下载错误时，增加随机延时的时间
    deltime(-1)

def deltime(t):
    global delay
    if t == 1:
        if delay > 1:
            delay -= 1
    if t == -1:
        delay += 1


if __name__ == '__main__':
    # 调试用
    # strs = 'a<s>d?g/g\g"c:e*v|\\\\\\'
    # str=re.sub(r'[<>?/\\|":*]','1',strs)
    #
    # print(str)
    # exit()
    try:
        os.mkdir(f'./png/{uid}')  # 检测画师文件夹是否创建
    except:
        print('已存在当前画师插画文件夹，请前往文件目录查看')
        exit()

    delay = 1
    url = f"https://www.pixiv.net/ajax/user/{uid}/profile/all?lang=zh"
    try:
        html = req.get(url, headers=header).json()
    except:
        print('画师作品pid获取错误，请检查画师uid')
        exit()
    pid = html['body']['illusts']
    pidList = pid.keys()
    print(pidList)
    print(len(pidList))
    for i in pidList:
        time.sleep(1)
        pids = 'ids[]=' + i
        try:
            # 获取画师作品详情链接
            res = req.get(
                f'https://www.pixiv.net/ajax/user/{uid}/profile/illusts?{pids}&work_category=illustManga'
                f'&is_first_page=1&lang=zh',
                headers=header).text
        except:
            print('图片链接请求错误')
            print(
                f'https://www.pixiv.net/ajax/user/{uid}/profile/illusts?{pids}&work_category=illustManga'
                f'&is_first_page=1&lang=zh')
            error(i, 'xxx')
            continue
        else:
            url = json.loads(res)['body']['works'][i]
            img(url)
            # 随机延时下载
            time.sleep(random.randint(delay, delay + 2) + random.random())
