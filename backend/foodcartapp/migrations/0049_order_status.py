# Generated by Django 3.2.15 on 2023-07-18 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0048_auto_20230715_2201'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('incoming', 'Необработанный'), ('in_progress', 'Принят в обработку'), ('delivery', 'Передан курьеру'), ('complete', 'Выполнен')], db_index=True, default='incoming', max_length=30, verbose_name='Статус'),
            preserve_default=False,
        ),
    ]