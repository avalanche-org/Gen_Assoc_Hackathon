#!/usr/bin/env python3  
#coding: utf-8  
__author__ : str  = "Umar <j_umar@outlook.com>  "
"""  
 !! DISCLAIMER HERE !! 
"""
import os , sys , gi , argparse    
gi.require_version("Gtk" , "3.0")  
from gi.repository import  Gtk  

from  typing  import List , Dict , Tuple   

##  main Window  frame setting  
WIDTH      : int = 0x32  <<  4   #  800  
HEIGHT     : int = 0x64  <<  3   #  800  
RESIZABLE  : bool =  False 


def show_mf  ( mf  : Gtk.Window   )  ->  None :  
    
    mf.connect("delete-event" ,  Gtk.main_quit) 
    mf.show_all() 
    Gtk.main() 


def main   ()  -> None :  
    basename  :  str  = "h3bionet  Gui" 
    
    main_window_frame  : Gtk.Window =  Gtk.Window( title=f"{basename} {WIDTH }x{HEIGHT}")  
    main_window_frame.set_border_width(0x00a) 
    main_window_frame.set_default_size(WIDTH , HEIGHT)  
    main_window_frame.set_resizable(RESIZABLE)  
     



    show_mf(main_window_frame)  



if __name__.__eq__("__main__")  :  
    main()  

