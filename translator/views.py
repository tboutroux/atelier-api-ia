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

    if not api_key:
        raise EnvironmentError("Google API Key not found in environment variables")

    match language.lower():

        case "es":
            lang_prompt = "en espagnol"

        case "en":
            lang_prompt = "en anglais"

        case "it":
            lang_prompt = "en italien"

        case "fr":
            lang_prompt = "en français"

        case _:
            raise ValueError(f"Language {language} not supported")

    prompt = f"""
        Traduis "{prompt}" {lang_prompt} et renvoie uniquement la traduction.
    """

    model = genai.GenerativeModel("gemini-1.5-flash")

    try:
        response = model.generate_content(prompt)
    except Exception as e:
        raise RuntimeError(f"An error occurred: {e}")
    
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
    
    @swagger_auto_schema(request_body=TranslationSerializer, responses={200: TranslationSerializer, 400: "Missing parameters", 500: "An error occurred during translation"})
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
        
        print(f"source_language: {source_language}")
        print(f"target_language: {target_language}")
        print(f"source_text: {source_text}")

        if not all([source_language, target_language, source_text]):
            return Response(
                data={"Response": "Missing parameters"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if target_language not in ["ES", "EN", "IT", "FR"]:
            return Response(
                data={"Response": "Invalid target language. Supported: ES, EN, IT, FR"},
                status=status.HTTP_400_BAD_REQUEST
            )


        try:
            target_text = translator(source_text, target_language)

            if "\n" in target_text:
                target_text = target_text.split("\n")[0]

        except ValueError as ve:
            return Response(
                data={"Response": str(ve)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                data={"Response": f"An error occurred during translation: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        object_exist = Translation.objects.filter(
            source_language=source_language,
            target_language=target_language,
            source_text=source_text
        ).exists()

        response = {
            "Response": "Translation created" if not object_exist else "Translation already exists",
            "translation": {
                "source_language": source_language,
                "target_language": target_language,
                "source_text": source_text,
                "target_text": target_text
            }
        }

        if not object_exist:
            Translation.objects.create(
                source_language=source_language,
                target_language=target_language,
                source_text=source_text,
                target_text=target_text
            )
            return Response(data=response, status=status.HTTP_201_CREATED)
        else:
            return Response(data=response, status=status.HTTP_200_OK)

def index(request):
    return render(request, 'index.html', context={})