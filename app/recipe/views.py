from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework import (
    viewsets,
    mixins,
    status,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    Ingredient,
    Recipe,
    Tag,
)
from recipe import serializers


class BaseRecipeAttributeViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin
):
    """Base ViewSet for user owned recipe attributes"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        Overriding the `get_queryset` default method
        Return objects for the current authenticated user only
        """
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
        queryset = self.queryset

        if assigned_only:
            queryset = queryset.filter(recipe__isnull=False)

        return queryset.filter(
            user=self.request.user
        ).order_by('-name').distinct()  # we make sure that the objects we return are unique # noqa: E501

    def perform_create(self, serializer):
        """Overriding `perform_create` method"""
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttributeViewSet):
    """Manage tags in the database"""
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(BaseRecipeAttributeViewSet):
    """Manage ingredients in the database"""
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in the database"""
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def _params_to_ints(self, query_string: str) -> [int]:
        """Convert a list of string IDs to a list of int"""
        return [int(str_id) for str_id in query_string.split(',')]

    def get_queryset(self):
        """
        Overriding the `get_queryset` default method
        Return objects for the current authenticated user only
        """
        tags = self.request.query_params.get('tags')
        ingredients = self.request.query_params.get('ingredients')

        queryset = self.queryset

        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)  # django syntax for filtering on foreign key objects # noqa: E501

        if ingredients:
            ingredient_ids = self._params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredient_ids)

        return queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """
        Overriding serializer class
        Return appropriate serializer class
        """
        if self.action == 'retrieve':
            #  we check if the action is a get detail ``retrieve`
            return serializers.RecipeDetailSerializer
        elif self.action == 'upload_image':
            # if the action is our custom action to upload images
            return serializers.RecipeImageSerializer

        return serializers.RecipeSerializer

    def perform_create(self, serializer):
        """Overriding `perform_create` method"""
        serializer.save(user=self.request.user)

    # we use the `@action` decorator to use a custom action in the ViewSet
    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to a recipe"""
        recipe = self.get_object()  # gets the object that is being accessed based on the id on the url (pk) # noqa: E501

        serializer = self.get_serializer(
            recipe,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )
