#!/usr/bin/env Rscript
args = commandArgs(trailingOnly = TRUE) 

#   @MaryemT 

#   avalanche-org

#   /Gen_Assoc

#-------  Summary
#-------  ped, map and phen files given as arguments
#         Should a problem occur, contact : NdeyeMarieme.top@pasteur.sn

#-------  Packages

if(("optparse" %in% rownames(installed.packages())) == F){
  install.packages("optparse", dependencies=TRUE, repos="http://cran.r-project.org")
} 
if(("stringr" %in% rownames(installed.packages())) == F){
  install.packages("optparse", dependencies=TRUE, repos="http://cran.r-project.org")
} 
if(("descr" %in% rownames(installed.packages())) == F){
  install.packages("descr", dependencies=TRUE, repos="http://cran.r-project.org")
} 

#-------  Functions

# -- [count the number of family the individual is implicated in]
Numb_trios <- function(dataset){
  for (i in dataset$V2){

    for (i in intersect(dataset$V2,dataset$V3)){      #si i est pere

      numb_f_partners = nrow(unique(dataset[dataset$V3 == i, c(3,4)]))
      numb_couple = numb_couple + numb_f_partners
    }
    return(numb_couple)
  }
}

#-------  Collect arguments

library(optparse)
library(stringr)
library(descr)

path = getwd()

dt <- Sys.time()

cat("_____________________________\n\n")
cat("Working directory:",path,"\n")
cat("Run started at: ",as.character(dt),"\n")



# Options
option_list = list(
  make_option(c("--pedfile"), type="character", help="ped file", metavar="character"),
  make_option(c("--mapfile"), type="character", help="map file", metavar="character"),
  make_option(c("--phenfile"), type="character", help="phenotype file", metavar="character")
)

opt_parser = OptionParser(option_list=option_list)
opt = parse_args(opt_parser)

path_to_file = unlist(str_split(opt$pedfile, unlist(str_split(opt$pedfile,"/"))[length(unlist(str_split(opt$pedfile,"/")))]))[1]

opt$pedfile = unlist(str_split(opt$pedfile,"/"))[length(unlist(str_split(opt$pedfile,"/")))]
opt$mapfile = unlist(str_split(opt$mapfile,"/"))[length(unlist(str_split(opt$mapfile,"/")))]
opt$phenfile = unlist(str_split(opt$phenfile,"/"))[length(unlist(str_split(opt$phenfile,"/")))]

if(is.null(opt$pedfile)) {cat("Option --pedfile is required. \n Execution stopped.")}
if(is.null(opt$mapfile)) {cat("Option --mapfile is required. \n Execution stopped.")}
if(is.null(opt$phenfile)) stop(cat("Option --phenfile is required. \n Execution stopped."))

# --- Files

ped = read.delim(paste0(path_to_file, opt$pedfile), header = F , stringsAsFactors = F)
map = read.delim(paste0(path_to_file, opt$mapfile), header = F , stringsAsFactors = F)
phen = read.delim(paste0(path_to_file, opt$phenfile), header = F , stringsAsFactors = F)

#phen = read.table(paste0(path_to_file, opt$phenfile), header = T)

# --- Variables
numb_couple = 0

# ---   SUMMARY STATISTICS  ---
# --- --- --- --- --- --- --- - 

cat("\nGenerating Summary Statistics..\n")
cat("\n   ---  Data loaded \n")
cat("-- ", opt$pedfile,"\n-- ", opt$mapfile,"\n-- ", opt$phenfile,"\n")

cat("\n   ---  Data description \n")   
cat("-- ","Families :", length(unique(ped$V1)),"\n")
cat("-- ","Founders :", length(which(ped$V3 == 0)),"\n")
cat("-- ","Nuclear Families :", Numb_trios(ped),"\n\n")
cat("   -  Sex description \n")
cat("-- ",nrow(ped), "individuals","\t",length(which(ped$V5== "1")), "males", length(which(ped$V5== "2")), "females \n\n")
cat("   -  Markers :\n")
cat("-- ",nrow(map)," markers \n\n")
cat("   -  Missing values \n")
cat("-- ","missing at \t: ", length(ped[ped == '0 0']), " / ",nrow(ped)* (ncol(ped)-6),"positions \n")
cat("-- ","Percentage \t:  ", (length(ped[ped == '0 0'])/(nrow(ped)* (ncol(ped)-6))) * 100,"%\n\n")

cat("   -  Phenotype description \n")

cat("-- ","in" ,opt$phenfile,"\t:" ,(ncol(phen)-2)," phenotype(s) detected\n\n")

phenotypes = colnames(phen)[3:ncol(phen)]

i=1; j = 1; count = 0

for (i in 1:length(phenotypes)){
  
  if(isFALSE(phen[, phenotypes[i]][j]%%1==0) && isTRUE(phen[, phenotypes[i]][j] != 0)){
    count = count + 1
  }
  cat("-- ","Phenotype ",phenotypes[i], " : ")
  if(count>=1){
    cat(" quantitative -------------\n\n")
    cat( descr(phen[,phenotypes[i]]))
  }
  if (count==0){
    cat(" categorial   -------------\n\n")

    cat(" Levels:\t", sort(unique(phen[,phenotypes[i]])),"\n Counts:\t", table(phen[,phenotypes[i]]),"\n")

  }
  
  cat("\n")
  count = 0
}


# --- Check for Mendelian errors

# plink_ = "/home/g4bbm/tools/Plink/plink"

#cat("--- Check Mendelian errors")
# cmd = paste0("cp ",paste0(path_to_file, opt$pedfile)," check_mendel.ped ; cp ",paste0(path_to_file, opt$mapfile)," check_mendel.map")
# system(cmd)
# 
# system(paste0(plink_ ," --file check_mendel --mendel --out sample_check"))
# system("rm *check*")        
