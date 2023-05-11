from django.shortcuts import render

from config.settings import CF_ID, CF_TOKEN
from rest_framework.views import APIView
from rest_framework.response import Response
import requests

class GetUploadURL(APIView):
    def post(self, request):
        url= f"https://api.cloudflare.com/client/v4/accounts/{CF_ID}/images/v2/direct_upload"
        one_time_url = requests.post(
            url, 
            headers={
                "Authorization":f"Bearer {CF_TOKEN}"    
            }
        )
        one_time_url = one_time_url.json()
        result=one_time_url.get('result')
        return Response({"id":result.get("id"), "uploadURL": result.get('uploadURL')})