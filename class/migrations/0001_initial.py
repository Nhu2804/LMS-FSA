# Generated by Django 5.1.1 on 2024-09-17 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClassInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_class', models.CharField(max_length=255, unique=True)),
                ('number_student', models.PositiveIntegerField()),
                ('class_mentor', models.CharField(max_length=255)),
            ],
        ),
    ]
