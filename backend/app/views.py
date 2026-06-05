from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal




@api_view(['GET','POST'])
def ServiceView(request):

    if request.method=='GET':
        services = Service.objects.filter(is_active=True)
        serializers = ServiceSerializer(services, many=True)

        return Response({
            "status": "success",
            "salon_name": "Barb Arena",
            "results": len(serializers.data),
            "data": serializers.data
        })

    elif request.method == 'POST':
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def ServiceCreate(reauest):
    serializer = ServiceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def assign_templates_to_dates(request):
    template_id = request.data.get('template_id')
    dates = request.data.get('dates')

    if not template_id or not dates:
        return Response ({"error": "template_id and dates are required."}, status=400)

    try:
        template = ScheduleTemplate.objects.get(id=template_id)
    except ScheduleTemplate.DoesNotExist:
        return Response ({"error": "Template not found."}, status=404)

    template_slots = template.slots.all()

    for date_str in dates:
        slots_to_create = []
        for temp_slot in template_slots:
            if not Slot.objects.filter(date=date_str, start_time=temp_slot.start_time).exists():
                slots_to_create.append(
                    Slot(
                        date=date_str,
                        start_time=temp_slot.start_time,
                        end_time=temp_slot.end_time,
                        is_booked=False
                    )
                )
            Slot.objects.bulk_create(slots_to_create)
        return Response({"message": "Template assigned and slots generated successfully!"})






