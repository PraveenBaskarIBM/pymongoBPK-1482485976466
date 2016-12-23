import os
import pymongo
#import ssl
import json  
from pymongo import MongoClient
try:
  from SimpleHTTPServer import SimpleHTTPRequestHandler as Handler
  from SocketServer import TCPServer as Server
except ImportError:
  from http.server import SimpleHTTPRequestHandler as Handler
  from http.server import HTTPServer as Server

# Read port selected by the cloud for our application
PORT = int(os.getenv('PORT', 8000))
# Change current directory to avoid exposure of control files
os.chdir('static')

# VCAP_SERVICES mapping Start

services = os.getenv('VCAP_SERVICES')
services_json = json.loads(services)
mongodb_url = services_json['compose-for-mongodb'][0]['credentials']['uri']
#connect:
client = MongoClient(mongodb_url)  
#get the default database:
db = client.get_default_database()  
print('connected to mongodb!, welcome to mongodb connection, have a fun') 

###----Regression Code begins------###
import pandas as pd
import cPickle as pickle
import sklearn

data = pd.read_csv('d1_test.csv', header=None, names=['col1', 'col2', 'col3', 'col4', 'col5', 'col6'])
print data
print('\n')
with open('test3_model.pkl', 'rb') as f:
  classifier = pickle.load(f)

del data['col1']
predicted_set = classifier.predict(data)
prob_predicted = classifier.predict_proba(data)

data = pd.DataFrame(data, columns=["col1", "col2", "col3", "col4", "col5", "col6"])
pred = pd.DataFrame(predicted_set, columns=["col7"])
df_prob = pd.DataFrame(prob_predicted, columns=["col8", "col9"])

frame1 = [data,pred]
df1 = pd.concat(frame1,axis=1, join_axes=[data.index])
frame2 = [df1,df_prob]
df2 = pd.concat(frame2,axis=1, join_axes=[data.index])

df2['col10'] = df2['col9'].map(lambda x: 'Low' if x < 0.5 else 'Medium' if x < 0.75 else 'High')
del df2['col1']
print df2


###----Regression Code Ends------###

# VCAP_SERVICES mapping END

httpd = Server(("", PORT), Handler)
try:
  print("Start serving at port %i" % PORT)
  httpd.serve_forever()
except KeyboardInterrupt:
  pass
httpd.server_close()


