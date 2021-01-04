#!/usr/bin/env Rscript
args = commandArgs(trailingOnly = TRUE) 

#   @MaryemT 

#   avalanche-org

#   /Gen_Assoc

#-------  Summary
#-------  ped, map and phen files given as arguments
#         Should a problem occur, contact : NdeyeMarieme.top@pasteur.sn


if(("optparse" %in% rownames(installed.packages())) == F){
  install.packages("optparse", dependencies=TRUE, repos="http://cran.r-project.org")
} 

#-------  Functions

# -- [count the number of family the individual is implicated in]
NucFam <- function(i, dataset) {
  n =  nrow(unique(dataset[dataset$V3 == i, c(3,4)]))
  if(n == 0){
    n =  nrow(unique(dataset[dataset$V4 == i, c(3,4)]))
  }
  if(nrow(dataset[dataset$V2 == i,]) > 0 ){
    if( dataset[dataset$V2 == i, 3] != "0" & dataset[dataset$V2 == i, 4] != "0"){
      n = n + 1
    }
  }
  return(n)
}


#-------  Paths
path = getwd()
plink_ = "/home/g4bbm/tools/Plink/plink"

#-------  Collect arguments

library(optparse)

cat("_____________________________")
cat("\n*** Working directory: ",path,"\n")

# Options
option_list = list(
  make_option(c("--pedfile"), type="character", help="ped file", metavar="character"),
  make_option(c("--mapfile"), type="character", help="map file", metavar="character"),
  make_option(c("--phenfile"), type="character", help="phenotype file", metavar="character")
  
)

opt_parser = OptionParser(option_list=option_list)
opt = parse_args(opt_parser)

if(is.null(opt$pedfile)) stop("Option --pedfile is required.")
if(is.null(opt$mapfile)) stop("Option --mapfile is required.")
if(is.null(opt$phenfile)) stop("Option --phenfile is required.")

# --- Files
ped = read.delim(paste0(path,"/",opt$pedfile), header = F , stringsAsFactors = F)
map = read.delim(paste0(path,"/",opt$mapfile), header = F , stringsAsFactors = F)
phen = read.delim(paste0(path,"/",opt$phenfile), header = F , stringsAsFactors = F)

# --- File Control

if (( nrow(map) != ncol(ped)-6) | nrow(phen)!=nrow(ped) ) stop(
  cat("\n /!\ Files do not match. \n"),
  cat("**", ncol(ped)-6 ," markers for ped file \n"),
  cat("**", nrow(map) ," markers for map file \n")
)

# --- Variables
numb_snps = nrow(ped)* (ncol(ped)-6)
missing_snps= length(ped[ped == '0 0'])
total_nuc_Fam= 0
individuals= ped$V2
for (i in 1:length(individuals)) { total_nuc_Fam = total_nuc_Fam + NucFam(individuals[i], ped); i = i+1}

# --- Summary output

cat("\n Data loaded\n--- ",
    opt$pedfile,"\n--- ",
    opt$mapfile,"\n--- ",
    opt$phenfile,"\n\n",
    
    ncol(ped)-6,"markers" ,nrow(ped), "individuals  | ",
    length(which(ped$V5== "1")), "males", length(which(ped$V5== "2")), "females \n",
    "Number of Nuclear families  : " , total_nuc_Fam,"\n",
    "in" ,opt$phenfile,"\t:" ,(ncol(phen)-2)," phenotype(s) detected\n",
    
    "\n   ---  Missing values\n",
    "missing at \t: ", missing_snps, "positions \n",
    "%(0 0)\t\t:  ", (missing_snps/numb_snps)*100,"\n\n",
    "  ---  Check for Mendelian errors \n")

# --- Check for Mendelian errors

cmd = paste0("cp ",opt$pedfile," check_mendel.ped ; cp ",opt$mapfile," check_mendel.map")
system(cmd)

system(paste0(plink_ ," --file check_mendel --mendel --out sample_check"))
system("rm *check*")        

