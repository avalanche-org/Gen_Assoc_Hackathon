# ------------------------------------------------------ #
# ------------------------------------------------------ #
# ------------------------------------------------------ #

### FUNCTION 1:

ped_to_offspring_father_mother <- function(ped, pos_snp_to_analyze, phenfile, pos_phen_to_analyse, mapfile, out){ # NEW : mapfile
  
  # ------------------------------------------------------ #
  if((ncol(ped) < (max(pos_snp_to_analyze)+6)) | (min(pos_snp_to_analyze)<0) 
     | (length(pos_snp_to_analyze)+6) > ncol(ped)){
    stop("Enable to map all markers \nPlease CHECK you markers set!!!")
  }
  if(length(pos_snp_to_analyze) != length(unique(pos_snp_to_analyze))){
    stop("One or more markers are repeted in the given markers set!!!")
  }
  ped <- ped[,c(1:6, 6+pos_snp_to_analyze)]
  phenfile <- phenfile[,c(1:2, 2+pos_phen_to_analyse)]
  
  nbloci <- length(pos_snp_to_analyze)
  l <- nbloci
  colnames(ped) <- c("family","idDN","father","mother","sex","quanti_phen", paste0("idlocus",1:l))
  ped$quanti_phen = NULL
  colnames(phenfile) <- c("family", "idDN","quanti_phen")
  ped <- merge(ped, phenfile, by= c("family", "idDN"), all.x = T)
  ped <- ped[,c("family","idDN","father","mother","sex","quanti_phen", paste0("idlocus",1:l))]
  
  # ------------------------------------------------------ #
  paternal_geno=data.frame(unique(ped$father))
  names(paternal_geno)=c("idDN")
  paternal_geno=unique(merge(paternal_geno,ped[,c("family","idDN",paste0("idlocus",1:l))], by="idDN"))
  names(paternal_geno)=c("father","family",paste0("falocus",1:l))
  
  maternal_geno=data.frame(unique(ped$mother))
  names(maternal_geno)=c("idDN")
  maternal_geno=unique(merge(maternal_geno,ped[,c("family","idDN",paste0("idlocus",1:l))], by="idDN"))
  names(maternal_geno)=c("mother","family",paste0("molocus",1:l))
  
  # ------------------------------------------------------ #
  gendata=unique(ped[,c("family","idDN","father","mother","sex","quanti_phen",paste0("idlocus",1:l))])
  gendata=merge(gendata, paternal_geno, by=c("family","father"), all.x=T)
  gendata=merge(gendata, maternal_geno, by=c("family","mother"), all.x=T)
  rm(paternal_geno,maternal_geno)
  
  gendata[,(ncol(gendata)-3*l+1):ncol(gendata)][is.na(gendata[,(ncol(gendata)-3*l+1):ncol(gendata)])]="0 0"
  gendata=gendata[,c("family","idDN","father","mother","sex","quanti_phen",paste0("idlocus",1:l), paste0("falocus",1:l), paste0("molocus",1:l))]
  gendata=gendata[order(gendata$family,gendata$idDN),]
  
  # ------------------------------------------------------ #
  gendata2=unique(gendata[!is.na(gendata$quanti_phen), 
                          c(paste0(c("fa","mo","id"),"locus",sort(rep(1:nbloci,3))),"father","mother","idDN","sex","quanti_phen")])
  for (i in 1:nbloci) {
    gendata2=unique(gendata2[gendata2[,paste0("falocus",i)]!="0 0" & gendata2[,paste0("molocus",i)]!="0 0" & gendata2[,paste0("idlocus",i)]!="0 0",])
  }
  
  #------------LOOKING FOR CONSTANT MARKERS-----------------#
  nbloci.new = 0
  for(i in 1:nbloci){
    fa_allele1 = substr(gendata2[,(i*3)-2] , 1, 1)
    fa_allele2 = substr(gendata2[,(i*3)-2] , 3, 3)
    mo_allele1 = substr(gendata2[,(i*3)-1] , 1, 1)
    mo_allele2 = substr(gendata2[,(i*3)-1] , 3, 3)
  
    if(sum((fa_allele1 != fa_allele2) * 1) >= 1 | sum((mo_allele1 != mo_allele2) * 1) >= 1){
      nbloci.new = nbloci.new + 1
    }
    else{
      gendata2 = gendata2[, -c((i*3), ((i*3)-1), ((i*3)-2))]
      cat(paste0("\nMarker at position ", mapfile[pos_snp_to_analyze[i], ], " (position : ",pos_snp_to_analyze[i], ") skipped, because of no variation in the genotype across individuals!\n\n"))
      pos_snp_to_analyze = pos_snp_to_analyze[-c(i)]
    }
  }
  nbloci = nbloci.new 
  if(nbloci == 0){
    return(list(gendata2, nbloci, pos_snp_to_analyze))
  }
  #--------------------------------------------------------#
  
  # ------------------------------------------------------ #
  write.table(gendata2, file=paste(path,"/", out, ".work",sep=""), sep=" ", quote=F, row.names=F, col.names=F)
  gendata2=read.table(paste(path,"/", out, ".work",sep=""), sep=" ")
    names(gendata2)=c(paste0(c("fal","fal","mol","mol","chl","chl"), sort(rep(1:nbloci,3*2)),rep(c("a1","a2"),3)),
                      "father","mother","child","sex","quanti_phen")
  # ------------------------------------------------------ #
  
  return(list(gendata2, nbloci, pos_snp_to_analyze))
}


# ------------------------------------------------------ #
# ------------------------------------------------------ #
# ------------------------------------------------------ #
# ---------- LISTE OF POSSIBLE K-UPLET ----------------- #
# ------------------------------------------------------ #

### FUNCTION 2:

alleles_sets <- function(gendata2, nbloci){
  
  l <- nbloci
  alleles_all = unique(sort(c(as.matrix(gendata2[,1:(6*l)]))))
  nballeles_all=length(alleles_all)
  
  # ------------------------------------------------------ #
  taballeles=matrix(NA,nbloci,nballeles_all)
  rownames(taballeles)=c(paste("locus",1:nbloci,sep=""))
  colnames(taballeles)=c(paste("allele",alleles_all,sep=""))
  for (l in 1:nbloci){
    alleles = unique(sort(c(as.matrix(gendata2[,((l-1)*6+1):(6*l)]))))
    taballeles[l,1:length(alleles)]=alleles
  }
  rm(l)
  
  # ------------------------------------------------------ #
  locus_alleles = list()
  for (i in 1:nrow(taballeles)){
    locus_alleles[[i]] = taballeles[i,]
  }
  res = expand.grid(locus_alleles,stringsAsFactors = F)
  kuplet=NULL
  for(i in 1:ncol(res)){
    kuplet=paste0(kuplet,res[,i])
  }
  kuplet = sort(kuplet)
  nbkuplet=length(kuplet)
  rm(i,res,locus_alleles)
  
  # ------------------------------------------------------ #
  return(list(taballeles, kuplet, nbkuplet))
}

# ------------------------------------------------------ #
# ------------------------------------------------------ #
# ------------------------------------------------------ #
# SIMULATION OF POSSIBLE CHILDREN FOR AMBIGUOUS TRANSMISSIONS #
# ----------------------------------------------------------- #

### FUNCTION 3:

managing_ambiguous_transmission <- function(gendata2){
  
  gendata2$countw=1
  gendata2$realchild=1
  
  for (n in 1:nrow(gendata2)){
    
    nbdoubt=0
    locusdoubt=0
    for (l in 1:nbloci){
      if (gendata2[n,6*(l-1)+1]==gendata2[n,6*(l-1)+3] & gendata2[n,6*(l-1)+1]==gendata2[n,6*(l-1)+5] &
          gendata2[n,6*(l-1)+2]==gendata2[n,6*(l-1)+4] & gendata2[n,6*(l-1)+2]==gendata2[n,6*(l-1)+6] &
          gendata2[n,6*(l-1)+1]!=gendata2[n,6*(l-1)+2] &
          gendata2$realchild[n]==1){
        nbdoubt=nbdoubt+1
        locusdoubt[nbdoubt]=l
      }
    }
    
    if (nbdoubt>0) {
      gensimchild=NULL
      for (p in (nbdoubt-1):0) {
        gensimchild = c(gensimchild,rep(c(rep(1,2^p),rep(2,2^p)),2^(nbdoubt-p-1)))
      }
      gensimchild=matrix(gensimchild,2^nbdoubt,nbdoubt)
      
      for (i in 1:2^nbdoubt){
        gendata2=rbind(gendata2,gendata2[n,])
        gendata2[nrow(gendata2),6*(locusdoubt-1)+5]=gensimchild[i,]
        gendata2[nrow(gendata2),6*(locusdoubt-1)+6]=gensimchild[i,]
      }
      
      gendata2$countw[n]=0
      gendata2$countw[(nrow(gendata2)-2^nbdoubt+1):nrow(gendata2)]=1/2^nbdoubt
      gendata2$realchild[(nrow(gendata2)-2^nbdoubt+1):nrow(gendata2)]=0
      
    }
  }
  rm(n,l,p,i)
  
  # ------------------------------------------------------ #
  return(gendata2)
}


# ------------------------------------------------------ #
# ------------------------------------------------------ #
# ------------------------------------------------------ #
# --- TO COMPUTE MATRIX OF SUMULTANEOUS TRANSMISSION --- #
# ------------------------------------------------------ #

### FUNCTION 4:

computing_transmat <- function(kuplet, gendata2, nbloci, locus_on_X = 0){
  
  l <- nbloci
  transmat=matrix(0,length(kuplet),length(kuplet))
  rownames(transmat)=kuplet
  colnames(transmat)=kuplet
  
  # ------------------------------------------------------ #
  for (n in 1:nrow(gendata2)){
    
    kuplet_fa_T=NULL; kuplet_mo_T=NULL; kuplet_fa_NT=NULL; kuplet_mo_NT=NULL
    
    for (l in 1:nbloci){
      
      if ((length(setdiff(locus_on_X,l))==length(locus_on_X)) | (length(setdiff(locus_on_X,l))!=length(locus_on_X) & gendata2$sex[n]==2)){
        
        for (ii in 1:length(taballeles[l,][!is.na(taballeles[l,])])){
          for (jj in ii:length(taballeles[l,][!is.na(taballeles[l,])])){
            for (uu in 1:length(taballeles[l,][!is.na(taballeles[l,])])){
              for (vv in uu:length(taballeles[l,][!is.na(taballeles[l,])])){
                i=taballeles[l,][!is.na(taballeles[l,])][ii]; j=taballeles[l,][!is.na(taballeles[l,])][jj]
                u=taballeles[l,][!is.na(taballeles[l,])][uu]; v=taballeles[l,][!is.na(taballeles[l,])][vv]
                if (gendata2[n,6*(l-1)+1]==i & gendata2[n,6*(l-1)+2]==j & gendata2[n,6*(l-1)+3]==u & gendata2[n,6*(l-1)+4]==v & ((gendata2[n,6*(l-1)+5]==i & gendata2[n,6*(l-1)+6]==u) | (gendata2[n,6*(l-1)+5]==u & gendata2[n,6*(l-1)+6]==i))){
                  kuplet_fa_T=paste(kuplet_fa_T,i, sep=""); kuplet_mo_T=paste(kuplet_mo_T,u, sep=""); kuplet_fa_NT=paste(kuplet_fa_NT,j, sep=""); kuplet_mo_NT=paste(kuplet_mo_NT,v, sep="")}
                else {
                  if (gendata2[n,6*(l-1)+1]==i & gendata2[n,6*(l-1)+2]==j & gendata2[n,6*(l-1)+3]==u & gendata2[n,6*(l-1)+4]==v & ((gendata2[n,6*(l-1)+5]==i & gendata2[n,6*(l-1)+6]==v) | (gendata2[n,6*(l-1)+5]==v & gendata2[n,6*(l-1)+6]==i))){
                    kuplet_fa_T=paste(kuplet_fa_T,i, sep=""); kuplet_mo_T=paste(kuplet_mo_T,v, sep=""); kuplet_fa_NT=paste(kuplet_fa_NT,j, sep=""); kuplet_mo_NT=paste(kuplet_mo_NT,u, sep="")}
                  else {
                    if (gendata2[n,6*(l-1)+1]==i & gendata2[n,6*(l-1)+2]==j & gendata2[n,6*(l-1)+3]==u & gendata2[n,6*(l-1)+4]==v & ((gendata2[n,6*(l-1)+5]==j & gendata2[n,6*(l-1)+6]==u) | (gendata2[n,6*(l-1)+5]==u & gendata2[n,6*(l-1)+6]==j))){
                      kuplet_fa_T=paste(kuplet_fa_T,j, sep=""); kuplet_mo_T=paste(kuplet_mo_T,u, sep=""); kuplet_fa_NT=paste(kuplet_fa_NT,i, sep=""); kuplet_mo_NT=paste(kuplet_mo_NT,v, sep="")}
                    else {
                      if (gendata2[n,6*(l-1)+1]==i & gendata2[n,6*(l-1)+2]==j & gendata2[n,6*(l-1)+3]==u & gendata2[n,6*(l-1)+4]==v & ((gendata2[n,6*(l-1)+5]==j & gendata2[n,6*(l-1)+6]==v) | (gendata2[n,6*(l-1)+5]==v & gendata2[n,6*(l-1)+6]==j))){
                        kuplet_fa_T=paste(kuplet_fa_T,j, sep=""); kuplet_mo_T=paste(kuplet_mo_T,v, sep=""); kuplet_fa_NT=paste(kuplet_fa_NT,i, sep=""); kuplet_mo_NT=paste(kuplet_mo_NT,u, sep="")}
                    }
                  }
                }
              }}}}
      }
      
      # ------------------------------------------------------ #
      if (length(setdiff(locus_on_X,l))!=length(locus_on_X) & gendata2$sex[n]==1){
        
        if (gendata2[n,6*(l-1)+1]==1 & gendata2[n,6*(l-1)+2]==1 & gendata2[n,6*(l-1)+3]==1 & gendata2[n,6*(l-1)+4]==2 & gendata2[n,6*(l-1)+5]==2 & gendata2[n,6*(l-1)+6]==2){
          kuplet_fa_T=paste(kuplet_fa_T,1, sep=""); kuplet_mo_T=paste(kuplet_mo_T,2, sep=""); kuplet_fa_NT=paste(kuplet_fa_NT,1, sep=""); kuplet_mo_NT=paste(kuplet_mo_NT,1, sep="")}
        
        if (gendata2[n,6*(l-1)+1]==1 & gendata2[n,6*(l-1)+2]==1 & gendata2[n,6*(l-1)+3]==1 & gendata2[n,6*(l-1)+4]==2 & gendata2[n,6*(l-1)+5]==1 & gendata2[n,6*(l-1)+6]==1){
          kuplet_fa_T=paste(kuplet_fa_T,1, sep=""); kuplet_mo_T=paste(kuplet_mo_T,1, sep=""); kuplet_fa_NT=paste(kuplet_fa_NT,1, sep=""); kuplet_mo_NT=paste(kuplet_mo_NT,2, sep="")}
        
        if (gendata2[n,6*(l-1)+1]==2 & gendata2[n,6*(l-1)+2]==2 & gendata2[n,6*(l-1)+3]==1 & gendata2[n,6*(l-1)+4]==1 & gendata2[n,6*(l-1)+5]==1 & gendata2[n,6*(l-1)+6]==1){
          kuplet_fa_T=paste(kuplet_fa_T,1, sep=""); kuplet_mo_T=paste(kuplet_mo_T,1, sep=""); kuplet_fa_NT=paste(kuplet_fa_NT,1, sep=""); kuplet_mo_NT=paste(kuplet_mo_NT,1, sep="")}
        
        if (gendata2[n,6*(l-1)+1]==2 & gendata2[n,6*(l-1)+2]==2 & gendata2[n,6*(l-1)+3]==1 & gendata2[n,6*(l-1)+4]==2 & gendata2[n,6*(l-1)+5]==2 & gendata2[n,6*(l-1)+6]==2){
          kuplet_fa_T=paste(kuplet_fa_T,1, sep=""); kuplet_mo_T=paste(kuplet_mo_T,2, sep=""); kuplet_fa_NT=paste(kuplet_fa_NT,1, sep=""); kuplet_mo_NT=paste(kuplet_mo_NT,1, sep="")}
        
        if (gendata2[n,6*(l-1)+1]==2 & gendata2[n,6*(l-1)+2]==2 & gendata2[n,6*(l-1)+3]==1 & gendata2[n,6*(l-1)+4]==2 & gendata2[n,6*(l-1)+5]==1 & gendata2[n,6*(l-1)+6]==1){
          kuplet_fa_T=paste(kuplet_fa_T,1, sep=""); kuplet_mo_T=paste(kuplet_mo_T,1, sep=""); kuplet_fa_NT=paste(kuplet_fa_NT,1, sep=""); kuplet_mo_NT=paste(kuplet_mo_NT,2, sep="")}
        
        if (gendata2[n,6*(l-1)+1]==1 & gendata2[n,6*(l-1)+2]==1 & gendata2[n,6*(l-1)+3]==2 & gendata2[n,6*(l-1)+4]==2 & gendata2[n,6*(l-1)+5]==2 & gendata2[n,6*(l-1)+6]==2){
          kuplet_fa_T=paste(kuplet_fa_T,1, sep=""); kuplet_mo_T=paste(kuplet_mo_T,2, sep=""); kuplet_fa_NT=paste(kuplet_fa_NT,1, sep=""); kuplet_mo_NT=paste(kuplet_mo_NT,2, sep="")}
        
        if (gendata2[n,6*(l-1)+1]==2 & gendata2[n,6*(l-1)+2]==2 & gendata2[n,6*(l-1)+3]==2 & gendata2[n,6*(l-1)+4]==2 & gendata2[n,6*(l-1)+5]==2 & gendata2[n,6*(l-1)+6]==2){
          kuplet_fa_T=paste(kuplet_fa_T,1, sep=""); kuplet_mo_T=paste(kuplet_mo_T,2, sep=""); kuplet_fa_NT=paste(kuplet_fa_NT,1, sep=""); kuplet_mo_NT=paste(kuplet_mo_NT,2, sep="")}
        
        if (gendata2[n,6*(l-1)+1]==1 & gendata2[n,6*(l-1)+2]==1 & gendata2[n,6*(l-1)+3]==1 & gendata2[n,6*(l-1)+4]==1 & gendata2[n,6*(l-1)+5]==1 & gendata2[n,6*(l-1)+6]==1){
          kuplet_fa_T=paste(kuplet_fa_T,1, sep=""); kuplet_mo_T=paste(kuplet_mo_T,1, sep=""); kuplet_fa_NT=paste(kuplet_fa_NT,1, sep=""); kuplet_mo_NT=paste(kuplet_mo_NT,1, sep="")}
      }
    }
    
    # ------------------------------------------------------ #
    if (length(setdiff(kuplet,kuplet_fa_T))!=length(kuplet) & length(setdiff(kuplet,kuplet_fa_NT))!=length(kuplet) & length(setdiff(kuplet,kuplet_mo_T))!=length(kuplet) & length(setdiff(kuplet,kuplet_mo_NT))!=length(kuplet)){
      transmat[kuplet_fa_T,kuplet_fa_NT] = transmat[kuplet_fa_T,kuplet_fa_NT] + gendata2$countw[n]*abs(gendata2$quanti_phen[n])/sum(abs(gendata2$quanti_phen)*gendata2$countw)*sum(gendata2$countw)
      transmat[kuplet_mo_T,kuplet_mo_NT] = transmat[kuplet_mo_T,kuplet_mo_NT] + gendata2$countw[n]*abs(gendata2$quanti_phen[n])/sum(abs(gendata2$quanti_phen)*gendata2$countw)*sum(gendata2$countw)}
    
  }
  
  # ------------------------------------------------------ #
  rm(i,j,l,n,u,v,ii,jj,uu,vv,kuplet_fa_NT,kuplet_fa_T,kuplet_mo_NT,kuplet_mo_T)
  
  transmat[transmat==0]=0.0000001
  sum(transmat)
  
  # ------------------------------------------------------ #
  return(transmat)
}


# ------------------------------------------------------ #
# ------------------------------------------------------ #
# ------------------------------------------------------ #
# - TRANSMISSION INTENSITY OF ALLELES AT SINGLE LOCUS -- #
# ------------------------------------------------------ #

### FUNCTION 5:

computing_alpha <- function(gendata2, taballeles, nbloci, transmat){
  
  l=nbloci
  alleles_all = unique(sort(c(as.matrix(gendata2[,1:(6*l)]))))
  nballeles_all=length(alleles_all)
  
  alpha=matrix(NA,nbloci,nballeles_all)
  rownames(alpha)=c(paste("locus",1:nbloci,sep=""))
  colnames(alpha)=c(paste("allele",alleles_all,sep=""))
  
  for (l in 1:nbloci){
    for (a in taballeles[l,][!is.na(taballeles[l,])]){
      alpha[paste0("locus",l),paste0("allele",a)]=sum(transmat[substr(rownames(transmat),l,l)==paste(a),substr(colnames(transmat),l,l)!=paste(a)])/(sum(transmat[substr(rownames(transmat),l,l)==paste(a),substr(colnames(transmat),l,l)!=paste(a)])+sum(transmat[substr(rownames(transmat),l,l)!=paste(a),substr(colnames(transmat),l,l)==paste(a)]))
    }}
  rm(a,l)
  
  # ------------------------------------------------------ #
  return(alpha)
}


# ------------------------------------------------------ #
# ------------------------------------------------------ #
# ------------------------------------------------------ #
# ----- NUMBER OF TRANSMITTED AND NOT-TRANSMITTED ------ #
# ------------------------------------------------------ #

### FUNCTION 6:

transmitted_non_transmitted_counts <- function(transmat){
  k=0
  nT=0
  nNT=0
  for (i in 1:(dim(transmat)[2]-1)){
    for (j in (i+1):dim(transmat)[1]){
      k=k+1
      nT[k]=transmat[i,j]
      nNT[k]=transmat[j,i]
    }}
  rm(i,j,k)
  return(list(nT, nNT))
}


# ------------------------------------------------------ #
# ------------------------------------------------------ #
# ------------------------------------------------------ #
# ----- Number of possible alternative hypotheses ------ #
# ------------------------------------------------------ #

### FUNCTION 7:

number_of_models <- function(nbloci){
  nbmodel= nbloci
  if(nbloci>=2){
    for (i in 2:nbloci){
      nbmodel= nbmodel+ 2*choose(nbloci,i)
    }}
  return(nbmodel)
}


# ------------------------------------------------------ #
# ------------------------------------------------------ #
# ------------------------------------------------------ #
# ------- SINGLE TRANSMISSION PROBABILITIES ------------ #
# ------------------------------------------------------ #

### FUNCTION 8:

single_locus_transmission_probs <- function(nbmodel, nT, nbloci, taballeles, nbkuplet, kuplet, alpha, gendata2){
  
  nb_info_transmi <- NULL
  tau <- matrix(0,nbmodel,length(nT))
  ddl <- 0
  
  for (m in 1:nbloci){
    ddl[m]=length(taballeles[m,][!is.na(taballeles[m,])])-1
    
    nb_info_transmi[m] = (
      nrow(gendata2[
        gendata2[,paste("fal",m,"a",1, sep="")]!=
          gendata2[,paste("fal",m,"a",2, sep="")]
        & gendata2[,"realchild"]==1
        ,]) +
        nrow(gendata2[
          gendata2[,paste("mol",m,"a",1, sep="")]!=
            gendata2[,paste("mol",m,"a",2, sep="")]
          & gendata2[,"realchild"]==1
          ,]))
    
    k=0
    for (ii in 1:(nbkuplet-1)){
      for (jj in (ii+1):nbkuplet){
        i=kuplet[ii];j=kuplet[jj]
        k=k+1
        a=as.numeric(substr(i,m,m))
        b=as.numeric(substr(j,m,m))
        tau[m,k]=alpha[paste0("locus",m),paste0("allele",a)]/(alpha[paste0("locus",m),paste0("allele",a)]+alpha[paste0("locus",m),paste0("allele",b)])
      }}
  }
  rm(a,b,i,j,ii,jj,k)
  
  return(list(tau, ddl, nb_info_transmi))
}


# ------------------------------------------------------ #
# ------------------------------------------------------ #
# ------------------------------------------------------ #
# ------- L-UPLET TRANSMISSION PROBABILITIES ----------- #
# ------------------------------------------------------ #

### FUNCTION 9:

l_uplet_transmission_probabilities <- function(nbloci, taballeles, alpha, transmat, tau, ddl, nb_info_transmi){
  m <- nbloci
  for (n in 2:nbloci){
    
    marker_sets <- combn(nbloci, n)
    
    for (j in 1:ncol(marker_sets)){
      
      marker_sets_j <- marker_sets[, j]
      w_nbloci <- length(marker_sets_j)
      w_taballeles <- taballeles[paste0("locus", marker_sets_j),]
      w_alpha <- alpha[paste0("locus", marker_sets_j),]
      
      w_alleles <- NULL
      for (i in marker_sets_j){
        w_alleles <- paste0(w_alleles, substr(rownames(transmat), i, i))
      }
      rm(i,j)
      
      temp_transmat <- transmat
      rownames(temp_transmat) <- w_alleles
      colnames(temp_transmat) <- w_alleles
      
      w_kuplet <- w_alleles
      w_nbkuplet <- length(w_kuplet)
      
      w_transmat <- matrix(0, w_nbkuplet, w_nbkuplet)
      rownames(w_transmat) <- w_kuplet
      colnames(w_transmat) <- w_kuplet
      
      for (set_i in w_kuplet){
        for (set_j in w_kuplet){
          w_transmat[set_i,set_j] <- sum(temp_transmat[rownames(temp_transmat)==set_i, colnames(temp_transmat)==set_j])
        }
      }
      rm(set_i, set_j)
      
      w_nT <- transmitted_non_transmitted_counts(w_transmat)[[1]]
      w_nNT <- transmitted_non_transmitted_counts(w_transmat)[[2]]
      
      
      # MULTIPLICATIVE #
      
      m <- m + 1
      k=a=b=0
      for (ii in 1:(w_nbkuplet-1)){
        for (jj in (ii+1):w_nbkuplet){
          i=w_alleles[ii]; j=w_alleles[jj]
          k=k+1
          x=y=1
          df=0
          for (l in 1:w_nbloci){
            a[l]=as.numeric(substr(i,l,l))
            b[l]=as.numeric(substr(j,l,l))
            x = x*w_alpha[paste0("locus", marker_sets_j[l]),paste0("allele",a[l])]
            y = y*w_alpha[paste0("locus", marker_sets_j[l]),paste0("allele",b[l])]
            df = df + length(w_taballeles[l,][!is.na(w_taballeles[l,])])-1
          }
          tau[m,k] = x/(x+y)
          ddl[m] = df
          nb_info_transmi[m] = sum(w_nT+w_nNT)
        }}
      rm(a,b,i,j,ii,jj,k,l,x,y,df)
      
      # EPISTASIS #
      
      m <- m + 1
      k=0
      for (ii in 1:(w_nbkuplet-1)){
        for (jj in (ii+1):w_nbkuplet){
          i=w_alleles[ii]; j=w_alleles[jj]
          k=k+1
          tau[m,k]=(sum(w_transmat[i,-which(colnames(w_transmat) == i)])/(sum(w_transmat[i,-which(colnames(w_transmat) == i)])+sum(w_transmat[-which(colnames(w_transmat) == i),i])))/((sum(w_transmat[i,-which(colnames(w_transmat) == i)])/(sum(w_transmat[i,-which(colnames(w_transmat) == i)])+sum(w_transmat[-which(colnames(w_transmat) == i),i])))+(sum(w_transmat[j,-which(colnames(w_transmat) == j)])/(sum(w_transmat[j,-which(colnames(w_transmat) == j)])+sum(w_transmat[-which(colnames(w_transmat) == j),j]))))
        }}
      rm(i,j,ii,jj,k)
      
      df=1
      for (l in 1:w_nbloci){
        df=df*length(w_taballeles[l,][!is.na(w_taballeles[l,])])
      }
      
      ddl[m] = df-1
      nb_info_transmi[m] = sum(w_nT+w_nNT)
      rm(l,df)
    }
  }
  return(list(tau,ddl,nb_info_transmi, m))
}

# ------------------------------------------------------ #
# ------------------------------------------------------ #
# ------------------------------------------------------ #
# ------------------ LOG-LIKELIHOODS ------------------- #
# ------------------------------------------------------ #

### FUNCTION 10:

log_likelihoods_computation <- function(tau,nT, nNT, m, ddl){
  # MODEL0: WHITE MODEL
  
  LL0= -log(2)*sum(nT+nNT)
  LL0
  
  # MODEL 1 to m
  
  LL=0
  mTDT=0
  pvalmTDT=0
  
  for (l in 1:m){
    LL[l]= sum(nT*log(tau[l,]/(1-tau[l,]))) + sum((nT+nNT)*log(1-tau[l,]))
    mTDT[l]=2*(LL[l]-LL0)
    pvalmTDT[l]=1-pchisq(mTDT[l],ddl[l])
  }
  pCorFDR = p.adjust(pvalmTDT, method = "fdr")
  rm(l)
  return (list(LL,LL0, mTDT, pvalmTDT, pCorFDR))
}


# ------------------------------------------------------ #
# ------------------------------------------------------ #
# ------------------------------------------------------ #
# ---------------- TO DISPLAY RESULTS ------------------ #
# ------------------------------------------------------ #

### FUNCTION 11:

display_results <- function(marker_names, LL, LL0, mTDT, pvalmTDT, pCorFDR){
  models = SNPcomb = marker_names
  if (length(marker_names)>1){
    for (i in 2:length(models)){
      subcomb = combn(SNPcomb,i)
      for (j in 1:ncol(subcomb)){
        models = c(models, paste("Additive",paste(subcomb[,j], collapse="+"), sep=":"))
        models = c(models, paste("Epistasis",paste(subcomb[,j], collapse="*"), sep=":"))
        
      }
    }
  }
  ResultsMultilocus=data.frame(models, nb_info_transmi=round(nb_info_transmi),LL1=round(LL,1),LL0=round(LL0,1),mTDT_Stat=round(mTDT,2),DF=ddl, mTDT_asympt_Pval=pvalmTDT, mTDT_asympt_Pval_FDR=pCorFDR)
  return(ResultsMultilocus)
}

# ------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------- #
# ---------------- TO COMPUTE MATRIX OF SUMULTANEOUS TRANSMISSION SIMULATED------------------ #
# ------------------------------------------------------------------------------------------- #

### FUNCTION 12:

computing_sim_transmat <- function(kuplet, gendata2, nbloci, locus_on_X = 0){
  
  transmat=matrix(0,length(kuplet),length(kuplet))
  rownames(transmat)=kuplet
  colnames(transmat)=kuplet
  
  for (n in 1:nrow(gendata2)){
    
    kuplet_fa_T=NULL; kuplet_mo_T=NULL; kuplet_fa_NT=NULL; kuplet_mo_NT=NULL
    
    for (l in 1:nbloci){
      
      if ((length(setdiff(locus_on_X,l))==length(locus_on_X)) | (length(setdiff(locus_on_X,l))!=length(locus_on_X) & gendata2$sex[n]==2)){
        kuplet_fa_T_and_NT=paste(sample(gendata2[n,6*(l-1)+(1:2)])) ; kuplet_mo_T_and_NT=paste(sample(gendata2[n,6*(l-1)+(3:4)])) 
        kuplet_fa_T=paste0(kuplet_fa_T,kuplet_fa_T_and_NT[1])	; kuplet_mo_T=paste0(kuplet_mo_T,kuplet_mo_T_and_NT[1])
        kuplet_fa_NT=paste0(kuplet_fa_NT,kuplet_fa_T_and_NT[2])	; kuplet_mo_NT=paste0(kuplet_mo_NT,kuplet_mo_T_and_NT[2])
        
      }
    }
    
    if (length(setdiff(kuplet,kuplet_fa_T))!=length(kuplet) & length(setdiff(kuplet,kuplet_fa_NT))!=length(kuplet) & length(setdiff(kuplet,kuplet_mo_T))!=length(kuplet) & length(setdiff(kuplet,kuplet_mo_NT))!=length(kuplet)){
      transmat[kuplet_fa_T,kuplet_fa_NT] = transmat[kuplet_fa_T,kuplet_fa_NT] + gendata2$countw[n]*abs(gendata2$quanti_phen[n])/sum(abs(gendata2$quanti_phen)*gendata2$countw)*sum(gendata2$countw)
      transmat[kuplet_mo_T,kuplet_mo_NT] = transmat[kuplet_mo_T,kuplet_mo_NT] + gendata2$countw[n]*abs(gendata2$quanti_phen[n])/sum(abs(gendata2$quanti_phen)*gendata2$countw)*sum(gendata2$countw)}
    
  }
  rm(l,n,kuplet_fa_NT,kuplet_fa_T,kuplet_mo_NT,kuplet_mo_T)
  
  transmat[transmat==0]=0.0000001
  return(transmat)
}

# ------------------------------------------------------ #
# ------------------------------------------------------ #
# ------------------------------------------------------ #
# ------------ TO COMPUTE EMPIRICAL P-VALUES ----------- #
# ------------------------------------------------------ #

### FUNCTION 13:

compute_empirical_Pval <- function(nbsimul, kuplet, pedfile2, nbloci, locus_on_X = 0){
  SimTestStat = NULL
  transmatsaved = transmat
  
  SimTestStat <- foreach (repetition=1:nbsimul, .combine='rbind') %dopar% {
    
    transmat_sim <- computing_sim_transmat(kuplet, pedfile2, nbloci, locus_on_X)
    
    alpha <- computing_alpha(pedfile2, taballeles, nbloci, transmat_sim)
    
    res <- transmitted_non_transmitted_counts(transmat_sim)
    nT <- res[[1]]
    nNT <- res[[2]]
    rm(res)
    
    nbmodel <- number_of_models(nbloci)
    
    res <- single_locus_transmission_probs(nbmodel, nT, nbloci, taballeles, nbkuplet, kuplet, alpha, pedfile2)
    tau <- res[[1]]
    ddl <- res[[2]]
    nb_info_transmi <- res[[3]]
    m = nbloci
    
    if (nbloci > 1){
      res <- l_uplet_transmission_probabilities (nbloci, taballeles, alpha, transmat_sim, tau, ddl, nb_info_transmi)
      tau <- res[[1]]
      ddl <- res[[2]]
      nb_info_transmi <- res[[3]]
      m <- res[[4]]
    }
    
    res <- log_likelihoods_computation(tau,nT, nNT, m, ddl)
    LL <- res[[1]]
    LL0 <- res[[2]]
    mTDT <- res[[3]]
    pvalmTDT <- res[[4]]
    pCorFDR <- res[[5]]
    SimTestStat <- mTDT
  }
  
  if (nbsimul==1){
    SimTestStat <- t(SimTestStat)
  }
  
  empPval = NULL
  for (i in 1:ncol(SimTestStat)){
    empPval[i] = mean((SimTestStat[,i] > ResultsMultilocus$mTDT_Stat[i]) * 1 )
  }
  ResultsMultilocus$mTDT_empirical_Pval = empPval
  rm(i)
  ResultsMultilocus$mTDT_empirical_Pval_FDR = p.adjust(empPval, method = "fdr")
  return(ResultsMultilocus)
}

