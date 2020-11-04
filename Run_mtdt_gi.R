


#   @MaryemT 
#   avalanche-org
#   /Gen_Assoc


#-------  This is a script to test m-TDT and genotype_inference tools

#    ---  A family-based sample is provided in the GitHub repository: malaria_senegal
#    ---  Data description: 2000 snps of 481 individuals

#    ---  If you running script on your own data make sure to have clean data
#    ---  with 0 mendelian or heterozygous haplotypes errors
#    ---  in PLINK file format: ped , map, phen


#         Should a problem occur, contact : NdeyeMarieme.top@pasteur.sn


rm(list = ls())


#-------  FUNCTIONS
#-------------------------------------------------------------------


merge_out_files <- function(){
  # --- This function merges genoInference.R's outputs
  
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
  # --- This function prepares ped file for m-TDT run
  
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

run_recursive_gi <- function(filename, cutsize, nbcores){
  #   ----  This function runs Genotype inference on ped file until there is no more snps to infer
  gain = 1
  run = 0
  while (gain != 0){
    
    run = run + 1
    
    ped = read.delim(paste0(filename,".ped"), header = F, stringsAsFactors = F)
    
    cat("\n---- Run n°:", run, "\n","\t Running genotype inference on:", filename, "\n")
    
    system(paste0("Rscript genoInference.R --file ", filename, " --cutsize ", cutsize, " --cores ", nbcores), wait = T, intern = F)
    #system("sleep 20", wait = T, intern = F)
    
    cat("Merging files..\n \t Done. \n")
    ped_gi = merge_out_files()
    
    
    system("rm out*")
    cat("\n--- Run ",run, " finished", "\n\n")
    
    
    gain = (length(ped[ped == '0 0'])) - (length(ped_gi[ped_gi== '0 0']))
    
    cat(" Total number of snps in - malaria_senegal set :\t", nrow(ped)* (ncol(ped)-6), "\n",
        "Missing Values in 'Before'- malaria_senegal set :\t", length(ped[ped == '0 0']), "\n",
        "Missing Values in 'After'- malaria_senegal set :\t", length(ped_gi[ped_gi== '0 0']), "\n",
        '==>  Number of inferred genotype :\t\t\t', gain )
    
    if (gain != 0){
      
      write.table(ped_gi,file = paste0("sample_",run,".ped"),
                  quote = F, col.names = F, row.names = F, sep = "\t")
      
      cmd = paste0("cp ",filename,".map sample_",run,".map")
      system(cmd)
      
      filename = paste0("sample_",run)
      cat("\n\nTrying to infer more snps..\n")
    }
    
    else {
      cat("\n\nReached maximum number of inferred snps. \nBye!")
    }
    
  }
  
}


#-------  PREPARE ENVIRONMENT
#-------------------------------------------------------------------

#    ---  set paths

setwd("/home/mtop/gi/")                                 
plink_ = "/home/g4bbm/tools/Plink/plink"
  
# Change path to plink in genoInference.R at line 48

#   --- unzip files

system("unzip genotype_inference.zip")
system("unzip mTDT.zip")
system("unzip malaria_senegal")

system("mv malaria_senegal/* .")
system("cp genotype_inference/mendel_table* .; cp genotype_inference/g* .")

#    ---  Check for Mendelian errors

system(paste0(plink_ ," --file malaria_senegal --mendel --out malaria_senegal_check"))
system("rm *check*")


malaria_senegal_ped = read.delim("malaria_senegal.ped", header = F , stringsAsFactors = F)


#-------  RUN GENOTYPE INFERENCE: single or recursively
#--------------------------------------------------------------------------------

# OPT1   ---  Recursive GI
# run_recursive_gi("malaria_senegal", 100, 4)
# malaria_senegal_gi_ped = read.delim("sample_1.ped", header = F , stringsAsFactors = F)

# OPT2   ---  Single run

system("Rscript genoInference.R --file malaria_senegal --cutsize 100 --cores 4")
malaria_senegal_gi_ped = merge_out_files()
system(("rm out*"))

#    ---  SUMMARY 
sum(malaria_senegal_ped$V2 == malaria_senegal_gi_ped$V2)

n_miss_before_1= length(malaria_senegal_ped[malaria_senegal_ped == '0 0'])
n_miss_after_1  = length(malaria_senegal_gi_ped[malaria_senegal_gi_ped == '0 0'])
tot_snps = nrow(malaria_senegal_ped)* (ncol(malaria_senegal_ped)-6)


cat(" Total number of snps in - malaria_senegal set :\t", tot_snps, "\n",
    "Missing Values in 'Before'- malaria_senegal set :\t", n_miss_before_1, "\n",
    "Missing Values in 'After'- malaria_senegal set :\t", n_miss_after_1, "\n",
    '==>  Number of inferred genotype :\t\t\t', n_miss_before_1 - n_miss_after_1 )

sum((malaria_senegal_ped[,7:ncol(malaria_senegal_ped)] != malaria_senegal_gi_ped[,7:ncol(malaria_senegal_gi_ped)])) 


#-------  RUN m-TDT
#-------------------------------------------------------------------

#   We will perform two runs:
#   => only m-TDT : initial ped file malaria_senegal_ped
#   => GI + m-TDT : infered ped file malaria_senegal_gi_ped

#    ---  Prepare files for m-TDT run


# - CompletePedigree

#make sure the column names match
colnames(malaria_senegal_gi_ped) = paste0("V", 1:ncol(malaria_senegal_gi_ped))
colnames(malaria_senegal_ped)    = paste0("V", 1:ncol(malaria_senegal_ped))

malaria_senegal_gi_mtdt_ped = rbind(malaria_senegal_gi_ped, 
                                    completePedigree(malaria_senegal_gi_ped))

malaria_senegal_mtdt_ped = rbind(malaria_senegal_ped,
                                 completePedigree(malaria_senegal_ped))

# - write files

malaria_senegal_gi_mtdt_map = paste0("M", (7:ncol(malaria_senegal_gi_mtdt_ped)-6))

malaria_senegal_mtdt_map = paste0("M", (7:ncol(malaria_senegal_mtdt_ped)-6))

write.table(malaria_senegal_gi_mtdt_ped, "malaria_senegal_gi_mtdt.ped",
            sep = "\t", quote = F, col.names = F, row.names = F)

write.table(malaria_senegal_gi_mtdt_map, "malaria_senegal_gi_mtdt.map",
            sep = "\t", quote = F, col.names = F, row.names = F)

write.table(malaria_senegal_mtdt_ped, "malaria_senegal_mtdt.ped",
            sep = "\t", quote = F, col.names = F, row.names = F)

write.table(malaria_senegal_mtdt_map, "malaria_senegal_mtdt.map",
            sep = "\t", quote = F, col.names = F, row.names = F)


#    ---  

system("mkdir mtdt_gi; mv *gi_mtdt* mtdt_gi")

system("mkdir mtdt; mv *mtdt.* mtdt")

system("cp -r libs mtdt")
system("cp -r libs mtdt_gi")



#    ---  

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









