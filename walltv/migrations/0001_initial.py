# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-21 22:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import embed_video.fields
import walltv.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageForCarouselPanel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_file', models.ImageField(upload_to='', verbose_name='Archivo de imagen')),
            ],
            options={
                'verbose_name_plural': 'Imagenes para carrusel',
                'abstract': False,
                'verbose_name': 'Imagen para carrusel',
            },
        ),
        migrations.CreateModel(
            name='Panel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False)),
                ('name', models.CharField(max_length=255, verbose_name='Nombre')),
                ('columns', models.PositiveSmallIntegerField(default=12, help_text='Columnas en una fila no deberían exceder 12', verbose_name='Columnas')),
            ],
            options={
                'verbose_name_plural': 'Paneles',
                'abstract': False,
                'ordering': ('order',),
                'verbose_name': 'Panel',
            },
            bases=(models.Model, walltv.models.ModelRenderMixin),
        ),
        migrations.CreateModel(
            name='Row',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False)),
                ('name', models.CharField(max_length=255, verbose_name='Nombre')),
                ('columns', models.PositiveSmallIntegerField(default=12, help_text='Columnas en una fila no deberían exceder 12', verbose_name='Columnas')),
                ('height', models.PositiveSmallIntegerField(default=100, help_text='Porcentage usado verticalmente de la pantalla', verbose_name='Altura')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='childs', to='walltv.Row', verbose_name='Padre')),
            ],
            options={
                'verbose_name_plural': 'Filas',
                'abstract': False,
                'ordering': ('order',),
                'verbose_name': 'Fila',
            },
            bases=(walltv.models.ModelRenderMixin, models.Model),
        ),
        migrations.CreateModel(
            name='CarouselPanel',
            fields=[
                ('panel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='walltv.Panel')),
                ('interval', models.PositiveSmallIntegerField(default=5, help_text='The amount of time to delay between automatically cycling an item.', verbose_name='Interval')),
            ],
            options={
                'verbose_name_plural': 'Paneles de carrusel de imágenes',
                'abstract': False,
                'verbose_name': 'Panel de carrusel de imágenes',
            },
            bases=('walltv.panel',),
        ),
        migrations.CreateModel(
            name='ImagePanel',
            fields=[
                ('panel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='walltv.Panel')),
                ('image', models.ImageField(upload_to='uploads', verbose_name='Imagen')),
            ],
            options={
                'verbose_name_plural': 'Paneles de imagen',
                'abstract': False,
                'verbose_name': 'Panel de imagen',
            },
            bases=('walltv.panel',),
        ),
        migrations.CreateModel(
            name='RSSPanel',
            fields=[
                ('panel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='walltv.Panel')),
                ('url', models.URLField(verbose_name='URL')),
            ],
            options={
                'verbose_name_plural': 'Paneles de RSS',
                'abstract': False,
                'verbose_name': 'Panel de RSS',
            },
            bases=('walltv.panel',),
        ),
        migrations.CreateModel(
            name='TextPanel',
            fields=[
                ('panel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='walltv.Panel')),
                ('text', models.TextField(verbose_name='Texto')),
            ],
            options={
                'verbose_name_plural': 'Paneles de texto',
                'abstract': False,
                'verbose_name': 'Panel de texto',
            },
            bases=('walltv.panel',),
        ),
        migrations.CreateModel(
            name='URLVideoPanel',
            fields=[
                ('panel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='walltv.Panel')),
                ('video_url', embed_video.fields.EmbedVideoField(verbose_name='URL del video')),
            ],
            options={
                'verbose_name_plural': 'Paneles de video con URL',
                'abstract': False,
                'verbose_name': 'Panel de video con URL',
            },
            bases=('walltv.panel',),
        ),
        migrations.CreateModel(
            name='VideoPanel',
            fields=[
                ('panel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='walltv.Panel')),
                ('file', models.FileField(upload_to='', verbose_name='Archivo')),
            ],
            options={
                'verbose_name_plural': 'Paneles de video',
                'abstract': False,
                'verbose_name': 'Panel de video',
            },
            bases=('walltv.panel',),
        ),
        migrations.CreateModel(
            name='WeatherPanel',
            fields=[
                ('panel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='walltv.Panel')),
                ('location', models.CharField(max_length=255, verbose_name='Ubicación')),
            ],
            options={
                'verbose_name_plural': 'Paneles de tiempo',
                'abstract': False,
                'verbose_name': 'Panel de tiempo',
            },
            bases=('walltv.panel',),
        ),
        migrations.AddField(
            model_name='panel',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='panels', to='walltv.Row', verbose_name='Padre'),
        ),
        migrations.AddField(
            model_name='panel',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_walltv.panel_set+', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='imageforcarouselpanel',
            name='carousel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='walltv.CarouselPanel'),
        ),
    ]
