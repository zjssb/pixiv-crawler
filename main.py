import os
import requests as req
import threads



# 作家 uid
uid = ''
# 线程的个数
threadNum = 1
# 浏览器header
header = {
    'Referer': 'https://www.pixiv.net/',
    'User-Agent': '',
    'Cookie': '',
}

if __name__ == '__main__':
    # 调试用

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
    # pidList = list()
    pidList = pid.keys()
    print(pidList)
    print(len(pidList))
    pids = threads.datas(list(pid.keys()))
for i in range(threadNum):
    myTrand = threads.myThread(pids, uid)
    myTrand.start()
