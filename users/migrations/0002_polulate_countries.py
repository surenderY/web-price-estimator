from django.db import migrations


def load_countries(apps, schema_editor):
    Country = apps.get_model('users', 'Country')
    countries = [
        ("Australia", "AU"),
        ("Belgium", "BE"),
        ("Brazil", "BR"),
        ("Canada", "CA"),
        ("Finland", "FI"),
        ("France", "FR"),
        ("Germany", "DE"),
        ("India", "IN"),
        ("Indonesia", "ID"),
        ("Israel", "IL"),
        ("Italy", "IT"),
        ("Japan", "JP"),
        ("Luxembourg", "LU"),
        ("Malaysia", "MY"),
        ("Netherlands", "NL"),
        ("Norway", "NO"),
        ("Philippines", "PH"),
        ("Poland", "PL"),
        ("Saudi Arabia", "SA"),
        ("Singapore", "SG"),
        ("Spain", "ES"),
        ("Sweden", "SE"),
        ("Thailand", "TH"),
        ("United Arab Emirates", "AE"),
        ("United Kingdom", "UK"),
        ("United States of America", "US"),
    ]

    for name, code in countries:
        Country.objects.update_or_create(code=code, defaults={'name': name})


def unload_countries(apps, schema_editor):
    Country = apps.get_model('users', 'Country')
    Country.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_countries, reverse_code=unload_countries),
    ]