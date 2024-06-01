from django.http import JsonResponse

def default(request)->JsonResponse:
    return JsonResponse({"message": "Not authenticated"})