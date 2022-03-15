from django.db.models import Avg
from django_filters import (CharFilter, FilterSet, ModelChoiceFilter,
                            NumberFilter)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.response import Response

from reviews.models import Category, Comment, Genre, Review, Title
from .permissions import IsAdminOrModerOrReadOnly, IsAdminOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleCreateSerializer, TitleSerializer)


class CreateListDeleteMixinSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    pass


class TitleFilter(FilterSet):
    genre = ModelChoiceFilter(
        field_name="genre",
        to_field_name='slug',
        queryset=Genre.objects.all()
    )
    category = ModelChoiceFilter(
        field_name="category",
        to_field_name='slug',
        queryset=Category.objects.all()
    )
    name = CharFilter(
        field_name="name",
        lookup_expr='icontains'
    )
    year = NumberFilter(
        field_name="year"
    )


class CategoryViewSet(CreateListDeleteMixinSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'


class GenreViewSet(CreateListDeleteMixinSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return TitleSerializer
        return TitleCreateSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrModerOrReadOnly,)

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs['pk']
        title_id = kwargs['title_id']
        get_object_or_404(Review, pk=pk, title_id=title_id)
        return super().retrieve(request, *args, **kwargs)

    def get_queryset(self):
        title_id = self.kwargs['title_id']
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs['title_id']
        title = get_object_or_404(Title, pk=title_id)
        return serializer.save(
            author=self.request.user,
            title=title
        )

    def get_serializer_context(self):
        context = super(ReviewViewSet, self).get_serializer_context()
        context["title_id"] = self.kwargs["title_id"]
        context["author"] = self.request.user
        return context


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrModerOrReadOnly,)

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs['pk']
        review_id = kwargs['review_id']
        get_object_or_404(Comment, pk=pk, review_id=review_id)
        return super().retrieve(request, *args, **kwargs)

    def get_queryset(self):
        title_id = self.kwargs['title_id']
        review_id = self.kwargs['review_id']
        review = get_object_or_404(
            Review,
            pk=review_id,
            title_id=title_id)
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs['title_id']
        review_id = self.kwargs['review_id']
        review = get_object_or_404(
            Review,
            pk=review_id,
            title_id=title_id)
        return serializer.save(
            author=self.request.user,
            review=review
        )

    def partial_update(self, request, *args, **kwargs):
        pk = kwargs['pk']
        review_id = kwargs['review_id']
        review = get_object_or_404(
            Comment,
            pk=pk,
            review_id=review_id)
        serializer = CommentSerializer(review,
                                       data=request.data,
                                       partial=False)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors)
        return super().partial_update(request, *args, **kwargs)
