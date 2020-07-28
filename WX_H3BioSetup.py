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

def  avoid_deprecation_osx () : 
    osx_version= os.popen("sw_vers -productVersion").read() 
    require_version=float(10.13)
    major,minor,patch= osx_version.split(".")
    current_version=major+"."+minor
    if not float(current_version) >= require_version  :
        log.error("please  upgrade your system Rstudio require  10.13+ ")
        sys.exit(21) 


def direct_downloader ( direct_link)  :  
    filename    = direct_link.split("/")[-1]
    if  os.path.exists(filename)  : 
        print("{} is already present ".format(filename)) 
        return None
    
    # testing for mac    
    if  define_OS.__eq__("darwin") and  filename.__eq__("RStudio-1.3.1056.dmg") : 
        print("Cannot Download  {}  ".format(filename))
        avoid_deprecation_osx()  
    
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
    
     
    # windows installation  
    rlang_exe , rstudio  = (
            pckg_direct_link["Rlang"].split("/")[-1] , 
            pckg_direct_link["Rstudio"].split("/")[-1] 
        )

    if define_OS.__eq__("windows")  : 
        current_path = os.getcwd() 
        os.system(current_path+"/"+rlang_exe) 
        os.system(current_path+"/"+rstudio)  
       
    if define_OS.__eq__("darwin") : 
        
        # R lang  
        if not has_command("R")  : 
            install_Rlang = sbp_cmdexe("sudo  installer -pkg  {} -target  /  >  /dev/null".format(rlang_exe)) 
            if  install_Rlang  ==   0x00  :  sys.stdout.write("R successfully installed") 
            if  install_Rlang  !=   0x00  :  sys.stderr.write("Fail to install  R Lang") 
        
        else :  print("R  Lang [Ok] ")
        
        # R Studio
        print("Mounting  file image ...")  
        mountdir = sbp_cmdexe("hdiutil  mount {}".format(rstudio))
        if  mountdir != 0x00 : 
            log.error("fail to auto mount {}".format(rstudio)) 
            
        supposed_mounted_volume  = "/Volumes/{}/RStudio.app".format(rstudio[:-4]) 
        cpy_status = sbp_cmdexe("sudo  cp -R  {} /Applications".format(supposed_mounted_volume))  
        
        if  cpy_status == 0x000  : print("Rstudio [Ok]")
        if  cpy_status != 0x000  : 
            sys.stderr.write("file  to  Build  {}".format(rstudio))
            sys.exit(1) 

     

if __name__ =="__main__":  
    main()  
