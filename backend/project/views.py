from django.http import JsonResponse

def home(request)->JsonResponse:
    return JsonResponse(data={"message": "Hello, World!"})