
import time
def main():
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
    'Basal cell membrane':'cell membrane','Glyoxysome membrane':'glyoxysomal membrane','Uropodium':'uropod','Nuclear pore complex':'nuclear pore'}
    start_time = time.time()
    # Remove duplicate values in dictionary
    # Using loop
    temp = []
    res = dict()
     
    for key, val in translation_dict.items():
       
        if val not in temp:
            temp.append(val)
            res[key] = val
     
    # printing result
    print("The dictionary after values removal : " + str(res))
    print("System terminates normally in: " + str(end_time - start_time) + "seconds\n")
    
if __name__ == "__main__":
    main()