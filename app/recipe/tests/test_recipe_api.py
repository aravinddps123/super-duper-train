"""
Tests for recipe APIs.
"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe
from recipe.serializers import (
    RecipeSerializer,
    RecipeDetailSerializer,
)
RECIPIES_URL = reverse('recipe:recipe-list')


def detail_url(recipe_id):
    """Create and return a detail URL for a recipe"""
    # we need to pass in recipe_id that is why we have function
    return reverse('recipe:recipe-detail', args=(recipe_id,))


# create  a general recipe creation method for different testing
def create_recipe(user, **params):
    """Create and return a Sample Recipe"""
    defaults = {

        'title': 'Sample Recipe title',
        'time_minutes': 22,
        'price': Decimal('5.25'),
        'description': 'Sample Recipe description',
        'link': 'http://example.com/recipe.pdf',
    }

    defaults.update(params)

    recipe = Recipe.objects.create(user=user, **defaults)
    return recipe


class PublicRecipeAPITests(TestCase):
    """Test unauthenticate API requests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API"""
        res = self.client.get(RECIPIES_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase):
    """Test authenticated API requests"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrive_recipies(self):
        """Test retriving a list of recipies"""
        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPIES_URL)

        recipes = Recipe.objects.all().order_by('-id')

        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipe_list_limited_to_user(self):
        """Test list of recipes is limited to authenticated user"""
        other_user = get_user_model().objects.create_user(
            'other@example.com',
            'password123'
        )
        # here we are creating the other user
        # now we are going to create 2 recipe with other and authenticated user
        create_recipe(user=other_user)
        create_recipe(user=self.user)  # authenticated user

        res = self.client.get(RECIPIES_URL)
        # api response of authenticated user
        # db recipie of authenticated user
        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        # cheking if both are same

    def test_get_recipe_detail(self):
        """Test get recipe detail"""
        recipe = create_recipe(user=self.user)

        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)

    def test_create_recipe(self):
        """Test creating a recipe"""

        payload = {
            'title': 'Sample recipe',
            'time_minutes': 30,
            'price': Decimal('5.99'),
        }

        res = self.client.post(RECIPIES_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])

        # here we are comparing the payload with db data
        for k, v in payload.items():
            self.assertEqual(getattr(recipe, k), v)
        # checking if the recipe is created by current user
        self.assertEqual(recipe.user, self.user)
