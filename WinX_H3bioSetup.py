#!/usr/bin/env  python3  
# -*- coding: utf-8 -*- 

__author__ =  "jukoo <j_umar@outlook.fr>"  
"""
Generic installation for  Windows 
"""
import os 
import sys 
import platform  
import requests  
import zipfile 
import logging as log 
 
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

pckg_direct_link= { 
        "Plink"  :"http://s3.amazonaws.com/plink1-assets/plink_{sys_arch}_20200616.zip".format(sys_arch=define_OS+Arch)  , 
        "Rstudio":"https://cran.r-project.org/bin/windows/base/R-4.0.2-win.exe",
        "Rlang"  :"https://download1.rstudio.org/desktop/windows/RStudio-1.3.1056.exe" , 
} 


def main ( )   : 
    
    for bin_pkg , d_link  in  pckg_direct_link.items() :  
        file_src=direct_downloader(d_link)
        if os.path.exists(str(file_src)) :  
            print("{} [ok]".format(bin_pkg))
        elif file_src is None : pass 
        else  : 
            log.error("Fail to install  {} ".format(bin_pkg)) 
            

    #  Plink Extraction  
    try :os.mkdir("Plink_src") 
    except  FileExistsError  :  pass  
    zipf =  pckg_direct_link["Plink"].split("/")[-1]
    if os.path.exists(zipf)  :
        try : 
            with  zipfile.ZipFile(zipf  , "r")  as  fz : 
                fz.extractall("Plink")
        except zipfile.BadZipFile as  Bz  : 
            print(Bz)
            sys.exit(2)  

if __name__ =="__main__":  
    main()  
