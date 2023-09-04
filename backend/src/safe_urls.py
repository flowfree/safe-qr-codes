from typing import List, Tuple
import json
import requests 


def check_url(url: str, api_key: str) -> Tuple[bool, List[str]]:
    is_safe = False
    threat_details = []

    api_url = "https://safebrowsing.googleapis.com/v4/threatMatches:find"

    data = {
        "client": {
            "clientId": "your-client-id",
            "clientVersion": "1.0.0",
        },
        "threatInfo": {
            "threatTypes": [
                "MALWARE",
                "SOCIAL_ENGINEERING",
                "THREAT_TYPE_UNSPECIFIED",
                "UNWANTED_SOFTWARE",
                "POTENTIALLY_HARMFUL_APPLICATION"
            ],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}],
        },
    }

    response = requests.post(f"{api_url}?key={api_key}", json=data)

    if response.status_code == 200:
        data = response.json()
        if 'matches' in data:
            is_safe = False  
            for item in data['matches']:
                threat_details.append(item['threatType'] + ' / ' + item['platformType'])
        else:
            is_safe = True   
    else:
        print(f"Error: {response.status_code}")

    return is_safe, threat_details
