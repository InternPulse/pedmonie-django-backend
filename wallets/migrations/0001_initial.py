
# Generated by Django 5.1.4 on 2025-02-20 21:33

import django.db.models.deletion
import django.utils.timezone
import uuid
# Generated by Django 5.1.6 on 2025-02-17 17:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('wallet_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('sn', models.CharField(blank=True, db_index=True, max_length=50, unique=True, verbose_name='Serial Number')),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('currency', models.CharField(default='NGN', max_length=3)),
                ('createdAt', models.DateTimeField(default=django.utils.timezone.now)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('merchant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'wallets',
                'ordering': ['-createdAt'],
            },
        ),
        migrations.CreateModel(
            name='Withdrawal',
            fields=[
                ('withdrawal_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('sn', models.CharField(blank=True, db_index=True, max_length=50, unique=True, verbose_name='Serial Number')),
                ('amount', models.DecimalField(decimal_places=4, max_digits=19)),
                ('initial_balance', models.DecimalField(decimal_places=4, max_digits=19)),
                ('final_balance', models.DecimalField(decimal_places=4, max_digits=19)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('successful', 'Successful'), ('failed', 'Failed')], default='pending', max_length=20)),
                ('createdAt', models.DateTimeField(default=django.utils.timezone.now)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('merchant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'withdrawals',
                'ordering': ['-createdAt'],
            },
        ),
    ]
