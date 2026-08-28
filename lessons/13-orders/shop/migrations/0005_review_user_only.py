# Lesson 11 - Authorization / ownership of reviews

# Учебный момент: старые отзывы хранили author_name (текст), но не user (FK).
# Django не может автоматически понять, какому User принадлежит author_name="Roman".
# Поэтому перед тем как сделать user обязательным, мы удаляем демо-отзывы без user.
# В реальном проекте разработчик пишет data migration: сопоставить author_name с User
# или назначить отзывы вручную.

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def remove_reviews_without_user(apps, schema_editor):
    Review = apps.get_model('shop', 'Review')
    Review.objects.filter(user__isnull=True).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_profile'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(remove_reviews_without_user),
        migrations.RemoveField(
            model_name='review',
            name='author_name',
        ),
        migrations.AlterField(
            model_name='review',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='reviews',
                to=settings.AUTH_USER_MODEL,
                verbose_name='пользователь',
            ),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.PositiveSmallIntegerField(
                validators=[
                    django.core.validators.MinValueValidator(
                        1,
                        message='Оценка не может быть меньше 1.',
                    ),
                    django.core.validators.MaxValueValidator(
                        5,
                        message='Оценка не может быть больше 5.',
                    ),
                ],
                verbose_name='оценка',
            ),
        ),
    ]
