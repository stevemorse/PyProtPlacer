import time
import json

def get_good_hits(in_file_name,out_file_name):
    outfile = open(out_file_name,'w')
    outfile.write("{:<60} {:<25} {:<12} {:<7} {:<7} {:<7} {:<7} {:<7} {:<7} {:<7}".format\
                  ("query","target","evalue","pident","bits","qcov","tcov","qlen","tlen","alnlen"))
    outfile.write("\n")
    line_number = 0
    for line in open(in_file_name, 'r'):
        line_number +=  1
        if line_number == 1:
            continue
        if line_number > 1:
            tabs = line.split("\t")
            query = tabs[0]
            target = tabs[1]
            evalue = float(str(tabs[2]))
            pident = float(tabs[3])
            bits = float(tabs[4])
            qcov = float(tabs[5])
            tcov = float(tabs[6])
            qlen = float(tabs[7])
            tlen = float(tabs[8])
            alnlen = float(tabs[9])
            if evalue <= 1e-30 and pident >= 70.0 and qcov >= 0.7:
                outfile.write("{:<60} {:<25} {:<12} {:<7} {:<7} {:<7} {:<7} {:<7} {:<7} {:<7}".format\
                              (query,target,evalue,pident,bits,qcov,tcov,qlen,tlen,alnlen))
                outfile.write("\n")
                
def main():
    res_dict = json.load(open("res.json"))
    start_time = time.time()
    sprot_in_file_name = res_dict.get('sprot_in_file_name')
    #uniref50_in_file_name = res_dict.get('uniref50_in_file_name')
    sprot_out_file_name = res_dict.get('sprot_out_file_name')
    #uniref50_out_file_name = res_dict.get('uniref50_out_file_name')
    in_file_name = sprot_in_file_name
    out_file_name = sprot_out_file_name
    
    '''
    #in_file_name = "/home/steve/Desktop/mmseq2/sprotRes.tab"
    in_file_name = "/home/steve/Desktop/mmseq2/uniref50Res.tab"
    #out_file_name = "/home/steve/Desktop/mmseq2/sprotHits.txt"
    out_file_name = "/home/steve/Desktop/mmseq2/uniref50Hits.txt"
    '''
    
    get_good_hits(in_file_name,out_file_name)
    end_time = time.time()
    print("System terminates normally in: " + str(end_time - start_time) + "seconds\n")
    
if __name__ == "__main__":
    main()