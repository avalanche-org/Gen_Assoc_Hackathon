# INSTALLATION GUIDE LINE   [ Beta version ]
---
The H3BioNet  Installation Wizard is availabe on GNU/Linux, Windows and Mac OS X operating systems.

Make a quick installation of : 
- Plink
- R lang  
- RStudio  

## For GNU/Linux
--- 
Before launching H3BioNet setup, you must already have Bash version 4ˆ. 
To check this out 
```
$ echo $BASH_VERSINFO  
```
* this installation  cover the majority GNU/Linux OS  
such as :
    - OpenSuse                                          [ recommanded version 15]
    - Debian   ( or Debian Base  like Ubuntu 18)        [ recommanded version 9 - 10]
    - RedHat   
        -  Fedora                                       [ recommanded version 19 - 28]  
        -  Centos                                       [ recommanded version 7  - 8 ]
        -  ... 

To run the  installation  wizard  you need just  to  type  
```
$ sudo ./H3bioSetup.sh
``` 
>  have  Problem please   read the Trouble shooting section bellow 

##  Windows and Mac OS X  
---   
Before  running  the  installation wizard  
you need to have some requirements 
-  python3   or  Conda 

*Warning  for Mac  user* 
>  we recommand  to have   Mac OS X version  10.13+ 
to see your mac os version type this command bellow 
```
$ sw_vers -productVersion 
```
###  MAC OS X

```

$ ./WX_H3BioSetup.py  
```

### Windows

If you have  python3 available  in your  System 
you can run directly the setup  

```

> python WX_H3BioSetup.py
```
However  if  you  run Conda
first activate  the environment 

```
 >  conda  activate  
```
and run  the setup  

```
>  python WX_H3BioSetup.py 
```
and that's it !

# TROUBLE SHOOTING   
---
* For any issue  encountered  with  this setup  please  contact  the maintainer <j_umar@outlook.com> 
If you are a member of Avalanche Team please submit an issue  or make a pull request 

In some case when you run the script at the first time it may fail due to  pip module (depreciated version). 
In General the setup resolve this  conflict  by  auto install the  missing  libraries and required libraries 

On first execution fail
---  
You might upgrade your pip module version/ install your pip module

```
$ python3 -m pip install  --upgrade pip 
```
and relaunch  the setup 