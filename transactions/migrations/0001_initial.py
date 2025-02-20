
import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[

                ('transaction_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('order_id', models.UUIDField()),
                ('merchant_id', models.UUIDField()),
                ('gateway_name', models.CharField(max_length=50)),
                ('gateway_transaction_identifier', models.CharField(max_length=50)),
                ('payment_channel', models.CharField(max_length=50)),
                ('amount', models.DecimalField(decimal_places=4, max_digits=19)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('successful', 'Successful'), ('failed', 'Failed')], max_length=10)),
                ('currency', models.CharField(default='NGN', max_length=50)),

                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'transactions',
            },
        ),
    ]
