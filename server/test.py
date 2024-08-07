from rcsbsearchapi.search import SequenceQuery
import os
tcr1="VTQIPAALSVPEGENLVLNCSFTDSAIYNLQWFRQDPGKGLTSLLLIQSSQREQTSGRLNASLDKSSGRSTLYIAASQPGDSATYLCAVMGTTDSWGKLQFGAGTQVVVTP"
tcr2="VTQTPKHLITATGQRVTLRCSPRSGDLSVYWYQQSLDQGLQFLIQYYNGEERAKGNILERFSAQQFPDLHSELNLSSLELGDSALYFCASSVATYSTDTQYFGPGTRLTVL"
results = SequenceQuery(tcr1+tcr2, 1, 1)
    
# results("polymer_entity") produces an iterator of IDs with return type - polymer entities
polyid_list = [polyid for polyid in results("polymer_entity")]
print(polyid_list)
polyid_list=[polyid.split('_')[0] for polyid in polyid_list]

# with open('../downloads/list_file.txt', 'w') as file:
#     file.write(','.join(polyid_list))  # Join the list into a single string with commas separating items
    
# cmd_download = "../downloads/batch_download.sh -f ../downloads/list_file.txt -p" ## 利用wget进行下载
# os.system(cmd_download)