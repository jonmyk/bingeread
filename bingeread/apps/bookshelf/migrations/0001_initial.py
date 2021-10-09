# Generated by Django 3.1.6 on 2021-05-03 14:05

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BookMeta',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('selfLink', models.URLField()),
                ('volumeInfo', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='ListMeta',
            fields=[
                ('lid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(1)])),
                ('private', models.BooleanField(default=True)),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ListEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid', models.CharField(max_length=20, null=True)),
                ('lid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookshelf.listmeta')),
            ],
        ),
        migrations.AddConstraint(
            model_name='listmeta',
            constraint=models.UniqueConstraint(fields=('uid', 'name'), name='unique_list_name'),
        ),
        migrations.AddConstraint(
            model_name='listentry',
            constraint=models.UniqueConstraint(fields=('lid', 'bid'), name='unique_book_entry'),
        ),
    ]
