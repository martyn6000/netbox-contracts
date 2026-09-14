from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netbox_contracts', '0003_currency_contractassignment_currency_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='currency',
            name='comments',
            field=models.TextField(blank=True),
        ),
    ]
