import requests
import subprocess
import re


def excuteCommand(com):
    ex = subprocess.Popen(com, stdout=subprocess.PIPE, shell=True)
    out, err = ex.communicate()
    status = ex.wait()
    # print("cmd in:", com)
    # print("cmd out: ", out.decode())
    return out.decode()


ip = excuteCommand("curl -sm8 ip.sb").replace("\n", "").replace(" ", "")
context = requests.get(f"https://scamalytics.com/ip/{ip}", timeout=30).text
temp1 = re.findall(f">Fraud Score: (.*?)</div", context)[0]
print(f"欺诈分数(越低越好)：{temp1}")
temp2 = re.findall(f"<div(.*?)div>", context)[-6:]
nlist = ["匿名代理", "Tor出口节点", "服务器IP", "公共代理", "网络代理", "搜索引擎机器人"]
for i, j in zip(temp2, nlist):
    temp3 = re.findall(f"\">(.*?)</", i)[0]
    print(f"{j}: {temp3}")
status = 0
for i in range(1, 101):
    try:
        context1 = requests.get(
            f"https://cf-threat.sukkaw.com/hello.json?threat={str(i)}",
            timeout=1).text
        try:
          if "pong!" not in context1:
              print(
                  "Cloudflare威胁得分高于10为爬虫或垃圾邮件发送者,高于40有严重不良行为(如僵尸网络等),数值一般不会大于60")
              print("Cloudflare威胁得分：", str(i))
              status = 1
              break
        except:
            pass
    except:
      status = -1
      pass
if i == 100 and status == 0:
    print("Cloudflare威胁得分(0为低风险): 0")
