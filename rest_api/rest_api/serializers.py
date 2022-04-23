from rest_framework import serializers
from .models import FileModel,FileDetailsModel, ColumnDetailsModel

class ColumnDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ColumnDetailsModel
        fields = ["id",
                  "file_details",
                  "order",
                  "column_name",
                  "minimum",
                  "maximum",
                  "mean",
                  "percentile_10th",
                  "percentile_90th",
                  "missing_percentage",]

class FileDetailsSerializer(serializers.ModelSerializer):
    columns = ColumnDetailsSerializer(many=True, read_only=True)

    class Meta:
        model = FileDetailsModel
        fields = ["id",
                  "file_id",
                  "number_of_columns",
                  "number_of_rows",
                  "columns"]

class FileSerializer(serializers.ModelSerializer):
    details = FileDetailsSerializer(many=True, read_only=True)

    class Meta:
        model = FileModel
        fields = ["id",
                  "file",
                  "date_created",
                  "details"]