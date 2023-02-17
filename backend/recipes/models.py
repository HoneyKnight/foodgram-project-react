from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название тега',
        max_length=100,
        unique=True
    )
    color = models.CharField(
        verbose_name='Цвет тега',
        max_length=10,
        unique=True
    )
    slug = models.SlugField(
        verbose_name='Ссылка на тег',
        max_length=100,
        unique=True
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['id']

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название ингредиента',
        max_length=100
    )
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        max_length=100
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name']

    def __str__(self) -> str:
        return f'{self.name}, {self.measurement_unit}'


class IngredientAmount(models.Model):
    recipe = models.ForeignKey(
        'Recipe',
        verbose_name='Рецепт',
        related_name='recipes',
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        related_name='ingredients',
        on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='Количество',
        validators=[
            MinValueValidator(1, 'Добавьте хотя бы 1 ингредиент')
        ]
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredient'
            )
        ]

    def __str__(self) -> str:
        return f'{self.ingredient.name} - {self.amount}'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        related_name='recipes',
        on_delete=models.CASCADE
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        related_name='recipes'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through=IngredientAmount,
        verbose_name='Ингредиенты',
        related_name='recipes'
    )
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=100
    )
    image = models.ImageField(
        verbose_name='Картинка рецепта',
        upload_to='recipes/images/'
    )
    text = models.TextField(
        verbose_name='Описание',
        max_length=500
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления рецепта',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='favorites',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        related_name='favorites',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite'),
        ]

    def __str__(self) -> str:
        return f'{self.user} - {self.recipe.name}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='cart',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        related_name='cart',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_cart_recipe'
            )
        ]

    def __str__(self) -> str:
        return f'{self.author}, {self.recipe}'
