from django import forms
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.simplejson import simplejson


class MarkdownWidget(forms.Textarea):
    class Media:
        js = (
                settings.STATIC_URL + 'django_markdown/jquery.markitup.js',
                settings.STATIC_URL + 'django_markdown/markdown.js',
        )
        css = {
            'screen': (
                settings.STATIC_URL + 'django_markdown/skins/%s/style.css' % getattr(settings, 'MARKDOWN_EDITOR_SKIN', 'markitup'),
                settings.STATIC_URL + 'django_markdown/markdown.css',
            )
        }

    def render(self, name, value, attrs=None):
        html = super(MarkdownWidget, self).render(name, value, attrs)
        
        editor_settings = getattr(settings, 'MARKDOWN_EDITOR_SETTINGS', {})
        editor_settings['previewParserPath'] = reverse('django_markdown_preview')
        
        html += ("""
                <script type="text/javascript">
                (function($) {
                    $(document).ready(function() {
                        $("#%(id)s").markItUp($.extend(miu.settings, %(settings)s));
                    });
                })(jQuery || django.jQuery);
                </script>
                """ % {'id': attrs['id'], 'settings': simplejson.dumps(editor_settings)})
        return mark_safe(html)

