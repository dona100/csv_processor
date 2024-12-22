import csv
import json
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from .models import User
from .serializers import UserSerializer


class CSVUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if not file:
            return JsonResponse({'error': 'No file uploaded.'}, status=400)

        if not file.name.endswith('.csv'):
            return JsonResponse({'error': 'Invalid file type. Only .csv files are accepted.'}, status=400)

        decoded_file = file.read().decode('utf-8')
        csv_reader = csv.DictReader(decoded_file.splitlines())

        success_count = 0
        failure_count = 0
        errors = []

        for row in csv_reader:
            serializer = UserSerializer(data=row)
            if serializer.is_valid():
                try:
                    serializer.save()
                    success_count += 1
                except Exception as e:
                    failure_count += 1
                    errors.append({'row': row, 'error': str(e)})
            else:
                failure_count += 1
                errors.append({'row': row, 'errors': serializer.errors})

        response_data = {
            'records_saved': success_count,
            'records_rejected': failure_count,
            'errors': errors,
        }

        
        with open('response_output.json', 'w', encoding='utf-8') as json_file:
            json.dump(response_data, json_file, ensure_ascii=False, indent=4)

        return JsonResponse({'message': 'CSV processed. Check response_output.json for details.'})


# import csv
# from django.http import JsonResponse
# from rest_framework.views import APIView
# from rest_framework.parsers import MultiPartParser
# from .models import User
# from .serializers import UserSerializer


# class CSVUploadView(APIView):
#     def get(self, request, *args, **kwargs):
#         users = User.objects.all()  # Retrieve all users from the database
#         serializer = UserSerializer(users, many=True)  # Serialize the queryset
#         return JsonResponse(serializer.data, safe=False)  # Return data in JSON format
    
#     parser_classes = [MultiPartParser]

#     def post(self, request, *args, **kwargs):
#         print("Request Content-Type:", request.content_type)
#         print("FILES:", request.FILES)
#         file = request.FILES.get('file')
#         if not file:
#             return JsonResponse({'error': 'No file uploaded.'}, status=400)

#     # Debugging: Log the file name and content type
#         print(f"Uploaded file: {file.name}, Content Type: {file.content_type}")

#         if not file.name.endswith('.csv'):
#             return JsonResponse({'error': 'Invalid file type. Only .csv files are accepted.'}, status=400)
#         # if not file or not file.name.endswith('.csv'):
#         #     return JsonResponse({'error': 'Invalid file type. Only .csv files are accepted.'}, status=400)
        
#         decoded_file = file.read().decode('utf-8')
#         csv_reader = csv.DictReader(decoded_file.splitlines())

#         success_count = 0
#         failure_count = 0
#         errors = []

#         for row in csv_reader:
#             serializer = UserSerializer(data=row)
#             if serializer.is_valid():
#                 try:
#                     serializer.save()
#                     success_count += 1
#                 except Exception as e:
#                     failure_count += 1
#                     errors.append({'row': row, 'error': str(e)})
#             else:
#                 failure_count += 1
#                 errors.append({'row': row, 'errors': serializer.errors})

#         response_data = {
#             'records_saved': success_count,
#             'records_rejected': failure_count,
#             'errors': errors,
#         }
#         return JsonResponse(response_data)

