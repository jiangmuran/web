import hashlib,flask,json,random,secrets,uuid,time,requests
import datetime

def loadConf(file="config.json"):
    with open(file,"r",encoding="utf-8") as f:
        return json.load(f)
def writeConf(config,file="config.json"):
    with open(file,"w+",encoding="utf-8") as f:
        json.dump(config,f)
app=flask.Flask("billsystem")

def get_bal(acc):
	config=loadConf()
	return requests.get(config["coinserver"]+"/api/v1/getbalance?account="+acc).json()

@app.route("/api/get")
def apiget():
	config=loadConf()
	if len(config["accountlist"]) == 0:
		for i in config["waitlist"]:
			if time.time()-i["time"] >= config["waittime"]:
				config["accountlist"].append({"username":i["username"],"password":i["password"]})
				config["waitlist"].remove(i)
	if len(config["accountlist"]) == 0:
		wasd=requests.get(config["coinserver"]+"/api/v1/register").json()
		config["accountlist"].append({"username":wasd["account"],"password":wasd["password"]})
	
	choose=random.choice(config["accountlist"])
	config["accountlist"].remove(choose)
	genkey=secrets.token_urlsafe(64)
	config["waitlist"].append({"username":choose["username"],"password":choose["password"],"time":time.time(),"before_balance":get_bal(choose["username"])["balance"],"key":genkey})
	writeConf(config)
	return {"account":choose["username"],"key":genkey}
	
@app.route("/api/check")
def apicheck():
	username=flask.request.args.get("acc")
	key=flask.request.args.get("key")
	config=loadConf()
	choose=-1
	for i in config["waitlist"]:
		if i["username"] == username:
			choose=i
	if (choose == -1):
		return {"message":"ERR_INV_ACC","usermessage":"账号不存在（可能账号已过期或者内部错误），请尝试重新生成。如果您已经支付，请保留付款证据（转账截图，生成界面截图）并联系我"}
	after_balance=get_bal(choose["username"])["balance"]
	if after_balance - choose["before_balance"] > 0:
		pass
	else:
		return {"message":"ERR_BALANCE_NOT_CHANGE","usermessage":"账号余额没有改变，请确认是否完成充值？"}
	if choose["key"] != key:
		return {"message":"ERR_KEY_NOT_MATCH","usermessage":"密钥不匹配（内部错误），可能是因为极小概率的并发或者您试图攻击？请尝试重新生成。如果您已经支付，请保留付款证据（转账截图，生成界面截图）并联系我"}
	key=str(random.randint(1000000,999999999999))
	config["donelist"].append({"money":after_balance - choose["before_balance"],"key":key})
	config["accountlist"].append({"username":choose["username"],"password":choose["password"]})
	config["waitlist"].remove(choose)
	writeConf(config)
	data={"account":choose["username"],"password":choose["password"],"to":config["adminuser"]["username"],"amount":after_balance}
	n=requests.post(config["coinserver"]+"/api/v1/transfer",data=data)
	print(n.json())
	return {"message":key+" "+str(after_balance - choose["before_balance"]),"usermessage":"生成成功！您的存储金额（可能有极小误差）："+str(after_balance - choose["before_balance"])+" 您的转账码："+key+" 请注意，提取时可能会收取少量手续费，具体请参考提取界面。"}
	
@app.route("/api/use")
def apiuse():
	username=flask.request.args.get("acc")
	key=flask.request.args.get("key")
	config=loadConf()
	choose=-1
	for i in config["donelist"]:
		if i["key"] == key:
			choose=i
	if (choose == -1):
		return {"message":"ERR_INV_KEY","usermessage":"key不存在（可能是内部错误）"}
	data={"account":config["adminuser"]["username"],"password":config["adminuser"]["password"],"to":username,"amount":choose["money"]*config["sxf"]}
	print(data)
	n=requests.post(config["coinserver"]+"/api/v1/transfer",data=data)
	if "balance" in n.json():
		config["donelist"].remove(choose)
		writeConf(config)
		return {"message":"done."+str(choose["money"])+"|"+str(choose["money"]*config["sxf"]),"usermessage":"成功！手续费前："+str(choose["money"])+"手续费后："+str(choose["money"]*config["sxf"])}
	else:
		return {"message":n.json()["error"],"usermessage":n.json()["error"]}
	



app.run(host="0.0.0.0",port=8849)

