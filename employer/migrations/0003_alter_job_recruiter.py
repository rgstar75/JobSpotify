# Generated by Django 3.2.4 on 2021-06-13 20:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recruiter', '0002_applicants_selectedapplicants'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='recruiter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to=settings.AUTH_USER_MODEL),
        ),
    ]
