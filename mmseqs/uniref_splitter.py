from lxml import etree
import json
import time

def strip_name_space(element):
    # namespace stripping code from:
    # https://stackoverflow.com/questions/13412496/
    # python-elementtree-module-how-to-ignore-the-namespace-of-xml-files-to-locate-ma
    if '}' in element.tag:
        element.tag = element.tag.split('}', 1)[1]  # strip all namespaces
    for at in list(element.attrib.keys()): # strip namespaces of attributes too
        if '}' in at:
            newat = at.split('}', 1)[1]
            element.attrib[newat] = element.attrib[at]
            del element.attrib[at]

def make_file_header(outfile):
    outfile.write("<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>")
    outfile.write("\n")
    outfile.write("<entries>")
    outfile.write("\n")
    
def make_file_footer(outfile):
    outfile.write("</entries>")
    outfile.flush()
    outfile.close()
           
def slice_file(in_file_name,out_file_base_name,ns):
    entries = 0
    file_count = 0
    out_file_name = out_file_base_name + "_" + str(file_count) + ".xml"
    outfile = open(out_file_name,'w')
    make_file_header(outfile)
    context = etree.iterparse(in_file_name, tag = ns + 'entry', events = ('start', 'end'))
    #context = etree.iterparse(in_file_name, events = ('start', 'end')) 
    for event, element in context:
        strip_name_space(element)
        if event != 'end':
            continue
        if entries < 100000:
            entries +=1
            outfile.write(etree.tostring(element, encoding='unicode'))
            outfile.flush()
        else:
            #close old file, make new file, reset entries and increment file file_count
            entries = 0
            make_file_footer(outfile)
            print("new file: " + str(file_count))
            out_file_name = out_file_base_name + "/slice_" + str(file_count) + ".xml"
            outfile = open(out_file_name,'w')
            make_file_header(outfile)
            file_count += 1
        # manual garbage collection
        # memory cleaning code from:
        # https://stackoverflow.com/questions/12160418/
        # why-is-lxml-etree-iterparse-eating-up-all-my-memory
        element.clear()
        # Also eliminate now-empty references from the root node to element
        for ancestor in element.xpath('ancestor-or-self::*'):
            while ancestor.getprevious() is not None:
                del ancestor.getparent()[0]
    del context
    print("total files: " + str(file_count))
    #close last file        
    make_file_footer(outfile)

def main():
    start_time = time.time()
    ns = "{http://uniprot.org/uniref}"
    res_dict = json.load(open("/home/steve/eclipse-workspace/PyProtPlacer/res.json"))
    in_file_name = res_dict.get("uniref50_parse_file_name")
    out_file_base_name = res_dict.get("uniref50_base_file_name")
    slice_file(in_file_name,out_file_base_name,ns)
    end_time = time.time()
    print("System terminates normally in: " + str(end_time - start_time) + "seconds\n")
    
if __name__ == "__main__":
    main()