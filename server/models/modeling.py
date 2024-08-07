
import requests
import time
import os
from Bio import SeqIO

    
def swiss_model(token, target_seq, seq_id, outpath):
    # 创建建模项目
    response = requests.post(
        "https://swissmodel.expasy.org/automodel",
        headers={ "Authorization": f"Token {token}" },
        json={ 
            "target_sequences": ["VTQIPAALSVPEGENLVLNCSFTDSAIYNLQWFRQDPGKGLTSLLLIQSSQREQTSGRLNASLDKSSGRSTLYIAASQPGDSATYLCAVMGTTDSWGKLQFGAGTQVVVTP",
                                 "VTQTPKHLITATGQRVTLRCSPRSGDLSVYWYQQSLDQGLQFLIQYYNGEERAKGNILERFSAQQFPDLHSELNLSSLELGDSALYFCASSVATYSTDTQYFGPGTRLTVL"],
            "project_title": seq_id
        },
        timeout=10)
    
    # 查看运行状态并返回结果下载链接
    project_id = response.json()["project_id"] ## 获取 project id
    url_list = []
    score_list = []
    while True:
        ## 每隔10s不断地查看运行状态，完成或失败都会终止并输出信息
        time.sleep(10)
        response = requests.get(
            f"https://swissmodel.expasy.org/project/{ project_id }/models/summary/", 
            headers={ "Authorization": f"Token {token}" })
        response_object = response.json()
        status = response_object["status"]
        
        if status == "COMPLETED":
            for model in response_object['models']:
                url_list.append(model['coordinates_url'])
                score_list.append(model["qmean_global"]["avg_local_score"]) ## 记录平均局部最高分
            break
        elif status == "FAILED":
            break
    
    # 下载最高分（平均局部最高分）对应的结构
    max_score = max(score_list)
    max_struct = url_list[score_list.index(max_score)] ## 下载局部最高分对应的结构
    with open(outpath+"model_score.log", "a") as outF: ## 将每个蛋白的局部最高分输出
        outF.write("SeqID: %s, Score: %s\n" % (seq_id, max_score))
    cmd_download = "wget "+max_struct+" -O "+outpath+seq_id+".pdb.gz" ## 根据url利用wget进行下载并重命名为 序列ID.pdb.gz
    os.system(cmd_download)
    # cmd_rmwget = "rm wget-log" ## 删掉wget下载时重定向生成的 wget-log文件
    # os.system(cmd_rmwget)


def swiss_model_single_seq(token,inf_fa, outpath): ## 单个序列的提交，token（swiss-model提供的令牌）inf_fa（输入文件，fasta格式）；outpath（输入文件路径）
    for record in SeqIO.parse(inf_fa, "fasta"):
        target_seq = str(record.seq)
        seq_id = record.id
    # swiss_model(token=token, target_seq=target_seq,seq_id=seq_id,outpath=outpath)
    if target_seq and seq_id:  
        swiss_model(token=token, target_seq=target_seq, seq_id=seq_id, outpath=outpath)
    else:
        print("No valid sequences found in the input file.")

token = "d91eec442acbfcb67171d94d81dbafa6e7a2a47a" ## 登入swiss-model会在自己的账户那里生成 token，复制过来即可。
inf_fa = "/Users/salvatores/Documents/TCRpMHCmodel/TCRpMHCmodel/server/models/test.fasta" ## fasta格式的输入文件
outpath = "./" ## 结果输出到当前目录（注意最后要有 /）
swiss_model_single_seq(token, inf_fa, outpath)
