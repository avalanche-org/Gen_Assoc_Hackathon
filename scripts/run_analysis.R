#!/usr/bin/env Rscript

args = commandArgs(trailingOnly = TRUE) 

#   @MaryemT 

#   avalanche-org

#   /Gen_Assoc

#-------  run_analysis.R
#-------  Receive all arguments to run mTDT 

# plink_ = "/home/g4bbm/tools/Plink/plink" (not a requierement)

#   --- Install Required Packages

if(("optparse" %in% rownames(installed.packages())) == F){
  install.packages("optparse", dependencies=TRUE, repos="http://cran.r-project.org")
}

if(("stringr" %in% rownames(installed.packages())) == F){
  install.packages("optparse", dependencies=TRUE, repos="http://cran.r-project.org")
} 

#   ---  Functions

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

#   ---  Collect arguments

# --- Options

library(optparse)

option_list = list(
  make_option(c("--pedfile"), type="character", help="name of 'ped' file", metavar="character"),
  make_option(c("--mapfile"), type="character", help="name of 'map' file", metavar="character"),
  make_option(c("--phenfile"), type="character", help="name of phenotype file", metavar="character"),
  make_option(c("--phen"), type="numeric", default = "1", help="the position of the phenotype (only one) to analyze from the 'phenotype' file without counting the 2 first columns", metavar="character"),
  make_option(c("--nbsim"), type="numeric", help="number of simulations for the computation of empirical P-values. The default value is 0 and will correspond to the case where only asymptotic P-values are provided. If sample size is limited or if there is LD (linkage disequilibrium) among markers analyzed, asymptotic theory is no more valid and then empirical P-values should be computed using simulations", metavar="character"),
  make_option(c("--nbcores"), type="numeric", help="number of cores to use for the run, if the user wants to speed up the run by using multiple cores, as the program can run in parallelized at the simulation step if included to obtain empirical P-values. So, this option is useful only if --nbsim  option is used.``", metavar="character"),
  make_option(c("--markerset"), type="character", help="we advise at the running step to include a limited number of markers, e.g. 3 to 5, (using the markerset option describe below) to avoid both (i) facing a huge number of alternative hypotheses to test and (i i) having sparse count tables for transmitted versus non transmitted alleles combinations across markers. As discussed in the method paper, MTDT has not been optimized for screen multiple markers effect within a large number of markers, but within a set p redefined subgroup of markers of interest, e.g. markers with intermediate marginal effect.", metavar="character"))

opt_parser = OptionParser(option_list=option_list)
opt = parse_args(opt_parser)


library(stringr)

cat("\n,_______ Starting analysis ________ \n")
cat("\n __ Working directory:",getwd(), "\n\n")

cmd= paste0("--pedfile ", opt$pedfile, " --mapfile ", opt$mapfile, " --phenfile ", opt$phenfile, " --phen ",opt$phen, 
            " --markerset ", opt$markerset, " --nbsim ", opt$nbsim,  " --nbcores ", opt$nbcores)

# --- Detect selected flags and write command

flag <- unlist(str_split(c(cmd),"--"))[-1]
positions= NULL

for (i in 1:length(flag)){
  if (unlist(str_split(flag[i]," "))[2] == ""){positions = c(positions, i)}
}
if (length(positions)>0){
  flag = flag[-positions]
}

cat(" * Selected flags: \n")
for (i in 1:length(flag)){
  cat(paste0(" --",flag[i], "\n"))
}


#   ---  File management

# --- Basenames
ped_basename = unlist(str_split(unlist(str_split(opt$pedfile,"/"))[length(unlist(str_split(opt$pedfile,"/")))], ".ped"))[1]
map_basename = unlist(str_split(unlist(str_split(opt$mapfile,"/"))[length(unlist(str_split(opt$mapfile,"/")))], ".map"))[1]
phen_basename = unlist(str_split(unlist(str_split(opt$phenfile,"/"))[length(unlist(str_split(opt$phenfile,"/")))], ".phen"))[1]


# --- Read Files
cat("\n * Reading files...\t")

ped = read.delim(opt$pedfile, header = F , stringsAsFactors = F)
map = read.delim(opt$mapfile, header = F , stringsAsFactors = F)
phen = read.delim(opt$phenfile, header = F , stringsAsFactors = F)

cat('Done. \n')

# --- Process files with Complete Pedigree function

cat("\n * Preparing files for mTDT run... \n ")

mtdt_ped = rbind(ped, completePedigree(ped))
mtdt_map = paste0("M", (7:ncol(mtdt_ped)-6))

# --- write CP files

cat("* Writing processed files... \n ")

write.table(mtdt_ped, paste0(unlist(str_split(ped_basename,".ped"))[1],"_CP.ped"),
            sep = "\t", quote = F, col.names = F, row.names = F)
write.table(mtdt_map, paste0(unlist(str_split(map_basename,".map"))[1],"_CP.map"),
            sep = "\t", quote = F, col.names = F, row.names = F)

# ---  run command
cmd = paste0("cp ", opt$phenfile, " .")
system(cmd)

cmd = paste0("Rscript mtdt.R --pedfile ", 
             unlist(str_split(ped_basename,".ped"))[1],"_CP.ped --mapfile ",
             unlist(str_split(ped_basename,".ped"))[1],"_CP.map --phenfile ", 
             phen_basename,".phen ")

# -- complete cmd

for (i in 4:length(flag)){    
  cmd = paste0(cmd," --",flag[i])
}

cat("\n ** Starting run.. \n ",cmd,"\n\n")
system(cmd)
# --- Output 

cat("\n ** Writing results... \n")

output <- read.csv("weighted_res_multilocus.csv", sep = ";")

if (opt$nbsim == 0){
  
  ### Output
  
  cat("\n ___________________________________________________________________________  \n\n")
  system("cat weighted_res_multilocus.csv  | column -t -s ';' > x; awk '{print $1,$2,$3,$4,$5,$6,$7}' x | column -t -s ' '; rm x")
  cat("\n ")
  cat("___________________________________________________________________________  \n\n")
  
  
  ### Classement selon p-value croissant
  
  cat("--- Rank of the 10 most significant markers in descending order ------------\n\n")
  t <- output[order(output$mTDT_asympt_Pval),]
  
  write.table(t[1:10,], "10_significants_markers",sep = "\t", quote = F, col.names = T, row.names = F)
  system("cat 10_significants_markers | column -t  > x; awk '{print $1,$2,$3,$4,$5,$6,$7}' x | column -t  ; rm  x 10_significants_markers")
  cat("\n----------------------------------------------------------------------------") 
}



if (opt$nbsim > 0){
  
  ### Output 
  
  cat("\n ___________________________________________________________________________________________________________________________________________  \n\n")
  system("cat weighted_res_multilocus.csv  | column -t -s ';'")
  cat("\n ___________________________________________________________________________________________________________________________________________  \n\n")

  ### Classement selon p-value croissant
  cat("--- Rank of the 10 most significant markers in descending order ----------------------------------------------------------------------\n\n")
  t <- output[order(output$mTDT_empirical_Pval_FDR),]
  
  write.table(t[1:10,], "10_significants_markers",sep = "\t", quote = F, col.names = T, row.names = F)
  system("cat 10_significants_markers | column -t ; rm 10_significants_markers")
  cat("\n--------------------------------------------------------------------------------------------------------------------------------------") 
}



 #---- Output filename

if (is.null(opt$markerset) == TRUE ){
  name_ = paste0(unlist(str_split(ped_basename,".ped"))[1],"_SM_results")
}
if (is.null(opt$markerset) == FALSE){
  name_ = paste0(unlist(str_split(ped_basename,".ped"))[1],"_MM_results")
}

cmd = paste0("mkdir ", name_,"; mv weighted* ", name_," ; mv *_CP.* ", name_,"; mv ",phen_basename ,".phen ",name_)
system(cmd)

#------------

cat("\n ** Run finished. Results are written in ", name_, "\n\n\n")
rm(list=ls())

