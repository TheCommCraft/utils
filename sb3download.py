import zipfile, requests, json, pickle
from io import BytesIO

headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0','Accept': '*/*','Accept-Language': 'en, en;q=0.8','Origin': 'https://scratch.mit.edu','Connection': 'keep-alive','Referer': 'https://scratch.mit.edu/','Sec-Fetch-Dest': 'empty','Sec-Fetch-Mode': 'cors','Sec-Fetch-Site': 'same-site','Pragma': 'no-cache','Cache-Control': 'no-cache'}

def download_project(project_id, buffer=None):
    buffer = buffer or BytesIO()
    if isinstance(buffer, str):
        with open(buffer, "wb") as f:
            return download_project(project_id, f)
    project_token = requests.get(f"https://api.scratch.mit.edu/projects/{project_id}", headers=headers).json()["project_token"]
    project_json = requests.get(f"https://projects.scratch.mit.edu/{project_id}", headers=headers, params = {
        'token': project_token,
    }).json()
    with zipfile.ZipFile(buffer, 'w') as zipf:
        zipf.writestr('project.json', json.dumps(project_json))
        for target in project_json["targets"]:
            for asset in target["costumes"]+target["sounds"]:
                content = requests.get(f'https://assets.scratch.mit.edu/internalapi/asset/{asset["md5ext"]}/get/', headers=headers).content
                zipf.writestr(asset["md5ext"], content)
    return buffer

download_project(PROJECT_ID, FILENAME)
