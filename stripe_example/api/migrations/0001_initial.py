
from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.RunSQL("""CREATE SCHEMA IF NOT EXISTS content""")
    ]
