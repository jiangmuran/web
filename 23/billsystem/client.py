import os

print("JMR驱动管理器正在尝试安装运行库")
os.system("pip install -i https://pypi.tuna.tsinghua.edu.cn/simple requests")
print("安装完成")
import requests
SERVER="http://s1.jiangmuran.com:8849"

def get():
	print("正在尝试获取转账目标")
	nncc=requests.get(SERVER+"/api/get").json()
	key1=nncc["key"]
	acc=nncc["account"]
	while True:
		input("请往指定账户转账并按下回车："+acc)
		nnn=requests.get(SERVER+"/api/check?key="+key1+"&acc="+acc).json()
		print(nnn['usermessage'])
		if (nnn['message'][0] != "E"):
			break
	print("充值成功！")
def use():
	key=input("请输入转账码：")
	acc=input("请输入转账对象：")
	print(requests.get(SERVER+"/api/use?key="+key+"&acc="+acc).json()['usermessage'])

while True:
	print("欢迎来到awacoin-billsystem\n(1)制造转账码\n(2)使用转账码")
	choose=input("请选择：")
	if choose=="1":
		get()
	if choose=="2":
		use()
