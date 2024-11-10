from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
#from django_filters import rest_framework as filters
from translator.models import Translation
from translator.serializers import TranslationSerializer

# Create your views here.

class TranslationViewSet(APIView):

    def get(self, request):
        pass
    
    def post(self, request):
        pass
    
    def put(self, request, pk):
        pass
    
    def delete(self, request, pk):
        pass
