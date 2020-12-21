#!/usr/bin/env  python3  
#coding :  utf-8  
__author__="Umar <j_umar@outlook.com>" 


import os , sys  
from  typing import  Dict ,  Tuple , List  
from  glob import glob  

class  FileOps  : 
      
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
                
                if __entry__.is_file()  : 
                    total_byte+= __entry__.stat().st_size  
                if __entry__.is_dir()  : 
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
