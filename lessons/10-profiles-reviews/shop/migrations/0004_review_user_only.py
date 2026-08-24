# Generated manually for Lesson 10

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def clear_demo_reviews(apps, schema_editor):
    Review = apps.get_model('shop', 'Review')
    Review.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_alter_category_options_alter_product_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(clear_demo_reviews, migrations.RunPython.noop),
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
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(5),
                ],
                verbose_name='оценка',
            ),
        ),
    ]
