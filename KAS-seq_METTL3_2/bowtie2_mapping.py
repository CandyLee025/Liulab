GROUP=["KAS-seq_ALKBH3","KAS-seq_ALKBH5"]
SAMPLE=["Ctrl","KO"]

TREATMENT=["input","IP"]
REP=["rep1","rep2"]

DUP=["raw","rmdup","unique"]

INDEX="~/reference/index/bowtie2/mm19/mm19"

rule all:
  input:
    expand("{group}/04_bam_{dup}/{group}_{sample}_{treatment}_{rep}.bam.bai",dup=DUP,group=GROUP,sample=SAMPLE,treatment=TREATMENT,rep=REP)
    
rule bowtie2_mapping:
  input:
    "{group}/02_trim_galore/{group}_{sample}_{treatment}_{rep}_trimmed.fq.gz"
  output:
    temp("{group}/04_bam_raw/{group}_{sample}_{treatment}_{rep}.sam"),
    "{group}/04_bam_raw/{group}_{sample}_{treatment}_{rep}.bam",
    "{group}/04_bam_raw/{group}_{sample}_{treatment}_{rep}.summary.txt"
  params:
    index=INDEX
  log:
    "{group}/logs/bowtie2_mapping/{group}_{sample}_{treatment}_{rep}.log"
  threads: 10
  shell:
    """
    /disk1/home/user_09/anaconda3/envs/bowtie2/bin/bowtie2 -x {params.index} \
      -p {threads} -U {input} -S {output[0]} > {output[2]} 2>&1
    /disk1/home/user_09/anaconda3/envs/LinLong/bin/samtools sort -@ {threads} {output[0]} -o {output[1]} > {log} 2>&1
    """
  
rule samtools_rmdup:
  input:
    "{group}/04_bam_raw/{group}_{sample}_{treatment}_{rep}.bam"
  output:
    "{group}/04_bam_rmdup/{group}_{sample}_{treatment}_{rep}.bam"
  log:
    "{group}/logs/samtools_rmdup/{group}_{sample}_{treatment}_{rep}.log"
  threads: 1
  shell:
    "/disk1/home/user_09/anaconda3/envs/LinLong/bin/samtools rmdup -s {input} {output} > {log} 2>&1"
    
rule bam_index:
  input:
    "{group}/04_bam_{dup}/{group}_{sample}_{treatment}_{rep}.bam"
  output:
    "{group}/04_bam_{dup}/{group}_{sample}_{treatment}_{rep}.bam.bai"
  log:
    "{group}/logs/bam_index/{dup}/{group}_{sample}_{treatment}_{rep}.log"
  threads: 4
  shell:
    "/disk1/home/user_09/anaconda3/envs/LinLong/bin/samtools index -@ {threads} {input} > {log} 2>&1"
 
rule bam_unique:
  input:
    "{group}/04_bam_rmdup/{group}_{sample}_{treatment}_{rep}.bam"
  output:
    "{group}/04_bam_unique/{group}_{sample}_{treatment}_{rep}.bam"
  log:
    "{group}/logs/bam_unique/{group}_{sample}_{treatment}_{rep}.log"
  threads:10
  shell:
    "/disk1/home/user_09/anaconda3/envs/LinLong/bin/samtools view -@ {threads} -q 10 -bS {input} \
    | /disk1/home/user_09/anaconda3/envs/LinLong/bin/samtools sort -@ {threads} -o {output} >> {log} 2>&1"
  

