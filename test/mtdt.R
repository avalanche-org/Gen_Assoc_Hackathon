ls()
rm(list=ls())

# Installation of required packages
if(("doParallel" %in% rownames(installed.packages())) == F){
  install.packages("doParallel", dependencies=TRUE, repos="http://cran.r-project.org")
} 
if(("optparse" %in% rownames(installed.packages())) == F){
  install.packages("optparse", dependencies=TRUE, repos="http://cran.r-project.org")
} 


require(doParallel)
require(optparse)

# Options
option_list = list(
  make_option(c("--nbsim"), type="integer", default=0, help="The number of simulations", metavar="character"),
  make_option(c("--nbcores"), type="integer", default=1, help="The number of cores", metavar="character"),
  make_option(c("--markerset"), type="character", default=NULL, help="The number of cores", metavar="character"),
  make_option(c("--pedfile"), type="character", default=NULL, help="Name of the ped file.", metavar="character"),
  make_option(c("--mapfile"), type="character", default=NULL, help="Name of the map file.", metavar="character"),
  make_option(c("--phenfile"), type="character", default=NULL, help="Name of the phenotype file.", metavar="character"),
  make_option(c("--phen"), type="integer", default=1, help="Position of the phenotype to be analysed.", metavar="character"),
  make_option(c("--out"), type="character", default="weighted_res_multilocus", help="Outfile name", metavar="character")
)

opt_parser = OptionParser(option_list=option_list)
opt = parse_args(opt_parser)

registerDoParallel(cores=opt$nbcores) 

path = system("pwd", intern = T)

source(paste0(path,"/libs/modules.R"))
setwd(path)

# 
if(is.null(opt$pedfile)) stop("Option --pedfile is required.")
if(is.null(opt$mapfile)) stop("Option --mapfile is required.")
if(is.null(opt$phenfile)) stop("Option --phenfile is required.")

# recap. options
cat(paste0("--pedfile ", opt$pedfile, "\n"))
cat(paste0("--mapfile ", opt$mapfile, "\n"))
cat(paste0("--phenfile ", opt$phenfile, "\n"))
cat(paste0("--phen ", opt$phen, "\n"))
cat(paste0("--nbsim ", opt$nbsim, "\n"))
cat(paste0("--nbcores ", opt$nbcores, "\n"))
cat(paste0("--out ", opt$out, "\n"))

pedfile=read.table(paste0(path,"/", opt$pedfile), sep="\t", header=FALSE, stringsAsFactors = F)
mapfile=read.table(paste0(path,"/", opt$mapfile), sep="\t", header=FALSE, stringsAsFactors = F)
phenfile=read.table(paste0(path,"/", opt$phenfile), sep="\t", header=FALSE, stringsAsFactors = F)

steps = ifelse(is.null(opt$markerset), (ncol(pedfile)-6), 1) # [NEW]
if(steps > 1) cat(paste0("\n\nScreening all the ", steps," markers..\n"))
res_final_final = NULL

for(step in 1:steps){
  
  if(steps > 1){ # screening all markers one by one...
    markerset = c(step)
    cat(paste0(mapfile[step,]," (postion : ", step, ") is being analysed...\n"))
  } 
  else {
    markerset = as.numeric(strsplit(opt$markerset,",")[[1]])
    cat(paste0("--markerset ", markerset, "\n"))
  }
  
  ### CALLING FUNCTION 1:
  res1 <- ped_to_offspring_father_mother(pedfile, markerset, phenfile, opt$phen, mapfile, opt$out)
  pedfile2 <- res1[[1]]
  nbloci <- res1[[2]]
  markerset <- res1[[3]] # NEW
  rm(res1)
  if(nbloci == 0) next # NEW
  
  ### CALLING FUNCTION 2:
  res2 <- alleles_sets(pedfile2, nbloci)
  taballeles <- res2[[1]]
  kuplet <- res2[[2]]
  nbkuplet <- res2[[3]]
  rm(res2)
  
  ### CALLING FUNCTION 3:
  pedfile2 <- managing_ambiguous_transmission(pedfile2)
  
  ### CALLING FUNCTION 4:
  transmat <- computing_transmat(kuplet, pedfile2, nbloci)
  
  ### CALLING FUNCTION 5:
  alpha <- computing_alpha(pedfile2, taballeles, nbloci, transmat)
  
  ### CALLING FUNCTION 6:
  res6 <- transmitted_non_transmitted_counts(transmat)
  nT <- res6[[1]]
  nNT <- res6[[2]]
  rm(res6)
  
  ### CALLING FUNCTION 7:
  nbmodel <- number_of_models(nbloci)
  
  ### CALLING FUNCTION 8:
  res8 <- single_locus_transmission_probs(nbmodel, nT, nbloci, taballeles, nbkuplet, kuplet, alpha, pedfile2)
  tau <- res8[[1]]
  ddl <- res8[[2]]
  nb_info_transmi <- res8[[3]]
  m <- nbloci
  
  ### CALLING FUNCTION 9:
  if(length(markerset)>1){ 
    res9 <- l_uplet_transmission_probabilities (nbloci, taballeles, alpha, transmat, tau, ddl, nb_info_transmi)
    tau <- res9[[1]]
    ddl <- res9[[2]]
    nb_info_transmi <- res9[[3]]
    m <- res9[[4]]
  }
  
  ### CALLING FUNCTION 10:
  res10 <- log_likelihoods_computation(tau,nT, nNT, m, ddl)
  LL <- res10[[1]]
  LL0 <- res10[[2]]
  mTDT <- res10[[3]]
  pvalmTDT <- res10[[4]]
  pCorFDR <- res10[[5]]  
  
  ### CALLING FUNCTION 11:
  res11 <- display_results(mapfile[markerset,], LL, LL0, mTDT, pvalmTDT, pCorFDR)
  #res11 <- display_results(mapfile[pos_snp_to_analyze,], LL, LL0, mTDT, pvalmTDT, pCorFDR) # NEW
  res_final= ResultsMultilocus = res11
  
  
  ### CALLING FUNCTION 13:
  if(opt$nbsim>0){ 
    #if(step == 1){
      #cat(paste0("Running ", opt$nbsim,  " Simulations...\n")) 
      #cat("Please wait, this may take a while...\n")
    #}
    res_final <- compute_empirical_Pval(nbsimul = opt$nbsim, kuplet, pedfile2, nbloci)
  }
  
  
  res_final_final = rbind(res_final_final, res_final)
}

### WRITING FINAL RESULT
write.csv2(res_final_final, file = paste(path, "/", opt$out, ".csv", sep=""), quote=F, row.names=F) # [ NEW ]    
cat("Results are written on the file indicated below:\n")
cat(paste0("'",path, "/", opt$out, ".csv'\n"))
cat("Bye\n")
