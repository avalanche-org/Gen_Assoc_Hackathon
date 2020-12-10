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
        0x258      ,     #  HEIGHT 
        False      ,     #  RESIZABLE
        0x0a             #  BORDER  WIDTH  
        )             
 
dbox  = setting (  
        0x32 << 3  ,     # WIDTH 
        0x64 >> 2  ,     # HEIGHT
        False      ,     # RESIZABLE 
        0x05             # BORDER WIDTH
       ) 


def  current_dir_view ( actual_path  )  :   
    if sys.platform.__eq__("linux") :  
        p =  os.popen(f"tree {actual_path}").read()  
        return  p  

def show_frame  ( mf  : Gtk.Window)  ->  None : 
    """ 
    show_frame  : Generic  function do display  frame 
    show  widget frame  
    @param :  
    mf <main frame>  :  Gtk.Window 
    @return:  
    None 
    """
    
    mf.connect("delete-event" ,  Gtk.main_quit) 
    mf.show_all()
    Gtk.main()

default_file  : str  = str ()  

mut_label : str = str () 

def chooser  ( btn_wiget: Gtk.Button  ,  entry_widget : Gtk.Entry , chooser_type  :str  = "directory")  -> None : 
    """ 
    file_chooser  :  file chooser wiget  
    give the way to choose file
    @param  :  
    dialog_widget :  Gtk.Button   ( attached to event clicked )  
    entry_widget  :  Gtk.Entry    ( auto fill entry point  with the choosen file )  
    @return :  
    None  
    """
    global  mut_label  
    def_attr     =   Gtk.FileChooserAction.OPEN      \
                     if   chooser_type.lower().__eq__("file") \
                     else  Gtk.FileChooserAction.SELECT_FOLDER

    mut_label    = "Open File" if   chooser_type.lower().__eq__("file") \
                    else  "Select Folder"


    fc_dialog  : Gtk.FileChooserDialog  = Gtk.FileChooserDialog ( 
            title  =   f"please  select  a  {chooser_type} "  , 
            parent =   None ,   
            action =   def_attr #Gtk.FileChooserAction.SELECT_FOLDER  if  chooser_type.__eq__(""
            )

    fc_dialog.add_button(f"_{mut_label}" ,Gtk.ResponseType.OK) 
    fc_dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL) 
    fc_dialog.set_default_response(Gtk.ResponseType.OK) 
    
    response  =  fc_dialog.run() 
    if  response.__eq__(Gtk.ResponseType.OK) :  
        print(f"clicked  {chooser_type}... ") 
        print(f"{chooser_type}  selected {fc_dialog.get_filename()}")
        default_file =  fc_dialog.get_filename()  
        entry_widget.set_text( fc_dialog.get_filename() )
        fc_dialog.destroy() 
    else  : 
        fc_dialog.destroy()


def dialog_box (main_frame : Gtk.Window)->  None : 
    """
    dialog_box :  display  little dialog Box  
    @param  : 
    main_frame  :  Gtk.Window   ( the next frame called  on start event )  
    @return  : 
    None 
    """

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
    #  TODO  :
    # [] read default path to   config  file  to file  this area
    entry.set_text(os.getcwd()) 
    vbox.pack_start(entry , True , True , 0 )  

    # buttons   
    startbtn    : Gtk.Button = Gtk.Button(label="Start !")  
    choose_file : Gtk.Button = Gtk.Button(label=f"Select {mut_label}") 
    cancelbtn   : Gtk.Button = Gtk.Button(label="Close x") 
    
    # events
    startbtn.connect("clicked"   , main_frame      ,  dialog_frame) 
    choose_file.connect("clicked", chooser ,  entry ) 
    cancelbtn.connect("clicked"  ,  Gtk.main_quit)
    

    # box layer display   
    hbox.pack_start(startbtn    , True , True , 0 ) 
    hbox.pack_start(choose_file , True , True , 0 ) 
    hbox.pack_start(cancelbtn   , True , True , 0 )

    mainbox.pack_start(vbox   , True , True , 0 ) 
    mainbox.pack_start(hbox   , True , True , 0 ) 
    
    dialog_frame.add(mainbox) 
    
    show_frame(dialog_frame)  


state  :  str  ="yes"   

def rbtn_on_toggle  ( rbt_wiget  : Gtk.RadioButton ) ->   None :  
    """ 
    rbtn_on_toggle  :  get  the state  of radio button  on toggle event  
    @param    : 
    rbt_wiget :   Gtk.RadioButton  
    @return   :  
    None  
    """
    global state  
    state  =   (rbt_wiget.get_label() , rbt_wiget.get_label()) [rbt_wiget.get_active()]  
    sys.stdout.write("{}\n".format(state)) 
 

def even_launch   ( btn_widget :  Gtk.Button)  ->  None  :  
    """
    even_lauchn 
    @param :  
    btn_widget :  Gtk.Button   
    event  trigger  to run choice  
    @return  : 
    None
    """
    print(f" =>    { state }  ")


def main_frame  ( open_from_dialog :Gtk.Button  , dbox_frame  : Gtk.Window)  -> None :
    
    dbox_frame.destroy() 

    main_window_frame  : Gtk.Window =  Gtk.Window( title=f"{basename} {mw.WIDTH}x{mw.HEIGHT}")  
    main_window_frame.set_border_width(mw.BORDER_WIDTH) 
    main_window_frame.set_default_size(mw.WIDTH ,  mw.HEIGHT)  
    main_window_frame.set_resizable(mw.RESIZABLE)

    main_container: Gtk.Box    =  Gtk.Box(spacing=0x06  , orientation = Gtk.Orientation.VERTICAL )  
    
    #  ------------  BOX  CONTAINER  LAYOUT -----  )
    
    choicebox     : Gtk.Box    =  Gtk.Box(spacing=0x06 ,  orientation= Gtk.Orientation.VERTICAL)

    label         : Gtk.Label        = Gtk.Label(label="Do you want to run Genotype Inference ?")  
  
    
    yes_rbtn  : Gtk.RadioButton  =  Gtk.RadioButton.new_with_label_from_widget(None,"yes")  
    yes_rbtn.connect("toggled" , rbtn_on_toggle)
   
    no_rbtn      : Gtk.RadioButton  =  Gtk.RadioButton.new_from_widget(yes_rbtn)  
    no_rbtn.set_label("no") 
    no_rbtn.connect("toggled" , rbtn_on_toggle)
    
    
    validate_btn    : Gtk.Button    = Gtk.Button(label=f"Run")  
    validate_btn.connect("clicked" , even_launch)  
    
    #SUB BOX  CONTAINER  THAT'S CONTAINER  FILES LISTER  AND SUMMARY
    slogbox         : Gtk.Box       = Gtk.Box(spacing=0x06 ,  orientation= Gtk.Orientation.HORIZONTAL)  

    ## SUMMARY SECTION   
    summary_expender_area  :  Gtk.Expander   =  Gtk.Expander(label="Show Summary")  
    summary_expender_area.set_expanded(True) 
     
    summary   :  Gtk.Label =  Gtk.Label() 
    summary.set_text("""
-> this  is  a simple  test
-> bla bla  bla 
-> bla bla bla again 
            """) 
    summary_expender_area.add(summary)
    
    
    ## FILE LISTER  SECTION  
    filelistbox   : Gtk.Box    = Gtk.Box(spacing=0x06 ,  orientation=Gtk.Orientation.VERTICAL )
    dir  =  current_dir_view("/home/juko/Desktop/Pasteur/Sandbox/H3BioNet/Gen_Assoc_Hackathon/")
    frame_viewer  : Gtk.Frame   =  Gtk.Frame(label=f"{dir}")   
    
    slogbox.pack_start(summary_expender_area , True ,True  ,  0 ) 
    slogbox.pack_start(frame_viewer, True ,True ,  0 )   


    # BUTTONS BOX  
    btnsbox       : Gtk.Box    =  Gtk.Box(spacing=0x06 ,  orientation= Gtk.Orientation.HORIZONTAL)

    # -------------------

    choicebox.pack_start(label         , True  , True  , 0 ) 
    choicebox.pack_start(yes_rbtn      , True  , True  , 0 )  
    choicebox.pack_start(no_rbtn       , True  , True  , 0 )  
    choicebox.pack_start(validate_btn  , True  , False , 0 ) 
 
    quit_bnt      : Gtk.Button =  Gtk.Button(label="Quit")  
    quit_bnt.connect("clicked" , Gtk.main_quit)  
    btnsbox.pack_start(quit_bnt ,  True , False,0 )  

    
    main_container.pack_start(choicebox , False, False , 0 ) 
    main_container.pack_start(slogbox   , True , True , 0 ) 
    main_container.pack_start(btnsbox   , False, False , 0 ) 
    
    main_window_frame.add(main_container) 
    
    
    show_frame(main_window_frame)  


def main   ()  -> None :  
     
    dialog_box(main_frame)  


if __name__.__eq__("__main__")  : 
    try  : 
        main()  
    except KeyboardInterrupt  as  brutalExit :  
        sys.stderr.write("{}\n".format(brutalExit)) 

