import json
from typing import Final

import pandas as pd
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import FileModel, FileDetailsModel, ColumnDetailsModel
from .serializers import FileSerializer, FileDetailsSerializer, ColumnDetailsSerializer

# ===================================DATA ANALYSIS==========================================
def analyze(file):
    data = pd.read_csv(file.path)

    columns_name = [column for column in data.columns]

    columns_minimum = [data[columns_name[i]].min() for i in range(len(columns_name))]
    columns_maximum = [data[columns_name[i]].max() for i in range(len(columns_name))]
    columns_mean = [data[columns_name[i]].mean() for i in range(len(columns_name))]
    columns_10th = [data[columns_name[i]].quantile(0.1) for i in range(len(columns_name))]
    columns_90th = [data[columns_name[i]].quantile(0.9) for i in range(len(columns_name))]
    missing_percentage = [data[columns_name[i]].isnull().sum()*100/ len(data.any()) for i in
                          range(len(columns_name))]

    analyzed_data = {
        "column_name": columns_name,
        "minimum": columns_minimum,
        "maximum": columns_maximum,
        "mean": columns_mean,
        "percentile_10th": columns_10th,
        "percentile_90th": columns_90th,
        "missing_values": missing_percentage}

    result = pd.DataFrame(analyzed_data)

    return result

def size(df):
    return len(df.index), len(df.columns)

# ===================================FILE==========================================
@csrf_exempt
@api_view(["POST"])
def uploadFile(request):
    if request.method == 'POST':
        print("============================POST==================================")
        serializer = FileSerializer(data=request.FILES)
        if serializer.is_valid():
            serializer.save()

            # file analysis
            id = serializer.data.get('id')
            fileObject = FileModel.objects.get(id=id)
            result = analyze(fileObject.file)

            rows, columns = size(result)
            # create a file details object
            detailsObject = FileDetailsModel.objects.create(file_id=fileObject,
                                                            number_of_columns=columns,
                                                            number_of_rows=rows)

            # create a cщlumn object for each column
            for iter in range(rows):
                ColumnDetailsModel.objects.create(file_details=detailsObject,
                                                  order=iter,
                                                  column_name=result["column_name"][iter],
                                                  minimum=result["minimum"][iter],
                                                  maximum=result["maximum"][iter],
                                                  mean=result["mean"][iter],
                                                  percentile_10th=result["percentile_10th"][iter],
                                                  percentile_90th=result["percentile_90th"][iter],
                                                  missing_percentage=result["missing_values"][iter])

            returnObject=FileSerializer(instance=fileObject)
            print("============================END==================================")
            return JsonResponse(data=returnObject.data, safe=False, status=status.HTTP_201_CREATED)
        return JsonResponse(data=serializer.data, safe=False, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET'])
def getAllFiles(request):
    if request.method == 'GET':
        print("===========================GET===================================")
        files = FileModel.objects.all()
        serializer = FileSerializer(files, many=True)
        return JsonResponse(data=serializer.data, safe=False, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['GET'])
def filesHandle(request, pk):
    try:
        file = FileModel.objects.get(pk=pk)
    except FileModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        print("============================GET==================================")
        serializer = FileSerializer(file)
        return JsonResponse(data=serializer.data, safe=True)
# ===========================================================================================

# ===================================FILE_DETAILS==========================================

@csrf_exempt
@api_view(['GET'])
def fileDetailsHandleList(request):
    if request.method == 'GET':
        print("===========================GET===================================")
        fileDetails = FileDetailsModel.objects.all()
        serializer = FileDetailsSerializer(fileDetails, many=True)
        return JsonResponse(data=serializer.data, safe=False, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['GET'])
def fileDetailsHandle(request, pk):
    try:
        fileDetails = FileDetailsModel.objects.get(pk=pk)
    except FileDetailsModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        print("============================GET==================================")
        serializer = FileDetailsSerializer(fileDetails)
        return JsonResponse(data=serializer.data, safe=True, status=status.HTTP_200_OK)
# ===========================================================================================

# ===================================COLUMN_DETAILS==========================================

@csrf_exempt
@api_view(['GET'])
def columnDetailsHandleList(request):
    if request.method == 'GET':
        print("===========================GET===================================")
        columnDetails = ColumnDetailsModel.objects.all()
        serializer = ColumnDetailsSerializer(columnDetails, many=True)
        return JsonResponse(data=serializer.data, safe=False, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['GET'])
def columnDetailsHandle(request, pk):
    try:
        columnDetails = ColumnDetailsModel.objects.get(pk=pk)
    except ColumnDetailsModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        print("============================GET==================================")
        serializer = ColumnDetailsSerializer(columnDetails)
        return JsonResponse(data=serializer.data, safe=True, status=status.HTTP_200_OK)
# ===========================================================================================


# ===================================FILE_STATISTICS==========================================

@csrf_exempt
@api_view(['GET'])
def getStatistics(request, pk, statistic):
    try:
        file = FileModel.objects.get(pk=pk)
    except FileModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        print("============================GET==================================")
        serializer = FileSerializer(file)

        object = serializer.data.get("details")

        temp_list =[]
        for key, value in object[0].items():
            if key == 'columns':
                temp_list.append(value)
                break

        list_of_statistics = []
        list_of_columns_names=[]

        for i in range(len(temp_list[0])):
            for keys,values in temp_list[0][i].items():
                if keys == "column_name":
                    list_of_columns_names.append(values)
                if keys == statistic:
                    list_of_statistics.append({list_of_columns_names[i]:values})


        return JsonResponse(data=list_of_statistics, safe=False)
# ===========================================================================================