# [count the number if family the individual is implicated in]
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

extractdbwork <- function(dbMap, step, cutSize, file){
  # SNPs set => Plink input for extraction 
  write.table(
    x = dbMap$V2[(((step*cutSize)-cutSize)+1):(step*cutSize)], 
    quote = F, 
    sep = "\t", 
    col.names = F, 
    row.names = F, 
    append = F,
    file = paste0("extraction",step,".txt")
  )
  
  #/home/g4bbm/tools/Plink//plink 
  system(paste0("/home/g4bbm/tools/Plink/plink ",
                paste0("--file ", file, " "), 
                "--extract extraction",step,".txt ",
                "--recode tab --silent ",
                "--out dbwork",step))
  
  dbwork = read.table(
    file = paste0("dbwork",step,".ped"), 
    sep = "\t", 
    header = F, 
    stringsAsFactors = F, 
    strip.white = T, 
    na.strings = "0 0"
  )
  
  return(dbwork);
}

case.1 <- function(i, s, p1, p2, dataset){
  if(nrow(p1) == 1 & nrow(p2) == 1){
    if(!is.na(p1[,s]) & !is.na(p2[,s])){
      par1Alleles = str_split_fixed(p1[,s], " ", n = 2)
      p2Alleles = str_split_fixed(p2[,s], " ", n = 2)
      
      if((par1Alleles[,1] == par1Alleles[,2]) & (p2Alleles[,1] == p2Alleles[,2])){
        dataset[dataset$V2==i,s] = paste(sort(c(as.numeric(par1Alleles[,1]), as.numeric(p2Alleles[,1]))), collapse = " ")
        #cat(paste("[case 1] ind : ", i, "genotype : ",  s, " inferred to : ", dataset[dataset$V2==i,s], "\n"))
        #next
        return(dataset)
      }
    }
  }
  return(dataset)
}

case.2 <- function(i, s, nb.offsprings, df.offsprings,dataset){
  if(nb.offsprings >1){
    offSpring1 = offSpring2= NULL
    for(offspring in 1:nb.offsprings){
      if(!is.na(df.offsprings[offspring, s])){
        offSpringAllele = str_split_fixed(df.offsprings[offspring, s], " ", n = 2)
        
        if(offSpringAllele[,1] == offSpringAllele[,2]){
          # One homozygous offspring
          if(is.null(offSpring1)){
            offSpring1 = df.offsprings[offspring, s]
          }
          else if(offSpring1 != df.offsprings[offspring, s]){
            offSpring2 = df.offsprings[offspring, s]
            dataset[dataset$V2==i,s] = paste(
              unique(
                sort(
                  as.numeric(
                    str_split_fixed(paste(offSpring1,offSpring2, collapse = " "), " ", n = 4)
                  )
                )
              ), collapse = " ")
            #cat(paste("[case 2] ind : ", i, "genotype : ",  s, " inferred to : ", dataset[dataset$V2==i,s], "\n"))
            break
          }
        }
      }
    }
  } 
  return(dataset)
}

case.3 <- function(i, s, ind.as.par, p1, p2, nb.offsprings, df.offsprings, dataset){
  if(nb.offsprings >1){
    parterns = unique(df.offsprings[, ifelse(ind.as.par=="V3", "V4", "V3")])
    indPartener =  ifelse(ind.as.par=="V3", "V4", "V3")
    for(partern in unique(parterns)){
      p1 = dataset[dataset$V2 ==df.offsprings[1,ind.as.par],]
      p2 = dataset[dataset$V2 == partern, ]  
      dfOffsprings_tmp = df.offsprings[ 
        df.offsprings[,indPartener] == partern & 
          df.offsprings[,ind.as.par] == i , ]
      
      if(nrow(p1) >  0 & nrow(p2) > 0){
        if((!is.na(p1[,s]) & is.na(p2[,s])) | (is.na(p1[,s]) & !is.na(p2[,s]))){
          par = ifelse(is.na(p1[,s]), p2[,s], p1[,s])
          parAlleles = str_split_fixed(par, " ", n = 2)
          
          if((parAlleles[,1] == parAlleles[,2])){
            case3satisfied = 0
            for(offspring in 1:nrow(dfOffsprings_tmp)){
              if(!is.na(dfOffsprings_tmp[offspring, s])){
                offSpringAllele = str_split_fixed(dfOffsprings_tmp[offspring, s], " ", n = 2)
                if(case3satisfied == 0 & offSpringAllele[,1] == parAlleles[,1] & offSpringAllele[,2] == parAlleles[,2]){
                  case3satisfied = case3satisfied + 1
                } else if(offSpringAllele[,1] != offSpringAllele[,2]){
                  case3satisfied = case3satisfied + 1
                }
              }
              
              if(case3satisfied == 2){
                dataset[dataset$V2==i,s] = "1 2"
                #cat(paste0("[case 3] ind :", i ," - par1 : ",p1[,s], " inferred to ", dataset[dataset$V2==i,s], " | ", "par2 : ",p2[,s], "\n"))
                break
              }
            }
          }
        }
      }
    }
  }
  return(dataset)
}

getp1 <- function(i, dataset){
  return(dataset[dataset$V2 == i, 3])
}

getp2 <- function(i, dataset){
  return(dataset[dataset$V2 == i, 4])
}

case.4 <- function(i, s, ind.as.par, p1, p2, nb.offsprings, df.offsprings, mendel_tab, dataset){
  if(nb.offsprings >2){
    parterns = unique(df.offsprings[, ifelse(ind.as.par=="V3", "V4", "V3")])
    indPartener =  ifelse(ind.as.par=="V3", "V4", "V3")
    
    for(partern in unique(parterns)){
      p1 = dataset[dataset$V2 == df.offsprings[1,ind.as.par], ]
      p2 = dataset[dataset$V2 == partern, ]
      df.offsprings_tmp = df.offsprings[ df.offsprings[,indPartener] == partern & df.offsprings[,ind.as.par] == i, ]
      
      H_table = NULL
      
      for(offsprings_geno in unique(df.offsprings_tmp[ , s])){
        offsprings_geno_ = gsub(" ", "", offsprings_geno)
        H_table = rbind(H_table,mendel_tab[mendel_tab$Offspring == offsprings_geno_, ])
      }
      
      length_unique = length(unique(df.offsprings_tmp[ , s]))
      if(length_unique > 1){
        H_table = H_table[H_table$Prob != 1, ]
      }
      
      d = H_table$P1 - H_table$P2
      H_table$P1P2S = ifelse(d<0, paste0(H_table$P1,H_table$P2), paste0(H_table$P2, H_table$P1))
      
      if(length(intersect(unique(df.offsprings_tmp[ , s]), "1 1")) > 0){
        H_table = H_table[H_table$P1 != 22 & H_table$P2 != 22, ]
      }
      
      if(length(intersect(unique(df.offsprings_tmp[ , s]), "2 2")) > 0){
        H_table = H_table[H_table$P1 != 11 & H_table$P2 != 11, ]
      }
      
      Hypotheses = unique(H_table$P1P2S)
      
      best.p.value = 0
      best.hypothese = NA
      
      for(Hypothese in Hypotheses){
        # Expected distribution
        exp_dist = mendel_tab[mendel_tab$P1P2 == Hypothese, "Prob" ]  * nrow(df.offsprings_tmp)
        names(exp_dist) = mendel_tab[mendel_tab$P1P2 == Hypothese, "Offspring" ]
        
        # Observed distribution
        obs_dist = table(df.offsprings_tmp[ , s])
        obs_dist_names = gsub(" ", "", names(obs_dist))
        obs_dist = as.vector(obs_dist)
        names(obs_dist) = obs_dist_names
        
        #input for fisher test
        if(length(obs_dist) > length(exp_dist)){
          for(genotype in names(obs_dist)){
            exp_dist[genotype] = ifelse(is.na(exp_dist[genotype]), 0, exp_dist[genotype])
          }
          exp_dist = exp_dist[order(names(exp_dist))]
        } else if(length(obs_dist) < length(exp_dist)){
          for(genotype in names(exp_dist)){
            obs_dist[genotype] = ifelse(is.na(obs_dist[genotype]), 0, obs_dist[genotype])
          }
          obs_dist = obs_dist[order(names(obs_dist))]
        } else{
          obs_dist = obs_dist[order(names(obs_dist))]
          exp_dist = exp_dist[order(names(exp_dist))]
        }
        
        input_mat = rbind(obs_dist, exp_dist)
        
        if(ncol(input_mat) == 1){
          best.p.value = 1
          best.hypothese = Hypothese
        } else{
          if(!is.na(sum(input_mat))){
            res = chisq.test(input_mat)
            if(best.p.value < res$p.value){
              best.p.value = res$p.value
              best.hypothese = Hypothese
            }
          }
        }
      }
      
      results = c( best.hypothese, best.p.value)
      names(results) = c( "best.hypothese", "best.p.value")
      
      # [inference both parents]
      if(is.na(best.hypothese) == FALSE & length(parterns) == 1 &
         NucFam(i,dataset) == 1 & NucFam(parterns,dataset) == 1){
        dataset[dataset$V2 == i, s] = paste(substring(best.hypothese, 1, 1), substring(best.hypothese, 2, 2)) 
        dataset[dataset$V2 == parterns, s] = paste(substring(best.hypothese, 3, 3), substring(best.hypothese, 4, 4))
        #cat(paste0("[case 4] ",  ", Parent 1: ",i , "->", dataset[dataset$V2 == i, s], ", Parent 2: ", parterns, "->",dataset[dataset$V2 == parterns, s], "\n"))
      }
    }
  }
  return(dataset)
}

# ['dbwork' stands for Malaria Senegal Sample]
genoInference <-function(dbwork, step){
  before = sum(is.na(dbwork))
  
  mendel_table = read.table("mendel_table.tsv", sep = "\t", strip.white = TRUE, header = TRUE, stringsAsFactors = FALSE)
  
  for(ind in dbwork$V2){
    # missing genotypes 
    snps = which(is.na(dbwork[dbwork$V2 == ind,]))
    if(length(snps) == 0) next
    
    # individuals parents
    par1 = dbwork[dbwork$V2 == dbwork[dbwork$V2 == ind, "V3"],]
    par2 = dbwork[dbwork$V2 == dbwork[dbwork$V2 == ind, "V4"],]
    
    # individuals offsprings
    indASPar = ifelse(dbwork[dbwork$V2 == ind, "V5"] == 1, "V3" , "V4")
    dfOffsprings = dbwork[which(dbwork[, indASPar] == ind), ]
    nbOffSprings = nrow(dfOffsprings)
    
    for(snp in snps){
      dbwork = case.1(i = ind, s = snp, p1 = par1 , p2 = par2, dataset = dbwork)
      dbwork = case.2(i = ind, s = snp, nb.offsprings = nbOffSprings, df.offsprings = dfOffsprings, dataset = dbwork)
      dbwork = case.3(i = ind, s = snp, ind.as.par = indASPar, p1 = par1, p2 = par2, nb.offsprings = nbOffSprings, df.offsprings=dfOffsprings, dataset=dbwork)
      # dbwork = case.4(i=ind, s=snp, ind.as.par=indASPar, p1=par1, p2=par2, nb.offsprings=nbOffSprings, df.offsprings=dfOffsprings, mendel_tab = mendel_table, dataset=dbwork)
    } #snps loop
  } #ind loop
  
  after = sum(is.na(dbwork))
  cat(paste0("\n\nGENOTYPE INFERENCE FOR SUBSET NUMBER : ", step ,
             " \n[before] nb missing geno: ", before, "\n"))
  cat(paste0("[after] nb missing geno: ", after, "\n"))
  cat(paste0("Nb of genotypes inferred for subset [", step, "] : ", (before - after),  "\n\n"))
  
  return(dbwork)
}

####_________________________________________________________________________________________####

#[LOAD LIBRARIES]
#library(pedigree)
require(optparse)
#require(foreach)
require(doParallel)
#require(gtools)
library(stringr)
#source("genoInference_libs.R")

# Options
option_list = list(
  make_option(c("--cores"), type="integer", default=2, help="Number of cores to be used", metavar="character"),
  
  make_option(c("--cutsize"), type="integer", default=50, help="Number of SNP in each sub database", metavar="character"),
  
  make_option(c("--out"), type="character", default="out", help="Ouput file name.", metavar="character"),
  
  make_option(c("--file"), type="character", default="file", help="Basename (.ped, .fam)", metavar="character")
)
opt_parser = OptionParser(option_list=option_list)
opt = parse_args(opt_parser)

registerDoParallel(cores = opt$cores) 
cutSize = opt$cutsize        
setwd(system("pwd", intern = T))           

dbMap = read.table(
  file = paste0(opt$file,".map"), 
  sep = "", 
  header = F, 
  stringsAsFactors = F, 
  strip.white = T
)

nbSteps = ceiling(nrow(dbMap)/cutSize)

### _______________STEP 1________________###
step = 1
# [database extraction]
dbwork = extractdbwork(dbMap, step, cutSize, opt$file)
#completion = completePedigree(dbwork)
#dbwork = rbind(dbwork, completion)

# [genotype inference] 
dbwork = genoInference(dbwork, step)
write.table(dbwork, sep = "\t", quote = F, file = paste0(opt$out ,step, ".ped"), col.names = F, row.names = F, na = "0 0")
# remove temp files
system(paste0("rm dbwork", step, ".*"))
system(paste0("rm extraction", step, ".txt"))
### ________________END_STEP 1____________###

results = foreach(step = 2:nbSteps, .combine=cbind) %dopar% { 
  if(step<nbSteps){ 
    
    # [database extraction]
    dbwork = extractdbwork(dbMap, step, cutSize, opt$file)
    
    #dbwork = rbind(dbwork, completion)
    # [genotype inference] 
    dbwork = genoInference(dbwork, step)
    
    write.table(dbwork, sep = "\t", quote = F, file = paste0(opt$out, step, ".ped"), col.names = F, row.names = F, na = "0 0")
    # remove temp files
    system(paste0("rm dbwork", step, ".*"))
    system(paste0("rm extraction", step, ".txt"))
    
  } 
  else{
    # [database extraction]
    n = NULL
    if(nrow(dbMap)%%cutSize == 0){
      n = cutSize
    }
    else{
      n = nrow(dbMap)%%cutSize
    }
    dbwork = extractdbwork(dbMap, nbSteps, n, opt$file)
    
    #dbwork = rbind(dbwork, completion)
    # [genotype inference] 
    dbwork = genoInference(dbwork, step)
    
    write.table(dbwork, sep = "\t", quote = F, file = paste0(opt$out, step, ".ped"), col.names = F, row.names = F, na = "0 0")
    # remove temp files
    system(paste0("rm dbwork", step, ".*"))
    system(paste0("rm extraction", step, ".txt"))
  }
}
