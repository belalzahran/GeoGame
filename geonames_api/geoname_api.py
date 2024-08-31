import requests
import requests.packages
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

        print(f"Request List: {ep_params}\n\n")

        full_url = self.url + endpoint
        # headers = {'x-api-key': self._api_key}



        response = requests.request(
            method=http_method,
            url=full_url,
            verify=self._ssl_verify,
            # headers=headers,
            params=ep_params,
            json=data)
        
        # print(f"Response status code: {response.status_code}")
        # print(f"Response content: {response.text}")
        data_out = response.json()

        if response.status_code >= 200 and response.status_code <= 299:     # OK
            return data_out
        raise Exception(data_out["message"])    # Todo: raise custom exception later
    






    def get(self, endpoint: str = '', ep_params: Dict = None) -> List[Dict]:
        return self._do(http_method='GET', endpoint=endpoint, ep_params=ep_params)
    
    def post(self, endpoint: str = '', ep_params: Dict = None, data: Dict = None):
        return self._do(http_method='POST', endpoint=endpoint, ep_params=ep_params, data=data)
    
    def delete(self, endpoint: str = '', ep_params: Dict = None, data: Dict = None):
        return self._do(http_method='DELETE', endpoint=endpoint, ep_params=ep_params, data=data)
    
