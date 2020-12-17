#!/usr/bin/env python3  
#coding: utf-8  
__author__ : str  = "Umar <j_umar@outlook.com>  "
__version__: str  = "1.0.1" 
__stage__  : str  = "alpha"  

"""  
 !! DISCLAIMER HERE  !! 
"""
import os , sys , gi , argparse    
gi.require_version("Gtk" , "3.0")  
from gi.repository import  Gtk , GLib

from time import sleep 
from  typing  import List , Dict , Tuple  
from  collections import  namedtuple 

basename  :  str  = f"mTDT {__stage__} v{__version__}"  
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
#  PARAMETER FOR  START UP  DIALOG  BOX   
dbox  = setting (  
        0x32 << 3  ,     # WIDTH 
        0x64 >> 2  ,     # HEIGHT
        False      ,     # RESIZABLE 
        0x05             # BORDER WIDTH
       ) 

#  PARAMETER FOR  MIDDLEWARE  CHECKER  
pb   = setting  (  
       0x32  << 3  ,     # WIDTH 
       0x64  >> 2  ,     # HEIGHT  
       False       ,     # RESIZABLE 
       0x05              # BORDER WIDTH
       ) 

def  current_dir_view ( actual_path  )  :   
    if sys.platform.__eq__("linux") :  
        p =  os.popen(f"tree {actual_path}").read()  
        return  p  

def show_frame  ( mf : Gtk.Window)  ->  None : 
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

abs_path_dir_target  :str  =   str()  
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
    global  abs_path_dir_target  
    def_attr     =   Gtk.FileChooserAction.OPEN      \
                     if   chooser_type.lower().__eq__("file") \
                     else  Gtk.FileChooserAction.SELECT_FOLDER

    mut_label    = "Open File" if   chooser_type.lower().__eq__("file") \
                    else  "Select Folder"


    fc_dialog  : Gtk.FileChooserDialog  = Gtk.FileChooserDialog ( 
            title  =   f"please  select  a  {chooser_type} "  , 
            parent =   None ,   
            action =   def_attr 
            )

    fc_dialog.add_button(f"_{mut_label}" ,Gtk.ResponseType.OK) 
    fc_dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL) 
    fc_dialog.set_default_response(Gtk.ResponseType.OK) 
    
    response  =  fc_dialog.run() 
    if  response.__eq__(Gtk.ResponseType.OK) :  
        print(f"clicked  {chooser_type}... ") 
        print(f"{chooser_type}  selected {fc_dialog.get_filename()}") 
        default_file =  fc_dialog.get_filename()  
        entry_widget.set_text( fc_dialog.get_filename())
        abs_path_dir_target =fc_dialog.get_filename()  
        
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
    
    vbox     : Gtk.Box  =  Gtk.Box(spacing=0x06 ,  orientation= Gtk.Orientation.HORIZONTAL)  
    hbox     : Gtk.Box  =  Gtk.Box(spacing=0x06 ,  orientation= Gtk.Orientation.HORIZONTAL)
    # logo  area 
    logo_label  : Gtk.Label  =  Gtk.Label()  
    logo_label.set_markup("<big> Gen  Assoc  </big>")
    logo_label.set_max_width_chars(78) 

    choose_file : Gtk.Button = Gtk.Button(label=f"Browse {mut_label}") 
    # input entry  
    entry    : Gtk.Entry  =  Gtk.Entry()  
    #  TODO  :
    # [] read default path to   config  file  to file  this area 
    entry.set_text(os.getcwd()) 
    vbox.pack_start(entry , True , True , 0 )  
    vbox.pack_start(choose_file , False , True , 0 ) 
    # buttons   
    startbtn    : Gtk.Button = Gtk.Button(label="Start !")  
    cancelbtn   : Gtk.Button = Gtk.Button(label="Abort x")

    
    # events
    #startbtn.connect("clicked"   , main_frame      ,  dialog_frame) 
    startbtn.connect("clicked"   , middleware_checker , dialog_frame,  os.getcwd() )#     ,  dialog_frame) 
    choose_file.connect("clicked", chooser ,  entry ) 
    cancelbtn.connect("clicked"  ,  Gtk.main_quit)
    

    # box layer display   
    hbox.pack_start(startbtn    , True , False, 0 ) 
    hbox.pack_start(cancelbtn   , True , False, 0 )

    mainbox.pack_start(logo_label  , True , True , 0 ) 
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



 
call_count   : int = 0x000  
def  on_timeout (
        trigger : bool                      , 
        activity_bar     : Gtk.ProgressBar  , 
        main_container   : Gtk.Window       , 
        dbox_frame       : Gtk.Window  
        )  ->     bool   :   

    global call_count  
    call_count+=1 
    print("0> " ,  call_count  ) 
    trigger   =  (True , False)[call_count  >=  0x64 >> 1  ]  # replace  0x64 by the  size of the folder  !  
    if trigger : activity_bar.pulse() 
    else  :  
        activity_bar.set_text("laoding data ")  
        activity_bar.set_show_text(True)  
        sleep(2) 
        main_container.destroy()
        Gtk.main_quit()

        #call  main frame   after  killin'  midchecker  
        main_frame(dbox_frame)
    return trigger  

def middleware_checker ( 
        start_btn_launcher  :  Gtk.Button ,
        dbox                :  Gtk.Window,
        abs_path_dir_target :  str )  ->  None   : 

    """
    check  the integrity of the folder if  it has all requirements available  
    """  
    main_pb  : Gtk.Window =  Gtk.Window(title=f"{basename}://{abs_path_dir_target} {pb.WIDTH}x{pb.HEIGHT}")  
    main_pb.set_border_width(pb.BORDER_WIDTH)  
    main_pb.set_default_size(pb.WIDTH , pb.HEIGHT)  
    main_pb.set_resizable(pb.RESIZABLE) 
    
    vbox          : Gtk.Box            =  Gtk.Box (spacing =0x06   , orientation =  Gtk.Orientation.VERTICAL ) 
    activity_bar  :  Gtk.ProgressBar   =  Gtk.ProgressBar()
    activity_bar.pulse()  
    trigger  =  True
    
    status: str  =  f"Scanning ... {abs_path_dir_target.split('/')[-1]}" 
    activity_bar.set_text(status) 
    activity_bar.set_show_text(True)  
    
    timout_id    =    GLib.timeout_add(0x64, on_timeout ,trigger ,  activity_bar  ,main_pb ,   dbox) 
    if  trigger  == False  :   print("and of animation")

    vbox.pack_start(activity_bar  , True ,True , 0  )   
    main_pb.add(vbox) 
    show_frame(main_pb) 
     


def kill_frame  (target_frame  :Gtk.Window )  :  
    target_frame.destroy() 
    Gtk.main_quit()  
    

#def main_frame  ( open_from_dialog :Gtk.Button  , dbox_frame  : Gtk.Window)  -> None :
def main_frame  (dbox_frame  : Gtk.Window)  -> None :
    
    kill_frame(dbox_frame) 

    main_window_frame  : Gtk.Window =  Gtk.Window( title=f"{basename} ://  {abs_path_dir_target}  {mw.WIDTH}x{mw.HEIGHT}")  
    main_window_frame.set_border_width(mw.BORDER_WIDTH) 
    main_window_frame.set_default_size(mw.WIDTH ,  mw.HEIGHT)  
    main_window_frame.set_resizable(mw.RESIZABLE)

    master_container : Gtk.Box    =  Gtk.Box(spacing=0x06  , orientation = Gtk.Orientation.VERTICAL)  
    main_container: Gtk.Box    =  Gtk.Box(spacing=0x06  , orientation = Gtk.Orientation.HORIZONTAL )  

    
    file_viewer   : Gtk.Box    =  Gtk.Box(spacing=0x06  , orientation = Gtk.Orientation.VERTICAL )
    fa    = Gtk.Button(label="file area")   
    file_viewer.pack_start (fa , True , True , 0 ) 
    
    container_box : Gtk.Box    =  Gtk.Box(spacing=0xA   , orientation = Gtk.Orientation.VERTICAL )  
    setup_box     : Gtk.Box    =  Gtk.Box(spacing=0x06  , orientation = Gtk.Orientation.HORIZONTAL) 
    # setup_box  component
    #  combox box 
    #  TODO  :  add   data  inside combo box    
    ped_label     : Gtk.Label  =  Gtk.Label(label="ped :")  
    ped_cb        : Gtk.ComboBoxText  =  Gtk.ComboBoxText() 
    
    med_label     : Gtk.Label  =  Gtk.Label(label="med :") 
    med_cb        : Gtk.ComboBoxText  =  Gtk.ComboBoxText() 
    
    phen_label    :  Gtk.Label = Gtk.Label(label ="phen :") 
    phen_cb        : Gtk.ComboBoxText  =  Gtk.ComboBoxText()
    
    setup_box.pack_start(ped_label , True , True ,  0 )  
    setup_box.pack_start(ped_cb    , True , True ,  0 )  
    setup_box.pack_start(med_label , True , True ,  0 )  
    setup_box.pack_start(med_cb    , True , True ,  0 )  
    setup_box.pack_start(phen_label, True , True ,  0 )  
    setup_box.pack_start(phen_cb   , True , True ,  0 )  


    choose_box    : Gtk.Box    =  Gtk.Box(spacing=0x06  , orientation = Gtk.Orientation.HORIZONTAL)  
    # check box  area 
    
    run_btn       : Gtk.Button =  Gtk.Button(label="Run Analysis")  
    
    log_container : Gtk.Box    =  Gtk.Box(spacing=0x06  , orientation = Gtk.Orientation.VERTICAL )  

    bottombox       : Gtk.Box    =  Gtk.Box(spacing=0x06 ,  orientation= Gtk.Orientation.HORIZONTAL)
    quit_bnt      : Gtk.Button =  Gtk.Button(label="Quit")  
    quit_bnt.connect("clicked" , Gtk.main_quit)  
    bottombox.pack_start(quit_bnt ,  True , False,0 )  


    bnt1  =  Gtk.Button(label="1") 
    bnt2  =  Gtk.Button(label="2") 
    bnt2a =  Gtk.Button(label="2a") 
    bnt2b =  Gtk.Button(label="2b") 



    choose_box.pack_start(bnt2a , True , True , 0  )  
    choose_box.pack_start(bnt2b, True , True , 0  )
    

    bnt3  =  Gtk.Button(label="3")
    log_container.pack_start(bnt3, True , True , 0 )   
    
    container_box.pack_start(setup_box , False , False , 0 )  
    container_box.pack_start(choose_box , True , True , 0 ) 
    container_box.pack_start(run_btn ,  True , True , 0 )
    container_box.pack_start(log_container, True , True , 0 )   

    main_container.pack_start(file_viewer , True  , True  ,  0 )  
    main_container.pack_start(container_box , True , True , 0  )  
    
    master_container.pack_start(main_container ,  True ,True , 0 )
    master_container.pack_start(bottombox, False,True ,  0 )  

    
    

    
    


    
    #  ------------  BOX  CONTAINER  LAYOUT -----  )
    """  
    
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
    summary.set_text("
-> this  is  a simple  test
-> bla bla  bla 
-> bla bla bla again 
            ") 
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
 
        
    main_container.pack_start(choicebox , False, False , 0 ) 
    main_container.pack_start(slogbox   , True , True , 0 ) 
    main_container.pack_start(btnsbox   , False, False , 0 ) 
    """  
    main_window_frame.add(master_container) 
    
    
    show_frame(main_window_frame)  


def main   ()  -> None :  
     
    dialog_box(main_frame)  


if __name__.__eq__("__main__")  : 
    try  : 
        main()  
    except KeyboardInterrupt  as  brutalExit :  
        sys.stderr.write("{}\n".format(brutalExit)) 

