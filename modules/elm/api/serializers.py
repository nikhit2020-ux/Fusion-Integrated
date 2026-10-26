from rest_framework import serializers
from modules.elm.models import LeaveApplication

class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveApplication
        fields = "__all__"