from django.shortcuts import render
from django.contrib.auth.models import User
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
        if slots_to_create:
            Slot.objects.bulk_create(slots_to_create)
            
    return Response({"message": "Template assigned and slots generated successfully!"})


@api_view(['POST'])
def create_booking(request):
    service_id = request.data.get('service_id')
    date_str = request.data.get('date')
    start_time_str = request.data.get('start_time')
    customer_id = request.data.get('customer_id')
    customer_name = request.data.get('customer_name')

    if not all([service_id, date_str, start_time_str]):
        return Response({"error": "service_id, date, and start_time are required."}, status=400)

    try:
        service = Service.objects.get(id=service_id)
    except Service.DoesNotExist:
        return Response({"error": "Service not found."}, status=404)

    # Resolve customer dynamically
    if customer_name:
        customer, created = User.objects.get_or_create(username=customer_name)
    elif customer_id:
        customer = User.objects.filter(id=customer_id).first()
    else:
        customer = User.objects.first()

    if not customer:
        customer = User.objects.create_user(username='guest', password='password123')

    # Get the consecutive slots required for this service
    required_slots = service.required_slot
    all_slots = list(Slot.objects.filter(date=date_str).order_by('start_time'))

    try:
        start_slot = Slot.objects.get(date=date_str, start_time=start_time_str)
        start_idx = all_slots.index(start_slot)
    except (Slot.DoesNotExist, ValueError):
        return Response({"error": "Starting slot not found."}, status=404)

    # Check if there are enough slots ahead
    if start_idx + required_slots > len(all_slots):
        return Response({"error": "Not enough consecutive slots available."}, status=400)

    slots_to_book = all_slots[start_idx : start_idx + required_slots]

    # Validate that none of the slots are already booked
    for slot in slots_to_book:
        if slot.is_booked:
            return Response({"error": "One or more slots are already booked."}, status=400)

    # Create the Booking
    booking = Booking.objects.create(
        customer=customer,
        service=service,
        status='PENDING'
    )
    booking.slots.set(slots_to_book)

    # Block the slots immediately so other customers don't double-book
    for slot in slots_to_book:
        slot.is_booked = True
        slot.save()

    serializer = BookingSerializer(booking)
    return Response(serializer.data, status=201)


@api_view(['GET'])
def list_bookings(request):
    bookings = Booking.objects.all().order_by('-created_at')
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def update_booking_status(request, booking_id):
    action = request.data.get('action') # "confirm" or "reject"
    
    try:
        booking = Booking.objects.get(id=booking_id)
    except Booking.DoesNotExist:
        return Response({"error": "Booking not found."}, status=404)

    if action == "confirm":
        booking.status = "CONFIRMED"
        booking.save()
        
    elif action == "reject":
        booking.status = "REJECTED"
        booking.save()
        # Release the slots back to being available
        for slot in booking.slots.all():
            slot.is_booked = False
            slot.save()
            
    else:
        return Response({"error": "Invalid action. Use 'confirm' or 'reject'."}, status=400)

    serializer = BookingSerializer(booking)
    return Response(serializer.data)


@api_view(['GET'])
def available_slots(request):
    date_str = request.query_params.get('date')
    required_slots_str = request.query_params.get('required_slots', '1')

    if not date_str:
        return Response({"error": "date parameter is required."}, status=400)

    try:
        required_slots = int(required_slots_str)
        if required_slots < 1:
            raise ValueError()
    except ValueError:
        return Response({"error": "required_slots must be a positive integer."}, status=400)

    slots = list(Slot.objects.filter(date=date_str).order_by('start_time'))

    if required_slots == 1:
        available = [s for s in slots if not s.is_booked]
        serializer = SlotSerializer(available, many=True)
        return Response(serializer.data)

    available_start_slots = []
    n = len(slots)
    
    for i in range(n - required_slots + 1):
        window = slots[i : i + required_slots]
        valid = True
        
        for j in range(required_slots):
            if window[j].is_booked:
                valid = False
                break
            if j > 0 and window[j].start_time != window[j-1].end_time:
                valid = False
                break
                
        if valid:
            available_start_slots.append(window[0])

    serializer = SlotSerializer(available_start_slots, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def list_templates(request):
    templates = ScheduleTemplate.objects.all()
    serializer = ScheduleTemplateSerializer(templates, many=True)
    return Response(serializer.data)






