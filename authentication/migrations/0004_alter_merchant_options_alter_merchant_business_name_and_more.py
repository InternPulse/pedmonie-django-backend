# Generated by Django 5.1.4 on 2025-02-15 12:22

import django.core.validators
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_remove_merchant_password_hash_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='merchant',
            options={'default_related_name': 'merchants', 'permissions': [('manage_balance', 'Can manage merchant balance'), ('verify_kyc', 'Can verify merchant KYC details'), ('manage_orders', 'Can manage merchant orders'), ('manage_wallets', 'Can manage merchant wallets'), ('manage_transactions', 'Can manage merchant transactions'), ('manage_merchants', 'Can manage other merchants')]},
        ),
        migrations.AlterField(
            model_name='merchant',
            name='business_name',
            field=models.CharField(max_length=50, validators=[django.core.validators.MinLengthValidator(2)]),
        ),
        migrations.AlterField(
            model_name='merchant',
            name='bvn',
            field=models.CharField(blank=True, help_text='(Bank Verification Number)', max_length=30, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='merchant',
            name='cac_number',
            field=models.CharField(blank=True, help_text='(Corporate Affairs Commission)', max_length=30, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='merchant',
            name='email',
            field=models.EmailField(max_length=50, unique=True, validators=[django.core.validators.EmailValidator()]),
        ),
        migrations.AlterField(
            model_name='merchant',
            name='first_name',
            field=models.CharField(default='', max_length=50, validators=[django.core.validators.MinLengthValidator(2)]),
        ),
        migrations.AlterField(
            model_name='merchant',
            name='last_name',
            field=models.CharField(max_length=50, validators=[django.core.validators.MinLengthValidator(2)]),
        ),
        migrations.AlterField(
            model_name='merchant',
            name='merchant_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='merchant',
            name='middle_name',
            field=models.CharField(blank=True, help_text='(Optional)', max_length=50),
        ),
    ]
