import os
import time
import json

def count_files(dir_path):
    # code based on: https://pynative.com/python-count-number-of-files-in-a-directory/
    count = 0
    # Iterate directory
    for path in os.listdir(dir_path):
        # check if current path is a file
        if os.path.isfile(os.path.join(dir_path, path)):
            count += 1
    print('File count:', count)
    return count
def merge(dir_name,merged_file_name):
    outfile = open(merged_file_name,'w')
    num_files = count_files(dir_name)
    for file_nums in range(num_files):
        #file_name = dir_name + "fasta" + str(file_nums) + ".emapper.annotations.tsv"
        file_name = dir_name + "fasta" + str(file_nums) + "prodigal.emapper.annotations.tsv"
        for line in open(file_name, 'r'):
            # keep titles from first file...otherwise strip all commented lines
            if not line.startswith('##'):
                if file_nums == 0 and line.startswith('#q'):
                    outfile.write(line)
                elif not line.startswith('#'):
                    outfile.write(line)
                else:
                    print("comment line..not written to file")
    outfile.flush()
    outfile.close()            
            
def main():
    start_time = time.time()
    #res_dict = json.load(open("/nfs/speed-scratch/ste_mors/venv/PyProtPlacer/res.json"))
    res_dict = json.load(open("/home/steve/eclipse-workspace/PyProtPlacer/res.json"))
    #merge(res_dict.get("dir_name"),res_dict.get("merged_file_name"))
    merge(res_dict.get("prodigal_dir_name"),res_dict.get("prodigal_merged_file_name"))
    end_time = time.time()
    print("System terminates normally in: " + str(end_time - start_time) + "seconds\n")
    
if __name__ == "__main__":
    main()
