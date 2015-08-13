# cap3 output processing and analysis

# CAP3 run #

example project: http://cgpdb.ucdavis.edu/SNP_Discovery_CDS/

**cap3 input.fasta -o 80 -p 90 > output.cap3.80.90 &**

(overlap 80 nucleotides, identity - 90%)

# CAP3 output processing #

**GENERATION OF CONTIG COMPLEXITY INFO:**

```
python Python_CAP3_ContigExtractor_Uni_2007_03_19.py
What type of output do you want? (1/2): 1
Enter the SOURCE file name: output.cap3.80.90
Enter the DESTINATION file name: output.cap3.80.90.Info
Default contig file name prefix is Contig
Enter the contig file name prefix:My_Assy_
```

**EXTRACTION OF CAP3 ALIGNMENTS:**

```
python Python_CAP3_ContigExtractor_Uni_2007_03_19.py
What type of output do you want? (1/2): 2
Enter the SOURCE file name: output.cap3.80.90
Enter the DESTINATION directory with alignments: output.cap3.80.90.Align
Default contig file extension is aln
Enter the contig file extension :
Default contig file name prefix is Contig
Enter the contig file name prefix:My_Assy_
```

**CONCATENATION OF ALL ALIGNMENTS INTO ONE LARGE FILE:**

```
cd output.cap3.80.90.Align
cat My_Assy_*.aln > ../output.cap3.80.90.Align.txt
cd ../
```

**SNP DISCOVERY:**

```
python Python_CAP3_MM_Finder_Uni_2008_01_26c.py 
Enter the SOURCE file name: output.Align.txt
Enter the DESTINATION file name: output.cap3.80.90.MM
Enter the CONSENSUS_ID pattern: My_Assy_
```

**EXAMPLE SEQS COVERAGE FILE OUTPUT:**

```
structure of output.cap3.80.90.MM.seqs.coverage file/table
  [1]        [2]    [3]*    [4]         [5]        [6]     [7]     [8]
CONTIG ID Position  Gap  Position   A T G C N -   Depth  Consensus  MM

My_Assy_1   1950    [0]     1950    0:28:0:0:0:0    28      T       0
My_Assy_1   1951    [0]     1951    28:0:0:0:0:0    28      A       0
My_Assy_1   1952    [0]     1952    1:13:0:14:0:0   28      C       14
My_Assy_1   1953    [0]     1953    28:0:0:0:0:0    28      A       0
My_Assy_1   1954    [0]     1954    0:14:0:14:0:0   28      C       14
My_Assy_1   1955    [0]     1955    29:0:0:0:0:0    29      A       0
My_Assy_1   1956    [0]     1956    0:30:0:0:0:0    30      T       0
My_Assy_1   1957    [0]     1957    0:0:15:15:0:0   30      C       15
My_Assy_1   1958    [0]     1958    0:29:0:0:0:0    29      T       0
My_Assy_1   1959    [0]     1959    0:0:0:29:0:0    29      C       0
My_Assy_1   1960    [0]     1960    0:33:0:0:0:0    33      T       0

* - column [3] – Gap Adjustment, real position on assembly is indicated on column 4
[5] – ‘ATGCN-’ content, for example 1:13:0:14:0:0 correspond to 1 ‘A’, 13 ‘T’ and 14 ‘C’ letters in the alignment
[8] – number of total mis-matches over consensus sequence
```