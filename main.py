import os
import requests as req
import threads



# 作家 uid
uid = '18302514'
# 线程的个数
threadNum = 1
# 浏览器header
header = {
    'Referer': 'https://www.pixiv.net/',
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
