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
from  collections import  namedtuple 

basename  :  str  = "Gen Assoc" 
#  THIS  IS GLOBAL SETTING   
#  EVERY FRAME  IS BASED ON THIS SETTING  
#  YOU  CAN  ADD PROPERTY  ON THE LIST BELLOW  


SETTING_PARAMS  :  List[str]   =  [ 
        "WIDTH", 
        "HEIGHT",
        "RESIZABLE",
        "BORDER_WIDTH"
        ]  

setting   = namedtuple("setting" , SETTING_PARAMS)  

#  PARAMETER  DEFINITION FOR MAIN WINDOW  
mw = setting(
        0x32 << 4  ,     #  WIDTH 
        0x64 << 3  ,     #  HEIGHT 
        False      ,     #  RESIZABLE
        0x0a             #  BORDER  WIDTH  
        )             
 
dbox  = setting (  
        0x32 << 3  ,     # WIDTH 
        0x64 >> 2  ,     # HEIGHT
        False      ,     # RESIZABLE 
        0x05             # BORDER WIDTH
       ) 

def show_frame  ( mf  : Gtk.Window    ,  *wigets)  ->  None :
    
    mf.connect("delete-event" ,  Gtk.main_quit) 
    mf.show_all()
    Gtk.main()

def dialog_box (main_frame)->  None : 


    dialog_frame  : Gtk.Window  =  Gtk.Window(title=f"{basename} {dbox.WIDTH}x{dbox.HEIGHT}")  
    dialog_frame.set_border_width(dbox.BORDER_WIDTH) 
    dialog_frame.set_default_size(dbox.WIDTH , dbox.HEIGHT) 
    dialog_frame.set_resizable(dbox.RESIZABLE)  
     
    #  box  layer 
    
    mainbox  : Gtk.Box  =  Gtk.Box(spacing=0x06 ,  orientation= Gtk.Orientation.VERTICAL)  
    vbox     : Gtk.Box  =  Gtk.Box(spacing=0x06 ,  orientation= Gtk.Orientation.VERTICAL)  
    hbox     : Gtk.Box  =  Gtk.Box(spacing=0x06 ,  orientation= Gtk.Orientation.HORIZONTAL)
    # input entry  
    entry    : Gtk.Entry  =  Gtk.Entry()  
    entry.set_text(os.getcwd())  #  get path from config file  
    vbox.pack_start(entry , True , True , 0 )  
    # buttons  
    startbtn    : Gtk.Button = Gtk.Button(label="Start !")  
    cancelbtn   : Gtk.Button = Gtk.Button(label="Close x") 
    
    # events    
    startbtn.connect("clicked"   , main_frame ,  dialog_frame) 
    cancelbtn.connect("clicked"  ,  Gtk.main_quit)
    

    # package  layout  
    hbox.pack_start(startbtn  , True , True , 0 ) 
    hbox.pack_start(cancelbtn , True , True , 0 )

    mainbox.pack_start(vbox   , True , True , 0 ) 
    mainbox.pack_start(hbox   , True , True , 0 ) 
    
    dialog_frame.add(mainbox) 
    
    show_frame(dialog_frame)  


def main_frame  ( open_from_dialog :Gtk.Button  , dbox_frame  : Gtk.Window)  -> None :
    
    dbox_frame.destroy()

    main_window_frame  : Gtk.Window =  Gtk.Window( title=f"{basename} {mw.WIDTH}x{mw.HEIGHT}")  
    main_window_frame.set_border_width(mw.BORDER_WIDTH) 
    main_window_frame.set_default_size(mw.WIDTH ,  mw.HEIGHT)  
    main_window_frame.set_resizable(mw.RESIZABLE)

    main_container: Gtk.Box    =  Gtk.Box(spacing=0x06  , orientation = Gtk.Orientation.VERTICAL)
    # CHOICE BOX  
    # TODO  : 
    # add radio buttons  and  run button  
    choicebox     : Gtk.Box    =  Gtk.Box(spacing=0x06 ,  orientation= Gtk.Orientation.VERTICAL) 
    test_btn1   = Gtk.Button(label=  " box 1 " )  
    choicebox.pack_start(test_btn1 , True , True , 0 )  
    # LOG OR SUMMARY BOX
    slogbox       : Gtk.Box    =  Gtk.Box(spacing=0x06 ,  orientation= Gtk.Orientation.VERTICAL)  
    test_btn2    = Gtk.Button(label="box2") 
    slogbox.pack_start(test_btn2 , True ,True ,  0 ) 
    
    # BUTTONS BOX  
    btnsbox       : Gtk.Box    =  Gtk.Box(spacing=0x06 ,  orientation= Gtk.Orientation.HORIZONTAL)
    
    quit_bnt      : Gtk.Button =  Gtk.Button(label="Quit")  
    quit_bnt.connect("clicked" , Gtk.main_quit)  
    btnsbox.pack_start(quit_bnt ,  True , True,0 )  



    
    main_container.pack_start(choicebox , True , True , 0 ) 
    main_container.pack_start(slogbox   , True , True , 0 ) 
    main_container.pack_start(btnsbox   , False, True , 0 ) 
    
    main_window_frame.add(main_container) 
    
    

    show_frame(main_window_frame)  



def main   ()  -> None :  
     
    dialog_box(main_frame)  


if __name__.__eq__("__main__")  : 
    try  : 
        main()  
    except KeyboardInterrupt  as  brutalExit :  
        sys.stderr.write("{}\n".format(brutalExit)) 

