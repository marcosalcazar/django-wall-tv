# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-26 01:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import embed_video.fields
import paintstore.fields
import walltv.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenericRow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('columns', models.PositiveSmallIntegerField(default=12, help_text='Columnas en una fila no deberían exceder 12', verbose_name='Columnas')),
                ('height', models.PositiveSmallIntegerField(default=100, help_text='Porcentage usado verticalmente de la pantalla', verbose_name='Altura')),
                ('background_color', paintstore.fields.ColorPickerField(blank=True, max_length=7, null=True)),
                ('enabled', models.BooleanField(default=True, verbose_name='Habilitado')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, walltv.models.ModelRenderMixin),
        ),
        migrations.CreateModel(
            name='ImageForCarouselPanel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False)),
                ('image_file', models.ImageField(upload_to='uploads', verbose_name='Archivo de imagen')),
            ],
            options={
                'verbose_name_plural': 'Imagenes para carrusel',
                'verbose_name': 'Imagen para carrusel',
                'ordering': ('order',),
                'abstract': False,
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
                'verbose_name': 'Panel',
                'ordering': ('order',),
                'abstract': False,
            },
            bases=(models.Model, walltv.models.ModelRenderMixin),
        ),
        migrations.CreateModel(
            name='CarouselPanel',
            fields=[
                ('panel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='walltv.Panel')),
                ('interval', models.PositiveSmallIntegerField(default=5, help_text='The amount of time (in seconds) to delay between automatically cycling an item.', verbose_name='Intervalo')),
            ],
            options={
                'verbose_name_plural': 'Paneles de carrusel de imágenes',
                'verbose_name': 'Panel de carrusel de imágenes',
                'abstract': False,
            },
            bases=('walltv.panel',),
        ),
        migrations.CreateModel(
            name='ContentRow',
            fields=[
                ('genericrow_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='walltv.GenericRow')),
            ],
            options={
                'verbose_name': 'Fila de contenido',
            },
            bases=('walltv.genericrow',),
        ),
        migrations.CreateModel(
            name='FooterRow',
            fields=[
                ('genericrow_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='walltv.GenericRow')),
                ('text', models.CharField(max_length=255, verbose_name='Texto')),
            ],
            options={
                'verbose_name': 'Fila de pie',
            },
            bases=('walltv.genericrow',),
        ),
        migrations.CreateModel(
            name='HeaderRow',
            fields=[
                ('genericrow_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='walltv.GenericRow')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='uploads', verbose_name='Logo')),
                ('logo_alt_text', models.CharField(max_length=255, verbose_name='Texto alternativo de logo')),
            ],
            options={
                'verbose_name': 'Fila de cabecera',
            },
            bases=('walltv.genericrow',),
        ),
        migrations.CreateModel(
            name='ImagePanel',
            fields=[
                ('panel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='walltv.Panel')),
                ('image', models.ImageField(upload_to='uploads', verbose_name='Imagen')),
            ],
            options={
                'verbose_name_plural': 'Paneles de imagen',
                'verbose_name': 'Panel de imagen',
                'abstract': False,
            },
            bases=('walltv.panel',),
        ),
        migrations.CreateModel(
            name='Row',
            fields=[
                ('genericrow_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='walltv.GenericRow')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False)),
                ('name', models.CharField(max_length=255, verbose_name='Nombre')),
            ],
            options={
                'verbose_name_plural': 'Custom rows',
                'verbose_name': 'Custom row',
                'ordering': ('order',),
                'abstract': False,
            },
            bases=('walltv.genericrow', models.Model),
        ),
        migrations.CreateModel(
            name='RSSPanel',
            fields=[
                ('panel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='walltv.Panel')),
                ('feed_url', models.URLField(verbose_name='URL')),
                ('feed_interval', models.PositiveSmallIntegerField(default=30, help_text='The amount of time (in seconds) to delay between automatically cycling an item.', verbose_name='Intervalo')),
                ('feed_reload_interval', models.PositiveSmallIntegerField(default=30, help_text='The amount of time (in minutes) to delay until a reload of the feed.', verbose_name='Reload interval')),
            ],
            options={
                'verbose_name_plural': 'Paneles de RSS',
                'verbose_name': 'Panel de RSS',
                'abstract': False,
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
                'verbose_name': 'Panel de texto',
                'abstract': False,
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
                'verbose_name': 'Panel de video con URL',
                'abstract': False,
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
                'verbose_name': 'Panel de video',
                'abstract': False,
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
                'verbose_name': 'Panel de tiempo',
                'abstract': False,
            },
            bases=('walltv.panel',),
        ),
        migrations.AddField(
            model_name='panel',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='panels', to='walltv.GenericRow', verbose_name='Padre'),
        ),
        migrations.AddField(
            model_name='panel',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_walltv.panel_set+', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='genericrow',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_walltv.genericrow_set+', to='contenttypes.ContentType'),
        ),
        migrations.CreateModel(
            name='RSSOneLinePanel',
            fields=[
                ('rsspanel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='walltv.RSSPanel')),
            ],
            options={
                'abstract': False,
            },
            bases=('walltv.rsspanel',),
        ),
        migrations.AddField(
            model_name='row',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='childs', to='walltv.GenericRow', verbose_name='Padre'),
        ),
        migrations.AddField(
            model_name='imageforcarouselpanel',
            name='carousel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='walltv.CarouselPanel'),
        ),
    ]
