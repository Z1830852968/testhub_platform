from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ExplorationRun, FeatureItem, ExplorationArtifact
from .serializers import ExplorationRunSerializer, FeatureItemSerializer, ExplorationArtifactSerializer
from .tasks import run_system_exploration, stop_system_exploration

class ExplorationRunViewSet(viewsets.ModelViewSet):
    queryset = ExplorationRun.objects.all()
    serializer_class = ExplorationRunSerializer

    def get_queryset(self):
        project_id = self.request.query_params.get('project')
        if project_id:
            return self.queryset.filter(project_id=project_id)
        return self.queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        run_id = serializer.instance.id
        # Trigger Celery task
        run_system_exploration.delay(run_id)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['post'])
    def stop(self, request, pk=None):
        run = self.get_object()
        if run.status in ['pending', 'running']:
            # Set signal to stop
            stop_system_exploration(run.id)
            run.status = 'stopped'
            run.save()
            return Response({'status': 'stop signal sent'})
        return Response({'error': 'Run is not active'}, status=status.HTTP_400_BAD_REQUEST)

class FeatureItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FeatureItem.objects.all()
    serializer_class = FeatureItemSerializer

    def get_queryset(self):
        run_id = self.request.query_params.get('run')
        if run_id:
            return self.queryset.filter(run_id=run_id)
        return self.queryset

class ExplorationArtifactViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ExplorationArtifact.objects.all()
    serializer_class = ExplorationArtifactSerializer
