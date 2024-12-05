from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from translator.models import Translation
from translator.serializers import TranslationSerializer
import google.generativeai as genai
from drf_yasg.utils import swagger_auto_schema
import os
# Create your views here.

def translator(prompt: str, language: str) -> str:
    api_key = os.environ.get('GOOGLE_API_KEY') # To complete
    genai.configure(api_key=api_key)

    match language.lower():

        case "ES":
            lang_prompt = "en espagnol"

        case "EN":
            lang_prompt = "en anglais"

        case "IT":
            lang_prompt = "en italien"

        case _:
            raise ValueError("Language not supported")

    prompt = f"""
        Traduis "{prompt}" {lang_prompt} et renvoie uniquement la traduction.
    """

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text
        
class AllTranslation(APIView):
    
    def get(self, request):
        """
        Get all translations

        Returns:
            Response: The response with all translations
        """

        data = Translation.objects.all()

        serialized_data = TranslationSerializer(data, many=True)
        return Response(data={
            "Response": "All translations",
            "translations": serialized_data.data
        }, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(request_body=TranslationSerializer)
    def post(self, request):
        """
        Create a new translation
        
        Args:
            source_language (str): The source language
            target_language (str): The target language
            source_text (str): The source text
            target_text (str): The target text

        Returns:
            Response: The response with the new translation
        """

        # Paramètres simulés pour le test
        source_language = request.GET.get('source_language', None)
        target_language = request.GET.get('target_language', None)
        source_text = request.GET.get('source_text', None)
        target_text = translator(source_text, target_language)

        if not any([source_language, target_language, source_text]):
            return Response(data={"Response": "Missing parameters"}, status=status.HTTP_400_BAD_REQUEST)

        # Vérifier si la traduction existe déjà
        object_exist = Translation.objects.filter(
            source_language=source_language,
            target_language=target_language,
            source_text=source_text
        ).exists()  # Renvoie un booléen directement

        # Structure de réponse de base
        response = {
            "Response": "",
            "translation": {
                "source_language": source_language,
                "target_language": target_language,
                "source_text": source_text,
                "target_text": target_text
            }
        }

        if object_exist:
            response["Response"] = "Translation already exists"
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            # Créer la nouvelle traduction
            Translation.objects.create(
                source_language=source_language,
                target_language=target_language,
                source_text=source_text,
                target_text=target_text
            )
            response["Response"] = "Translation created"
            return Response(data=response, status=status.HTTP_201_CREATED)

def index(request):
    return render(request, 'index.html', context={})