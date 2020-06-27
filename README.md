OMIM GeneMap2.txt phenotypes extracter :
=========================

This is a simple script to parse the genemap2.txt file and extract MIM phenotypes associated to each genes. 
Input file can be downloaded from [OMIM Downloads](https://omim.org/downloads)(registration required).

This script is based on fschiettecatte's work (https://github.com/fschiettecatte/omim-genemap2-parser).

Usage (Powershell) : cat .\genemap2.txt | python.exe .\Genemap2ToPheno.py > output.txt
