from datetime import date

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


class Category(models.Model):
    """Категории (типы) произведений."""
    name = models.CharField(
        max_length=10,
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Уникальный идентификатор категории'
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Жанры произведений."""
    name = models.CharField(
        max_length=10,
        verbose_name='Название жанра'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Уникальный идентификатор жанра'
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведение, к которому пишут отзывы."""
    name = models.CharField(
        max_length=200,
        blank=False,
        verbose_name='Название произведения'
    )
    year = models.PositiveIntegerField(
        db_index=True,
        validators=[MaxValueValidator(date.today().year)],
        verbose_name='Год создания'
    )
    description = models.TextField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='Описание'
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='category_of_title',
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='Жанр'
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Жанр'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Произведение'
    )

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    """"Отзывы к произведениям."""
    text = models.TextField(
        'Текст отзыва',
        help_text='Ваш отзыв тут. Обязательное поле.'
    )
    pub_date = models.DateTimeField(
        'Дата публикации отзыва',
        auto_now_add=True,
        db_index=True
    )
    score = models.PositiveSmallIntegerField(
        'Оценка',
        help_text='Ваша оценка произведению (1-10) Обязательное поле.',
        validators=[MinValueValidator(0),
                    MaxValueValidator(10)]
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение, на которое отзыв'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ["-pub_date"]
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='author has only one review'
            )]

    def __str__(self):
        return self.text[:50]


class Comment(models.Model):
    """"Комментарии к отзывам."""
    text = models.TextField(
        'Текст комментария',
        help_text='Ваш коммент тут. Обязательное поле.'
    )
    pub_date = models.DateTimeField(
        'Дата публикации комментария',
        auto_now_add=True,
        db_index=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Произведение, к которому комментарий'
    )

    class Meta:
        verbose_name = 'Комментарий к отзыву'
        verbose_name_plural = 'Комментарии к отзывам'
        ordering = ["-pub_date"]

    def __str__(self):
        return self.text[:50]
