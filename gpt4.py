import requests
from uuid import uuid4
from re import findall

class Completion:
    def create(self, prompt):
        impersonate = "chrome107"
        url = "https://you.com/api/streamingSearch"
        headers = {
            "User-Agent": impersonate,
            "cache-control": "no-cache",
            "referer": "https://you.com/search?q=gpt4&tbm=youchat",
            "cookie": f"safesearch_guest=Off; uuid_guest={str(uuid4())}",
        }
        params = {
            "q": prompt,
            "page": 1,
            "count": 10,
            "safeSearch": "Off",
            "onShoppingPage": False,
            "mkt": "",
            "responseFilter": "WebPages,Translations,TimeZone,Computation,RelatedSearches",
            "domain": "youchat",
            "queryTraceId": str(uuid4()),
            "chat": [],
        }
        custom_certificate_path = "./certificates/custom-certificate.pem"
        response = requests.get(url, headers=headers, params=params, verify=False)

        response = "".join(findall(r"{\"youChatToken\": \"(.*?)\"}", response.text)).replace("\\n", "\n").replace("\\\\", "\\").replace('\\"', '"')
        return response
