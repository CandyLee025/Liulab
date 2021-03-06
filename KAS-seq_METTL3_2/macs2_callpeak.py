GROUP=["KAS-seq_ALKBH3","KAS-seq_ALKBH5"]
SAMPLE=["Ctrl","KO"]

TREATMENT=["input","IP"]
REP=["rep1","rep2"]

rule all:
  input:
    expand("{group}/06_macs2/regular/{group}_{sample}_{rep}_peaks.narrowPeak",group=GROUP,sample=SAMPLE,rep=REP),
    expand("{group}/06_macs2/broad/{group}_{sample}_{rep}_peaks.broadPeak",group=GROUP,sample=SAMPLE,rep=REP),
    expand("{group}/06_macs2/broad/{group}_{sample}_{rep}_nomodel_peaks.broadPeak",group=GROUP,sample=SAMPLE,rep=REP),

rule macs2_callpeak_regular:
  input:
    "{group}/05_bedtools/bed_extend/{group}_{sample}_IP_{rep}_ext.bed",
    "{group}/05_bedtools/bed_extend/{group}_{sample}_input_{rep}_ext.bed"
  output:
    "{group}/06_macs2/regular/{group}_{sample}_{rep}_peaks.narrowPeak",
    "{group}/06_macs2/regular/{group}_{sample}_{rep}_peaks.xls"
  log:
    "{group}/logs/macs2_callpeak/regular/{group}_{sample}_{rep}.log"
  params:
    out_name="{group}_{sample}_{rep}",
    out_dir="{group}/06_macs2/regular"
  shell:
    "/disk1/home/user_09/anaconda3/envs/m6A/bin/macs2 callpeak \
      -t {input[0]} -c {input[1]} \
      -n {params.out_name} \
      -g mm -q 0.01 \
      --outdir {params.out_dir} > {log} 2>&1"
      
rule macs2_callpeak_broad:
  input:
    "{group}/05_bedtools/bed_extend/{group}_{sample}_IP_{rep}_ext.bed",
    "{group}/05_bedtools/bed_extend/{group}_{sample}_input_{rep}_ext.bed"
  output:
    "{group}/06_macs2/broad/{group}_{sample}_{rep}_peaks.broadPeak",
    "{group}/06_macs2/broad/{group}_{sample}_{rep}_peaks.xls"
  log:
    "{group}/logs/macs2_callpeak/broad/{group}_{sample}_{rep}.log"
  params:
    out_name="{group}_{sample}_{rep}",
    out_dir="{group}/06_macs2/broad"
  shell:
    "/disk1/home/user_09/anaconda3/envs/m6A/bin/macs2 callpeak \
      -t {input[0]} -c {input[1]} \
      -n {params.out_name} \
      --broad --broad-cutoff 0.01 \
      -g mm -q 0.01 \
      --outdir {params.out_dir} > {log} 2>&1"
      
rule macs2_callpeak_broad_nomodel:
  input:
    "{group}/05_bedtools/bed_extend/{group}_{sample}_IP_{rep}_ext.bed",
    "{group}/05_bedtools/bed_extend/{group}_{sample}_input_{rep}_ext.bed"
  output:
    "{group}/06_macs2/broad/{group}_{sample}_{rep}_nomodel_peaks.broadPeak",
    "{group}/06_macs2/broad/{group}_{sample}_{rep}_nomodel_peaks.xls"
  log:
    "{group}/logs/macs2_callpeak/broad/{group}_{sample}_{rep}_nomodel.log"
  params:
    out_name="{group}_{sample}_{rep}_nomodel",
    out_dir="{group}/06_macs2/broad"
  shell:
    "/disk1/home/user_09/anaconda3/envs/m6A/bin/macs2 callpeak \
      --nomodel \
      -t {input[0]} -c {input[1]} \
      -n {params.out_name} \
      --broad --broad-cutoff 0.01 \
      -g mm -q 0.01 \
      --outdir {params.out_dir} > {log} 2>&1"
