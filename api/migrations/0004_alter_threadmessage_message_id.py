# Generated by Django 3.2.12 on 2022-02-18 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0003_threadmessage_message_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="threadmessage",
            name="message_id",
            field=models.PositiveBigIntegerField(
                db_index=True, help_text="The message id.", unique=True
            ),
        ),
    ]
