# Generated manually (Django not installed) following the pattern of 0007

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('birds', '0007_bird_local_name_dogri_bird_local_name_kashmiri_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField()),
                ('subject', models.CharField(blank=True, max_length=200)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
