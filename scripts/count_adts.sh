#!/bin/bash
#$ -cwd
#$ -q batchq
#$ -l h_vmem=10G
#$ -M rbeagrie
#$ -m aes
#$ -o count4.out
#$ -e count4.err
#$ -N count4

source /home/molhaem2/rbeagrie/.virtualenvs/CITE-seq/bin/activate

python3 CITE-seq-count.py \
  -R1 <(for lane in 1 2 3 4; do ls -1 $base/RB_CS1-P_L00${lane}*/*_R1_001.fastq.gz; done | xargs zcat | gzip) \
  -R2 <(for lane in 1 2 3 4; do ls -1 $base/RB_CS1-P_L00${lane}*/*_R2_001.fastq.gz; done | xargs zcat | gzip) \
  --tags tags.csv -cbf 1 -cbl 16 -umif 17 -umil 26 --TAG_regex "^[NATGC]{12}[TGC][A]{6,}" \
  --hamming-distance 2 --whitelist cell_barcodes.txt --output adt_counts.txt
