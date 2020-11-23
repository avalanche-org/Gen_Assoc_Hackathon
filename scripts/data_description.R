

#   @MaryemT 
#   avalanche-org
#   /Gen_Assoc

#   Descriptif au chargement des fichiers ped, map, phen 

                          #   * file names
                          #   * sortie plink af GUI ? 


plink_ = "/home/g4bbm/tools/Plink/plink"


ped = read.delim("sample.ped", header = F , stringsAsFactors = F)
map = read.delim("sample.map", header = F , stringsAsFactors = F)
phen = read.delim("sample.phen", header = F , stringsAsFactors = F)

#    ---  SUMMARY

numb_snps = nrow(ped)* (ncol(ped)-6)
missing_snps= length(ped[ped == '0 0'])


cat("--- Data description  \t \n\n", ncol(ped)-6,"snps of", nrow(ped), "individuals \n",
    "\t Total number of missing snps :\t", missing_snps, "\n",
    "\t Percentage of missing values :\t", (missing_snps/numb_snps)*100,
    "\n   ---  Check for Mendelian errors \n")

#    ---  Check for Mendelian errors

system(paste0(plink_ ," --file sample --mendel --out sample_check"))
system("grep Mendel sample_check.log; rm *check*")                  #log?

