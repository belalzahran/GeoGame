import requests
import requests.packages
from requests.exceptions import JSONDecodeError, RequestException
from typing import List, Dict



class RestAdapter:

    def __init__(self, hostname: str, api_key: str = '', ver: str = 'v1', ssl_verify: bool = False):
        
        self.username = 'belalzzz'
        self.url = "https://{}/{}/".format(hostname, ver)
        self._api_key = api_key
        self._ssl_verify = ssl_verify
        if not ssl_verify:
            # noinspection PyUnresolvedReferences
            requests.packages.urllib3.disable_warnings()
        
    
    def _do(self, http_method: str, endpoint: str = '', ep_params: Dict = None, data: Dict = None):

        if ep_params is None:
            ep_params = {}
        ep_params.update({'username': self.username})

        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; MyPythonScript/1.0)',
            'x-api-key': self._api_key}

        # print(f"Request List: {ep_params}\n\n")

        full_url = self.url + endpoint
        # headers = {'x-api-key': self._api_key}


        try:
            response = requests.request(
                method=http_method,
                url=full_url,
                headers=headers,
                verify=self._ssl_verify,
                # headers=headers,
                params=ep_params,
                json=data,
                timeout=10)
        
            # print(f"Response status code: {response.status_code}")
            # print(f"Response content: {response.text}")

            if not response.ok:
                raise RequestException(f"HTTP Error")
            try:
                data_out = response.json()
            
            except JSONDecodeError as e:
                raise JSONDecodeError(f"JSON Decode Error")
            
            return data_out

        except RequestException as req_err:
            # print(f"Request failed")
            raise
        
        except JSONDecodeError as json_err:
            print(f"Failed to decode JSON")
            raise

        except Exception as err:
            print(f"An unexpected error occurred")
            raise

    






    def get(self, endpoint: str = '', ep_params: Dict = None) -> List[Dict]:
        return self._do(http_method='GET', endpoint=endpoint, ep_params=ep_params)
    
    def post(self, endpoint: str = '', ep_params: Dict = None, data: Dict = None):
        return self._do(http_method='POST', endpoint=endpoint, ep_params=ep_params, data=data)
    
    def delete(self, endpoint: str = '', ep_params: Dict = None, data: Dict = None):
        return self._do(http_method='DELETE', endpoint=endpoint, ep_params=ep_params, data=data)
    
