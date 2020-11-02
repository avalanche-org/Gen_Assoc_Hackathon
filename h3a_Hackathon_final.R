rm(list = ls())

completePedigree <- function(dbwork){
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

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                                                        #DATA CLEANING PROCESS with PLINK: Dont take into acccount
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


setwd("/home/share/malaria_senegal/test_geno_inference")
plink_ = "/home/g4bbm/tools/Plink/plink"

# cleaning intermediate files 
system("rm ou*")
system("rm *samp*")
system("rm *autosome*")
system("rm *plink*")

# Extract autosomes
system(paste0(plink_," --bfile malaria_senegal --chr 1-22 --recode12 --out malaria_senegal_autosome"))

map = read.delim("malaria_senegal_autosome.map", header = F)

write.table(sample(map$V2,100),  col.names = F, row.names = F, quote = F, file = "sample.tsv")

# Extract sample dataset
system(paste0(plink_, " --file malaria_senegal_autosome --extract sample.tsv --recode12 --out malaria_senegal_autosome_samp"))

# Set for mendel errors
system(paste0(plink_, " --file malaria_senegal_autosome_samp --set-me-missing --make-bed --out malaria_senegal_autosome_samp_clean"))

# Recode bed to ped
system(paste0(plink_, " --bfile malaria_senegal_autosome_samp_clean --recode 12 --tab --out malaria_senegal_autosome_samp_clean"))

# Load Original dataset
# Anonymization
malaria_senegal_autosome_samp_clean = read.delim("malaria_senegal_autosome_samp_clean.ped", header = F , stringsAsFactors = F)
for(i in 1:6){
  malaria_senegal_autosome_samp_clean[,i] = gsub("D", "S1", malaria_senegal_autosome_samp_clean[, i])
  malaria_senegal_autosome_samp_clean[,i] = gsub("N", "S2", malaria_senegal_autosome_samp_clean[, i])
}
write.table(malaria_senegal_autosome_samp_clean, "malaria_senegal_autosome_samp_clean.ped", sep = "\t", quote = F, col.names = F, row.names = F)
#--------------------------------------------------------------------------------------------------------------------------------------

#------------------ Run genotype inference script
#--------------------------------------------------------------------------------

system("Rscript genoInference.R --file malaria_senegal_autosome_samp_clean --cutsize 50 --cores 4")

# MERGE
malaria_senegal_autosome_samp_clean_gi = read.delim(paste0("out1.ped"), header = F, stringsAsFactors = F)
out.files  = list.files()[grep("out", list.files())]
if(length(out.files) > 1){
  for(i in 2:length(out.files)){
    tmp = read.delim(paste0("out",i,".ped"), header = F, stringsAsFactors = F)
    malaria_senegal_autosome_samp_clean_gi  = cbind(malaria_senegal_autosome_samp_clean_gi, tmp[, 7:ncol(tmp)])
  }
}

# CHECK : wheter GI have changed any orignal ? 
# Load Original dataset
# malaria_senegal_autosome_samp_clean = read.delim("malaria_senegal_autosome_samp_clean.ped", header = F , stringsAsFactors = F)

# Check if individuals in 'before' dataset are in the same order than the 'after' dataset
sum(malaria_senegal_autosome_samp_clean$V2 == malaria_senegal_autosome_samp_clean_gi$V2)

n_miss_before = length(malaria_senegal_autosome_samp_clean[malaria_senegal_autosome_samp_clean == '0 0'])
n_miss_after  = length(malaria_senegal_autosome_samp_clean_gi[malaria_senegal_autosome_samp_clean_gi == '0 0'])
cat("Missing Values in 'Before'-Dataset :  ", n_miss_before, "\n")
cat("Missing Values in 'After'-Dataset :  ", n_miss_after, "\n")
cat('Number of inferred genotype : ', n_miss_before - n_miss_after )
sum((malaria_senegal_autosome_samp_clean[,7:ncol(malaria_senegal_autosome_samp_clean)] != malaria_senegal_autosome_samp_clean_gi[,7:ncol(malaria_senegal_autosome_samp_clean_gi)]))
### END-EVALUATION

colnames(malaria_senegal_autosome_samp_clean_gi) = paste0("V", 1:ncol(malaria_senegal_autosome_samp_clean_gi))

colnames(malaria_senegal_autosome_samp_clean)    = paste0("V", 1:ncol(malaria_senegal_autosome_samp_clean))

malaria_senegal_autosome_samp_clean_gi_mtdt = rbind(malaria_senegal_autosome_samp_clean_gi, 
                                                    completePedigree(malaria_senegal_autosome_samp_clean_gi))

malaria_senegal_autosome_samp_clean_mtdt = rbind(malaria_senegal_autosome_samp_clean, 
                                                 completePedigree(malaria_senegal_autosome_samp_clean))

malaria_senegal_autosome_samp_clean_gi_mtdt_map = paste0("M", 7:ncol(malaria_senegal_autosome_samp_clean_gi_mtdt))

malaria_senegal_autosome_samp_clean_mtdt_map = paste0("M", 7:ncol(malaria_senegal_autosome_samp_clean_mtdt))

write.table(malaria_senegal_autosome_samp_clean_gi_mtdt, "malaria_senegal_autosome_samp_clean_gi_mtdt.ped",
            sep = "\t", quote = F, col.names = F, row.names = F)

write.table(malaria_senegal_autosome_samp_clean_gi_mtdt_map, "malaria_senegal_autosome_samp_clean_gi_mtdt.map",
            sep = "\t", quote = F, col.names = F, row.names = F)

write.table(malaria_senegal_autosome_samp_clean_mtdt, "malaria_senegal_autosome_samp_clean_mtdt.ped",
            sep = "\t", quote = F, col.names = F, row.names = F)

write.table(malaria_senegal_autosome_samp_clean_mtdt_map, "malaria_senegal_autosome_samp_clean_mtdt.map",
            sep = "\t", quote = F, col.names = F, row.names = F)

system("mkdir mtdt_gi")
system("mv *gi_mtdt* mtdt_gi")
system("mkdir mtdt")
system("mv *clean_mtdt* mtdt")
system("cp -r libs mtdt")
system("cp -r libs mtdt_gi")

system("rm ou*")

malaria_senegal_autosome_samp_clean_gi_mtdt_phen = cbind(malaria_senegal_autosome_samp_clean_gi_mtdt[,1:2], 
                                                         round(rnorm(nrow(malaria_senegal_autosome_samp_clean_gi_mtdt), sd = 0.51, mean = 0.51), 2))

write.table(malaria_senegal_autosome_samp_clean_gi_mtdt_phen, 
            "mtdt/malaria_senegal_autosome_samp_clean_mtdt.phen",
            sep = "\t", quote = F, col.names = F, row.names = F)

write.table(malaria_senegal_autosome_samp_clean_gi_mtdt_phen, 
            "mtdt_gi/malaria_senegal_autosome_samp_clean_gi_mtdt.phen",
            sep = "\t", quote = F, col.names = F, row.names = F)

#system("Rscript mtdt.R --nbcores 20  --pedfile malaria_senegal_autosome_samp_clean_mtdt.ped --phenfile malaria_senegal_autosome_samp_clean_mtdt.phen --phen 1 --mapfile  malaria_senegal_autosome_samp_clean_mtdt.map ")
#system("Rscript mtdt.R --nbcores 20  --pedfile malaria_senegal_autosome_samp_clean_mtdt.ped --phenfile malaria_senegal_autosome_samp_clean_mtdt.phen --phen 1 --mapfile  malaria_senegal_autosome_samp_clean_mtdt.map ")

# Check : wether inferred genotypes were 'correctely inferred'
write.table(malaria_senegal_autosome_samp_clean_gi, 
            file = "malaria_senegal_autosome_samp_clean_gi.ped",
            quote = F, col.names = F, row.names = F, sep = "\t")

system("cp malaria_senegal_autosome_samp_clean.map malaria_senegal_autosome_samp_clean_gi.map")

system(paste0(plink_ ," --file malaria_senegal_autosome_samp_clean_gi --mendel --out malaria_senegal_autosome_samp_clean_gi"))

mtdt_gi = read.table("/home/share/malaria_senegal/test_geno_inference/mtdt_gi/weighted_res_multilocus.csv", sep = ";", header = T, stringsAsFactors  = F, dec = ",")
mtdt = read.table("/home/share/malaria_senegal/test_geno_inference/mtdt/weighted_res_multilocus.csv", sep = ";", header = T, stringsAsFactors = F, dec = ",")

length(intersect(mtdt$models, mtdt_gi$models))

setdiff(mtdt_gi$models, mtdt$models)

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
