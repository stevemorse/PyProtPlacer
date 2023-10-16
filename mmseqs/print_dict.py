
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
    'Host cellular thylakoid membrane':'host thylakoid membrane','Host lysosome':'host cell lysosome'}
    
    start_time = time.time()
    count_file = open("/home/steve/Desktop/mmseq2/trans_dict.txt", 'w')
    count_file.write("{:<30} {:<10}".format("swiss prot location name","go term"))
    for swiss_prot,go_term in translation_dict:
            count_file.write("{:<30} {:<10}".format(swiss_prot,go_term))
    end_time = time.time()
    print("System terminates normally in: " + str(end_time - start_time) + "seconds\n")
    
if __name__ == "__main__":
    main()