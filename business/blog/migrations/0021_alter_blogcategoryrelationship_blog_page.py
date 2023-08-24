# Generated by Django 4.2.4 on 2023-08-24 09:42

from django.db import migrations
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0020_alter_highlightpage_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogcategoryrelationship',
            name='blog_page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_pages', to='blog.blogpage'),
        ),
    ]
