import hashlib, logging, os
from datetime import datetime
from hashlib import sha256
from sys import exit
from time import sleep
from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair
from Crypto.Hash import SHA256
from flask import Flask, jsonify, redirect, render_template, request, url_for,Response,abort
from flask_pymongo import PyMongo
import json
import requests
from requests.auth import HTTPBasicAuth
from functools import wraps
from itertools import zip_longest
from flask_cors import CORS
from flask_paginate import Pagination,get_page_args

app = Flask(__name__)
CORS(app)
# client = pymongo.MongoClient('http://localhost:27017/')

# client.bigchain.authenticate('sonam', 'Asdf12@34')
# uri ="mongodb://sonam:Asdf12@34@localhost:27017/bigchain"
#client = pymongo.MongoClient("mongodb://sonam:Asdf12@34@localhost:27017/bigchain")
app.config['MONGO_HOST'] = 'localhost'
app.config['MONGO_PORT'] = '27017'
app.config['MONGO_DBNAME'] = 'bigchain'
app.config['MONGO_USERNAME'] = 'bigchain'
app.config['MONGO_PASSWORD'] = 'Qwert123'
app.config['MONGO_AUTH_SOURCE'] = 'admin'
# app.config['MONGO_USERNAME']='sonam'
# app.config['MONGO_PASSWORD']='Asdf12@34'
app.config["MONGO_URI"] = "mongodb://bigchain:Qwert123@localhost:27017/bigchain"
mongo = PyMongo(app)

bulk_txids = True
bulk_assets = True

bdb_root_url = 'http://localhost:9984'
bdb = BigchainDB(bdb_root_url)

def require_appkey(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        auth = request.args.get('api_key')
        print("auth: ", auth)
        data = mongo.db.api_key.find()
        for i in data:
            if auth ==i['api_key']:
                return view_function(*args, **kwargs)

        else:
            abort(401)
    return decorated_function

# @app.route('/')
# #@require_appkey
# def index():
#    return render_template('search.html',)

# @app.route('/transactions')
# #@require_appkey
# def transactions():
#     return render_template('transaction.html')

# @app.route('/displayasset')
# #@require_appkey
# def displayasset():
#     return render_template('display_asset.html')

# @app.route('/generatekeypair')
# #@require_appkey
# def generatekeypair():
#     return render_template('create_keypair.html')

# @app.route('/transfer')
# #@require_appkey
# def transfer():
#     return render_template('transfer.html')

# @app.route('/blockid')
# #@require_appkey
# def blockid():
#     return render_template('blockid.html')

# @app.route('/transaction_ids')
# #@require_appkey
# def transactionids():
#     return render_template('transaction_ids.html')

# @app.route('/show_asset')
# #@require_appkey
# def showasset():
#     return render_template('show_asset.html')

@app.route('/create_keypair/<hash_type>',methods =['GET'])
def create_keypair(hash_type):
    if request.method == 'GET':
        # User = request.form['user']
        User= generate_keypair()
        hash_Object = SHA256.new(User.private_key.encode()+User.public_key.encode()).hexdigest() # generating hash from cryptokeypair of user
        data = mongo.db.users                                                                    #create new collection in mongodb named users
        data.insert({'Public_Key': User.public_key, 'Private_Key': User.private_key ,'Hash': hash_Object, "last_modified": datetime.now(), 'type':hash_type})
        return hash_Object

    elif request.method == 'POST':
        return render_template('method.html')

@app.route('/transferdata',methods =['POST','GET']) # create/ register a transaction.
def transaction():
    if request.method == 'POST':
        try:
            # print(request.args.get)
            # asset = request.args.get('asset')
            # asset_metadata = request.args.get('asset_metadata')
            # hash_Object = request.args.get('hash_Object')
            req_data = request.get_json()
            # print(req_data)
            # print(request.args.get)
            asset_metadata = request.args.get('asset_metadata')
            hash_Object = request.args.get('hash_Object')
            asset = req_data['asset']

            data =mongo.db.users.find()  #accessing data from mongodb collection named user
            for row in data:
                hashkey = row['Hash']
                if hash_Object== hashkey:
                    user = [row['Private_Key'], row['Public_Key']]

                    prepared_creation_tx = bdb.transactions.prepare(
                        operation='CREATE',
                        signers=user[1],
                        asset={'data':{'asset':asset}},
                        metadata={'meta':asset_metadata}
                    )
                    #print('prepared',prepared_creation_tx)
                    fulfilled_creation_tx = bdb.transactions.fulfill(
                    prepared_creation_tx,
                    private_keys=user[0]
                    )

                    sent_creation_tx = bdb.transactions.send_commit(fulfilled_creation_tx)
                    txid = fulfilled_creation_tx['id']
                    key = mongo.db.keys
                    key.insert({'txid':txid,'Hash':hashkey, "last_modified": datetime.now()})

                    if sent_creation_tx == fulfilled_creation_tx:            #check transaction status
                        return txid

            else:
                return render_template('invalidhash.html')

        except Exception as e:
            return render_template('500.html', error = str(e))


    elif request.method == 'GET':
        return render_template('method.html')


# @app.route('/transfer_asset',methods =['POST','GET']) # transfer an asset by providing appropriate hash keys.
# def transfer_asset():
#     global bulk_txids
#     if bulk_txids == True:

#         if request.method =='POST':
#             try:

#                 Hashkey_1 = request.form['Hashkey_1']
#                 Hashkey_2 = request.form['Hashkey_2']
#                 Txid = request.form['Txid']
#                 Data = mongo.db.users.find()
#                 for i in Data:
#                     if Hashkey_1 == i['Hash']:
#                         alice = [i['Private_Key'], i['Public_Key']]



#                     if Hashkey_2 ==i['Hash']:
#                         bob =[i['Private_Key'], i['Public_Key']]

#                         output_index = 0
#                         trans = mongo.db.transactions.find()  #accessing transactions stored in database

#                         for x in trans:
#                             if Txid == x['id']:
#                                 asset_id = Txid

#                         transfer_asset = {
#                             'id': asset_id
#                         }
#                         output = x['outputs'][output_index]
#                         transfer_input = {
#                             'fulfillment': output['condition']['details'],
#                             'fulfills':{
#                                 'output_index': output_index,
#                                 'transaction_id': asset_id
#                             },
#                             'owners_before': output['public_keys']
#                         }

#                         prepared_transfer_tx = bdb.transactions.prepare(
#                         operation='TRANSFER',
#                         asset=transfer_asset,
#                         inputs=transfer_input,
#                         recipients=bob[1],
#                         )

#                         fulfilled_transfer_tx = bdb.transactions.fulfill(
#                         prepared_transfer_tx,
#                         private_keys=alice[0],
#                         )


#                         sent_transfer_tx = bdb.transactions.send_commit(fulfilled_transfer_tx)
#                         if sent_transfer_tx == fulfilled_transfer_tx:         #check transfer status
#                             return jsonify(results = sent_transfer_tx)
#                         else:
#                             return render_template('utransaction.html')

#             except Exception as e:
#                 return render_template('wtransaction.html',error = str(e))

#         elif request.method == 'GET':
#             return render_template('method.html')

#     elif bulk_txids == False:
#         return render_template('bulk.html')


# @app.route('/display_asset',methods =['POST','GET']) # get asset and block hash using hash of the user.
# def display_asset():
#     if request.method =='POST':
#         try:
#             #print(request.form)
#             #Hashkey = request.form['Hashkey']
#             Hashkey = request.args.get('Hashkey')
#             data = mongo.db.keys.find()
#             Data=[]
#             transac_id=[]
#             Blockid=[]



#             for row in data:

#                 Hash_key=row['Hash']

#                 if Hashkey == Hash_key:
#                     Txid = row['txid']
#                     transac_id.append(row['txid'])
#                     block_height = bdb.blocks.get(txid=Txid)
#                     r = requests.get('http://localhost:26657/block?height='+str(block_height))

#                     mydata= json.loads(r.text)
#                     blockid =mydata['result']['block_meta']['block_id']['hash']
#                     Blockid.append(blockid)
#                     asset_data = mongo.db.assets.find()
#                     for i in asset_data:
#                         if Txid == i['id']:
#                             Data.append(i['data'])

#             res = [{"Data": n, "txid": i, "blockid":k} for n, i,k in zip(Data,transac_id,Blockid)]

#             return jsonify(results=res)
#         except UnboundLocalError as e:
#             return render_template('invalidhash.html',error = str(e))


#     elif request.method =='GET':
#         return render_template('method.html')

@app.route('/users/<page>',methods=['GET'])

def ussers(page):
    if request.method=='GET':
        try:
            Data=[]
            final_dict={}
            page_size = 10
            page_num = page
            skips = (page_size) * (int(page_num) - 1)

            query= {"type":"user"}
            users_hash= mongo.db.users.find(query).sort([('_id', -1)])
            usr_hash= mongo.db.users.find(query).sort([('_id', -1)]).skip(skips).limit(page_size)
            
            usr_dict={}
            usr_page={}
            usr_page['page']= int(page_num)
            usr_page['count']=users_hash.count()
            
            #usr_dict['usr_result']=usr_page
            final_dict['result']=usr_page
            
            for row in usr_hash:

                users_dict ={}
                txn_page_size = 5
                txn_page_num = 1
                txn_skips=(txn_page_size) * (int(txn_page_num) -1)
                device_id=row['Hash']
                
                data=get_usr_txn_list(txn_page_size,txn_page_num,txn_skips,device_id)
                print(data)
                users_dict['txs']=data
                #get devices list

                dev_page_size = 5
                dev_page_num = 1
                dev_skips=(dev_page_size) * (int(dev_page_num) -1)
                dev_data=get_dev_list(dev_page_size,dev_page_num,dev_skips,device_id)
                users_dict['device_hash']=dev_data
                users_dict['user_hash']=row['Hash']
                
                Data.append(users_dict)
            final_dict['users']=Data

            return json.dumps(final_dict)
        except Exception as e:
            return str(e)    






@app.route('/userss/<id>',methods =['GET'])     #get all the transaction ids using hash of the user.
def transaction_ids(id):
    # global bulk_assets
    # if bulk_assets== True:
   
    if request.method=='GET':
        try:

            users_dict ={}
            txn_page_size = 5
            txn_page_num = 1
            txn_skips=(txn_page_size) * (int(txn_page_num) -1)
            device_id=id
            
            data=get_usr_txn_list(txn_page_size,txn_page_num,txn_skips,device_id)
           
            users_dict['txs']=data

            dev_page_size = 5
            dev_page_num = 1
            dev_skips=(dev_page_size) * (int(dev_page_num) -1)
            dev_data=get_dev_list(dev_page_size,dev_page_num,dev_skips,device_id)
            users_dict['device_hash']=dev_data
            users_dict['user_hash']=id


               
            return json.dumps(users_dict)
        except Exception as e:
            return  str(e)  

@app.route('/transactions/<page>',methods=['GET'])
def txids(page):
    if request.method=='GET':
        try:
            
            Data=[]
            final_dict={}
            page_size = 10
            page_num = page
            skips = (page_size) * (int(page_num) - 1)
            query={"data.asset.type_check" :{ "$regex": "^c" }}
            txn_hash = mongo.db.assets.find(query).sort([('_id', -1)])
            trxn_hash = mongo.db.assets.find(query).sort([('_id', -1)]).skip(skips).limit(page_size)
            
            txn_dict={}
            txn_page={}
            txn_page['page']= int(page_num)
            txn_page['count']=txn_hash.count()
            
            #txn_dict['txn_result']=txn_page
            final_dict['result']=txn_page

            for row in trxn_hash:

                txn_data=row['data']
                txn_data['txid']=row['id']
                # assetdata = i['data']
                # assetdata['id']=i['id']
                
                Data.append(txn_data)
            final_dict['data']=Data
            return json.dumps(final_dict)
        except Exception as e:
            return str(e)



@app.route('/transactionss/<id>', methods =['GET'])     # get asset data and block hash using transaction id.
def show_asset(id):
    if request.method =='GET':
        try:            
            
            Data =[]
            # for row in data:
            #     if id == row['txid']:
                    # block_height = bdb.blocks.get(txid=id)
                    # r = requests.get('http://localhost:26657/block?height='+str(block_height))
                    # mydata= json.loads(r.text)
                    #blockid =mydata['result']['block_meta']['block_id']['hash']

            asset_data = mongo.db.assets.find().sort([('_id', -1)])
            for i in asset_data:
                if id == i['id']:
                    i['data']['txid']=id
                
                return json.dumps(i['data'])

        except UnboundLocalError as e:
            return str(e)

    elif request.method =='POST':
        return render_template('method.html')

                   
                    

@app.route('/search/<id>',methods = ['GET'])
def searchs(id):

    if request.method =='GET':
        try:
            
            #Txid = request.form['txid']
            #txid=request.args.get('txid')
            newquery={"id":id}
            data = mongo.db.assets.find(newquery)
            Data =[]

            myquery  ={"type":"user","Hash" :id}
            dataa= mongo.db.users.find(myquery)
            
            query  ={"type":"device","Hash" :id}
            dataaa= mongo.db.users.find(query)
            
            
            if data.count() > 0:
                datam = {}
                datam['id'] = id
                datam['type']="transactions"
                Data.append(datam)
                
                return jsonify( Data[0])
           
            elif dataa.count() >0:
                   
            
            
                data={}
                data['id'] = id
                data['type']="users"
                Data.append(data)
                
                return jsonify( Data[0])

            elif dataaa.count()>0:
                data={}
                data['id'] = id
                data['type']="devices"
                Data.append(data)
                    
                return jsonify(Data[0])

        except UnboundLocalError as e:
            return render_template('invalidhash.html',error = str(e))

    elif request.method =='POST':
        return render_template('method.html')




# @app.route('/result',methods = ['POST','GET'])
# def search():
#     if request.method == 'POST':
#         try:
#             txid = request.form['txid']
#             block_height = bdb.blocks.get(txid=txid)  # get block height using transaction id
#             block = bdb.blocks.retrieve(str(block_height)) # retrieve the complete block using block height
#             return render_template ('result.html',result=block)

#         except Exception as e:
#             #log this exception for further reference check flask or python loggin library
#             return render_template('invalidhash.html',error= str(e))

#     elif request.method == 'GET':
#         return render_template('method.html')


# @app.route('/block_id',methods=['POST','GET'])   # get asset data, current and previous block hash using transaction id.
# def block_id():
#     if request.method =='POST':
#         try:
#             #txid = request.form['txid']
#             txid=request.args.get('txid')
#             block_height = bdb.blocks.get(txid=txid)
#             r = requests.get('http://localhost:26657/block?height='+str(block_height))
#             mydata= json.loads(r.text)
#             blockid =mydata['result']['block_meta']['block_id']['hash']
#             lastblockid =mydata['result']['block']['last_commit']['block_id']['hash']
#             Data = mongo.db.assets.find()

#             for row in Data:
#                 if txid == row['id']:
#                     asset_data = row['data']
#             mydict ={'blockid':blockid , 'lastblockid':lastblockid, 'asset_data':asset_data}
#             return jsonify(results = mydict)
#         except KeyError as e:
#             return render_template('invalidhash.html',error=str(e))

#     elif request.method == 'GET':
#         return render_template('method.html')



@app.route('/devices/<page>',methods=['GET'])

def device(page):
    if request.method =='GET':
        try:
            Data=[]
            final_dict={}
            page_size = 10
            page_num = page
            skips = (page_size) * (int(page_num) - 1)
           
            query= {"type":"device"}
            devc_hash= mongo.db.users.find(query).sort([('_id', -1)])
            dev_hash= mongo.db.users.find(query).sort([('_id', -1)]).skip(skips).limit(page_size)
            # initialise dict for device pagination
            dev_dict={}
            dev_page={}
            dev_page['page']= int(page_num)
            dev_page['count']=devc_hash.count()
            
            #dev_dict['dev_result']=dev_page
            final_dict['result']=dev_page
            
            for row in dev_hash:
                devices_dict ={}
                txn_page_size = 5
                txn_page_num = 1
                txn_skips=(txn_page_size) * (int(txn_page_num) -1)
                device_id=row['Hash']
                
                data=get_txn_list(txn_page_size,txn_page_num,txn_skips,device_id)
                devices_dict['txs']=data
                
                # get users list
                usr_page_size = 5
                usr_page_num = 1
                usr_skips=(usr_page_size) * (int(usr_page_num) -1)
                us_data=get_usr_list(usr_page_size,usr_page_num,usr_skips,device_id)
                devices_dict['users']=us_data
                devices_dict['device_hash']= device_id
                
                Data.append(devices_dict)   
            final_dict['devices']=Data 
                
            return json.dumps(final_dict)    
        except Exception as e:
            return str(e)

@app.route('/devicess/<id>',methods=['GET'])
def devicess(id):
  
    if request.method=='GET':
        try:

            devices_dict ={}
            txn_page_size = 5
            txn_page_num = 1
            txn_skips=(txn_page_size) * (int(txn_page_num) -1)
            device_id=id
            
            data=get_txn_list(txn_page_size,txn_page_num,txn_skips,device_id)
            devices_dict['txs']=data
                

            usr_page_size = 5
            usr_page_num = 1
            usr_skips=(usr_page_size) * (int(usr_page_num) -1)
            us_data=get_usr_list(usr_page_size,usr_page_num,usr_skips,device_id)
            devices_dict['users']=us_data
            devices_dict['device_hash']= id
            return json.dumps(devices_dict)
        except Exception as e:
            return render_template('invalidhash.html',error= str(e))              

@app.route('/transaction/<device_id>/<txn_page_num>', defaults= {"txn_page_size" : 5, "txn_skips" : -1},methods=['GET'])
@app.route('/transaction/<device_id>/<txn_page_num>/<txn_page_size>/<txn_skips>',methods=['GET'])
              
def get_txn_list(txn_page_size,txn_page_num,txn_skips,device_id):
    data={}
    flag = False
    if( txn_skips and txn_skips == -1):
        flag = True
        txn_skips = txn_page_size * (int(txn_page_num) - 1)
        
    txn_query  ={"data.asset.device_hash":device_id,"data.asset.type_check" :{ "$regex": "^c" }} ## to get txid and device id 
    txnn_data = mongo.db.assets.find(txn_query).sort([('_id', -1)])
    txn_data = mongo.db.assets.find(txn_query).sort([('_id', -1)]).skip(txn_skips).limit(txn_page_size)

    trxn_query =  {"data.asset.device_hash":device_id,"data.asset.type_check" :"device create"} 
    trxn_data = mongo.db.assets.find(trxn_query).sort([('_id', -1)]).skip(txn_skips).limit(txn_page_size)
    txn_dict={}
    txn_page={}
    txn_page['page']= txn_page_num
    if txn_data.count() >0 and trxn_data.count() >0:
       
        txn_page['count']=txnn_data.count() 
        
        txn_dict['txn_result']=txn_page
        
        transac_id=[]
        for tran in txn_data:
            transac_id.append(tran['id'])
        txn_dict['txid']=list(set(transac_id))
        
    elif trxn_data.count() >0 and not txn_data.count():
        txn_page['count']= 0
        txn_dict['txn_result']=txn_page
        txn_dict['txid']=[]
        
    if(flag):
        return json.dumps(txn_dict)
    else:
        return txn_dict


@app.route('/user/<device_id>/<usr_page_num>', defaults= {"usr_page_size" : 5, "usr_skips" : -1},methods=['GET'])
@app.route('/user/<device_id>/<usr_page_num>/<usr_page_size>/<usr_skips>',methods=['GET'])

def get_usr_list(usr_page_size,usr_page_num,usr_skips,device_id):
    data={}
    flag = False
    if( usr_skips and usr_skips == -1):
        flag = True
        usr_skips = usr_page_size * (int(usr_page_num) - 1)
                
    usr_query  ={"data.asset.device_hash":device_id,"data.asset.type_check" :{ "$regex": "^c" }} ## to get txid and device id 
    usr_data = mongo.db.assets.find(usr_query).sort([('_id', -1)]).skip(usr_skips).limit(usr_page_size)
    usrs_data = mongo.db.assets.find(usr_query).sort([('_id', -1)])
    user_query =  {"data.asset.device_hash":device_id,"data.asset.type_check" :"device create"} 
    user_data = mongo.db.assets.find(user_query).sort([('_id', -1)]).skip(usr_skips).limit(usr_page_size)
    usr_dict={}
    usr_page={}
    usr_page['page']= usr_page_num
    owner_id=''
    if usr_data.count() >0 and user_data.count():
       
        usr_page['count']=usrs_data.count() 
        
        usr_dict['usr_result']=usr_page
        
        user_id=[]
        for users in usr_data:
            user_id.append(users['data']['asset']['user_hash'])
        usr_dict['user_hash']=list(set(user_id))
        for owner in user_data:
            owner_id=(owner['data']['asset']['user_hash'])
             
        usr_dict['owner_hash']=owner_id
    elif user_data.count() >0 and not usr_data.count():
        usr_page['count']= 0
        usr_dict['usr_result']=usr_page
        usr_dict['user_hash']=[]
        for owner in user_data:
            owner_id=(owner['data']['asset']['user_hash'])
             
        usr_dict['owner_hash']=owner_id
        
    
    if(flag):
        return json.dumps(usr_dict)
    else:
        return usr_dict  

@app.route('/device/<device_id>/<dev_page_num>', defaults= {"dev_page_size" : 5, "dev_skips" : -1},methods=['GET'])
@app.route('/device/<device_id>/<dev_page_num>/<dev_page_size>/<dev_skips>',methods=['GET'])        

def get_dev_list(dev_page_size,dev_page_num,dev_skips,device_id):
    data={}
    flag = False
    if( dev_skips and dev_skips == -1):
        flag = True
        dev_skips = dev_page_size * (int(dev_page_num) - 1)
                
    dev_query  ={"data.asset.user_hash":device_id,"data.asset.type_check" :{ "$regex": "^c" }} ## to get txid and device id 
    dev_data = mongo.db.assets.find(dev_query).sort([('_id', -1)]).skip(dev_skips).limit(dev_page_size)

    dev_dict={}
    dev_page={}
    dev_page['page']= dev_page_num
    if dev_data.count() >0 :
       
        dev_page['count']=dev_data.count() 
        
        dev_dict['dev_result']=dev_page
        
        dev_id=[]
        for devices in dev_data:
            dev_id.append(devices['data']['asset']['device_hash'])
        dev_dict['device_hash']=list(set(dev_id))

    elif not dev_data.count():
        dev_page['count']= 0
        dev_dict['dev_result']=dev_page
        dev_dict['device_hash']=[]
    
    if(flag):
        return json.dumps(dev_dict)
    else:
        return dev_dict        

@app.route('/usr_transaction/<device_id>/<txn_page_num>', defaults= {"txn_page_size" : 5, "txn_skips" : -1},methods=['GET'])
@app.route('/usr_transaction/<device_id>/<txn_page_num>/<txn_page_size>/<txn_skips>',methods=['GET'])     

def get_usr_txn_list(txn_page_size,txn_page_num,txn_skips,device_id):
    data={}
    flag = False
    if( txn_skips and txn_skips == -1):
        flag = True
        txn_skips = txn_page_size * (int(txn_page_num) - 1)
        
    txn_query  ={"data.asset.user_hash":device_id,"data.asset.type_check" :{ "$regex": "^c" }} ## to get txid and device id 
    trxn_data = mongo.db.assets.find(txn_query).sort([('_id', -1)])
    txn_data = mongo.db.assets.find(txn_query).sort([('_id', -1)]).skip(txn_skips).limit(txn_page_size)

    # trxn_query =  {"data.asset.user_hash":device_id,"data.asset.type_check" :"device create"} 
    # trxn_data = mongo.db.assets.find(trxn_query).sort([('_id', -1)]).skip(txn_skips).limit(txn_page_size)
    txn_dict={}
    txn_page={}
    txn_page['page']= txn_page_num
    if txn_data.count() >0:
       
        txn_page['count']=trxn_data.count() 
        
        txn_dict['txn_result']=txn_page
        
        transac_id=[]
        for tran in txn_data:
            transac_id.append(tran['id'])
        txn_dict['txid']=list(set(transac_id))
        
    elif not txn_data.count():
        txn_page['count']= 0
        txn_dict['txn_result']=txn_page
        txn_dict['txid']=[]
        
    if(flag):
        return json.dumps(txn_dict)
    else:
        return txn_dict       
    
          

if __name__ == '__main__':
#    app.run(host='0.0.0.0', port=3000)
    app.run()
        


#
    

# @app.route('/devices/<page>',methods=['GET'])
    
# def device(page):
  
#     if request.method=='GET':
#         try:
#             page_size = 10
#             page_num = int(request.args.get('page')) if int(request.args.get('page')) else page
            
#             skips = (page_size) * (page_num - 1)
            
#             query  ={"type":"device"}
#             dataa= mongo.db.users.find(query).sort([('_id', -1)]).skip(skips).limit(page_size)
#             Data=[]
#             mydict={}
#             pages = {}
#             pages['count'] = dataa.count()
#             pages['page'] = page_num
#             mydict['result']= pages

#             for row in dataa:
#                 trxn_page = 1
#                 trxn_page_size = 5
#                 trxn_skip = trxn_page_size * (trxn_page - 1)    
                
#                 # get_list_transaction(trxn_page,trxn_page_size,trxn_skip, dataa)
#                 data={}
                
#                 newquery  ={"data.asset.device_hash":row['Hash'],"data.asset.type_check" :{ "$regex": "^c" }} ## to get txid and device id 
#                 dataaa = mongo.db.assets.find(newquery).sort([('_id', -1)]).skip(skips).limit(page_size)
#                 ## user hases ,txid ,device hash
#                 #newdict={}
#                 newpages = {}
#                 newpages['count'] = dataaa.count()
#                 newpages['page'] = page_num
                
                 
#                 # newqueryy  ={"data.asset.device_hash":row['Hash'],"data.asset.type_check" :"checkout"} ## to get txid and device id 
#                 # dataaaa = mongo.db.assets.find(newqueryy).sort([('_id', -1)]).skip(0).limit(1)
#                 ## user hases ,txid , device hash
                
#                 myquery =  {"data.asset.device_hash":row['Hash'],"data.asset.type_check" :"device create"} 
#                 ## owner hash , device hash , 

#                 datass = mongo.db.assets.find(myquery).sort([('_id', -1)]).skip(0).limit(1)
               
#                 #mykey = mongo.db.keys.find(query)
#                 if dataaa.count() > 0 and datass.count()>0:
#                     transac_id=[]
#                     user_id=[]
#                     owner=''
#                     for m in dataaa:
#                         user_id.append(m['data']['asset']['user_hash'])
#                         transac_id.append(m['id'])
#                     for l in datass:
#                         owner=l['data']['asset']['user_hash']
#                     data['txid_result']= pages
#                     data['txid'] = transac_id
#                     data['user_hash']=user_id
#                     data['device_hash']=row['Hash']
#                     data['owner_hash']=owner
#                     Data.append(data)
#                     mydict['data']=Data
#                 # elif dataaaa.count() > 0 and datass.count()>0:
#                 #     transac_id=[]
#                 #     user_id=[]
#                 #     owner=''
#                 #     for m in dataaaa:
#                 #         user_id.append(m['data']['asset']['user_hash'])
#                 #         transac_id.append(m['id'])
                       
#                 #     for l in datass:
#                 #         owner=l['data']['asset']['user_hash']
#                 #     data['txid'] = transac_id
#                 #     data['user_hash']=user_id
#                 #     data['device_hash']=row['Hash']
#                 #     data['owner_hash']=owner
#                 #     Data.append(data)
#                 #     mydict['data']=Data

#                 elif datass.count()>0 and not dataaa.count():
                     
#                     device_id=[]
#                     for m in datass:
                        
#                         device_id.append(m['data']['asset']['user_hash'])

#                     data['txid'] = []
#                     data['user_hash']=[]
#                     data['device_hash']=row['Hash']
#                     data['owner_hash']= None
#                     Data.append(data)    
#                     mydict['data']=Data   
                                     

#             return json.dumps(mydict)
#         except Exception as e:
#             return render_template('invalidhash.html',error= str(e))



       

