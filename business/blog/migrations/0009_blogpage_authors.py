# Generated by Django 4.2.4 on 2023-08-14 09:37

from django.db import migrations
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpage',
            name='authors',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, to='blog.author'),
        ),
    ]
