#!/usr/bin/env python
# -*- coding: utf-8 -*-


#
# This is a simple script to parse the genemap2.txt file that
# can be downloaded from https://omim.org/
#
# The file can downloaded from https://omim.org/downloads
# (registration required).
#


# Imports
import sys
import re

# print header
h = ["approvedGeneSymbol", "geneSymbols", "mimNumber","phenotypeText", "phenotypeMimNumber","inheritances"]
print("\t".join(h))

# Read from stdin
for line in sys.stdin:

    # Skip comments
    if line.startswith('#'):
        continue

    # Strip trailing new line
    line = line.strip('\n')

    # Get the values
    valueList = line.split('\t')

    # Get the fields
    chromosome = valueList[0]
    genomicPositionStart = valueList[1]
    genomicPositionend = valueList[2]
    cytoLocation = valueList[3]
    computedCytoLocation = valueList[4]
    mimNumber = valueList[5]
    geneSymbols = valueList[6]
    geneName = valueList[7]
    approvedGeneSymbol = valueList[8]
    entrezGeneID = valueList[9]
    ensemblGeneID = valueList[10]
    comments = valueList[11]
    phenotypeString = valueList[12]
    mouse = valueList[13]

    # Définir une fonction pour modifier le mode de transmission
    def my_inherintance(inheritance):
        inheritance = inheritance.strip()
        replacements = {'Autosomal': 'A', ' recessive': 'R', ' dominant': 'D', 'Y-linked': 'YL', 'X-linked': 'XL'}
        inheritance=re.sub('({})'.format('|'.join(map(re.escape, replacements.keys()))), lambda m: replacements[m.group()], inheritance)

        return  inheritance

    # Skip empty phenotypes
    if not phenotypeString:
        continue

    # Parse the phenotypes
    phenotypeFull = phenotypeString.split(';')
    for j, phenotype in enumerate(phenotypeFull):

        # Clean the phenotype
        phenotype = phenotype.strip()

        # Long phenotype
        matcher = re.match(r'^(.*),\s(\d{6})\s\((\d)\)(|, (.*))$', phenotype)
        if matcher:

            # Get the fields
            phenotypeText = matcher.group(1)
            phenotypeMimNumber = matcher.group(2)
            phenotypeMappingKey = matcher.group(3)
            inheritances = matcher.group(5)

            # Get the inheritances, may or may not be there
            if inheritances:
                inh = inheritances.split(',')
                for i, inheritance in enumerate(inh):
                    inh[i] = my_inherintance(inheritance)
                inheritances = ",".join(inh)
                                            
                # Update if inheritances
                phenotype = "|".join([phenotypeText, phenotypeMimNumber, inheritances])
            else:
                phenotype = "|".join([phenotypeText, "", ""])
                    
        # Short phenotype
        else:
            matcher = re.match(r'^(.*)\((\d)\)(|, (.*))$', phenotype)
            if matcher:

                # Get the fields
                phenotype = matcher.group(1)
                phenotypeMappingKey = matcher.group(2)
                inheritances = matcher.group(3)

                # Get the inheritances, may or may not be there
            if inheritances:
                inh = inheritances.split(',')
                for i, inheritance in enumerate(inh):
                    inh[i] = my_inherintance(inheritance)
                inheritances = ",".join(inh)
                                            
                # Update if inheritances
                phenotype = "|".join([phenotypeText, "", inheritances])
            else:
                phenotype = "|".join([phenotypeText, "", ""])

        # Update phenotype
        phenotypeFull[j] = phenotype

    phenotypeFull = "|".join(phenotypeFull)

    # Format columns
    phenotypeFull =phenotypeFull.split('|')
    phenotypeText= phenotypeFull[0]
    phenotypeMimNumber =phenotypeFull[1]
    inheritances=phenotypeFull[2]

    # Regrouper le texte, puis numéro OMIM puis phénotype
    if len(phenotypeFull)>3:
        for k,value in enumerate(phenotypeFull):
            if k<3: continue #skip first three columns already implemented
            if k % 3 == 0 and value != "": 
                if phenotypeText == "" : phenotypeText=value
                phenotypeText="/".join([phenotypeText,value])
            elif k % 3 == 1 and value != "":
                if phenotypeMimNumber == "" : phenotypeMimNumber=value 
                phenotypeMimNumber="/".join([phenotypeMimNumber,value])
            elif k % 3 == 2 and value != "": 
                if inheritances == "" : inheritances=value 
                inheritances="/".join([inheritances,value])

    phenotypeFull = '\t'.join([phenotypeText, phenotypeMimNumber,inheritances])

    # Export selected fields
    final = "\t". join([approvedGeneSymbol, geneSymbols, mimNumber, phenotypeFull])

    # Injecte la nouvelle ligne
    line = final
    print(line)