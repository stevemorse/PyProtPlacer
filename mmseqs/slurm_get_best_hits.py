from lxml import etree
import time
import json
import networkx
import obonet
import concurrent.futures
from threading import Lock
import os

def count_files(dir_path):
    # code based on: https://pynative.com/python-count-number-of-files-in-a-directory/
    count = 0
    # Iterate directory
    for path in os.listdir(dir_path):
        # check if current path is a file
        if os.path.isfile(os.path.join(dir_path, path)):
            count += 1
    print('File count:', count) 
    
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
'''
def get_loc(go_code,graph):
    # code from: https://notebook.community/dhimmel/obo/examples/go-obonet
    id_to_name = {id_: data.get('name') for id_, data in graph.nodes(data=True)}
    obsolete_list = ["GO:0016580"]
    name = "no location"
    if go_code not in obsolete_list:
        name = id_to_name[go_code]
    return name
'''
def get_super_locations(go_code,graph):
    # code from: https://notebook.community/dhimmel/obo/examples/go-obonet
    id_to_name = {id_: data.get('name') for id_, data in graph.nodes(data=True)}
    return sorted(id_to_name[superterm] for superterm in networkx.descendants(graph,go_code))

def get_location_class(go_code,graph):
    # code from: https://notebook.community/dhimmel/obo/examples/go-obonet
    id_to_name = {id_: data.get('name') for id_, data in graph.nodes(data=True)}
    # chloroplast:"GO:0009507"
    #    host cell chloroplast:"GO:0033652"
    # mitochondrion:"GO:0005739"
    #    host cell mitochondrion:"GO:0033650"
    #    host cell mitochondrial envelope:"GO:0044190"
    #    host cell mitochondrial membrane:"GO:0044191"
    #    host cell mitochondrial intermembrane space:"GO:0072492"
    #    mitochondrial chromosome:"GO:0000262"
    # endoplasmic reticulum:"GO:0005783"
    #    host cell endoplasmic reticulum:"GO:0044165"
    #    host cell endoplasmic reticulum lumen:"GO:0044166"
    # peroxisome:"GO:0005777","GO:0019818"
    #    host cell peroxisome:"GO:0120149"
    # nucleus:"GO:0005634"
    #    nuclear envelope:"GO:0005635","GO:0005636"
    #    nuclear outer membrane:"GO:0005640"
    #    nuclear outer membrane-endoplasmic reticulum membrane network:"GO:0042175"
    #    host cell nucleus:"GO:0042025","GO:0033649"
    #    host chromosome:"GO:0044383"
    #    nuclear lumen:"GO:0031981"
    #    nuclear chromosome:"GO:0000228"
    # secretory pathway elements not including ER components
    #    Golgi apparatus:"GO:0005794"
    #    secretory vesicle:"GO:0099503"
    #    transport vesicle:"GO:0030133"
    #    secretory granule:"GO:0030141"
    #    COPI-coated vesicle:"GO:0030137"
    #    COPII-coated ER to Golgi transport vesicle:"GO:0030134","GO:0030138","GO:0140045"
    #    host cell Golgi apparatus:"GO:0044177"
    #    postsynaptic Golgi apparatus:"GO:0150051" ?
    #    Golgi-associated vesicle:"GO:0005798"
    #    endocytic vesicle:"GO:0030139" ?
    #    GARP complex:"GO:0000938" ?
    #    host cell cytoplasmic vesicle:"GO:0044161" ?
    chloroplast_list = ["GO:0009507","GO:0033652"]
    mitochondrion_list = ["GO:0005739","GO:0033650","GO:0044190","GO:0044191","GO:0072492","GO:0000262"]
    endoplasmic_reticulum_list = ["GO:0005783","GO:0044165","GO:0044166"]
    peroxisome_list = ["GO:0005777","GO:0019818","GO:0120149"]
    nucleus_list = ["GO:0005634","GO:0005635","GO:0005636","GO:0005640","GO:0042175","GO:0042025","GO:0033649","GO:0044383",\
                    "GO:0031981","GO:0000228"]
    secretory_pathway_list = ["GO:0005794","GO:0099503","GO:0030133","GO:0030141","GO:0030137","GO:0030134","GO:0030138",\
                              "GO:0140045","GO:0044177","GO:0150051","GO:0005798","GO:0030139","GO:0000938","GO:0044161"]
    
    loc_name = "no location class"
    
    if go_code in chloroplast_list:
        loc_name = "chloroplast"
    super_list = get_super_locations(go_code,graph)
    for code in chloroplast_list:
        if id_to_name[code] in super_list:
            loc_name = "chloroplast"
            break
    
    if go_code in mitochondrion_list:
        loc_name = "mitochondrion"
    super_list = get_super_locations(go_code,graph)
    for code in mitochondrion_list:
        if id_to_name[code] in super_list:
            loc_name = "mitochondrion"
            break
        
    if go_code in endoplasmic_reticulum_list:
        loc_name = "endoplasmic reticulum"
    super_list = get_super_locations(go_code,graph)
    for code in endoplasmic_reticulum_list:
        if id_to_name[code] in super_list:
            loc_name = "endoplasmic reticulum"
            break
        
    if go_code in peroxisome_list:
        loc_name = "peroxisome"
    super_list = get_super_locations(go_code,graph)
    for code in peroxisome_list:
        if id_to_name[code] in super_list:
            loc_name = "peroxisome"
            break
        
    if go_code in nucleus_list:
        loc_name = "nucleus"
    super_list = get_super_locations(go_code,graph)
    for code in nucleus_list:
        if id_to_name[code] in super_list:
            loc_name = "nucleus"
            break
        
    if go_code in secretory_pathway_list:
        loc_name = "secretory pathway"
    for code in secretory_pathway_list:
        super_list = get_super_locations(go_code,graph)
        if id_to_name[code] in super_list:
            loc_name = "secretory pathway"
            break
        
    return loc_name 
  
def process_loc_hit(loc,loc_count_dict):
    if loc in loc_count_dict:
        current_count = loc_count_dict.get(loc)
        current_count += 1
        loc_count_dict[loc] = current_count
    else:
        loc_count_dict.update({loc:1})
    return loc_count_dict

def make_count_output(count_out_file_name,loc_count_dict,superloc_count_dict,hits):
    count_file = open(count_out_file_name, 'w')
    count_file.write("{:<30} {:<10}".format("location","count"))
    count_file.write("\n")
    for loc, count in sorted(loc_count_dict.items(),key=lambda item:item[1],reverse=True):
        count_file.write("{:<30} {:<10}".format(loc,count))
        count_file.write("\n")
    count_file.write("\n\n\n")
    count_file.write("{:<30} {:<10}".format("location","count"))
    count_file.write("\n")
    for loc, count in sorted(superloc_count_dict.items(),key=lambda item:item[1],reverse=True):
        count_file.write("{:<30} {:<10}".format(loc,count))
        count_file.write("\n")
    count_file.write("\n\n\n")
    count_file.write("total hits in: " + count_out_file_name + str(hits))

def get_go_loc(location):
    # this function translates old non-GO names found in swiss-Prot to proper GO terms
    translation_dict = {'Cell membrane':'plasma membrane','Virion':'virion component','Secreted':'no location class',\
    'Nucleus speckle':'nucleus','Mitochondrion matrix':'mitochondrion','Golgi apparatus membrane':'Golgi membrane',\
    'Acrosome':'acrosome vesicle','Flagellum axoneme':'axoneme','Cilium axoneme':'axoneme',\
    'Host endoplasmic reticulum-Golgi intermediate compartment':\
    'host cell endoplasmic reticulum-Golgi intermediate compartment membrane',\
    'Host endoplasmic reticulum lumen':'host cell endoplasmic reticulum lumen','Flagellum':'cilium',\
    'Nucleus envelope':'nuclear envelope','Target cell membrane':'plasma membrane',\
    'Apical cell membrane':'apical plasma membrane','Nucleus membrane':'nuclear membrane',\
    'Vacuole membrane':'plant-type vacuole membrane','Basolateral cell membrane':'basolateral plasma membrane',\
    'Lysosome membrane':'lysosomal membrane','Peroxisome membrane':'peroxisomal membrane',\
    'Microsome':'intracellular membrane-bounded organelle','Telomere':'chromosome, telomeric region',\
    'Cell inner membrane':'plasma membrane','Postsynaptic cell membrane':'postsynaptic membrane','Z line':'Z disc',\
    'Perinuclear region':'perinuclear region of cytoplasm','Phagosome':'phagocytic vesicle',\
    'Golgi stack membrane':'Golgi cisterna membrane','Presynaptic cell membrane':'presynaptic membrane',\
    'Coated pit':'clathrin-coated pit','Lateral cell membrane':'lateral plasma membrane','M line':'M band',\
    'Periplasm':'periplasmic space','Microsome membrane':'intracellular membrane-bounded organelle',\
    'Phagosome membrane':'phagocytic vesicle membrane','Contractile vacuole membrane':'contractile vacuolar membrane',\
    'Midbody ring':'Flemming body','Mitochondrion outer membrane':'mitochondrial outer membrane',\
    'Cellular thylakoid membrane':'thylakoid membrane','Mitochondrion inner membrane':'mitochondrial inner membrane',\
    'Synaptosome':'axon terminus','Cilium basal body':'ciliary basal body','Actin patch':'actin cortical patch',\
    'Preautophagosomal structure membrane':'Golgi membrane','Centromere':'chromosome, centromeric region',\
    'Mitochondrion nucleoid':'mitochondrial nucleoid','Mitochondrion membrane':'mitochondrial membrane',\
    'Preautophagosomal structure':'Golgi apparatus','Cellular chromatophore membrane':'organellar chromatophore membrane',\
    'Host cytoplasm':'host cell cytoplasm','Cytoplasmic granule':'cytoplasmic ribonucleoprotein granule',\
    'Host nucleus':'host cell nucleus','Host peroxisome':'host cell peroxisome','Cilium membrane':'ciliary membrane',\
    'Nucleus matrix':'nuclear matrix','Secretory vesicle membrane':'secretory granule membrane',\
    'Forespore outer membrane':'prospore membrane','Nucleus outer membrane':'nuclear outer membrane',\
    'Nucleus inner membrane':'nuclear inner membrane','Virion tegument':'viral tegument','Nucleus matrix':'nuclear matrix',\
    'Calyx':'calyx of Held','Uropodium':'uropod','Inflammasome':'canonical inflammasome complex','Host cytosol':'host cell cytosol',\
    'Host endoplasmic reticulum':'host cell endoplasmic reticulum','Stress granule':'cytoplasmic stress granule',\
    'Zymogen granule lumen':'zymogen granule','Cytoplasmic granule membrane':'cytolytic granule membrane',\
    'Bud neck':'cellular bud neck septin ring organization','Parasitophorous vacuole membrane':'symbiont-containing vacuolar membrane network',\
    'Host Golgi apparatus':'host cell Golgi apparatus','Fimbrium':'pilus','Mitochondrion intermembrane space':'mitochondrial intermembrane space',\
    'acrosome vesicle':'acrosomal vesicle','Flagellum basal body':'bacterial-type flagellum basal body',\
    'Flagellum membrane':'ciliary membrane','Perispore':'exosporium','Spore':'exosporium','Host endosome membrane':'host cell endosome membrane',\
    'Bacterial flagellum basal body':'bacterial-type flagellum basal body','Bacterial flagellum':'bacterial-type flagellum assembly',\
    'Invadopodium':'plasma membrane','Host trans-Golgi network':'trans-Golgi network','Host apical cell membrane':'host cell membrane',\
    'Basal cell membrane':'cell membrane','Glyoxysome membrane':'glyoxysomal membrane','Uropodium':'uropod','Nuclear pore complex':'nuclear pore',\
    'Forespore':'intracellular immature spore','intracellular immature spore':'intracellular immature spore','acrosome vesicle':'acrosomal vesicle',\
    'Host cell inner membrane':'host cell membrane','Host endoplasmic reticulum membrane':'host cell endoplasmic reticulum membrane',\
    'Apical lamina':'apical lamina of hyaline layer','Host membrane':'host cell membrane','Host Golgi apparatus membrane':'host cell Golgi membrane',\
    'Inner membrane complex':'inner membrane pellicle complex','Parasitophorous vacuole lumen':'symbiont-containing vacuole',\
    'Lysosome lumen':'lysosomal lumen','cell membrane':'plasma membrane','Bud':'budding cell bud growth','Peribacteroid space':'peribacteroid fluid',\
    'Host perinuclear region':'host cell perinuclear region of cytoplasm','Host mitochondrion membrane':'host cell mitochondrial membrane',\
    'Acrosome inner membrane':'inner acrosomal membrane','Peroxisome matrix':'peroxisomal matrix',\
    'Host rough endoplasmic reticulum membrane':'host cell rough endoplasmic reticulum membrane','Host microsome membrane':'host cell cytoplasmic vesicle membrane',\
    'Host plasmodesma':'host cell plasmodesma','Host nucleolus':'host cell nucleolus','Prevacuolar compartment membrane':'late endosome membrane',\
    'Host mitochondrion':'host cell mitochondrion','Inner mitochondrial membrane':'host cell mitochondrion','Acrosome membrane':'acrosomal membrane',\
    'COPII-coated vesicle membrane':'ER to Golgi transport vesicle membrane','Host endosome':'host cell endosome',\
    'Host cytoplasmic vesicle':'host cell cytoplasmic vesicle','Host lipid droplet':'host cell lipid droplet',\
    'Host cytoplasmic vesicle membrane':'host cell cytoplasmic vesicle membrane','Host filopodium':'host cell filopodium',\
    'Host late endosome membrane':'host cell late endosome membrane','Golgi apparatus lumen':'Golgi lumen','Surface film':'cell surface',\
    'Bud tip':'cellular bud tip','Vacuole lumen':'vacuole','Invadopodium':'plasma membrane','Spore core':'exosporium',\
    'Acrosome outer membrane':'outer acrosomal membrane','Host chloroplast envelope':'chloroplast envelope','Golgi outpost':'postsynaptic Golgi apparatus',\
    'Apicolateral cell membrane':'apicolateral plasma membrane','Host early endosome':'early endosome','Spore membrane':'exosporium',\
    'Cellular thylakoid lumen':'thylakoid lumen','Forespore inner membrane':'intracellular immature spore','Spore coat':'spore wall',\
    'Spore outer membrane':'outer endospore membrane','Zona pellucida':'egg coat','Extracellular vesicle membrane':'prominosome',\
    'Host synapse':'host cell synapse','Host presynaptic cell membrane':'host cell presynaptic membrane','Host secretory vesicle':'secretory vesicle',\
    'Host synaptic vesicle membrane':'host cell synaptic vesicle membrane','Prevacuolar compartment':'late endosome','Gem':'membrane raft',\
    'Host nucleus membrane':'host cell nuclear membrane','Host nucleus matrix':'host cell nuclear matrix','Host nucleoplasm':'host cell nucleoplasm',\
    'Host nucleus inner membrane':'host cell nuclear inner membrane','Secretory vesicle lumen':'clathrin-sculpted acetylcholine transport vesicle lumen',\
    'Host endomembrane system':'host cell endomembrane system','Myelin membrane':'myelin sheath','Host cis-Golgi network':'cis-Golgi network',\
    'Synaptic cell membrane':'synaptic membrane','Parasitophorous vacuole':'symbiont-containing vacuole',\
    'Host mitochondrion outer membrane':'host cell mitochondrial outer membrane','Nucleus lamina':'nuclear lamina','Spore polar tube':'endospore',\
    'Pseudopodium tip':'pseudopodium membrane','Tegument membrane':'host-symbiont bicellular tight junction',\
    'Barrier septum':'division septum site selection','Acrosome lumen':'acrosomal lumen','Bud membrane':'cellular bud membrane',\
    'Host rough endoplasmic reticulum':'host cell rough endoplasmic reticulum','COPII-coated vesicle':'COPII-coated ER to Golgi transport vesicle',\
    'Target cell':'cellular_component','Target cell cytoplasm':'cytoplasm','Flagellar pocket':'ciliary pocket',\
    'Host nucleus envelope':'host cell nuclear envelope','Host nucleus lamina':'host cell nuclear lamina','Host periplasm':'host cell periplasmic space',\
    'Host vacuole':'vacuole','Host pathogen-containing vacuole':'pathogen-containing vacuole',\
    'Host pathogen-containing vacuole membrane':'pathogen-containing vacuole membrane','Nucleus intermembrane space':'nuclear envelope lumen',\
    'Cytoplasmic granule lumen':'cytolytic granule lumen','Host cis-Golgi network membrane':'cis-Golgi network membrane',\
    'Host endoplasmic reticulum-Golgi intermediate compartment membrane':'endoplasmic reticulum-Golgi intermediate compartment',\
    'Spore cortex':'endospore cortex','Host smooth endoplasmic reticulum membrane':'host cell smooth endoplasmic reticulum membrane',\
    'Host':'host cellular component','Prospore':'intracellular immature spore','Mitosome matrix':'mitosome','Mitosome membrane':'mitosome',\
    'Host phagosome':'phagocytic vesicle','Phagosome lumen':'early phagosome lumen','Nucleolus fibrillar center':'fibrillar center',\
    'Forespore membrane':'prospore membrane','Mitochondrion envelope':'mitochondrial envelope',\
    'Host cellular thylakoid membrane':'host thylakoid membrane','Host lysosome':'host cell lysosome',\
    'Forespore intermembrane space':'intracellular immature spore','acrosome vesicle':'acrosomal vesicle','cell membrane':'plasma membrane',\
    'Host mitochondrion inner membrane':'host cell mitochondrial inner membrane','Invadopodium membrane':'plasma membrane',\
    'endospore':'cellular anatomical entity','Endoplasmic reticulum-Golgi intermediate compartment lumen':'Endoplasmic reticulum-Golgi intermediate compartment',\
    'Archaeal flagellum':'archaeal-type flagellum','Podosome membrane':'podosome','Paranodal septate junction':'paranodal junction',\
    'Host trans-Golgi network membrane':'trans-Golgi network membrane','Host early endosome membrane':'early endosome membrane',\
    'Hydrogenosome membrane':'hydrogenosomal membrane'}
    
    if location in translation_dict:
        location = translation_dict.get(location) 
    return location
  
def is_keep_upper_case(location):
    keep_upper_case_list = ['P-body','Z disc','Golgi apparatus','Golgi cisterna membrane',\
                            'I band','M band','Flemming body','Golgi membrane','Cvt vesicle membrane',\
                            'COPI-coated vesicle membrane','S-layer','PML body','Cajal body','Golgi stack',\
                            'T-tubule','A band','H zone','ER to Golgi transport vesicle membrane',\
                            'Golgi lumen','COPII-coated ER to Golgi transport vesicle',\
                            'COPI-coated vesicle']
    return location in keep_upper_case_list
        
def get_locations(in_file_name,graph,ns,loc_dict,lock):
    key_error_log_file = open("/home/steve/Desktop/mmseq2/keyErrorLog.txt", 'w')
    key_error_list = []
    local_dict = {}
    name_to_id = {data['name']: id_ for id_, data in graph.nodes(data=True) if 'name' in data}
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
                for child in element.findall(ns + 'comment'):
                    strip_name_space(child)
                    if child.attrib.get('type') == 'subcellular location':
                        for subloc in child.findall(ns + 'subcellularLocation'):
                            strip_name_space(subloc)
                            for location in subloc.findall(ns + 'location'):
                                strip_name_space(location)
                                loc = location.text.strip()
                                if location.attrib.get('evidence') != None:
                                    ecode = location.attrib.get('evidence')
                                else:
                                    ecode = "no ecode"
                                print('loc: ' + loc)
                                clean_loc = get_go_loc(loc)
                                print('clean_loc: ' + clean_loc)
                                #code to recover bad swiss prot names
                                if clean_loc not in key_error_list:
                                    try:
                                        if is_keep_upper_case(clean_loc):
                                            go_code = name_to_id[clean_loc]
                                        else:
                                            go_code = name_to_id[clean_loc[0].lower() + clean_loc[1:]]
                                    except KeyError:
                                        key_error_list.append(clean_loc)
                                        print("key error on: " + clean_loc + " ***********number of bad names now: " + str(len(key_error_list)))
                                        print("\n")
                                        key_error_log_file.write("key error on: " + clean_loc + " bad names now: " + str(len(key_error_list)))
                                        key_error_log_file.write("\n")
                                        key_error_log_file.flush()
                                    super_class = get_location_class(go_code,graph)
                                    local_dict.update({acc:(loc,super_class,ecode)})
                                    print(str(len(loc_dict)) + "\t",acc + " : ",loc + "\t",super_class + "\t",ecode + "\n")
            elif ns == "{http://uniprot.org/uniref}":
                # code from: https://notebook.community/dhimmel/obo/examples/go-obonet
                id_to_name = {id_: data.get('name') for id_, data in graph.nodes(data=True)}
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
                    for properties in element.findall(ns + 'property'):
                        if properties.attrib.get('type') == 'GO Cellular Component':
                            #print(etree.tostring(properties, encoding='unicode'))
                            go_code = properties.attrib.get('value')
                            loc = "no location"
                            super_class = "no location class"
                            if go_code not in key_error_list:
                                try:
                                    loc = id_to_name[go_code]
                                except KeyError:
                                    key_error_list.append(go_code)
                                    key_error_log_file.write("key error on: " + go_code + " bad codes now: " + str(len(key_error_list)))
                                    key_error_log_file.write("\n")
                                    key_error_log_file.flush()
                            if loc != "no location":
                                super_class = get_location_class(go_code,graph)
                            print(acc + " : " + go_code + " : " + " : " + loc + " : " + super_class)
                            local_dict.update({acc:(loc,super_class,go_code)})                
            else:
                print("error...schema not supported")
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
    key_error_log_file.close()
    for key in key_error_list:
        print("failed key: " + key)           
        with lock:
            loc_dict |= local_dict

def find_best_hits(in_file_name,out_file_name,loc_dict,ns,count_out_file_name):  
    line_number = 0
    last_query = "none"
    outfile = open(out_file_name,'w')
    loc_count_dict = {}
    superloc_count_dict = {}
    hits = 0
    if ns == "{http://uniprot.org/uniprot}":
        outfile.write("{:<60} {:<15} {:<15} {:<35} {:25} {:<10}".format("query","accession","evalue","location","super location","ecode"))
        outfile.write("\n")
    elif ns == "{http://uniprot.org/uniref}":
        outfile.write("{:<60} {:<15} {:<15} {:<35} {:<25} {:<10}".format("query","accession","evalue","location","super location","go_code"))
        outfile.write("\n")
    else:
        print('error...schema not supported')
    outfile.write("\n")
    for line in open(in_file_name, 'r'):
        line_number +=1
        if line_number == 1:
            continue
        elif line_number > 1: 
            tabs = line.split()
            #tabs = re.findall(r'\S+', line)
            query = tabs[0]
            accession = tabs[1]
            evalue = str(tabs[2])
            #print(query,accession,evalue)
            if query == last_query:
                continue
        else:
            print("OOPS...it should not be possible to get this message")
        if accession in loc_dict:
            last_query = query
            location = loc_dict.get(accession)
            hits += 1
            loc_count_dict = process_loc_hit(location[0],loc_count_dict)
            superloc_count_dict = process_loc_hit(location[1],loc_count_dict)
            outfile.write("{:<60} {:<15} {:<15} {:<35} {:<25} {:<10}".format(query,accession,evalue,location[0],location [1],location[2]))
            outfile.write("\n")
    outfile.close()
    make_count_output(count_out_file_name,loc_count_dict,superloc_count_dict,hits) 
    
def main():
    start_time = time.time()
    res_dict = json.load(open("/home/steve/eclipse-workspace/PyProtPlacer/res.json"))
    #ns = "{http://uniprot.org/uniprot}"
    ns = "{http://uniprot.org/uniref}"
    '''
    parse_file_name = res_dict.get("sprot_parse_file_name")
    count_out_file_name = res_dict.get("sprot_count_out_file_name")
    in_file_name = res_dict.get("sprot_in_file_name")
    out_file_name = res_dict.get("sprot_out_file_name")
    '''
    parse_file_name = res_dict.get("uniref50_parse_file_name")
    #parse_file_name = res_dict.get("test_uniref50_parse_file_name")
    count_out_file_name = res_dict.get("uniref50_count_out_file_name")
    in_file_name = res_dict.get("uniref50_in_file_name")
    out_file_name = res_dict.get("uniref50_out_file_name")
    
    print("start ontology load")
    graph = obonet.read_obo(res_dict.get("ontology_to_load"))
    print("ontology loaded")
    dir_path = res_dict.get("uniref50_base_file_name")
    lock = Lock()
    loc_dict = {}
    total_files = count_files(dir_path)
    base_file_name = res_dict.get("uniref50_base_file_name")
    with concurrent.futures.ThreadPoolExecutor as executor:
        for file_count in range(total_files):
            parse_file_name =  base_file_name + "/slice_" + str(file_count) + ".xml"
            executor.submit(get_locations,parse_file_name,graph,ns,loc_dict,lock)
    find_best_hits(in_file_name,out_file_name,loc_dict,ns,count_out_file_name)
    end_time = time.time()
    print("System terminates normally in: " + str(end_time - start_time) + "seconds\n")
    
if __name__ == "__main__":
    main()
