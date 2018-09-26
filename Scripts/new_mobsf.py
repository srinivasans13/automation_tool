
from json import loads
from requests_toolbelt import MultipartEncoder
import ast
import requests
import subprocess

import re
API_KEY = "1ef92fca5063fb59f96461374572a56de4976f5479303d53ff08e988d672847b"
FILE_NAME = "/Users/digitalsecurity/Desktop/ipa_files/whatsapp.apk"
SCAN_TYPE = FILE_NAME[-3:]
HASH = ""
headers = {
    'Authorization': API_KEY,

}
output = subprocess.CompletedProcess
def startMobSf(command):
    output_popen = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                    shell=True)

    try:
        output_popen.wait(20)

    except subprocess.TimeoutExpired:
        outs = output_popen.stdout.read(850)

        with open('simple.txt', 'w') as file:
            file.write(outs.decode('utf-8').rstrip('\n'))

    except Exception as e:
        print(e)



def uploadFile():
    print("here")
    # defining the api-endpoint
    API_ENDPOINT = "http://localhost:8000/api/v1/upload"

    # your API key here
    file = open(FILE_NAME,'rb')

    m = MultipartEncoder(
        fields={
                'file': ('demo.'+SCAN_TYPE, file, 'application/octet-stream')}
    )
    headers['Content-Type'] = m.content_type

    # sending post request and saving response as response object


    r = requests.post(url=API_ENDPOINT, headers=headers, data=m)
    dictionary = ast.literal_eval(r.text)
    global HASH
    HASH = dictionary['hash'].strip()
    file.close()

def scanFile():
    API_ENDPOINT = "http://localhost:8000/api/v1/scan"
    global headers ,HASH
    data = {
        'hash' : HASH,
        'file_name':'demo.'+SCAN_TYPE,
        'scan_type':SCAN_TYPE,


    }
    r = requests.post(url=API_ENDPOINT,headers = headers,data=data)
    print(r.text)


def generateReport_pdf():
    API_ENDPOINT = "http://localhost:8000/api/v1/download_pdf"
    global headers
    data  = {
        'hash' : HASH,
        'scan_type' : SCAN_TYPE
    }
    r = requests.post(url=API_ENDPOINT, headers=headers, data=data)
    with open('metadata.pdf','wb') as file:
        file.write(r.content)

def generateReport_JSON():
    API_ENDPOINT = "http://localhost:8000/api/v1/report_json"
    global headers
    data  = {
        'hash' : HASH,
        'scan_type' : SCAN_TYPE
    }
    r = requests.post(url=API_ENDPOINT, headers=headers, data=data)
    json = loads(r.content)
    print(json)

def kill_server():
    command = "lsof -t -i tcp:8000 | xargs kill -9"
    subprocess.run(command,shell=True)


kill_server()
startMobSf("python3 {} runserver".format("/Users/digitalsecurity/Downloads/Mobile-Security-Framework-MobSF-master/manage.py"))
uploadFile()
scanFile()
#generateReport_JSON()

generateReport_pdf()

kill_server()
