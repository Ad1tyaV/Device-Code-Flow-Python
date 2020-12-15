import json
import requests
import time
import re

class DCF:
    def __init__(self):
        self.client_id = ''
        self.scopes = ''
        self.devicecode_endpoint = 'https://login.microsoftonline.com/consumers/oauth2/v2.0/devicecode'
        self.get_token_endpoint = 'https://login.microsoftonline.com/consumers/oauth2/v2.0/token'
        self.device_code = None
        self.refreshToken = None
        self.accessToken = None
        self.stop = False

    def getTokens(self):       
        return self.accessToken,self.refreshToken

    def readEnvFiles(self):
        try:
            with open('env.json') as env_file:
                data = json.load(env_file)
        except FileNotFoundError as file_error:
            print('File doesn\'t exist - {}'.format(file_error))
            self.stop = True
        except Exception as exception:
            print('Something went wrong: {}'.format(exception))
            self.stop = True

        regexp = '[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}'
        if len(re.findall(regexp, self.client_id)) != len(client_id):
            self.stop = True
            print('Re-check env.json file')

        if data[client_id] == '' or data[scopes] == '':
            self.stop = True
            print('Re-check env.json file')

        self.client_id = data['client_id']
        self.scopes = data['scope']

    def get_polling_code(self):        
        payload = 'client_id={}&scope={}'.format(self.client_id,self.scopes)
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.get(self.devicecode_endpoint,headers=headers,data=payload)
        
        if response.status_code == 200:
            response_json = json.loads(response.content.decode())
            self.device_code = response_json['device_code']
            print(response_json['message'])    
        else:
            print(response.reason)
            print('Check env.json file')
            self.stop = True    

    def startFlow(self):
        self.readEnvFiles()
        if not self.stop:
            self.get_polling_code()
        if not self.stop:    
            self.start_polling()        

    def start_polling(self):    
        p = time.time()
        while True:
            time.sleep(10)
            q = time.time()
            if int(q-p) >=500:
                print('Request Timed out!')
                break
            else:
                # Make request from here
                grant_type='urn:ietf:params:oauth:grant-type:device_code'                              
                payload = 'grant_type={}&client_id={}&device_code={}'.format(grant_type,self.client_id,self.device_code)
                headers = {
                'Content-Type': 'application/x-www-form-urlencoded'            
                }
                response = requests.post(self.get_token_endpoint,headers=headers, data=payload)
                if response.status_code == 200:
                    json_response = json.loads(response.content.decode())
                    self.refreshToken = json_response['refresh_token']
                    self.accessToken = json_response['access_token']
                    break
                else:
                    if (int(q-p)%50) == 0:
                        print('Authentication Pending!')
                    continue