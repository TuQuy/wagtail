# Generated by Django 4.2.4 on 2023-08-27 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0023_learnsporttopicpage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
        migrations.DeleteModel(
            name='LearnSportTopicPage',
        ),
    ]
