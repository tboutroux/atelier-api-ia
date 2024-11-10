from django.shortcuts import render
from rest_framework import viewsets
#from django_filters import rest_framework as filters
from translator.models import Translation
from translator.serializers import TranslationSerializer

# Create your views here.

class TranslationViewSet(viewsets.ModelViewSet):
    queryset = Translation.objects.all()
    serializer_class = TranslationSerializer
