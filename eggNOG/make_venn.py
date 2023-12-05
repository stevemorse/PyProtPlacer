import os
import time
import json
from matplotlib_venn import venn2, venn2_circles, venn2_unweighted
from matplotlib_venn import venn3, venn3_circles
from matplotlib import pyplot as plt

def make_venn_2(file_one,file_two):
    line_num = 0
    file_one_dict = {}
    circle_one = 0
    circle_two = 0
    both_circles = 0
    for line in open(file_one, 'r'):
        line_num +=1
        if line_num != 1:
            line_items = line.split()
            #print(line_items[0])
            file_one_dict.update({line_items[0].strip():line})
            #print(line_items[0] + ":\n" + line)
            circle_one += 1
    line_num = 0
    for line in open(file_two, 'r'):
        line_num +=1
        if line_num != 1:
            line_items = line.split()
            #print(line_items[0])
            if line_items[0].strip() in file_one_dict:
                both_circles += 1 
            circle_two += 1        
    #venn2(subsets = (circle_one, circle_two, both_circles), set_labels = ('hit in uniref50 data', 'hit in swiss prot data'))
    venn2(subsets = (circle_one, circle_two, both_circles), set_labels = ('hit in blastx', 'hit in prodigal'))
    #plt.savefig("/home/steve/Desktop/eggNOG/hits.png")
    plt.savefig("/home/steve/Desktop/eggNOG/blastx_vs_prodigal_hits.png")          
    plt.show()

def make_venn_3(file_one,file_two,file_three):
    line_num = 0
    file_one_dict = {}
    file_two_dict = {}
    circle_one = 0
    circle_two = 0
    circle_three = 0
    circles_one_two = 0
    circles_one_three = 0
    circles_two_three = 0
    all_circles = 0
    
    for line in open(file_one, 'r'):
        line_num +=1
        if line_num != 1:
            line_items = line.split()
            #print(line_items[0])
            file_one_dict.update({line_items[0].strip():line})
            #print(line_items[0] + ":\n" + line)
            circle_one += 1
    line_num = 0
    for line in open(file_two, 'r'):
        line_num +=1
        if line_num != 1:
            line_items = line.split()
            #print(line_items[0])
            file_two_dict.update({line_items[0].strip():line})
            #print(line_items[0] + ":\n" + line)
            circle_two += 1
            if line_items[0].strip() in file_one_dict:
                circles_one_two += 1           
    line_num = 0
    for line in open(file_three, 'r'):
        line_num +=1
        if line_num != 1:
            line_items = line.split()
            #print(line_items[0])
            if line_items[0].strip() in file_one_dict and line_items[0].strip() in file_two_dict:
                all_circles += 1 
            elif line_items[0].strip() in file_one_dict:
                circles_one_three += 1
            elif line_items[0].strip() in file_two_dict:
                circles_two_three += 1
            circle_three += 1        
    venn3(subsets = (circle_one, circle_two,circles_one_two,circle_three,circles_one_three,circles_two_three,all_circles), 
          #set_labels = ('hit in uniref50 data', 'hit in swiss prot data', 'hit in eggNOG data'),
          set_labels = ('hit in uniref50 data', 'hit in swiss prot data', 'hit in prodigal eggNOG data'),
          set_colors = ("orange", "blue", "red"), alpha = 0.7)
    #plt.savefig("/home/steve/Desktop/eggNOG/all_hits.png")
    plt.savefig("/home/steve/Desktop/eggNOG/all_prodigal_hits.png")          
    plt.show()

def main():
    start_time = time.time()
    #res_dict = json.load(open("/nfs/speed-scratch/ste_mors/venv/PyProtPlacer/res.json"))
    res_dict = json.load(open("/home/steve/eclipse-workspace/PyProtPlacer/res.json"))
    file_one = res_dict.get("uniref50_in_file_name")
    file_two = res_dict.get("sprot_in_file_name")
    file_three = res_dict.get("merged_file_name")
    file_four = res_dict.get("prodigal_merged_file_name")
    #make_venn_2(file_one,file_two)
    make_venn_2(file_three,file_four)
    #make_venn_3(file_one,file_two,file_three)
    make_venn_3(file_one,file_two,file_four)
    end_time = time.time()
    print("System terminates normally in: " + str(end_time - start_time) + "seconds\n")
    
if __name__ == "__main__":
    main()