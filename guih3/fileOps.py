#!/usr/bin/env  python3  
#coding :  utf-8  
__author__="Umar <j_umar@outlook.com>" 

import os , sys   
from  typing import  Dict ,  Tuple , List  
from  glob import glob  

try  :   
    import pip  
except  :  
    sys.stderr.write("pip module  is  require to  install  automaticly the deps\n")
    sys.exit(1)  
else  :  
    try  : 
        import  pandas  as  pd
    except  ImportError  :   
        try : 
            pip.main(["install" ,  "pandas"])  
            pip.main(["install" ,  "xlrd"])   
        except  :  
            sys.stderr.write("fail to install  internal  libs ")  
        else :  
            sys.stdout.write("NOTE:  if  the  program  doesn't run \nplease relaunch it!\n THANKS!!!!" )  

class  FileOps  : 
      
    MAX_DEEP =  0X03
    def __init__ ( self , working_directory )  :  
        self.curdir  =  working_directory 
    

    def  format_byte ( 
            self  ,
            byte_size , 
            b_factor  : int =  0x400  , # 1024 
            )  -> int  : 
        if  byte_size <  b_factor  :  
            return  byte_size   
        byte_size /= b_factor  
        return   byte_size  

    def  get_size_of_directory   (self  ,  deep_folder = None ) ->  int  : 
        """  
        get  the size  of the current  working  directory  
        """  
        total_byte : int  = 0b00 
        dir_  = self.curdir if  deep_folder is None else  deep_folder 
        try :  
            for __entry__  in os.scandir(deep_folder)  :  
                if  self.MAX_DEEP.__eq__(0x00)  :  break 
                if __entry__.is_file()  : 
                    total_byte+= __entry__.stat().st_size  
                if __entry__.is_dir()  : 
                    self.MAX_DEEP-=1  
                    total_byte+=self.get_size_of_directory(deep_folder)  
                    

        except   NotADirectoryError  :
            sys.stderr.write("{} is  not a folder".format(self.curdir)) 
            sys.exit(2) 
        
        except   PermissionError  : 
            sys.stderr.write("you  have  no permission  for   {}".format(self.curdir)) 
         
            sys.exit(2) 
          
        size =  self.format_byte(total_byte) 
        return  size  

    def  list_files  ( 
            self , 
            filter_by_extension ,
            *allowed_extension
            ) ->  List[str]  :  
        """
        list  of  file  inside the directory
        @param
        filter_by_extention  : str   
            ->  list all files having the same extension  
        @return   : 
        list  
        """ 
        if  allowed_extension.__len__() > 0b00  :
            assert allowed_extension.__contains__(filter_by_extension)  
        
        print (self.curdir)  
        return  glob(f"{self.curdir}/*.{filter_by_extension}")


        pass
     
    def pedfile_colrow ( self, pedfile,def_sep="\t" ) : 
        dataframe  =  pd.read_csv(pedfile ,  sep=def_sep)  
        return  dataframe.columns.tolist()   
   

    def draw_tree  ( self )  : 
        """
        draw tree  of the folder content 
        pass
        """  
        pass  
    

"""
#  TESTING  ZONE 
def  main  () :
     
    previews_Dir = "../Environment" 
    f  = FileOps("../Environment") 
    print("---> "  , f.get_size_of_directory())
    
    print(f.list_files("py")) 






if __name__.__eq__("__main__")  :  
     main () 
"""
