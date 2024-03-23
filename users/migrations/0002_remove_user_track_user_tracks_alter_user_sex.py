# Generated by Django 5.0.2 on 2024-03-23 12:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
        ("web", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="track",
        ),
        migrations.AddField(
            model_name="user",
            name="tracks",
            field=models.ManyToManyField(to="web.track", verbose_name="Треки"),
        ),
        migrations.AlterField(
            model_name="user",
            name="sex",
            field=models.CharField(
                choices=[("M", "Мужской"), ("F", "Женский"), ("", "Не указано")],
                max_length=1,
                verbose_name="Пол",
            ),
        ),
    ]