<img width="200px" src="https://user-images.githubusercontent.com/23165406/126583507-4e720000-9b84-46c5-966d-f0aa5a5e7d95.png" />

# Introduction
Open Chromatin Regions (OCRs) or chromatin accessible regions often harbor many Cis-acting elements and various transcription factor binding sites.Therefore, the efficient and precise identification of interactions between OCRs is essential for understanding eukaryotic transcription regulation.Various high-throughput chromosome conformation capture-based methods gives researchers the possibility to study OCR-mediated loops. But limited by the resolution and cell volume, there are still many potential OCR-mediated loops that have not been explored.Here,  we present **CharID**, a two-step prediction model that combines deep learning and machine learning for predicting OCR-mediated loops.The **CharID** model consists of two parts, the **CharID-Anchor** model and the **CharID-loop** model. **CharID-Anchor** model discriminates well between Anchor and Non-anchor OCRs, and **CharID-Loop** model accurately predicts the interaction between OCRs as Anchor. Finally, we hosted a user-friendly web server including online prediction, query and visulization functionalities that can befreely accessed at http://peaksniffer.hzau.edu.cn/. 

# Steps to install and run CharID

## Step 1. Install  packages
### Following Python packages are required:
* numpy
* matplotlib
* sklearn
* HTSeq
* pyBigWig
* cooler
* pybedtools
* keras
* tensorflow-gpu

## Step 2. Install  Snakemake
We adopt an easy-to-use workflow software Snakemake to build our analysis  process, which combines a series of steps into a single pipeline. Snakemake and the  manual are provided in this [LINK](https://snakemake.readthedocs.io/en/stable/index.html). 
```
$ pip install snakemake==5.5.2
```

## Step 3. Download and run CharID
### (i) Download and install CharID
```
$ git clone https://github.com/Yin-Shen/CharID.git
```
```
$ echo "export PATH=\"${PWD}/CharID:\$PATH\" " >>~/.bashrc
$ source ~/.bashrc
$ cd CharID
$ chmod -R 744 CharID
```

The follow command can print help information.
```
CharID -h
```
Or print python scripts help information.
```

python model.py -h
```

### (ii) The directory structure of CharID 

The directory structure of CharID is as follows, which has three directories and three files.
```
    ├── src
    ├── loops
    ├── signal 
    ├── config.yaml
    ├── Snakefile
    └── CharID

```
#### Directories
* All the python and shell scripts are in directory “**CharID/src**”, but users generally don't need to care about it.
* Directory “**CharID/loops**”contains loops identified by experiments such as Hi-C, ChIA-PET.The user needs to put the data in bedpe format of loop in this directory.
* Directory “**CharID/signal** holds sequence feature data (CTCF, conservation) and functional genomic feature data (ChIP-Seq, RNA-Seq) needed for the CharID model. 

```
1. CTCF feature file is "CTCF_motifs_p1e-5_with_phastCons.txt",  which is already downloaded, no need to download.
```

```
2. conservation feature file need to download by yourself.The download link can be clicked on http://hgdownload.cse.ucsc.edu/goldenpath/hg19/phastCons100way/hg19.100way.phastCons .
Under the "signal" directory, create a new "phastCon_raw" folder, and store the downloaded files under this folder, as shown below.
```
```
chr1.phastCons100way.wigFix
chr2.phastCons100way.wigFix
chr3.phastCons100way.wigFix
chr4.phastCons100way.wigFix
chr5.phastCons100way.wigFix
chr6.phastCons100way.wigFix
chr7.phastCons100way.wigFix
chr8.phastCons100way.wigFix
chr9.phastCons100way.wigFix
chr10.phastCons100way.wigFix
chr11.phastCons100way.wigFix
chr12.phastCons100way.wigFix
chr13.phastCons100way.wigFix
chr14.phastCons100way.wigFix
chr15.phastCons100way.wigFix
chr16.phastCons100way.wigFix
chr17.phastCons100way.wigFix
chr18.phastCons100way.wigFix
chr19.phastCons100way.wigFix
chr20.phastCons100way.wigFix
chr21.phastCons100way.wigFix
chr22.phastCons100way.wigFix
chrX.phastCons100way.wigFix
chrY.phastCons100way.wigFix
```
```
3. ChIP-Seq and RNA-Seq Data for the specified cell lines can be downloaded from ENCODE in a format that can be standardized to the style below. In addition to the ChIP-Seq data used in this study below, users can also download other ChIP-Seq data of interest, as long as they are in bigWig format.
```
```
H3K4me1.bigWig
H3K4me2.bigWig
H3K4me3.bigWig
H3K9ac.bigWig
H3K9me3.bigWig
H3K27ac.bigWig
H3K27me3.bigWig
H3K36me3.bigWig
H3K79me2.bigWig
H4K20me1.bigWig
CTCF.bigWig
H2AFZ.bigWig
RAD21.bigWig
SMC3.bigWig
ZNF143.bigWig
RNA_seq.bigWig
```
#### Files
* config.yaml (Configuration file)
* Snakefile (Snakemake file)
* CharID (Software run files)

### (iii)Download the files needed to run

* Chromatin Accessible Regions Data with bed file in specified cell line (download in [ucsc ftp](http://hgdownload.cse.ucsc.edu/goldenPath/hg19/encodeDCC/wgEncodeUwDnase/))
* Human genome file in fasta format(download in UCSC, [hg19.fa.gz](https://hgdownload.soe.ucsc.edu/goldenPath/hg19/bigZips/hg19.fa.gz))
* Chromatin interaction Cool file(cool files are available on the [4DN data portal](https://data.4dnucleome.org/))

### (iv) Set the parameters of CharID
Configuration file “config.yaml” contains all parameters of the tool. To run CharID, you only need to revise three parameters in the following according to your path and file name, while leaving others as they are.
```
bed : /public/home/yshen/deep_learning/CharID/GM12878.bed  #Bed file of Chromatin Accessible Regions for input(Need full path)
directory : /public/home/yshen/deep_learning/CharID              #Current working root directory
genome : /public/home/yshen/deep_learning/CharID/hg19.fa    #Human genome file in fasta format(Need full path)
cooler : /public/home/yshen/deep_learning/CharID/Rao2014-GM12878-MboI-allreps-filtered.5kb.cool  #Chromatin interaction Cool file
```

### (v) Run CharID

Snakemake file defines rules to performance operations. We have created a rule for each target and intermediate file. It is not necessary for the users to rewrite it. A complete “Snakefile” file is shown in subsequent section.
```
CharID
```

CharID will perform four steps in turn and output the results of predicted OCRs-mediated loops to a .bedpe format file.

* **Data preprocessing**
* **CharID Anchor Model**
* **CharID Loop Model**
* ***De novo* prediction**

### (vi) Output files

If all steps are completed, the following result file is generated.

```
CharID_Anchor_Model_architecture.json---.json file of model architecture
CharID_Anchor_Model_weights.h5---.h5 file of model parameters
CharID_Anchor_Model_ROC.png---.png file of model ROC curve
CharID_Anchor_Model_Loss.png---.png file of model training loss decline
CharID_Anchor_Model_History.png---.png file of model training situation
CharID_Anchor_Model_predict.bed---.bed file of CharID Anchor model predict anchors
CharID_Loop_Model.model---model file of CharID Loop model
CharID_Loop_Model_ROC.svg---.svg file of CharID Loop model ROC and PR curve
CharID_Loop_Model_predict.bedpe---.bedpe file of CharID Loop predict loops
```
# Contact us

**Yin Shen**: shenyin1995@163.com <br>
