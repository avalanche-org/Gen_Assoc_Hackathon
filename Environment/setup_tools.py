#!/usr/bin/env  python3  
# -*- coding: utf-8 -*- 

__author__ = "jukoo <j_umar@outlook.com>"  

"""
H3ABIONET : 
----------
+ Generic installation  for  Linux  , Windows and Mac OS X   
+ This is a quick  setup  for H3ABIONET  environment that 
+ include  R lang  - Rstudio IDE - and Plink.
 -------------------------------------------
{ Please read the  INSTALLATION  guide line }
 -------------------------------------------
"""

import os 
import sys 
import platform  
import logging as log 
import subprocess 
from enum import Enum  
from collections import  namedtuple 

def  sbp_cmdexe ( cmd )  : 
    stdargv     =  subprocess.Popen(cmd , stdout=subprocess.PIPE  ,shell=True) 
    status_code =  stdargv.wait() 
    return  status_code     

try :
    import  pip
except :
    # probably pip   is not installed or  the version is deprecated
    trooble_shooting_cmd ="python{} -m pip  install --upgrade pip".format(sys.version_info.major)
    exit_status  =  sbp_cmdexe(trooble_shooting_cmd)
    if  not exit_status.__eq__(0b0000)  :
        log.error("failed to trouble shooting  pip module install")
        sys.exit(BaseAbort.EXIT_FAILURE.value)

try : 
    import requests 
    import zipfile 
except :   
    pip.main(["install" ,"requests"])  
    pip.main(["install" ,"zipfile"])


class BaseAbort  ( Enum ) : 
    EXIT_FAILURE  = 1  
    EXIT_SUCCESS  = 0  

   
DIRECT_LINK  =  namedtuple("DIRECT_LINK" , [ "plink"  , "rstudio" , "rlang"])  
source       =  DIRECT_LINK(
        "http://s3.amazonaws.com/plink1-assets/"  , 
        "https://download1.rstudio.org/desktop/"  , 
        "https://cran.r-project.org/bin/"
        )      

PLINK_BUILD_VERSION  ="20200616"            #   plink  1.90 Beta version 
RSTUDIO_SOFT_VERSION ="RStudio-1.3.1073"
RLANG_VERSION        ="R-4.0.2"


supported_distribtions =  {  
        "debian"  :  "apt-get" ,
        "fedora"  :   "dnf"    ,
        "RedHat"  :   "yum"    ,
        "openSuse":  "zypper"
        } 

define_OS   =  lambda x = None :  sys.platform
Arch        =  lambda x = None :  platform.architecture()[0b00][0:2] 

has_command =  lambda cmd  : (False , True) [ sbp_cmdexe("command -v {}".format(cmd)).__eq__(0b00) ]

def  detect_current_base_distro () :
    if  not define_OS.__eq__("linux") : return  
    for  dist , pkgman  in supported_distribtions.items() : 
        if has_command(pkgman)  : return  ( dist , pkgman) 


def  gnu_linux_r_collections (distro_name)  :   
    linux_r_build =  namedtuple("linux_r_build" , [ 
        "pkgm"    ,
        "rlang"   ,  
        "rstudio"
        ]) 
    
    linux_Ride_software_version=  RSTUDIO_SOFT_VERSION.lower() 
    __sb__ =  linux_r_build(  
            {
            "debian"  : "dpkg"              , 
            "fedora"  : "rpm"               , 
            "RedHat"  : "rpm"               , 
            "openSuse": "zypper" 
            }, 
            {
            "debian"  : "r-base r-base-dev" , 
            "fedora"  : "R"                 , 
            "RedHat"  : "R"                 , 
            "openSuse": "R-base" 
            },
            {
            "debian"  : source.rstudio +"bionic/amd64/{}-amd64.deb".format(linux_Ride_software_version)      ,  
            "fedora"  : source.rstudio +"centos8/x86_64/{}-x86_64.rpm".format(linux_Ride_software_version)   , 
            "RedHat"  : source.rstudio +"centos8/x86_64/{}-x86_64.rpm".format(linux_Ride_software_version)   ,   
            "openSuse": source.rstudio +"opensuse15/x86_64/{}-x86_64.rpm".format(linux_Ride_software_version) 
            }, 
            )  
    
    return  (__sb__.pkgm[distro_name] , __sb__.rlang[distro_name] ,__sb__.rstudio[distro_name]) 

    

print(define_OS()) 
print(Arch())

#  this  part is only  active on gnu/linux  os 
distro_name  , pkgm  = detect_current_base_distro()  
if distro_name and pkgm : print("your  base distribution is  \033[3;32m%s*\x1b[0m" % (distro_name) )   

# ---- 
def  macosx_version_ctrl ()  : pass  

def  Rstudio_ctrl (  mac_osx_version ) : 
    RStudio="RStudio-1.3.1056.dmg"
    def  depreciation_control  () : 
        current_osx_version = mac_osx_version() 
        allowed_version  = float(10.13) 
        if current_osx_version >=  allowed_version: return  RStudio 
        else: log.error("R Studion require mac  10.13+ make an upgrade")
        
    return depreciation_control  

@Rstudio_ctrl 
def  avoid_deprecation_osx () : 
    osx_version= os.popen("sw_vers -productVersion").read() 
    require_version=float(10.13)
    major,minor,patch= osx_version.split(".")
    current_version=major+"."+minor
    return  float(current_version)  


def direct_downloader ( direct_link)  :  
    filename    = direct_link.split("/")[-1]
    if  os.path.exists(filename)  : 
        print("-[i] {} is already present ".format(filename)) 
        return None
    
    # testing for mac    
    if  define_OS.__eq__("darwin") and  filename.__eq__("RStudio-1.3.1056.dmg") : 
        print("-[mac osx warning] Cannot Download  {}  ".format(filename))
        avoid_deprecation_osx()  
    
    print("-[i]  Downloading  -> \033[4;32m{}\033[0m".format(filename)) 
    binary_data = requests.get(direct_link) 
    #TODO :
    #[] get the full size of binary data  and  start  the download to autocomplet filee like wget 
    with  open  (filename ,  "wb") as  file_container : 
        file_container.write(binary_data.content) 
        return  filename  


def softpack_env   ( os_type , arch )  :
    if os_type.__eq__("darwin")  : 
        return  {
                "Plink"  :source.plink  +"plink_mac_{}.zip".format(PLINK_BUILD_VERSION) , 
                "Rstudio":source.rstudio+"macos/{}.dmg".format(RSTUDIO_SOFT_VERSION)    , 
                "Rlang"  :source.rlang  +"macosx/{}.pkg".format(RLANG_VERSION)  
                }
    if os_type.__eq__("win32") or  os_type.__eq__("win64")  :  
        return {
               "Plink"   :source.plink  +"plink_{sys_arch}_{build_V}.zip".format(sys_arch=define_OS[:3]+arch,build_V=PLINK_BUILD_VERSION) , 
               "Rstudio" :source.rstudio+"windows/{}.exe".format(RSTUDIO_SOFT_VERSION)                                                    ,
               "Rlang"   :source.rlang  +"windows/base/{}.exe".format(RLANG_VERSION)
               }
     
    if os_type.__eq__("linux")   : 
        *unused ,  rstudio = gnu_linux_r_collections(distro_name)
        del unused  
        arch  =  "x86_64" if  arch.__eq__("i386") or arch.__eq__("64") else "i686" 
        return {
               "Plink"   :source.plink  +"plink_linux_{}_{}.zip".format(arch , PLINK_BUILD_VERSION) ,  
               "Rstudio" :rstudio                                                                   
               # R lang  is download  from  package manager ... 
               }



def main ( )   :  
    
    pckg_direct_link = softpack_env(define_OS()  ,Arch())

    for bin_pkg , d_link  in  pckg_direct_link.items() :  
        file_src=direct_downloader(d_link)
        if os.path.exists(str(file_src)) :  
            print("-[i] \033[1;32m{}\033[0m[ok]".format(bin_pkg))
        elif file_src is None : pass 
        else  : 
            log.error("-[E] Fail to install  {}".format(bin_pkg)) 
            

    #  Plink Extraction  
    plink_folder_name = "Plink_src"
    try :os.mkdir(plink_folder_name) 
    except  FileExistsError  :  pass  
    zipf =  pckg_direct_link["Plink"].split("/")[-1]
    if os.path.exists(zipf)  :
        try : 
            with  zipfile.ZipFile(zipf  , "r")  as  fz : 
                fz.extractall(plink_folder_name) 
        except zipfile.BadZipFile as  Bz  : 
            print(Bz)
            log.warning("fail to exctract {}".format(zipf))
        else  :  
            plink_exec  = "{}/plink".format(plink_folder_name) 
            if os.path.exists(plink_exec) :  
                if  define_OS.__eq__("darwin") or define_OS.__eq__("linux"):  
                    exec_storage =  "/usr/bin/"
                    if  not os.path.exists(exec_storage+"plink")  :
                	# make it executable 
                        E_STAT   = sbp_cmdexe("chmod +x {}".format(plink_exec))
                        if  not E_STAT.__eq__(0b000)  :  log.warning("-[w]  cannot  make  plink as executable")
                        MV_STAT= sbp_cmdexe("sudo   mv   {}  {}".format(plink_exec , exec_storage))
                        if  not MV_STAT.__eq__(0b000)  : log.warning("-[w] Failed to enable  plink")
			
     
    rlang_exe , rstudio  = (
            pckg_direct_link["Rlang"].split("/")[-1]  if "Rlang" in  pckg_direct_link else  None   ,  
            pckg_direct_link["Rstudio"].split("/")[-1] 
        )

    if define_OS().__eq__("win32")  or define_OS().__eq__("win64") : 
        current_path = os.getcwd() 
        sys.stdout.write("executing  Plink ") 
        abs_plink_path =  "{}/{}/plink.exe".format(current_path,plink_folder_name)
        os.system(abs_plink_path)  
        sys.stdout.write("executing  R lang\n") 
        os.system(current_path+"/"+rlang_exe) 
        sys.stdout.write("executing  R Studio\n") 
        os.system(current_path+"/"+rstudio)  
       
    if define_OS().__eq__("darwin") : 
        
        # R lang  
        if not has_command("R")  : 
            install_Rlang = sbp_cmdexe("sudo  installer -pkg  {} -target  /  >  /dev/null".format(rlang_exe)) 
            if  install_Rlang  ==   0x00  :  sys.stdout.write("-[s] R successfully installed\n") 
            if  install_Rlang  !=   0x00  :  sys.stderr.write("-[i] Fail to install  R Lang\n") 
        
        else :  print("R  Lang [Ok] ")
        
        # R Studio
        sys.stdout.write("-[i] Mounting  file image ...")  
        mountdir = sbp_cmdexe("hdiutil  mount {}".format(rstudio))
        if  mountdir != 0x00 : 
            log.error("-[e] Failed to auto mount {}".format(rstudio)) 
            
        supposed_mounted_volume  = "/Volumes/{}/RStudio.app/".format(rstudio[:-4]) 
        cpy_status = sbp_cmdexe("sudo  cp -R  {} /Applications".format(supposed_mounted_volume))  
        
        if  cpy_status == 0x000  : print("Rstudio [Ok]")
        if  cpy_status != 0x000  : 
            sys.stderr.write("file  to  Build  {}".format(rstudio))
            sys.exit(1) 

    
    if define_OS().__eq__("linux") :  
        # Rlang  install 
        install  = lambda  x ,package: sbp_cmdexe("sudo {} install    {} -y  > /dev/null".format( x , package) ) 
        depackg  = lambda  x ,package: sbp_cmdexe("sudo {} --install  {}     > /dev/null".format( x , package) ) 

        related_dpkg_handler ,  related_rlang_package ,   unused   = gnu_linux_r_collections(distro_name) 
        del unused 

        if   not has_command("R")  :  
            sys.stdout.write("-[i] installing  R  lang\n")
            RINSTAT       =   install(pkgm , related_rlang_package)    
            
        else  : sys.stdout.write("-[i] R lang is already installed \n")  
        
        if  not has_command("rstudio")  : 
            ride_reqdep= "libclang-dev"
            i_dep = install(pkgm  , ride_reqdep)  
            if  i_dep.__eq__(0b00)  :  
                # install R studio ide 
                ride_install  = depackg(related_dpkg_handler , rstudio) 
                if  ride_install.__eq__(0b00):sys.stdout.write("-[s] rstudio is successfully installed\n")  
                else:sys.stderr.write("-[e] Failed to install  rstudio  ide !\n")  
            else    :sys.stderr.write("-[e] Failed to install  required dependencie for  rstudio  ide\n") 
            
        else        :sys.stdout.write("-[i] rstudio is already present\n")  
                

             
            
        
     

if __name__ =="__main__":  
    main()  
