import json
import os
import random
import time
import re
import requests as req

# 作家 uid
uid = '6121219'

header = {
    'Referer': 'https://www.pixiv.net/users/6049901/artworks?p=1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/113.0.0.0 Safari/537.36',
    'Cookie': 'login_ever=yes; first_visit_datetime_pc=2022-09-19+11%3A39%3A43; p_ab_id=5; p_ab_id_2=6; '
              'p_ab_d_id=878245443; yuid_b=EGZHhBc; _gid=GA1.2.1312501972.1691379192; '
              'PHPSESSID=38092362_klBtEkekQr4GW9sX3wTlrj7JCNj2GaQK; device_token=e40723202bbec53f7296cbc91e9bd7a7; '
              'privacy_policy_agreement=6; _ga_MZ1NL4PHH0=GS1.1.1691398498.1.1.1691398658.0.0.0; c_type=24; '
              'privacy_policy_notification=0; a_type=0; b_type=1; QSI_S_ZN_5hF4My7Ad6VNNAi=v:0:0; login_ever=yes; '
              '__cf_bm=zWtzMttsYWX1T4zpcf.hj1n41_H1MMcfOIYiC_LZydQ-1691472006-0-ASUtkTK/PFBWhinXx1rNlhPpDNxbvfbWzesg'
              '+rGnTzxRuaJXG8AdYsvX/OvfEyOZn5T55ASYKUmHcSiLW9cNIOGKGludb8IOBIgGPWKTzeG7; '
              'cf_clearance=X7wdDX2CWmbzFfW3A_iG0NeqQ_iihIF4QAgFvlqkYAs-1691472206-0-1-d94fcfed.b187dd42.8e4e900d-0.2'
              '.1691472206; _gat_UA-1830249-3=1; _ga=GA1.1.126982131.1663555186; '
              '_ga_75BBYNYN9J=GS1.1.1691470097.9.1.1691472218.0.0.0',
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

def error(id, name):
    with open(f'./png/{uid}/' + '下载失败.txt', 'a+', encoding='utf-8') as f:
        f.write(f'{id}:{name}' + '\n')
        f.close()
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
        print('当前画师插画已经下载完毕，前往文件目录查看')
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
            time.sleep(random.randint(delay, delay + 2) + random.random())
