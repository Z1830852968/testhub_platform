from rest_framework import serializers
from .models import ExplorationRun, FeatureItem, ExplorationArtifact

class FeatureItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureItem
        fields = '__all__'

class ExplorationArtifactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExplorationArtifact
        fields = '__all__'

class ExplorationRunSerializer(serializers.ModelSerializer):
    features = FeatureItemSerializer(many=True, read_only=True)
    artifacts = ExplorationArtifactSerializer(many=True, read_only=True)
    
    class Meta:
        model = ExplorationRun
        fields = '__all__'
