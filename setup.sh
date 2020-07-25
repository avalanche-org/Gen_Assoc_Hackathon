#!/bin/bash  

# Author  : jukoo <j_umar@outlook.fr> 

# H3BIONET :  environment  setup ! 
# -------- 
# A little programme to make an  quick  setup  for  H3BIONET 
#+ environment  that 's include  R  lang - R Studio  and Plink 
#+ it's cover a major  unix  and linux    operating System  
#+ Unfortunately  for Window  we recommand to use an GNU Emulator 
#+ Environment   [ Cygwin or Gitbash  ... ] 
#+ otherwise we suggest to read the installation guide line ...  

let  "version=1.0.0" 

set  -o errexit  # abort programme  if  an error was occured  

declare -r R_UID=$((2#000))  

declare -Ar MAIN_SUPPORTED_OS_ENV=(  
[GNU_LINUX]="Linux" 
[OSX]="Darwin"
[FREEBSD]="Freebsd" 
)

declare  -Ar  Win_GNU_EMULATOR=(
[LEEW]="cygwin"             # linux Environment Emulation for Windows
[GNU_UTILITY]="msys"        # GNU utilities  for  Windows   
)


has_command ()  {
    local is_define=`command -v $1` 
    if  [[  -n ${is_define} ]]   ; then 
        echo ${is_define} 
    fi
}  

detect_os_type () {
    local  sys_name=$(uname --kernel-name)  
    case  ${sys_name} in 
        ${MAIN_SUPPORTED_OS_ENV[GNU_LINUX]})
            echo -e "${MAIN_SUPPORTED_OS_ENV[GNU_LINUX]}";;
        ${MAIN_SUPPORTED_OS_ENV[OSX]})       
            echo -e "${MAIN_SUPPORTED_OS_ENV[OSX]}"      ;; 
        ${MAIN_SUPPORTED_OS_ENV[FREEBSD]}) 
            echo  -e "${MAIN_SUPPORTED_OS_ENV[FREEBSD]}" ;;    

        # For  Windows we recommanded to  use  GNU Emulator 
        #+ like Cygwin or  GitBash  
        #+ to correctly run the  setup  
        #+ or use  windows linux sub subsystem  
        ${Win_GNU_EMULATOR[LEEW]})
            #echo  -e "os : win [using cygwin emulator]"
            echo  -e "windows"                      ;;
        ${W32_GNU_EMULATOR[GNU_UTILITY]}) 
            echo -e "windows"                   ;;  
        *) 
            echo -e  "UNSUPPORTED OS  TYPE"  
            exit  1   ;;  
    esac   
}

unix_archtype () {
    local  arch=$(uname --machine) 
    echo   ${arch}  
}
readonly  os_name=$(detect_os_type)
readonly  arch_type=$(unix_archtype) 

echo -e  "Generic OS Name     : $os_name"  
echo -e  "System Architecture : $arch_type" 


if [[ ${os_name,,} == "linux"  ]] ||\
   [[ ${os_name,,} == "darwin" ]] ;then
   [[  ${UID}     -ne ${R_UID} ]]   && {
       echo  -e "~need to be root  to execute"
        exit 1 
    }
fi

dowloader  ()  {
    `wget --quiet ${1}`  
    [[  $? -eq 0 ]]  ||  {
        echo -e  "fail to reach ${1}"
            exit 2  
        }
}

is_Authenticate_binary () {
      
      local  g_sum=$(sha256sum ${2})
      local  sha256_summary=$(echo ${g_sum} |  cut -d " "  -f1)  
      local  snip=${#1} 
      if  [[ ${1} ==  ${sha256_summary:0:${snip}} ]]
      then 
         echo -e "+ Authentic Binairy Package"
         echo -e "+ Sha252 Signature : ${sha256_summary:0:${snip}} "
      else  
         echo -e "~ X Non Auth X " 
      fi  
}

[[ "PLINK" ]] 
{
    declare -r plink_static_url="http://s3.amazonaws.com/plink1-assets/plink" 
    declare -r build_version="20200616.zip" 
    get_related_plink_build () {  
        local sys_target  
         if   [[  ${os_name,,} == "linux" ]]   ;then 
             sys_target="_${os_name,,}_${arch_type}_" 
         elif [[ ${os_name,,}  == "darwin" ]]  ;then  
             sys_target="_mac_"  
         elif [[ ${os_name,,}  == "windows" ]] ;then
             sys_target="_win_64"
         fi       
         echo  ${sys_target}  
    }
    readonly  plink_link="${plink_static_url}$(get_related_plink_build)${build_version}" 
  
    if  [[ ! -f  ${plink_link##*/} ]] ; then 
        echo -e  "downloading plink >>  ${plink_link##*/}"  
        $(dowloader ${plink_link}) 
        plink_=${plink_link##*/}
        echo -e  "inflating ... ${plink_}"  
        unzip  ${plink_} -d  "plink" 
    fi     
}

sleep 1.2
[[ "R_LANG::STUDIO" ]] 
{   
    readonly  Ride_reqdep="libclang-dev" 
    readonly  Rbin_static_url="https://cran.r-project.org/bin/"             #  binary for  R lang  
    readonly  Ride_static_url="https://download1.rstudio.org/desktop/"      #  R studio  

    case  ${os_name,,}  in  
        "linux")   
            declare -Ar distro_list=(  
            [debian]="apt-get"          #  Debian  and  Debian base  
            [fedora]="dnf"
            [Redhat]="yum"
            [openSuse]="zypper"
            )  
            declare -Ar RpkgName=(
            [debian]="r-base  r-base-dev"
            [fedora]="R"
            [Redhat]="R"
            [openSuse]="R-base"
            )
            declare  -Ar releated_pkgm=(
            [debian]="dpkg"
            [fedora]="rpm"
            [Redhat]="rpm"
            [openSuse]="zypper"  
            ) 
            declare -Ar Ride_link=(
            [debian]="${Ride_static_url}bionic/amd64/rstudio-1.3.1056-amd64.deb"
            [fedora]="${Ride_static_url}centos8/x86_64/rstudio-1.3.1056-x86_64.rpm"
            [Redhat]="${Ride_static_url}centos8/x86_64/rstudio-1.3.1056-x86_64.rpm"
            [openSuse]="${Ride_static_url}opensuse15/x86_64/rstudio-1.3.1056-x86_64.rpm" 
            )
            declare -Ar Ride_sh256checkSum=(
            [debian]="cd1a9e17"
            [fedora]="bc4b3f44"
            [Redhat]="bc4b3f44"
            [openSuse]="0e881257"
            )

            declare  running_distro  dpkger  rsdurl  sha256_previews  
            #+ get dynamcly the  current distribution 
            for   distro in ${!distro_list[@]} ; do 
                [[  -n  `has_command  ${distro_list[${distro}]}` ]] && {
                     running_distro=${distro} 
                     dpkger=${releated_pkgm[${distro}]}
                     rsdurl=${Ride_link[${distro}]}  
                     sha256_previews=${Ride_sh256checkSum[${distro}]}
                     break  
                } 
            done 

            readonly  running_distro  dpkger rsdurl  sha256_previews 
            readonly  associated_pkgm=${distro_list[${running_distro}]} 
           
            [[  -n `has_command 'R'` ]]  ||  {
                echo -e  "Installing  R  Package  for  ${running_distro} ..."
                sudo ${associated_pkgm}  install   ${RpkgName[${running_distro}]} -y > /dev/null
                test $? -eq 0  && {
                    echo -e "R  package successfully installed" 
                 }||{ 
                     [[  -n `has_command 'R'` ]]   &&   {
                         echo -e "R  package successfully installed" 
                    }|| {
                     echo -e "Fail to install R  make sure to be root _"  
                     exit 2 
                    }
                 }
            }&&{
                echo  -e "+ -> R [Ok]"  
            }
            
            #+R studio installation 
            if  [[  -z `has_command 'rstudio'` ]] 
            then 
                rstudio_binfile=${rsdurl##*/} 
                echo -e "Downloading ... ${rstudio_binfile}" 
                if [[  ! -f  ${rstudio_binfile} ]]  ; then 
                    $(dowloader   ${rsdurl})  
                    test $? -eq 0  || {
                    echo -e "- Fail to install  ${rstudio_binfile}\nAbort"  
                    exit  1 
                    }
            
                fi 
                       
                if [[  -f ${rstudio_binfile} ]]   ; then 
                    echo -e "+ gattering ... authenticity bin "  
                    is_Authenticate_binary  ${Ride_sh256checkSum[${running_distro}]}  ${rstudio_binfile}
                    echo -e "![warn] : R Studio depend on  [ libclang-dev ] "
                    sleep 1
                    sudo  ${associated_pkgm}  install ${Ride_reqdep} -y  > /dev/null 
                    echo -e "Unpacking  ...  " ; sleep 1.2    
                    sudo  ${releated_pkgm[${running_distro}]} --install   ${rstudio_binfile} >  /dev/null
                    test  $? -eq 0 &&{
                        echo  -e "+ -> R Studio [Ok]"
                    }||{
                        echo  -e "- -> R Studio [Failed]"              
                    }
               
                fi
            else  
                echo  -e  "+ -> R Studio [Ok]"
                exit 0  
            fi
          
            ;;    
        "mac") 
            #  R lang
            if  [[  -z   `has_command 'R'` ]]  ; then 
                declare -r  direct_link="${Rbin_static_url}macosx/R-4.0.2.pkg"  
                echo -e  "Installing R  for ${os_name}"  
                readonly root_="/"
                $(dowloader ${direct_link})   
                sudo  installer  -pkg   ${direct_link##*/}  -target  ${root_}   >  /dev/null  
                test $? -eq 0  && {
                    echo -e "R  package successfully installed" 
                 }||{ 
                     [[  -n `has_command 'R'` ]]   &&   {
                         echo -e "R  package successfully installed" 
                    }|| {
                     echo -e "Fail to install R  make sure to be root _"  
                     exit 2 
                    }
                 }&&{
                    echo  -e "+ -> R [Ok]"  
                }   
            fi   
           
            # R studio  
            if  [[  -z  `has_command  'rstudio'` ]] ; then 
                dmg_src="${Ride_static_url}macos/RStudio-1.3.1056.dmg" 
                [[  -n  `has_command 'dmginstall'` ]]  && {
                     sudo dmginstall  ${dmg_src}   >  /dev/null 
                     test $?  -eq 0 ||  {
                         echo  -e "- Fail  to install  ${dmg_src##*/}"
                     }&&{
                         echo  -e "+ -> R studio [Ok]"
                     }

                }||{
                   echo -e "![warn] require  dmginstaller  to proceed\nAbort"
                   exit  2 
                }
            else
                echo  -e "+ -> R studio [Ok]"
            fi 
            ;;  
         "windows") 
             # This  phase require  Gnu Emulator like GitBash or Cygwin  to Proceed  
             # --- 
             # R lang  
             R_wbin="${Rbin_static_url}windows/base/R-4.0.2-win.exe"
             if  [[ -z `has_command 'R'` ]]  ;then  
                $(downloader  ${R_wbin}) 
                test  $? -eq  0 || { 
                    echo -e "- fail to install ${r_wbin##*/}\nabort"  
                    exit 2  
                }&&{
                    echo -e " the ${r_wbin##*/} is  available  click on  to began the installation"  
                    exit 0
                }
             else 
                  echo -e "+ -> R [OK]"
             fi
            
             # R studio  
             wexe_src="${Ride_static_url}windows/RStudio-1.3.1056.exe"
             
             if  [[  -z  `has_command  'rstudio'` ]] ; then  
                 $(dowloader ${wexe_src})
                test  $? -eq  0 || {
                    echo -e "- fail to install ${wexe_src##*/}\nabort"  
                    exit 2  
                }&&{
                    echo -e " the ${wexe_src##*/} is  available  click on  to began the installation"  
                    exit 0 
                }
            else
                echo  -e "+ -> R studio [Ok]"
            fi 
            ;;

         *);; 
     esac  
}

