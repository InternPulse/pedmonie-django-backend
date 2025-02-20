# Generated by Django 5.1.4 on 2025-02-20 21:37

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Merchant',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('merchant_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(blank=True, max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('business_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(max_length=15)),
                ('is_email_verified', models.BooleanField(default=False)),
                ('role', models.CharField(choices=[('merchant', 'Merchant'), ('superadmin', 'Super Admin')], default='merchant', max_length=20)),
                ('total_balance', models.DecimalField(decimal_places=4, default=0.0, max_digits=19)),
                ('is_staff', models.BooleanField(default=False)),
                ('nin', models.CharField(blank=True, max_length=30, null=True, unique=True)),
                ('is_nin_verified', models.BooleanField(default=False)),
                ('bvn', models.CharField(blank=True, max_length=30, null=True, unique=True)),
                ('is_bvn_verified', models.BooleanField(default=False)),
                ('cac_number', models.CharField(blank=True, max_length=30, null=True, unique=True)),
                ('is_business_cac_verified', models.BooleanField(default=False)),
                ('id_card', models.ImageField(blank=True, null=True, upload_to='id_cards/')),
                ('passport', models.ImageField(blank=True, null=True, upload_to='passports/')),
                ('is_kyc_verified', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'permissions': [('manage_balance', 'Can manage merchant balance'), ('verify_kyc', 'Can verify merchant KYC details'), ('manage_orders', 'Can manage merchant orders'), ('manage_wallets', 'Can manage merchant wallets'), ('manage_transactions', 'Can manage merchant transactions'), ('manage_merchants', 'Can manage other merchants')],
                'default_related_name': 'merchants',
            },
        ),
    ]
