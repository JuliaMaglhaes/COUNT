from counteye.models import Count
from rest_framework import serializers

class CountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Count
        fields = ('id', 'product', 'description','author', 'amount', 'category', 'status', 'counted')