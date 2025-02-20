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
            name='AuditLog',
            fields=[
                ('log_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('sn', models.CharField(blank=True, db_index=True, max_length=50, unique=True, verbose_name='Serial Number')),
                ('action', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('admin', models.ForeignKey(limit_choices_to={'role': 'superadmin'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
