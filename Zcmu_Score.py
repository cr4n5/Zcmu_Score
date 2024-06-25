import requests
import time
import json
import lxml.etree
import yagmail
import logging
import os

'''
使用之前先在config填写账号密码，邮箱SMTP服务账号授权码服务器地址，接收方邮箱，学年学期。例如2024.6.25填写为2023学年，12；2022.12.23填写为2022学年，3。
'''
# 配置日志
logging.basicConfig(filename='score.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

session = requests.Session()

with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

def login():
    global session

    url="https://cas.paas.zcmu.edu.cn/cas/login?service=https%3A%2F%2Fxjyt.zcmu.edu.cn%3A443%2Fcas%2Flogin%2Fcas%2Flogin%3Frzxx%3Dsupwisdom%26service%3Dhttps%253A%252F%252Fpuser.zcmu.edu.cn%252Fhome-page"
    login_url = "https://cas.paas.zcmu.edu.cn/cas/login?service=https%3A%2F%2Fxjyt.zcmu.edu.cn%3A443%2Fcas%2Flogin%2Fcas%2Flogin%3Frzxx%3Dsupwisdom%26service%3Dhttps%253A%252F%252Fpuser.zcmu.edu.cn%252Fhome-page"


    session.headers.update({
                    "Accept": "text/html, application/xhtml+xml, application/xml; q=0.9, */*; q=0.8",
                    "Accept-Language": "zh_CN",
                    "Connection": "keep-alive",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363",
                }
            )

    session.cookies.update({"Cookie": "SESSION=8b3b1b3b-3b3b-3b3b-3b3b-3b3b3b3b3b3b; Hm_lvt_d605d8df6bf5ca8a54fe078683196518={}; Hm_lpvt_d605d8df6bf5ca8a54fe078683196518={}".format(str(int(time.time())-10), str(int(time.time()))),})   

    data = {
        "username": config["login"]["username"],
        "password": config["login"]["password"],
        "captcha": "",
        "currentMenu": "1",
        "failN": "0",
        "_eventId": "submit",
        "geolocation": "",
        "execution": "",
        "submit": "稍等片刻……",
    }

    response = session.get(url)
    tree = lxml.etree.HTML(response.text)
    execution = tree.xpath('//input[@name="execution"]/@value')[0]
    data["execution"] = execution
    response = session.post(login_url, data=data, allow_redirects=False)
    request_url = response.headers["Location"]
    response = session.get(request_url, allow_redirects=True)


def send_email(content):
    # 连接服务器
    # 用户名、授权码、服务器地址
    yag_server = yagmail.SMTP(user=config["smtp_email"]["user"], password=config["smtp_email"]["password"], host=config["smtp_email"]["host"])

    # 发送对象列表
    email_to = config["smtp_email"]["email_to"]
    email_title = content
    email_content = content
    # # 附件列表
    # email_attachments = ['./attachments/report.png', ]

    # 发送邮件
    yag_server.send(email_to, email_title, email_content)

    # 关闭连接
    yag_server.close()

    print(f"Email sent with content: {content}")
    logging.info(f"Email sent with content: {content}")


def query_scores():
    cj_url = "https://jwmk.zcmu.edu.cn/jwglxt/cjjfgl/xkjsjfsqsh_cxKcxxView.html?doType=query&xnm={}&xqm={}&queryModel.showCount=999&queryModel.pageSize=999".format(config["time"]["XueNian"],config["time"]["XueQi"])
    global session
    login()

    kc={}
    if os.path.exists('kc.json'):
        with open('kc.json', 'r', encoding='utf-8') as f:
            kc = json.load(f)

    try:
        while True:
            response = session.get(cj_url,verify=False)
            if "学教一体化平台" in response.text:
                session = requests.Session()
                login()
                print("登陆过期，重新登录","时间：",time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                logging.error("登陆过期，重新登录")
                continue
            elif "学教一体化" in response.text:
                session = requests.Session()
                login()
                print("异地登陆，重新登录","时间：",time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                logging.error("异地登陆，重新登录")
                continue
            else:
                response = response.json()
                for i in response["items"]:
                    if i["kcmc"] not in kc:
                        kc[i["kcmc"]] = i["cj"]
                        content = i["kcmc"] + " " + i["cj"]
                        send_email(content)
                        with open('kc.json', 'w', encoding='utf-8') as f:
                            json.dump(kc, f, ensure_ascii=False, indent=4)
                    print(i["kcmc"],i["cj"],"查询时间：",time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                    logging.info(f"{i['kcmc']} {i['cj']}")
            time.sleep(60)
    except Exception as e:
        print(e)
        logging.error(e)
        send_email(str(e))


query_scores()
session = requests.Session()
query_scores()
send_email("重新启动失败")
    