import os.path
import sys
import yaml
import pprint
from config import *
import pymysql
import pandas as pd
from django.contrib.admin.templatetags.admin_list import results
import requests
import json
import csv
import pandas as pd
import numpy as np
#from __main__ import name
#from __main__ import name
#from nltk.sem.chat80 import items



try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai




global NAME
NAME=None

def extract(category,field):
    df = pd.read_csv('harvey.csv')
    print (df.loc[df['Items'] == category,field])
    split=df.loc[df['Items'] == category,field].str.split(',').tolist()[0]
    split=map(lambda s: s.strip(), split)
    return split

def product_list(category):
	f=open('har.json').read()
	data=json.loads(f)
	return data[category]

def clear_context(user_id):
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    request = ai.text_request()
    request.lang = 'de'
    request.resetContexts = True
    request.session_id = user_id
    request.query = 'hi'
    response = yaml.load(request.getresponse())

def call_api(dict_input):
    global out_dict
    out_dict = {}
    out_dict['messageText'] = []
    out_dict['messageSource'] = 'messageFromBot'
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    request = ai.text_request()
    request.lang = 'de'
    request.resetContexts = False
    request.session_id = dict_input['user_id']
    user_id=request.session_id
    request.query = dict_input['messageText']
    print(request.query)
    global item       
    response = yaml.load(request.getresponse())
    pp = pprint.PrettyPrinter(indent=4)
    json_data = response['result']['parameters']
    pp.pprint(response)
    df = pd.read_csv('harvey.csv')
    
   

    if response['result']['metadata']=={}:
        out_dict['messageText'].append(response['result']['fulfillment']['messages'][0]['speech'])
        return out_dict
    elif response['result']['metadata']['intentName'] == 'Default Fallback Intent':
        out_dict['messageText'].append(response['result']['fulfillment']['messages'][0]['speech'])
        return out_dict
    elif response['result']['metadata']['intentName'] == 'Default Welcome Intent':
        out_dict['messageText'].append(response['result']['fulfillment']['messages'][0]['speech'])
        return out_dict
    elif response['result']['metadata']['intentName'] == 'best_sellers':
        out_dict['messageText'].append('Here is what is trending right now..')
        out_dict["plugin"] = {'name': 'link', 'type': 'products', 'data': data}
        return out_dict
    elif response['result']['metadata']['intentName'] == 'hot_deals':
        out_dict['messageText'].append('Here are some amazing deals that won\'t last long! Please have a look')
        out_dict["plugin"] = {'name': 'deals', 'type': 'products', 'data': deals,'link':'yes','values':'https://www.harveynorman.com.au/hot-deals'}
        return out_dict
    elif response['result']['metadata']['intentName'] == 'gift_cards':
        out_dict['messageText'].append('Gift cards are always the best option when you stuck for gift ideas. Take a look below: ')
        out_dict["plugin"] = {'name': 'link', 'type': 'products', 'data': gift}
        return out_dict
    elif response['result']['metadata']=={}:
        out_dict['messageText'].append(response['result']['fulfillment']['messages'][0]['speech'])
        return out_dict
    elif response['result']['metadata']['intentName'] == 'Default Fallback Intent':
        out_dict['messageText'].append(response['result']['fulfillment']['messages'][0]['speech'])
        return out_dict
    		
    elif response['result']['metadata']['intentName'] == 'place_order':
        if json_data['sub_sub_category']=='':
		if json_data['Product_sub_category']=='':
			if json_data['product_category']=='':
				out_dict['messageText'].append(response['result']['fulfillment']['messages'][0]['speech'])
            			out_dict['plugin'] = {'name': 'autofill', 'type': 'items', 'data': category}
            			return out_dict
			else:
				out_dict['messageText'].append(response['result']['fulfillment']['messages'][0]['speech'])
            			out_dict['plugin'] = {'name': 'autofill', 'type': 'items', 'data': sub_items[json_data['product_category']]}
            			return out_dict
		else:
			out_dict['messageText'].append(response['result']['fulfillment']['messages'][0]['speech'])
            		out_dict['plugin'] = {'name': 'autofill', 'type': 'items', 'data': sub_sub_items[json_data['Product_sub_category']]}
            		return out_dict	
	else:
	    products=json_data['sub_sub_category']
	    lists=product_list(products)
	    link=df.loc[df['Items'] == products,'Link']
	    out_dict["plugin"] = {'name': 'lists', 'type': 'products', 'data': lists,'link':'yess','values':link}
            out_dict['messageText'].append('Here are the products according to your preference')
	    clear_context(user_id)
            return out_dict

        
        
    
           
          
                
