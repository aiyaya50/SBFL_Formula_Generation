# SBFL_Formula_Generation
## Essential Files
1. Gzoltar_compatible_formula_generation.ipynb is a jupyter notebook python file for generating Gzoltar compatible SBFL formulas based on the hybridization of Ajibode et al. (2022) and Idrees et al. (2023) approaches.
2. Formulas-readable.txt contains the 22 formulas generated by 1 above in a readable SBFL terms.
3. Formulas.txt contains the 22 generated formulas in Gzoltar terms whose adjustment and implementation are in the 'Generated_Formulas' repository
4. fl.py use the scripts in run.sh to export Defects4J buggy versions, gather coverage information and conduct fault localization on the buggy versions
5. result_analysis.py is to conduct FL result analysis usint TOP_N and wasted effort metrics.

<b>Note</b>
It worth noting that list of buggy lines from defects4j is neccessary to run result_analysis.py.
Download the buggy statements from https://bitbucket.org/rjust/fault-localization-data/src/master/analysis/pipeline-scripts/buggy-lines/ OR regenerate using extract_buggy_lines.sh file.

## Steps
1. Set up defects4j 
2. Run the Gzoltar_compatible_formula_generation.ipynb file in jupyter to generate the 22 formulas and manually adjust to conform with Gzoltar/java code
     OR use the formulars in the 'manually_adjusted_formulas' repository.
3. Set up Gzoltar and alter some of its files (e.g SFLFormulas.java) to incoporate the outcome of #1 above (For details see the https://github.com/aiyaya50/SBFL_Formula_Generation/Manually_adjusted_Formulas/README.md)
4. Edit path names in fl.py, run.sh, and result_analysis.py to those in your computer
5. Run fl.py to checkout the buggy versions of defects4j, gather coverage info and compute suspicious scores that will be deposited in the specified folder in run.sh
6. Run result_analysis.py to generate a csv file for TOP_N or wasted effort (Toggle the 'fl_metric' to True or False in line 5) 
7. Use other analysis and presentation methods on the generated files in #6 above
   
