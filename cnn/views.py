from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .cnn_model import predictDamageScore
from django.http import HttpResponse

@csrf_exempt
def process_inspection(request):
    if request.method == 'POST':
        images = request.FILES.getlist('images')

        results = []
        for image_file in images:
            # Process each image


            # Append the result to the list
            results.append({
                'filename': image_file.name,
                # Include any other relevant information or processed results
            })

        return JsonResponse({'results': results})

        # Return an error if the request method is not POST
    return JsonResponse({'error': 'Invalid request method'})

@csrf_exempt
def getInsurerRecommendations(request):
    regNo = request # get registration number from request (client will be pmp-motor)
