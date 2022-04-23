import requests
import datetime
import json
from django.core.files.uploadedfile import SimpleUploadedFile

url = 'http://127.0.0.1:8000/'

def ui():
    method = input("Choose a method:\n"
                   "1) GET\n"
                   "2) POST\n"
                   "3) EXIT\n"
                   )
    if method == "1":
        endpoint = input("Enter endpoint:\n "
                         "1) all_files/\n"
                         "2) file/\n"
                         "3) all_details/\n"
                         "4) file_details/\n"
                         "5) columns_details/\n"
                         "6) column/\n"
                         "7) statistics/\n")

        if endpoint == "1":
            response = requests.get(url + "all_files/")
            response_json = json.loads(response.text)
            return response_json

        elif endpoint == "2":
            file_id = input("Enter file id: ")
            response = requests.get(url + "file/"+file_id)
            response_json = json.loads(response.text)
            return response_json

        elif endpoint == "3":
            response = requests.get(url + "all_details/")
            response_json = json.loads(response.text)
            return response_json

        elif endpoint == "4":
            file_id = input("Enter file id: ")
            response = requests.get(url + "file_details/"+file_id)
            response_json = json.loads(response.text)
            return response_json

        elif endpoint == "5":
            response = requests.get(url + "columns_details/")
            response_json = json.loads(response.text)
            return response_json

        elif endpoint == "6":
            column_id = input("Enter column id: ")
            response = requests.get(url + "column/"+column_id)
            response_json = json.loads(response.text)
            return response_json

        elif endpoint == "7":
            available_statistics = {1:"minimum",
                                    2:"maximum",
                                    3:"mean",
                                    4:"percentile_10th",
                                    5:"percentile_90th",
                                    6:"missing_percentage"}

            file_id = input("Enter file id: ")
            print("Available statistics:\n"
                  "1)minimum\n"
                  "2)maximum\n"
                  "3)mean\n"
                  "4)percentile_10th\n"
                  "5)percentile_90th\n",
                  "6)missing_percentage\n")
            statistic = int(input("Enter statistic: "))
            response = requests.get(url + "statistics/"+file_id+'/'+available_statistics[statistic])
            response_json = json.loads(response.text)
            return response_json
        else:
            print("Wrong endpoint\n")

    if method == "2":
        endpoint = "upload_file/"
        file_name = input("Enter file name: ")
        file_path = input("Enter file path: ")
        file = open(file_path, 'rb')
        file_content = file.read()
        file.close()
        file_to_upload = SimpleUploadedFile(file_name, file_content)
        response = requests.post(url + endpoint, files={'file': file_to_upload})
        response_json = json.loads(response.text)
        return response_json


    if method == "3":
        exit("Exiting...")

def main():
    while True:
        response = ui()
        print(json.dumps(response,indent=4))

if __name__ == "__main__":
    main()