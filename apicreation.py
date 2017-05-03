'''
Created on 15-Apr-2017

@author: Aayush
'''
from flask import Flask, request
from flask_restful import Resource, Api
from requests_oauthlib import OAuth1
import requests

app = Flask(__name__)
api = Api(app)

class resoursesites():
    def google(self,query_gog):
        #url='https://www.googleapis.com/customsearch/v1?key=AIzaSyCllRU9INS17ljk6VHQN2VsjFtKqcoHSUo&cx=012566753202515436290:hx0gfzsksi0&q=the dark knight'
        url='https://www.googleapis.com/customsearch/v1?key=AIzaSyCllRU9INS17ljk6VHQN2VsjFtKqcoHSUo&cx=012566753202515436290:hx0gfzsksi0&q=%s'%query_gog
        qwerty=requests.get(url)
        return (qwerty.json())
    def twitter(self,query):
        #query=query.replace(" ", "%20")
        #print(query)
        if(' ' in query): 
            query=query.replace(" ","%20")
            #print('aayush')
            url='https://api.twitter.com/1.1/search/tweets.json?q=%s'%query
        else:
            query='%40'+query
            #print('tandon')
            #print(query)
            url='https://api.twitter.com/1.1/search/tweets.json?q=%s'%query
        #url='https://api.twitter.com/1.1/search/tweets.json?q=%40thedarknight'
        oauth = OAuth1("wwWdEmo9Jg8n3G0LKnU4Vl63A",
                client_secret="Tj21UmWnopUMyjW83XT7p0fI4WATYJPzHjU5Z6Rs6tb6Lv10wm",
                resource_owner_key="854329939172216833-rhscATnbRTJfMJfV2yEYndAvYwGVzy6",
                resource_owner_secret="BoXUYtOVkwg9VCS1TyMgujaB0XQBFVr1i9AwOAkfIq8hR")
        r = requests.get(url, auth=oauth)
        return (r.json())
    def duckduckgoo(self,query):
        #url1='http://api.duckduckgo.com/?q=the dark knight&format=json'
        url1='http://api.duckduckgo.com/?q=%s&format=json'%query
        q=requests.get(url1)
        return (q.json())
    def google_read(self,rfile,tfile,dfile,main_query):  
        g_url=rfile['items'][0]['link']
        g_text=rfile['items'][0]['snippet']
        for i in tfile['statuses']:
            if(i['entities']['urls']):
                t_url=i['entities']['urls'][0]['expanded_url']
                t_text=i['text']
                break
            else:
                continue
        
        if(dfile['Results']):
            d_url=dfile['Results'][0]['FirstURL']
            d_text=dfile['Results'][0]['Text']
        else:
            d_url=dfile['RelatedTopics'][0]['FirstURL']
            d_text=dfile['RelatedTopics'][0]['Text']
            
        dict1={
            "query": "%s"%main_query,
            "results": {
            "google": {"url": g_url,"text": g_text},
            "twitter": {"url": t_url,"text": t_text},
            "duckduckgo": {"url": d_url,"text": d_text}
            }
            }
        return (dict1)
                         
class Departments_Meta(Resource):
    def get(self):
        query1='facebook'
        rs=resoursesites()
        json1=rs.google(query1)
        json2=rs.twitter(query1)
        json3=rs.duckduckgoo(query1)
        dictionary1=rs.google_read(json1,json2,json3,query1)
        return(dictionary1)
        #return(json2)
api.add_resource(Departments_Meta, '/departments')

if __name__ == '__main__':
     app.run()