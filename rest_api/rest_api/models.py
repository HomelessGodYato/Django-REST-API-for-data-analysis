from django.db import models
from rest_framework import serializers


class FileModel(models.Model):
    file = models.FileField(blank=False, null=False)
    date_created = models.DateTimeField(auto_now_add=True)


class FileDetailsModel(models.Model):
    file_id = models.ForeignKey(FileModel, related_name="details", on_delete=models.CASCADE)

    number_of_columns = models.IntegerField(default=0, null=False)
    number_of_rows = models.IntegerField(default=0, null=False)


class ColumnDetailsModel(models.Model):
    file_details = models.ForeignKey(FileDetailsModel, related_name="columns", on_delete=models.CASCADE)

    order = models.IntegerField(default=-1)
    column_name = models.CharField(max_length=254)

    minimum = models.CharField(default="", max_length=254)
    maximum = models.CharField(default="", max_length=254)
    mean = models.CharField(default="", max_length=254)
    percentile_10th = models.CharField(default="", max_length=254)
    percentile_90th = models.CharField(default="", max_length=254)
    missing_percentage = models.CharField(default="", max_length=254)