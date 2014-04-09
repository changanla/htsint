#!/usr/bin/env python
"""
library of functions for use with the GeneOntology class
"""

import os,sys,re
from htsint import __basedir__

sys.path.append(__basedir__)
try:
    from configure import CONFIG
except:
    CONFIG = None

def get_ontology_file():
    """
    check for presence of ontology file
    raise exception when not found
    return the file path
    """

    if CONFIG == None:
        raise Exception("You must create a configure.py before GeneOntology")

    dataDir = CONFIG['data']

    ontologyFile = os.path.join(dataDir,'go.obo')
    if os.path.exists(ontologyFile) == False:
        raise Exception("Could not find 'go.obo' -- did you run FetchDbData.py?")

    return ontologyFile

def read_ontology_file():
    """
    read the ontology file to find term-term edges
    store all the relationships in a dictionary
    """

    ontologyFile = get_ontology_file()
    fid = open(ontologyFile,'r')
    termCount = 0
    goId = None
    goDict = {"cellular_component":{},
              "molecular_function":{},
              "biological_process":{}}

    def add_term(goNamespace,source,sink):
        #print source,sink
        if len(sink) != 1 or source == sink[0]:
            return
        if not re.search("GO\:",source) or not re.search("GO\:",sink[0]):
            raise Exception("Invalid go id in ontology file: %s, %s"%(source,sink[0]))

        if goDict[goNamespace].has_key(source) == False:
            goDict[goNamespace][source] = set([])
        goDict[goNamespace][source].update(sink)

    for linja in fid.readlines():
        linja = linja[:-1]

        ## find go id
        if re.search("^id\:",linja):
            goId = re.sub("^id\:|\s+","",linja)
            goName,goNamespace = None,None
            is_a,part_of = None,None
            isObsolete = False
            termCount += 1
            continue 

        ## find a few go id attributes
        if re.search("^name\:",linja):
            goName = re.sub("^name\:\s+","",linja)
        if re.search("^namespace\:",linja):
            goNamespace = re.sub("^namespace\:\s+","",linja)
        if re.search("^def\:",linja):
            goDef = re.sub("^def\:\s+","",linja)
            if re.search("OBSOLETE\.",goDef):
                isObsolete = True

        ## ignore obolete terms
        if goId == None or isObsolete == True:
            continue

        ## add term relationships (is_a)
        if re.search("^is\_a\:",linja):
            is_a = re.sub("^is\_a\:\s+","",linja)
            is_a_sink = re.findall("GO\:\d+",is_a)
            add_term(goNamespace,goId,is_a_sink)

        ## other term relationships
        #if re.search("^relationship\:",linja):
        #    part_of_sink = re.findall("GO\:\d+",linja)
        #    add_term(goNamespace,goId,part_of_sink)
            
    return goDict

def get_idmapping_file():
    """
    check for presence of the annotation file
    raise exception when not found
    return the file path
    """

    if CONFIG == None:
        raise Exception("You must create a configure.py before GeneOntology")

    dataDir = CONFIG['data']
    idmappingFile = os.path.join(dataDir,'idmapping.tb.db')
    if os.path.exists(idmappingFile) == False:
        raise Exception("Could not find 'idmapping.tb.db' -- did you run FetchDbData.py?")

    return idmappingFile

    
def read_idmapping_file():
    """
    read the idmapping file into a dictionary
    ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/idmapping/README
    
    target file is idmapping.tb from the uniprot knowledgebase

    1. UniProtKB-AC
    2. UniProtKB-ID
    3. GeneID (EntrezGene)
    4. RefSeq
    5. GI
    6. PDB
    7. GO
    8. IPI
    9. UniRef100
    10. UniRef90
    11. UniRef50
    12. UniParc
    13. PIR
    14. NCBI-taxon
    15. MIM
    16. UniGene
    17. PubMed
    18. EMBL
    19. EMBL-CDS
    20. Ensembl
    21. Ensembl_TRS
    22. Ensembl_PRO
    23. Additional PubMed
    """

    idmappingFile = get_idmapping_file()
    idmappingFid = open(idmappingFile,'rU')
    result = {}
    allTaxa = set([])

    debug = 0

    for record in idmappingFid:
        record = record[:-1].split("\t")
        debug += 1
        
        #print len(record),record
        uniprotKbAc = record[0]
        uniprotKbId = record[1]
        geneId = record[2]
        refseq = record[3]

        print debug, uniprotKbId, geneId, refseq

        if debug > 5:
            sys.exit()

        continue


        ## check that it is a uniprot entry
        if record[0][0] == "!":
            continue
        if record[0] != 'UniProtKB':
            print "houston!!", record[0]
            continue
        
        dbObjectId = record[1]
        dbObjectSymbol = record[2]
        goID = record[4]
        dbReference = record[5]
        evidenceCode = record[6]
        aspect = record[8]
        dbObjectType = record[11]
        taxon = re.sub("taxon:","",record[12])
        date = record[13]
        assignedBy = record[14]

        ## ignore annotations with multiple species
        if re.search("\|",taxon):
            continue

        if not result.has_key(dbObjectId):
            result[dbObjectId] = {'names':set([]),'annots':{},'taxon':taxon}

        result[dbObjectId]['annots'][goID] = [aspect,evidenceCode]
        result[dbObjectId]['names'].update([dbObjectSymbol])
        allTaxa.update([taxon])

    return list(allTaxa),result





"""
    for record in idmappingFid:
        record = record[:-1].split("\t")
        debug += 1
        
        print record

        if debug > 5:
            sys.exit()

        continue


        ## check that it is a uniprot entry
        if record[0][0] == "!":
            continue
        if record[0] != 'UniProtKB':
            print "houston!!", record[0]
            continue
        
        dbObjectId = record[1]
        dbObjectSymbol = record[2]
        goID = record[4]
        dbReference = record[5]
        evidenceCode = record[6]
        aspect = record[8]
        dbObjectType = record[11]
        taxon = re.sub("taxon:","",record[12])
        date = record[13]
        assignedBy = record[14]

        ## ignore annotations with multiple species
        if re.search("\|",taxon):
            continue

        if not result.has_key(dbObjectId):
            result[dbObjectId] = {'names':set([]),'annots':{},'taxon':taxon}

        result[dbObjectId]['annots'][goID] = [aspect,evidenceCode]
        result[dbObjectId]['names'].update([dbObjectSymbol])
        allTaxa.update([taxon])

    return list(allTaxa),result
"""