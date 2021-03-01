


#   @MaryemT 
#   avalanche-org
#   /Gen_Assoc


#-------  This is a script to test m-TDT and genotype_inference tools

#    ---  Family-based samples are provided in the GitHub repository
#    ---  in directory: "25markers.zip" | "genotype_inference.zip" | "mTDT.zip" | "summary.R" 

#    ---  If you running script on your own data make sure to have clean data
#    ---  with 0 mendelian or heterozygous haplotypes errors
#    ---  input file format: ped , map, phen : cf README.pdf

#         Should a problem occur, contact : NdeyeMarieme.top@pasteur.sn


rm(list = ls())



path = system("pwd", intern = T)
setwd(path)
plink_ = "/home/g4bbm/tools/Plink/plink"
data_= "25markers"

# Change path to plink in genoInference.R at line 48

#   ---  Functions

merge_out_files <- function(){
  
  # --- Merge genoInference.R's outputs
  
  merged_files = read.delim(paste0("out1.ped"), header = F, stringsAsFactors = F)
  
  out.files  = list.files()[grep("out", list.files())] 
  
  if(length(out.files) > 1){
    for(i in 2:length(out.files)){
      tmp = read.delim(paste0("out",i,".ped"), header = F, stringsAsFactors = F)
      merged_files  = cbind(merged_files, tmp[, 7:ncol(tmp)])
    }
  }
  rm(tmp)
  return(merged_files)
}

completePedigree <- function(dbwork){
  
  # --- Prepare ped file for m-TDT run
  
  fathers = unique(setdiff(unique(dbwork$V3), dbwork$V2))
  fathers = fathers[!(fathers%in%c("0"))]
  fathers_famIDs = unique(dbwork[dbwork$V3 %in% fathers, c(1,3)])
  
  mothers = unique(setdiff(unique(dbwork$V4), dbwork$V2))
  mothers = mothers[!(mothers%in%c("0"))]
  mothers_famIDs = unique(dbwork[dbwork$V4 %in% mothers, c(1,4)])
  
  dataset = NULL
  for(i in 1:nrow(fathers_famIDs)){
    dataset = rbind(dataset, c(fathers_famIDs[i,1], fathers_famIDs[i,2], "0", "0", "1", "2", rep(NA, length(1:(ncol(dbwork)-6)))))
  }
  for(i in 1:nrow(mothers_famIDs)){
    dataset = rbind(dataset, c(mothers_famIDs[i,1], mothers_famIDs[i,2], "0", "0", "2", "2", rep(NA, length(1:(ncol(dbwork)-6)))))
  }
  
  return(dataset)
}

#   ---  Files

system("unzip mTDT.zip; mkdir mTDT/; mv MTDT_* README.txt README.pdf __MAC* mTDT/; cp -r libs mtdt.R mTDT/;cp -r libs mtdt.R mTDT/")

system("mkdir genotype_inference; unzip genotype_inference.zip")   # -- no GI
system("mv __MACOSX* README.* documentation.* genotype_inference/; cp genoI* mendel* genotype_inference/")

system(paste0("unzip ", data_,".zip"))
data_= "sample"

ped = read.delim(paste0(data_,".ped"), header = F , stringsAsFactors = F)
map = read.delim(paste0(data_,".map"), header = F , stringsAsFactors = F)
phen = read.delim(paste0(data_,".phen"), header = F , stringsAsFactors = F)


#    ---  Check for Mendelian errors

#system(paste0(plink_ ," --file ", data_," --mendel --out ", data_,"_check"))
#system("rm *check*")

#   ---   Summary 

system(paste0("Rscript summary.R --pedfile ", data_,".ped --mapfile ", data_,".map --phenfile ", data_,".phen"))


#   ---   Genotype inference option

system(paste0("Rscript genoInference.R --file ", data_," --cutsize 10 --cores 4")) 

gi_ped = merge_out_files()
system(("rm out*"))


# ---   SUMMARY_GI  -----------------------------------------------

sum(ped$V2 == gi_ped$V2)


cat(" Total number of snps in - ", data_," set :\t", nrow(ped)* (ncol(ped)-6), "\n",
    "Missing Values in 'Before'- ", data_," set :\t", length(ped[ped == '0 0']), "\n",
    "Missing Values in 'After'- ", data_," set :\t", length(gi_ped[gi_ped == '0 0']), "\n",
    '==>  Number of inferred genotype :\t\t', (length(ped[ped == '0 0'])) - (length(gi_ped[gi_ped == '0 0'])) )

write.table(gi_ped, paste0(data_,"_gi.ped"),
            sep = "\t", quote = F, col.names = F, row.names = F)
write.table(map, paste0(data_,"_gi.map"),
            sep = "\t", quote = F, col.names = F, row.names = F)

#    ---  Check for Mendelian errors

system(paste0(plink_ ," --file ", data_,"_gi --mendel --out ", data_,"_check"))
#system("rm *check*")
#-------------------------------------------------------------------


#-------  RUN m-TDT
#-------------------------------------------------------------------

# --- Complete Pedigree

mtdt_ped = rbind(ped, completePedigree(ped))
mtdt_map = paste0("M", (7:ncol(mtdt_ped)-6))

# -- gi
mtdt_gi_ped = rbind(ped, completePedigree(ped))


# --- write files

write.table(mtdt_ped, paste0(data_,"_CP.ped"),
            sep = "\t", quote = F, col.names = F, row.names = F)

write.table(mtdt_map, paste0(data_,"_CP.map"),
            sep = "\t", quote = F, col.names = F, row.names = F)

# -- gi
write.table(mtdt_gi_ped, paste0(data_,"_gi_CP.ped"),
            sep = "\t", quote = F, col.names = F, row.names = F)


#-------  RUN 
#-------

# --  Single marker

# -

system(paste0("Rscript mtdt.R --nbcores 20  --pedfile ", data_,"_CP.ped --phenfile ", data_,".phen --phen 1 --mapfile  ", data_,"_CP.map "))

system("mkdir single_marker_results; mv weighted* single_marker_results")

# - gi

system(paste0("Rscript mtdt.R --nbcores 20  --pedfile ", data_,"_gi_CP.ped --phenfile ", data_,".phen --phen 1 --mapfile  ", data_,"_CP.map "))

system("mkdir single_marker_gi_results; mv weighted* single_marker_gi_results")

# --  Multi-marker

# - 

system(paste0("Rscript mtdt.R --nbcores 20 --nbsim 5 --markerset 1,2,3 --pedfile ", data_,"_CP.ped --phenfile ", data_,".phen --phen 1 --mapfile  ", data_,"_CP.map "))

system("mkdir multi_marker_results; mv weighted* multi_marker_results")

# - gi

system(paste0("Rscript mtdt.R --nbcores 20 --nbsim 5 --markerset 1,2,3 --pedfile ", data_,"_gi_CP.ped --phenfile ", data_,".phen --phen 1 --mapfile  ", data_,"_CP.map "))

system("mkdir multi_marker_gi_results; mv weighted* multi_marker_gi_results")


#   --------------------------------------------------------------------------

mtdt_sm = read.table(paste0(path,"/single_marker_results/weighted_res_multilocus.csv"), sep = ";", header = T, stringsAsFactors = F, dec = ",")
mtdt_sm_gi = read.table(paste0(path,"/single_marker_gi_results/weighted_res_multilocus.csv"), sep = ";", header = T, stringsAsFactors  = F, dec = ",")

length(intersect(mtdt_sm$models, mtdt_sm_gi$models))
setdiff(mtdt_sm$models, mtdt_sm_gi$models)


#STOP
mtdt_gi2 = mtdt_gi[mtdt_gi$models != "M357", ]

mtdt_gi2 = mtdt_gi2[order(mtdt_gi2$models),]

mtdt = mtdt[order(mtdt$models),]

sum(mtdt_gi2$models == mtdt$models)

sum( (mtdt$mTDT_asympt_Pval - mtdt_gi2$mTDT_asympt_Pval) != 0)

x  = mtdt$mTDT_asympt_Pval - mtdt_gi2$mTDT_asympt_Pval

y = ifelse(x>=0, 1, -1)

table(y)

plot(-log10(mtdt$mTDT_asympt_Pval), type = "l")

lines(-log10(mtdt_gi$mTDT_asympt_Pval), type = "l", col="red")









