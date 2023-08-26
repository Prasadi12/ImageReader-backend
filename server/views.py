from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import pytesseract
from PIL import Image, ImageEnhance

class ExtractTextView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        image = request.FILES.get('image')
        if image:
            image_path = default_storage.save(image.name, ContentFile(image.read()))
            img = Image.open(image_path)
            img = img.convert('L')  # Convert to grayscale
            img = ImageEnhance.Contrast(img).enhance(2.0)
            extracted_text = pytesseract.image_to_string(img, lang='eng', config='--psm 6')
            print(extracted_text)
            return Response({'text': extracted_text})
        else:
            return Response({'error': 'No image provided.'}, status=400)

