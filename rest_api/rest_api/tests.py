import datetime

from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase

from .models import FileModel, FileDetailsModel, ColumnDetailsModel


class FileUploadTestCase(APITestCase):

    def test_file_is_accepted(self):
        data = open('files/test_file.csv', 'rb')
        data = SimpleUploadedFile(content=data.read(), name=data.name, content_type='text/csv')
        response = self.client.post("/upload_file/", {'file': data,
                                                      'date_created': datetime.datetime.now(),
                                                      }, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_all_files(self):
        filename = 'test_file.csv'
        file_obj = File(open(f'files/{filename}', mode='rb'), name=filename)
        file = FileModel.objects.create(file=file_obj,
                                        date_created=datetime.datetime.now())

        response = self.client.get("/all_files/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_file(self):
        filename = 'test_file.csv'
        file_obj = File(open(f'files/{filename}', mode='rb'), name=filename)
        file = FileModel.objects.create(file=file_obj,
                                        date_created=datetime.datetime.now())
        response = self.client.get("/file/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_all_details(self):
        filename = 'test_file.csv'
        file_obj = File(open(f'files/{filename}', mode='rb'), name=filename)
        file = FileModel.objects.create(file=file_obj,
                                        date_created=datetime.datetime.now())
        file_id = FileModel.objects.get(id=1)

        detailsObject = FileDetailsModel.objects.create(file_id=file_id,
                                                        number_of_columns=4,
                                                        number_of_rows=4)
        response = self.client.get("/file_details/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_file_details(self):
        filename = 'test_file.csv'
        file_obj = File(open(f'files/{filename}', mode='rb'), name=filename)
        file = FileModel.objects.create(file=file_obj,
                                        date_created=datetime.datetime.now())
        file_id = FileModel.objects.get(id=1)
        detailsObject = FileDetailsModel.objects.create(file_id=file_id,
                                                        number_of_columns=4,
                                                        number_of_rows=4)

        response = self.client.get("/file_details/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_columns_details(self):
        filename = 'test_file.csv'
        file_obj = File(open(f'files/{filename}', mode='rb'), name=filename)
        file = FileModel.objects.create(file=file_obj,
                                        date_created=datetime.datetime.now())
        file_id = FileModel.objects.get(id=1)
        detailsObject = FileDetailsModel.objects.create(file_id=file_id,
                                                        number_of_columns=4,
                                                        number_of_rows=4)
        details_id = FileDetailsModel.objects.get(id=1)
        column = ColumnDetailsModel.objects.create(file_details=details_id,
                                                   order=1,
                                                   column_name='some_name',
                                                   minimum='0.0',
                                                   maximum='0.0',
                                                   mean='15.0',
                                                   percentile_10th='2.15871',
                                                   percentile_90th='9.123447',
                                                   missing_percentage='0.0')

        response = self.client.get("/column_details/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_column_details(self):
        filename = 'test_file.csv'
        file_obj = File(open(f'files/{filename}', mode='rb'), name=filename)
        file = FileModel.objects.create(file=file_obj,
                                        date_created=datetime.datetime.now())
        file_id = FileModel.objects.get(id=1)
        detailsObject = FileDetailsModel.objects.create(file_id=file_id,
                                                        number_of_columns=4,
                                                        number_of_rows=4)
        details_id = FileDetailsModel.objects.get(id=1)
        column = ColumnDetailsModel.objects.create(file_details=details_id,
                                                   order=1,
                                                   column_name='some_name',
                                                   minimum='0.0',
                                                   maximum='0.0',
                                                   mean='15.0',
                                                   percentile_10th='2.15871',
                                                   percentile_90th='9.123447',
                                                   missing_percentage='0.0')

        response = self.client.get("/column_details/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_file_statistic(self):
        filename = 'test_file.csv'
        file_obj = File(open(f'files/{filename}', mode='rb'), name=filename)
        file = FileModel.objects.create(file=file_obj,
                                        date_created=datetime.datetime.now())
        file_id = FileModel.objects.get(id=1)
        detailsObject = FileDetailsModel.objects.create(file_id=file_id,
                                                        number_of_columns=4,
                                                        number_of_rows=4)
        details_id = FileDetailsModel.objects.get(id=1)
        column = ColumnDetailsModel.objects.create(file_details=details_id,
                                                   order=1,
                                                   column_name='some_name',
                                                   minimum='0.0',
                                                   maximum='0.0',
                                                   mean='15.0',
                                                   percentile_10th='2.15871',
                                                   percentile_90th='9.123447',
                                                   missing_percentage='0.0')
        statistic = 'mean'
        response = self.client.get(f"/file/1/{statistic}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
