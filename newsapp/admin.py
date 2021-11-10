from django.contrib import admin
from .models import Category, News, Author

from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import gettext_lazy as _


# Define a new FlatPageAdmin
class FlatPageAdmin(FlatPageAdmin):
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'sites')}),
        (_('Advanced options'), {
            'classes': ('collapse',),
            'fields': (
                'enable_comments',
                'registration_required',
                'template_name',
            ),
        }),
    )


admin.site.register(Category)
admin.site.register(News)
admin.site.register(Author)



