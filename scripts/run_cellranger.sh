#!/bin/bash
#$ -cwd
#$ -q batchq
#$ -l h_vmem=22G
#$ -M rbeagrie
#$ -m aes
#$ -o cellranger.out
#$ -e cellranger.err
#$ -N cellranger

module load cellranger/2.1.1

cellranger count --id citeseq180912 --sample CITE-seq1-1,CITE-seq1-2,CITE-seq1-3,CITE-seq1-4 --localcores 4 --localmem 30 --transcriptome /package/cellranger/references-old/1.2.0/refdata-cellranger-mm10-1.2.0 --fastqs rawdata_180706,rawdata_180904,rawdata_180912
