from rest_framework import serializers
from .models import Service,TemplateSlot,ScheduleTemplate,Slot,Booking


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class TemplateSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateSlot
        fields = '__all__'

class ScheduleTemplateSerializer(serializers.ModelSerializer):
    slots = TemplateSlotSerializer(many=True, read_only=True)
    class Meta:
        model = ScheduleTemplate
        fields = ['id', 'name', 'slots']

class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    slots = SlotSerializer(many=True, read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    customer_username = serializers.CharField(source='customer.username', read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'customer', 'customer_username', 'service', 'service_name', 'slots', 'status', 'created_at']
