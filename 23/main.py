import hashlib,flask,json,random,secrets,uuid
import datetime
mines={}
def loadConf(file="datas.json"):
    with open(file,"r",encoding="utf-8") as f:
        return json.load(f)
def writeConf(config,file="datas.json"):

	with open(file,"w+",encoding="utf-8") as f: 
		json.dump(config,f)

app=flask.Flask("awaCoin")
server_config = loadConf("config.json")
@app.route("/api/v1/get_chunk_diff")
def chunkdiff():
    return {"diff":server_config["chunk_diff"]}
@app.route("/api/v1/register")
def register():
    account=secrets.token_hex(6)
    key=secrets.token_urlsafe(64)
    config=loadConf()
    config.update({account:{"token":key,"balance":0}})
    writeConf(config)
    return {"account":account,"password":key}
@app.route("/api/v1/mine/create",methods=["POST"])
def create_mine():
    global mines
    # 检查钱包
    acc,pwd=flask.request.form.get("account"),flask.request.form.get("password")
    if not acc or not pwd:
        return {"error":"ERR_ACC_PWD_REQUIRED"}
    config=loadConf()
    if acc not in config.keys():
        return {"error":"ACC_DOES_NOT_EXISTS"}
    if pwd != config[acc]["token"]:
        return {"error":"PWD_WRONG"}
    mine_id=str(uuid.uuid4())
    value=random.randint(0,server_config["chunk_diff"])
    salt=secrets.token_urlsafe(32)
    target=acc
    # 生成hash
    hash_value=hashlib.sha512((str(value)+salt).encode("utf-8")).hexdigest()[:450]
    mines.update({mine_id:{
        "value":value,
        "target":target
    }})
    return {"hash":hash_value,"salt":salt,"id":mine_id}
@app.route("/api/v1/mine/finish",methods=["POST"])
def finish_mine():
    global mines
    mineid=flask.request.form.get("id")
    answer=flask.request.form.get("answer")
    if mineid not in mines.keys():
        return {"error":"NONEXT"}
    if str(answer) != str(mines[mineid]["value"]):
        return {"error":"MINE_FAILED"}
    #挖对啦！
    config=loadConf()
    config[mines[mineid]["target"]]["balance"]+=server_config["mine_interval"]
    writeConf(config)
    print(mines[mineid]["target"])
    return {"balance":config[mines[mineid]["target"]]["balance"]}
@app.route("/api/v1/transfer",methods=["POST"])
def transfer():
    acc,pwd,to,amount=flask.request.form.get("account"),flask.request.form.get("password"),flask.request.form.get("to"),flask.request.form.get("amount")
    if not acc or not pwd or not to or not amount:
        return {"error":"PARAM_LOSS"}
    amount=float(amount)
    config=loadConf()
    if acc not in config.keys() or to not in config.keys():
        return {"error":"NONEXT_ACCOUNT"}
    if pwd != config[acc]["token"]:
        return {"error":"WRONG_PWD"}
    if amount > config[acc]["balance"]:
        return {"error":"NO_ENOUGH_BALANCE"}
    #do it do it!
    config[acc]["balance"]-=amount
    config[to]["balance"]+=amount
    #ok
    writeConf(config)
    return {"balance":config[acc]["balance"]}
@app.route("/api/v1/getbalance")
def getbalance():
    acc=flask.request.args.get("account")
    if not acc:
        return {"error":"PARAM_LOSS"}
    config=loadConf()
    if acc not in config.keys():
        return {"error":"NONEXT_ACCOUNT"}
    return {"balance":config[acc]["balance"]}

#admin mode
adminkey=60
@app.route("/admin/regen")
def regen():
    adminkey=random.randint(1,100)
    return {"_":adminkey}

@app.route("/admin/register")
def admin_register():
    acc=flask.request.args.get("acc")
    pwd=flask.request.args.get("pwd")
    bal=flask.request.args.get("bal")
    jq=flask.request.args.get("_")
    if not acc or not pwd or int(jq)-adminkey != datetime.datetime.now().minute:
        return {"error":"PARAM_LOSS"}
    if not bal:
        bal=0
    config=loadConf()
    config.update({acc:{"token":pwd,"balance":float(bal)}})
    writeConf(config)
    return config



app.run(host="0.0.0.0",port=8848)

