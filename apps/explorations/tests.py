from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.projects.models import Project
from apps.explorations.models import ExplorationRun, FeatureItem

User = get_user_model()

class ExplorationSmokeTest(APITestCase):
    def setUp(self):
        # Create user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # Create a test project
        self.project = Project.objects.create(name="Test Project", description="Smoke Test Project", owner=self.user)
        # Authenticate
        self.client.force_authenticate(user=self.user)

    def test_exploration_apis(self):
        """
        冒烟测试：测试探索创建、探索列表、功能点列表 API
        """
        # 1. 探索创建 (Create Exploration)
        url_create = '/api/explorations/runs/'
        data_create = {
            'project': self.project.id,
            'base_url': 'http://example.com',
            'auth_type': 'none',
            'max_steps': 5
        }
        response_create = self.client.post(url_create, data_create, format='json')
        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED, 
                         f"Failed to create exploration run: {response_create.data}")
        
        run_id = response_create.data.get('id')
        self.assertIsNotNone(run_id)

        # 2. 探索列表 (List Explorations)
        url_list = '/api/explorations/runs/'
        response_list = self.client.get(url_list)
        self.assertEqual(response_list.status_code, status.HTTP_200_OK)
        # Ensure our created run is in the list
        run_ids = [run['id'] for run in response_list.data['results']] if 'results' in response_list.data else [run['id'] for run in response_list.data]
        self.assertIn(run_id, run_ids)

        # 3. 创建功能点 (Create Feature Item to test Feature List)
        # Assuming we can create feature item via API or ORM. 
        # Feature list usually filters by run. Let's create via ORM for smoke testing the GET API.
        FeatureItem.objects.create(
            run_id=run_id,
            name="Login Button",
            description="A button to login",
            url="http://example.com/login"
        )

        # 4. 功能点列表 (List Feature Items)
        url_features = f'/api/explorations/features/?run={run_id}'
        response_features = self.client.get(url_features)
        self.assertEqual(response_features.status_code, status.HTTP_200_OK)
        features_data = response_features.data['results'] if 'results' in response_features.data else response_features.data
        self.assertTrue(len(features_data) > 0)
        self.assertEqual(features_data[0]['name'], "Login Button")
