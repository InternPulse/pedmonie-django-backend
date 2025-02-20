import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentGateway',
            fields=[
                ('sn', models.CharField(blank=True, db_index=True, max_length=50, unique=True, verbose_name='Serial Number')),
                ('gateway_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('gateway_name', models.CharField(max_length=100, unique=True)),
                ('gateway_logo', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=False)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'paymentgateways',
            },
        ),
        migrations.CreateModel(
            name='MerchantPaymentGateway',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('payment_gateways', models.JSONField(default=dict)),
                ('merchant_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='merchant_gateways', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'merchant_payment_gateway',
            },
        ),
    ]
