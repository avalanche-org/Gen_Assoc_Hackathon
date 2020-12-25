#!/usr/bin/env  python3  
#coding=utf-8  

__author__=   "Umar <j_umar@outlook.com>"

import os ,  sys , subprocess 
 
class  Utils  () :  

    def  __init__  ( self   ) :  
        pass  
    
    def exec_cmd ( self  , cmd  )  :  
        status  = subprocess.Popen (  cmd  ,   stdout=subprocess.PIPE , shell =True  )  
        x_stat  = status.wait() 
        return  x_stat

    def has_cmd  ( self   , cmd )  : 
        the_cmd_xist  =  self.exec_cmd(cmd)  
        if  not the_cmd_xist.__eq__(0x00)  :  
            sys.stderr.write ("you  {} command is not avalaible in your system  \n".format(cmd))
            sys.exit (1)   
            
    def stream_stdout  ( self  ,   cmdline_instruction  ,  io_redirect = None )  :  
        _io   = os.popen(cmdline_instruction).read() 
        if io_redirect is not  None  :  # io_redirect   should be a file   
            with open ( io_redirect , "w" )  as  log_register  :  
                log_register.write(_io) 
