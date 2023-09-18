import random
import threading
import time
import re
import requests as req
import os
import json

import main

header = main.header


class myThread(threading.Thread):

    def __init__(self, datas, uid):
        threading.Thread.__init__(self)
        self.datas = datas
        self.uid = uid

    def download(self, urls):
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
            self.error(imgId, name)
            return
        if html.ok:
            ans = 0
            ansStr = ''
            while True:
                if os.path.exists(f'./png/{self.uid}/{name}{ansStr}{gb}'):
                    ans += 1
                    ansStr = '_' + str(ans)
                else:
                    break
            with open(f'./png/{self.uid}/{name}{ansStr}-{imgId}{gb}', 'wb') as f:
                f.write(html.content)  # 成功下载
                f.close()
        else:
            print(html.status_code)
            self.error(imgId, name)
        pass

    def run(self):
        while True:

            pid = self.datas.get_url()
            if pid == 0:
                break
            time.sleep(1)
            pids = 'ids[]=' + pid
            try:
                # 获取画师作品详情链接
                res = req.get(
                    f'https://www.pixiv.net/ajax/user/{self.uid}/profile/illusts?{pids}&work_category=illustManga'
                    f'&is_first_page=1&lang=zh', headers=header).text
            except:
                print('图片链接请求错误')
                print(
                    f'https://www.pixiv.net/ajax/user/{self.uid}/profile/illusts?{pids}&work_category=illustManga'
                    f'&is_first_page=1&lang=zh')
                self.error(pid, 'xxx')
                continue
            else:
                url = json.loads(res)['body']['works'][pid]
                self.download(url)
            # 随机暂停3到5秒
            time.sleep(random.uniform(3, 5))

    def error(self, pid, name):
        with open(f'./png/{self.uid}/' + '下载失败.txt', 'a+', encoding='utf-8') as f:
            f.write(f'{pid}:{name}' + '\n')
            f.close()
        time.sleep(random.uniform(3, 5))


class datas:
    def __init__(self, lists):
        self.list = list(lists)

    def get_url(self):
        if len(self.list) == 0:
            return 0
        return self.list.pop(0)
