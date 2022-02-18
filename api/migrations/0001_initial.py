# Generated by Django 3.2.12 on 2022-02-18 13:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('thread_id', models.PositiveBigIntegerField(help_text='The id of this thread.', primary_key=True, serialize=False)),
                ('time_opened', models.DateTimeField(editable=False, help_text='When the thread was opened.')),
                ('time_closed', models.DateTimeField(blank=True, help_text='When the thread was closed.', null=True)),
                ('closed_by', models.PositiveBigIntegerField(blank=True, db_index=True, help_text='The id of the person who closed this thread.', null=True)),
                ('opened_by', models.PositiveBigIntegerField(db_index=True, help_text='The id of the person who opened this thread.')),
                ('topic', models.TextField(blank=True, default='', help_text='The topic for this thread.')),
            ],
            options={
                'ordering': ('time_opened',),
            },
        ),
        migrations.CreateModel(
            name='ThreadMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_id', models.PositiveBigIntegerField(db_index=True, help_text='The id for the author of this message.')),
                ('time_sent', models.DateTimeField(help_text='When was this model sent?')),
                ('is_helper', models.BooleanField(default=False, help_text='Was the author a helper when they sent this message?')),
                ('thread', models.ForeignKey(help_text='The thread to attach this to.', on_delete=django.db.models.deletion.CASCADE, to='api.thread')),
            ],
            options={
                'verbose_name': 'Thread Message',
                'verbose_name_plural': 'Thread Messages',
                'ordering': ('time_sent',),
            },
        ),
    ]