# Generated by Django 4.2 on 2023-05-19 09:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Organism",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("taxa_id", models.IntegerField(null=True)),
                ("clade", models.CharField(max_length=100)),
                ("genus", models.CharField(max_length=100)),
                ("species", models.CharField(max_length=100)),
            ],
            options={
                "unique_together": {("taxa_id", "clade", "genus", "species")},
            },
        ),
        migrations.CreateModel(
            name="Pfam",
            fields=[
                (
                    "domain_id",
                    models.CharField(max_length=50, primary_key=True, serialize=False),
                ),
                ("domain_description", models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="Protein",
            fields=[
                (
                    "protein_id",
                    models.CharField(max_length=50, primary_key=True, serialize=False),
                ),
                ("sequence", models.TextField()),
                ("length", models.IntegerField(default=0)),
                ("id_custom", models.IntegerField(blank=True, null=True)),
                (
                    "organism",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="proteins",
                        to="bioscience_app.organism",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Domain",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("domain_description", models.CharField(max_length=200)),
                (
                    "pfam",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bioscience_app.pfam",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DomainAssignment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start", models.IntegerField()),
                ("end", models.IntegerField()),
                (
                    "domain",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="domain_assignments",
                        to="bioscience_app.domain",
                    ),
                ),
                (
                    "protein",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="domain_assignments",
                        to="bioscience_app.protein",
                    ),
                ),
            ],
            options={
                "unique_together": {("protein", "domain", "start", "end")},
            },
        ),
    ]