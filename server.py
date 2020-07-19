# server.py
# where your python app starts

# init project
from flask import Flask, jsonify, render_template, request, url_for
application = Flask(__name__)

@application.route('/hmiside', methods=['GET', 'POST'])
def calculate_value_at_hmi():
  switcher_on_hmi= {11:4, 21:5, 12:6, 22:7, 13:8, 23:9, 14:10, 24:11, 15:12, 25:13, 16:14, 26:15}
  data= ast.literal_eval(request.args['vacs'])
  vacs_from_hmi= [int(x) for x in data]
  
  info_val= 0
  for i in vacs_from_hmi:
    try:
      #print(i, 2**switcher_on_hmi.get(i))
      info_val= info_val | (2 ** switcher_on_hmi.get(i))
      #print("info_val", info_val)
    except Exception as e:
      continue
  info_val= info_val | 1
  return (jsonify(info_val))

@application.route('/bb08side', methods=['GET', 'POST'])
def value_retrieval_at_bb08():
  #print("Consolidated value received from HMI: ", info_val)
  bin_res= '{:016b}'.format(int(request.args['info_val']))
  print("Binary Representation of Values received from HMI: ", bin_res[:4]+" "+bin_res[4:8]+" "+bin_res[8:12]+" "+bin_res[12:16])
  switcher= {5:11, 6:21, 7:12, 8:22, 9:13, 10:23, 11:14, 12:24, 13:15, 14:25, 15:16, 16:26}

  sel_vacs= list()
  lsb= bin_res[::-1]
  for i in range(len(lsb)):
    #print(i)
    if(lsb[i] == '1'):
      try:
        sel_vacs.append(switcher[i+1])
      except Exception as e:
        continue
  return(jsonify(bin_res[:4]+" "+bin_res[4:8]+" "+bin_res[8:12]+" "+bin_res[12:16]))
# I've started you off with Flask, 
# but feel free to use whatever libs or frameworks you'd like through `.requirements.txt`.

# unlike express, static files are automatic: http://flask.pocoo.org/docs/0.12/quickstart/#static-files

# http://flask.pocoo.org/docs/0.12/quickstart/#routing
# http://flask.pocoo.org/docs/0.12/quickstart/#rendering-templates
@application.route('/')
def hello():
  return render_template('index.html')
  
# listen for requests :)
if __name__ == "__main__":
  import ast
  from os import environ
  application.run(host='0.0.0.0', port=int(environ['PORT']))