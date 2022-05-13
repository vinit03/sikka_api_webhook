# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


@csrf_exempt
@require_http_methods(["POST"])
def AppointmentUpdateWebhookView(request):
    if request.method == 'POST':
        print(request.body)
        print("Data received from Webhook is: ", request.body)
        return HttpResponse("Webhook received!")
