import json
import requests
from decouple import config

def get_address(query, analyze_type=None, page=None, size=None):
    # analyze_code = default : similar (일부만 매칭된 값도 반환), possible : exact (정확히 입력한 값에 대하여만 반환)
    # page = 1 ~ 45 (결과 페이지 번호)
    # size = 1 ~ 30 (한 페이지에서 보여질 문서의 갯수)

    url = "https://dapi.kakao.com/v2/local/search/address.json"
    API_KEY = config("KAKAO_API")
    headers = {'Authorization': f'KakaoAK {API_KEY}'}
    params = {"query": query}

    if analyze_type != None:
        params["analyze_type"] = analyze_type

    if page != None:
        params['page'] = page

    if size != None:
        params['size'] = size

    res = requests.get(url, headers=headers, params=params)
    document = json.loads(res.text)
    return document['documents'][0]