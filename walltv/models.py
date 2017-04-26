import os

from django.conf import settings
from django.db import models
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from embed_video.fields import EmbedVideoField
from ordered_model.models import OrderedModel
from paintstore.fields import ColorPickerField
from polymorphic.models import PolymorphicModel


class ModelRenderMixin:
    """
    https://github.com/a1fred/django-model-render/
    """
    template_path = None

    def get_template_path(self):
        return getattr(
            self, "template_path", None) or os.path.join(
            self._meta.app_label,
            'models',
            self._meta.object_name.lower() + "." + getattr(
                settings, "MODEL_RENDER_DEFAULT_EXTENSION", "html"))

    def render(self, template=None, additional=None):
        """
        Render single model to its html representation.
        You may set template path in render function argument,
            or model's variable named 'template_path',
            or get default name: $app_label$/models/$model_name$.html
        Settings:
        * MODEL_RENDER_DEFAULT_EXTENSION
            set default template extension. Usable if you use jinja or others.
        :param template: custom template_path
        :return: rendered model html string
        """
        template_path = template or self.get_template_path()

        template_vars = {'model': self}
        if additional:
            template_vars.update(additional)

        rendered = render_to_string(template_path, template_vars)
        return mark_safe(rendered)


class GenericRow(PolymorphicModel, ModelRenderMixin):
    columns = models.PositiveSmallIntegerField(help_text=_('Columns in a row shouldn\'t exceed 12'),
                                               verbose_name=_('Columns'),
                                               default=12)
    height = models.PositiveSmallIntegerField(help_text=_('Percentage used vertically of the screen'),
                                              verbose_name=_('Height'),
                                              default=100)
    background_color = ColorPickerField(null=True, blank=True)
    enabled = models.BooleanField(verbose_name=_('Enabled'), default=True)

    def get_sorted_panels(self):
        panels = self.panels.all().get_real_instances()
        return sorted(panels, key=lambda x: x.order, reverse=True)


class HeaderRow(GenericRow):
    singleton_instance_id = settings.HEADER_ROW_PK
    logo = models.ImageField(verbose_name=_('Logo'), upload_to='uploads', null=True, blank=True)
    logo_alt_text = models.CharField(verbose_name=_('Logo alternative text'), max_length=255)

    class Meta:
        verbose_name = _('Header row')

    def __str__(self):
        return _('Header row')

    def get_template_path(self):
        return 'models/rows/headerrow.html'


class ContentRow(GenericRow):
    singleton_instance_id = settings.CONTENT_ROW_PK
    class Meta:
        verbose_name = _('Content row')

    def __str__(self):
        return _('Content row')

    def get_template_path(self):
        return 'models/rows/contentrow.html'


class FooterRow(GenericRow):
    singleton_instance_id = settings.FOOTER_ROW_PK
    text = models.CharField(max_length=255, verbose_name=_('Text'))

    class Meta:
        verbose_name = _('Footer row')

    def __str__(self):
        return _('Footer row')

    def get_template_path(self):
        return 'models/rows/footerrow.html'


class Row(GenericRow, OrderedModel):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    parent = models.ForeignKey(GenericRow, related_name='childs', verbose_name=_('Parent'), null=True, blank=True)

    class Meta(OrderedModel.Meta):
        verbose_name = _('Custom row')
        verbose_name_plural = _('Custom rows')

    def __str__(self):
        return self.name

    def get_template_path(self):
        return 'models/rows/contentrow.html'


class Panel(PolymorphicModel, OrderedModel, ModelRenderMixin):
    parent = models.ForeignKey(GenericRow, related_name='panels', verbose_name=_('Parent'),
                               null=True, blank=True)
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    columns = models.PositiveSmallIntegerField(help_text=_('Columns in a row shouldn\'t exceed 12'),
                                               verbose_name=_('Columns'),
                                               default=12)

    class Meta(OrderedModel.Meta):
        verbose_name = _('Panel')
        verbose_name_plural = _('Panels')
        ordering = ('order',)

    def __str__(self):
        return self.name

    def get_template_path(self):
        raise NotImplementedError()


class URLVideoPanel(Panel):
    """
    Used for Youtube/Vimeo/soundcloud
    """
    video_url = EmbedVideoField(verbose_name=_('Video URL'))

    def get_template_path(self):
        return 'models/panels/urlvideopanel.html'

    class Meta(Panel.Meta):
        verbose_name = _('URL video panel')
        verbose_name_plural = _('URL video panels')


class VideoPanel(Panel):
    file = models.FileField(verbose_name=_('File'))

    class Meta(Panel.Meta):
        verbose_name = _('Video panel')
        verbose_name_plural = _('Video panels')

    def get_template_path(self):
        return 'models/panels/videopanel.html'


class ImagePanel(Panel):
    image = models.ImageField(verbose_name=_('Image'), upload_to='uploads')

    class Meta(Panel.Meta):
        verbose_name = _('Image panel')
        verbose_name_plural = _('Image panels')

    def get_template_path(self):
        return 'models/panels/imagepanel.html'


class CarouselPanel(Panel):
    interval = models.PositiveSmallIntegerField(
        help_text=_('The amount of time (in seconds) to delay between automatically cycling an item.'),
        verbose_name=_('Interval'),
        default=5
    )

    class Meta(Panel.Meta):
        verbose_name = _('Carousel panel')
        verbose_name_plural = _('Carousel panels')

    def get_template_path(self):
        return 'models/panels/carouselpanel.html'


class ImageForCarouselPanel(OrderedModel):
    carousel = models.ForeignKey(CarouselPanel, related_name='images')
    image_file = models.ImageField(verbose_name=_('Image file'), upload_to='uploads')
    order_with_respect_to = 'carousel'

    class Meta(Panel.Meta):
        verbose_name = _('Image for carousel')
        verbose_name_plural = _('Images for carousel')
        ordering = ('order', )


class TextPanel(Panel):
    text = models.TextField(verbose_name=_('Text'))

    class Meta(Panel.Meta):
        verbose_name = _('Text panel')
        verbose_name_plural = _('Text panels')

    def get_template_path(self):
        return 'models/panels/textpanel.html'


class WeatherPanel(Panel):
    location = models.CharField(max_length=255, verbose_name=_('Location'))

    class Meta(Panel.Meta):
        verbose_name = _('Weather panel')
        verbose_name_plural = _('Weather panels')


class RSSPanel(Panel):
    feed_url = models.URLField(verbose_name=_('URL'))
    feed_interval = models.PositiveSmallIntegerField(
        help_text=_('The amount of time (in seconds) to delay between automatically cycling an item.'),
        verbose_name=_('Interval'),
        default=30
    )
    feed_reload_interval = models.PositiveSmallIntegerField(
        help_text=_('The amount of time (in minutes) to delay until a reload of the feed.'),
        verbose_name=_('Reload interval'),
        default=30
    )

    class Meta(Panel.Meta):
        verbose_name = _('RSS panel')
        verbose_name_plural = _('RSS panels')


class RSSOneLinePanel(RSSPanel):
    def get_template_path(self):
        return 'models/panels/rssonelinepanel.html'
