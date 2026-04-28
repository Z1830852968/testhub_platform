from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExplorationRunViewSet, FeatureItemViewSet, ExplorationArtifactViewSet

router = DefaultRouter()
router.register(r'runs', ExplorationRunViewSet, basename='exploration-run')
router.register(r'features', FeatureItemViewSet, basename='exploration-feature')
router.register(r'artifacts', ExplorationArtifactViewSet, basename='exploration-artifact')

urlpatterns = [
    path('', include(router.urls)),
]
