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

    def validate(self, data):
        if not data.get('base_url'):
            raise serializers.ValidationError({"base_url": "探索起始 URL (base_url) 不能为空。"})
        
        if data.get('max_steps') is None:
            data['max_steps'] = 10
            
        if not data.get('auth_type'):
            data['auth_type'] = 'none'
            
        return data

