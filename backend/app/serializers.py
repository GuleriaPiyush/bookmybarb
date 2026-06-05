from rest_framework import serializers
from .models import Service,TemplateSlot,ScheduleTemplate,Slot


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
