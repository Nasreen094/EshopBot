# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.gis.geoip import GeoIP
from rest_framework import status

from rest_framework import viewsets
from config import *
from api.externel_api import call_api
import requests
from rest_framework.decorators import permission_classes
from rest_framework import permissions
import apiai
import yaml
# Create your views here.

def page_reload_operation(question):
    question['messageSource'] = 'messageFromBot'
    
    
    question['messageText'] = ['Hi friend, Welcome to Harvey Normans! What are you looking for today? ']
    question["plugin"] = {'name': 'autofill', 'type': 'items', 'data': list}
    
    
    return question
def clear_context(user_id):
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    request = ai.text_request()
    request.lang = 'de'
    request.resetContexts = True
    request.session_id = user_id
    request.query = 'hi'
    response = yaml.load(request.getresponse())
    print (response)
    
    
@permission_classes((permissions.AllowAny,))
class TestAPI(viewsets.ViewSet):
    def create(self, request):
        question = request.data
        print question
        
        CACHE_ID = 'Constant'
        if 'user_id' in question:
            CACHE_ID = question['user_id']
#
        user_input = question['messageText']
        if question['messageSource'] == 'userInitiatedReset':
            clear_context(CACHE_ID)
            question = page_reload_operation(question)
            return Response(question)
        
        if 'something else' in question['messageText'].lower():
            question = message_something_else(question)
            return Response(question)
        
        question = call_api(question)
        print (question)

        return Response(question)
