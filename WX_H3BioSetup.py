#!/usr/bin/env  python3  
# -*- coding: utf-8 -*- 

__author__ =  "jukoo <j_umar@outlook.fr>"  

"""
Generic installation for  Windows and Mac OS X   
"""
import os 
import sys 
import platform  
import logging as log 
import subprocess  

def  sbp_cmdexe ( cmd )  : 
    stdargv     =  subprocess.Popen(cmd , stdout=subprocess.PIPE  ,shell=True) 
    status_code =  stdargv.wait() 
    return  status_code   #  0 => ok  | otherwise  -> fail  

try :
    import  pip
except :
    # probably pip   is not installed or  the version is depreciated
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

    
PLINK_BUILD_VERSION="20200616"   # this build  is PLINK  1.90 BETA   

define_OS   =  sys.platform
Arch        =  platform.architecture()[0b00][0:2] 

print(define_OS) 
print(Arch)

def direct_downloader ( direct_link)  :  
    filename    = direct_link.split("/")[-1]
    if  os.path.exists(filename)  : 
        print("{} is already present ".format(filename)) 
        return None 
    print("+ Downloading {}".format(filename)) 
    binary_data = requests.get(direct_link)  
    with  open  (filename ,  "wb") as  file_container : 
        file_container.write(binary_data.content) 
        return  filename  


def  pkg_dispatcher ( os_type  , arch )  :
    if  os_type.__eq__("darwin") :  
        return   { 
                "Plink"  :"http://s3.amazonaws.com/plink1-assets/plink_mac_{}.zip".format(PLINK_BUILD_VERSION)  , 
                "Rstudio":"https://download1.rstudio.org/desktop/macos/RStudio-1.3.1056.dmg", 
                "Rlang"  :"https://cran.r-project.org/bin/macosx/R-4.0.2.pkg"
                } 
    elif os_type.__eq__("windows") :
        return  { 
                "Plink"  :"http://s3.amazonaws.com/plink1-assets/plink_{sys_arch}_{build}.zip".format(sys_arch=define_OS+Arch , build=PLINK_BUILD_VERSION)  , 
                "Rstudio":"https://cran.r-project.org/bin/windows/base/R-4.0.2-win.exe",
                "Rlang"  :"https://download1.rstudio.org/desktop/windows/RStudio-1.3.1056.exe"
                } 
    else  :  
        log.error ( "not allowed to run on {} {}".format(os_type , arch))  
        

def  has_command ( cmd )  :  
    substitute_unix_cmd = "command -v {}".format(cmd) 
    is_available  = sbp_cmdexe(substitute_unix_cmd) 
    return (False , True)[is_available  == 0b000] 



def main ( )   :  
    
    pckg_direct_link = pkg_dispatcher(define_OS  ,Arch)
    print(pckg_direct_link) 

    for bin_pkg , d_link  in  pckg_direct_link.items() :  
        file_src=direct_downloader(d_link)
        if os.path.exists(str(file_src)) :  
            print("{} [ok]".format(bin_pkg))
        elif file_src is None : pass 
        else  : 
            log.error("Fail to install  {} ".format(bin_pkg)) 
            

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
            sys.exit(2)  
    
    # AutoRun exe file  
    current_path = os.getcwd() 
     
    # windows installation  
    rlang_exe , rstudio  = (
            pckg_direct_link["Rlang"].split("/")[-1] , 
            pckg_direct_link["Rstudio"].split("/")[-1] 
        )

    if define_OS.__eq__("window")  : 
        os.system(current_path+"/"+rlang_exe) 
        os.system(current_path+"/"+rstudio)  
       
    if define_OS.__eq__("darwin") : 
        # R lang  
        if not has_command("R")  : 
            install_Rlang = sbp_cmdexe("sudo  installer -pkg  {} -target  /  >  /dev/null".format(rlang_exe)) 
            assert(install_Rlang == 0) 
        
        # R Studio
        if not has_command("rstudio"):
            install_Rstudio = sbp_cmdexe("MOUNTDIR=$(echo `hdiutil mount {}| tail -1 \
                | awk '{$1=$2=""; print $0}'` | xargs -0 echo) \
                && sudo installer -pkg '${MOUNTDIR}'/*.pkg -target / > /dev/null".format(rstudio))

            #install_Rstudio = sbp_cmdexe("sudo dmginstall {} > /dev/null".format(rstudio))  
            assert(install_Rstudio == 0) 
     

if __name__ =="__main__":  
    main()  
