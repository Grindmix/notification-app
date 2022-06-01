from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from notify.models import Notification
from notify.serializer import NotificationSerializer

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@csrf_exempt
def notification_list(request):

    if request.method == 'GET':
        notifications = Notification.objects.all()
        serializer = NotificationSerializer(notifications, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = NotificationSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)

        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def notification_detail(request, pk):
    
    try:
        notification = Notification.objects.get(pk=pk)
    except Notification.DoesNotExist:
        return HttpResponse(status=404)
    
    if request.method == 'GET':
        serializer = NotificationSerializer(notification)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = NotificationSerializer(notification, data=data)
        
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        notification.delete()
        return JsonResponse({'message': 'deleted'}, status=200)


@csrf_exempt
def notification_send(request, pk):

    channel_layer = get_channel_layer()

    try:
        notification = Notification.objects.get(pk=pk)
    except Notification.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'POST':
        serializer = NotificationSerializer(notification)
        async_to_sync(channel_layer.group_send)('notification', {
            'type': 'notify',
            'content': serializer.data,
        })
        return HttpResponse(status=200)
    return HttpResponse(status=405)