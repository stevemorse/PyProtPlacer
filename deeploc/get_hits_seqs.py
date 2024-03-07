from lxml import etree
import time
import json
import re

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

def get_seq(in_file_name,ns):
    loc_dict = {}
    acc= ''
    seq = ''
    context = etree.iterparse(in_file_name, tag = ns + 'entry', events = ('start', 'end'))
    for event, element in context:
        #print(event,element)
        if event != 'end':
            continue
        strip_name_space(element)
        print(event,element.tag)
        if element.tag == 'entry':
            #find accession for swiss prot
            if ns == "{http://uniprot.org/uniprot}":
                for accession in element.findall(ns + 'accession'):
                    strip_name_space(accession)
                    acc = accession.text    
                for child in element.findall(ns + 'sequence'):
                    strip_name_space(child)
                    seq = child.text.strip()
            elif ns == "{http://uniprot.org/uniref}":
                #find accession for uniref50
                for member in element.findall(ns + 'representativeMember'):
                    #print(etree.tostring(member, encoding='unicode'))
                    strip_name_space(member)
                    for dbReferenceType in member.findall(ns + 'dbReference'):
                        #print(etree.tostring(dbReferenceType, encoding='unicode'))
                        strip_name_space(dbReferenceType)
                        for properties in dbReferenceType.findall(ns + 'property'):
                            #print(etree.tostring(properties, encoding='unicode'))
                            strip_name_space(properties)
                            if properties.attrib.get('type') == 'UniProtKB accession':
                                #print(etree.tostring(properties, encoding='unicode'))
                                acc = properties.attrib.get('value')
                                #print(acc)

                    for child in element.findall(ns + 'sequence'):
                        strip_name_space(child)
                        seq = child.text.strip()

            else:
                print("error...schema not supported")
        loc_dict.update({acc: seq})
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
    return loc_dict

def find_seq_of_hits(in_file_name, out_file_name, ns, seq_dict):
    outfile = open(out_file_name,'w')
    line_num = 0
    for line in open(in_file_name, 'r'):
        line_num += 1
        if line_num > 2:
            #line_items = line.split("\s")
            line_items = re.split(r'\s{2,}', line)
            accession = line_items[1]
            print(accession + "\n")
            loc = line_items[3]
            print(loc + "\n")
            sup_loc = line_items[4]
            print(sup_loc + "\n")
            ecode = line_items[5]
            print(ecode + "\n")
            if accession in seq_dict:
                seq = seq_dict.get(accession)
                outfile.write(">accession|" + accession)
                outfile.write("|location|" + loc)
                outfile.flush()
                outfile.write("|super location|" + sup_loc)
                outfile.flush()
                if ns == "{http://uniprot.org/uniprot}":
                    outfile.write("|ecode|" + ecode + "|\n")
                elif ns == "{http://uniprot.org/uniref}":
                    outfile.write("|gocode|" + ecode + "|\n")
                else:
                    print("namespace not supported")
                outfile.write(seq)
                outfile.write("\n")
    outfile.flush()
    outfile.close()

def main():
    start_time = time.time()
    res_dict = json.load(open("/home/steve/PycharmProjects/PyProtPlacer/res.json"))
    #ns = "{http://uniprot.org/uniprot}"
    ns = "{http://uniprot.org/uniref}"
    '''
    parse_file_name = res_dict.get("sprot_parse_file_name")
    in_file_name = res_dict.get("sprot_out_file_name")
    out_file_name = res_dict.get("sprot_seq_out_file_name")
    '''
    parse_file_name = res_dict.get("uniref50_parse_file_name")
    in_file_name = res_dict.get("uniref50_out_file_name")
    out_file_name = res_dict.get("uniref_seq_out_file_name")


    seq_dict = get_seq(parse_file_name,ns)
    find_seq_of_hits(in_file_name,out_file_name,ns,seq_dict)
    end_time = time.time()
    print("System terminates normally in: " + str(end_time - start_time) + "seconds\n")
    
if __name__ == "__main__":
    main()
