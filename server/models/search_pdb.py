import sys
import json
from rcsbsearchapi.search import SequenceQuery
import traceback
import requests
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import os
downloads_directory = os.path.join(os.path.dirname(__file__), '../downloads')
os.makedirs(downloads_directory, exist_ok=True)
def setup_session(retries=3, backoff_factor=0.3):
    
    session = requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=(500, 502, 503, 504),
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def download_pdb(pdb_id, download_dir):
    # url = f"https://ftp.rcsb.org/download/{pdb_id}.pdb"
    url=f"https://files.rcsb.org/download/{pdb_id}.pdb"
    session = setup_session()
    try:
        response = session.get(url)
        if response.status_code == 200:
            with open(f"{download_dir}/{pdb_id}.pdb", "wb") as file:
                file.write(response.content)
        else:
            print(f"Failed to download {pdb_id}: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {pdb_id}: {e}")


def search_sequence(tcr_alpha, tcr_beta,token):
    if tcr_beta:  
        query = SequenceQuery(tcr_alpha + tcr_beta, 1, 1)
    else:  
        query = SequenceQuery(tcr_alpha, 0.5, 1)
    results = query("entry")
    formatted_results = []
  
    if results:
        for result in results:

            download_pdb(result,downloads_directory)
            
            formatted_result = {
                "model_id": result,  
                # "sequence":tcr_alpha+tcr_beta,
                "score": 1,  
                "picture": "https://placeholder.com/100",  
                "download": f"https://files.rcsb.org/download/{result}.pdb"  # 构建下载链接
            }
            formatted_results.append(formatted_result)
        
        return {"results": formatted_results}
    else:
       return swiss_model(token=token, tcr_alpha=tcr_alpha , tcr_beta=tcr_beta, seq_id="TCR_Model")   
    return swiss_model(token=token, tcr_alpha=tcr_alpha , tcr_beta=tcr_beta, seq_id="TCR_Model") 
       
  
def swiss_model(token, tcr_alpha,tcr_beta, seq_id):
    response = requests.post(
        "https://swissmodel.expasy.org/automodel",
        headers={"Authorization": f"Token {token}"},
        json={
            "target_sequences": [
            tcr_alpha,
            tcr_beta
        ],
        #  "target_sequences": ["VTQIPAALSVPEGENLVLNCSFTDSAIYNLQWFRQDPGKGLTSLLLIQSSQREQTSGRLNASLDKSSGRSTLYIAASQPGDSATYLCAVMGTTDSWGKLQFGAGTQVVVTP",
        #                       "VTQTPKHLITATGQRVTLRCSPRSGDLSVYWYQQSLDQGLQFLIQYYNGEERAKGNILERFSAQQFPDLHSELNLSSLELGDSALYFCASSVATYSTDTQYFGPGTRLTVL"],
          "project_title": seq_id},
        timeout=10)
    
    project_id = response.json().get("project_id")
    url_list = []
    score_list = []
    while True:
        time.sleep(10)
        response = requests.get(
            f"https://swissmodel.expasy.org/project/{project_id}/models/summary/",
            headers={"Authorization": f"Token {token}"})
        response_object = response.json()
        status = response_object["status"]
        
        if status == "COMPLETED":
            for model in response_object['models']:
                url_list.append(model['coordinates_url'])
                score_list.append(model["qmean_global"]["avg_local_score"])
            break
        elif status == "FAILED":
            return {"error": "Modeling failed"}

    max_score = max(score_list)
    max_struct = url_list[score_list.index(max_score)] ## 下载局部最高分对应的结构
    url=max_struct.replace(".gz","")
    formatted_results = []
    formatted_result = {
                "model_id": project_id,  
                # "sequence":tcr_alpha+"+"+tcr_beta,
                "score": max_score,  
                # "picture": "https://placeholder.com/100",  
                "download": url  # 构建下载链接
            }
    formatted_results.append(formatted_result)
    session = setup_session()
    try:
        response = session.get(url)
        if response.status_code == 200:
            # with open(f"/Users/salvatores/Documents/TCRpMHCmodel/TCRpMHCmodel/server/downloads/{project_id}.pdb", "wb") as file:
            #     file.write(response.content)
            file_path = os.path.join(downloads_directory, f"{project_id}.pdb")
            with open(file_path, "wb") as file:
                file.write(response.content)
        else:
            print(f"Failed to download {project_id}: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {project_id}: {e}")
    return {"results": formatted_results}
 
        
if __name__ == '__main__':
    tcr_alpha = sys.argv[1]
    tcr_beta = sys.argv[2]
    token = "d91eec442acbfcb67171d94d81dbafa6e7a2a47a"
    result = search_sequence(tcr_alpha, tcr_beta,token)
    print(json.dumps(result))
        