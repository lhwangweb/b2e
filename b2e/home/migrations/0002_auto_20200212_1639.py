# Generated by Django 3.0.3 on 2020-02-12 16:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='urldata',
            options={'verbose_name': '縮址資料', 'verbose_name_plural': '縮址資料'},
        ),
        migrations.AlterModelOptions(
            name='urllog',
            options={'verbose_name': '縮址使用日誌', 'verbose_name_plural': '縮址使用日誌'},
        ),
        migrations.AlterField(
            model_name='urldata',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='建立時間'),
        ),
        migrations.AlterField(
            model_name='urldata',
            name='original_url',
            field=models.CharField(max_length=1023, verbose_name='原 Url'),
        ),
        migrations.AlterField(
            model_name='urldata',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='變更時間'),
        ),
        migrations.AlterField(
            model_name='urldata',
            name='url_hash',
            field=models.CharField(max_length=12, unique=True, verbose_name='Hash 碼'),
        ),
        migrations.AlterField(
            model_name='urllog',
            name='agent',
            field=models.CharField(max_length=1024, verbose_name='User Agent'),
        ),
        migrations.AlterField(
            model_name='urllog',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='建立時間'),
        ),
        migrations.AlterField(
            model_name='urllog',
            name='ip',
            field=models.CharField(max_length=130, verbose_name='IP'),
        ),
        migrations.AlterField(
            model_name='urllog',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='變更時間'),
        ),
        migrations.AlterField(
            model_name='urllog',
            name='urldata',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='url_items', to='home.Urldata', verbose_name='對應縮址'),
        ),
    ]