# Generated by Django 3.2.12 on 2022-02-27 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20220223_0401'),
    ]

    operations = [
        migrations.CreateModel(
            name='InitThread',
            fields=[
                ('thread_id', models.PositiveBigIntegerField(primary_key=True, serialize=False)),
                ('help_type', models.TextField(help_text='The help type based on the button pressed.')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]