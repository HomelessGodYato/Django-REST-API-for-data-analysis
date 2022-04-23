from django.contrib import admin
from .models import FileModel,FileDetailsModel,ColumnDetailsModel


admin.site.register(FileModel)
admin.site.register(FileDetailsModel)
admin.site.register(ColumnDetailsModel)

