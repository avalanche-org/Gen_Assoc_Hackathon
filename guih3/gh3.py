#!/usr/bin/env python3  
#coding: utf-8  
__author__ : str  = "Umar <j_umar@outlook.com>  "
__version__: str  = "1.0.1" 
__stage__  : str  = "alpha"  

"""  
This programme require   to use  python3+  
LICENSE  HERE !!  
""" 
import os , sys , gi , argparse    
gi.require_version("Gtk" , "3.0")  
from gi.repository import  Gtk , GLib

from time import sleep 
from  typing  import List , Dict , Tuple  
from  collections import  namedtuple

from  fileOps  import  FileOps  


basename  :  str  = f"mTDT {__stage__} v{__version__}" 

BOX_SPACING  : int  =   0x06 

#THIS  IS GLOBAL SETTING   
#+EVERY FRAME  IS BASED ON THIS SETTING  
#+YOU  CAN  ADD PROPERTY  ON THE LIST BELLOW  

SETTING_PARAMS  :  List[str]   =  [ 
        "WIDTH", 
        "HEIGHT",
        "RESIZABLE",
        "BORDER_WIDTH"
        ]  

setting   = namedtuple("setting" , SETTING_PARAMS)  

#  PARAMETER  DEFINITION FOR MAIN WINDOW  
mw = setting(
        0x3e8      ,     #  WIDTH 
        0x320      ,     #  HEIGHT 
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

#TODO  : figure out this function  to make  it  more  adptable for each os  
def  current_dir_view ( actual_path  )  :   
    if sys.platform.__eq__("linux") :  
        p =  os.popen(f"tree {actual_path}").read()  
        return  p 


def generic_alert_dialog  ( level_warning ,  mesg   , second_mesg  =   None   ) -> Gtk.ResponseType :  
    level_warning  =  level_warning.lower()  
    iweq  : Dict[str, Dict[str ,Gtk] ] =   {  
            "info":   { 
                "message_type"  : Gtk.MessageType.INFO , 
                "buttons"       : Gtk.ButtonsType.OK, 
                "text"          : mesg
                } , 
            "warning" : {  
                "message_type"  : Gtk.MessageType.WARNING , 
                "buttons"       : Gtk.ButtonsType.OK_CANCEL, 
                "text"          : mesg
                } , 
            "error"   :   { 
                "message_type"  : Gtk.MessageType.WARNING , 
                "buttons"       : Gtk.ButtonsType.CANCEL,
                "text"          : mesg 
                } ,
            "question":{
                "message_type"  : Gtk.MessageType.WARNING , 
                "buttons"       : Gtk.ButtonsType.YES_NO,
                "text"          : mesg  
                } 
            }
                
    assert  iweq.keys().__contains__(level_warning)  
    dbmesg  : Gtk.MessageDialog  =   Gtk.MessageDialog ( 
            transient_for =  None ,  
            flags         =  0x00 , 
            message_type  =  iweq[level_warning]["message_type"] , 
            buttons       =  iweq[level_warning]["buttons"],
            text          =  iweq[level_warning]["text"]  
            )
    if  second_mesg  is not None  :  dbmesg.format_secondary_text(second_mesg) 
    resp  =  dbmesg.run()
    dbmesg.destroy()  
    return resp  #  Gtk.ResponseType.OK CANCEL YES NO   
    


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
mut_label     : str  = str () 

abs_path_dir_target  :str  =  os.getcwd()  # start where   u'r

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
    mainbox  : Gtk.Box  =  Gtk.Box(spacing=BOX_SPACING ,  orientation= Gtk.Orientation.VERTICAL) 
    
    vbox     : Gtk.Box  =  Gtk.Box(spacing=BOX_SPACING ,  orientation= Gtk.Orientation.HORIZONTAL)  
    hbox     : Gtk.Box  =  Gtk.Box(spacing=BOX_SPACING ,  orientation= Gtk.Orientation.HORIZONTAL)
    # logo  area 
    logo_label  : Gtk.Label  =  Gtk.Label()  
    logo_label.set_markup("<big> Gen  Assoc  </big>")
    logo_label.set_max_width_chars(78) 

    choose_file : Gtk.Button = Gtk.Button(label=f"Browse {mut_label}") 
    # input entry  
    entry    : Gtk.Entry  =  Gtk.Entry()  
    #  TODO  :
    # [] read default path to   config  file  to file  this area 
    entry.set_text(abs_path_dir_target) 
    vbox.pack_start(entry , True , True , 0 )  
    vbox.pack_start(choose_file , False , True , 0 ) 
    # buttons   
    startbtn    : Gtk.Button = Gtk.Button(label="Start !")  
    cancelbtn   : Gtk.Button = Gtk.Button(label="Abort x")
    
    # events
    #startbtn.connect("clicked"   , main_frame      ,  dialog_frame) 
    choose_file.connect("clicked", chooser ,  entry )
    startbtn.connect("clicked"   , middleware_checker , dialog_frame,  entry )#     ,  dialog_frame) 
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

def on_togglable_widget ( w_togglable ) ->   None :  
    """ 
    rbtn_on_toggle  :  get  the state  of radio button  on toggle event  
    @param    : 
    rbt_wiget :   Gtk.RadioButton  
    @return   :  
    None  
    """ 
    global state  
    state  =   (w_togglable.get_label() , w_togglable.get_label()) [w_togglable.get_active()]  
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
        dir_size         : int              ,  
        main_container   : Gtk.Window       , 
        dbox_frame       : Gtk.Window  
        )  ->     bool   :   

    global call_count  
    call_count+=1 
    print("0> " ,  call_count  ) 
    trigger   =  (True , False)[call_count  >=  0x64 >> 1  ]  # TODO :  replace  0x64 by the  size of the folder  !  
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


#  get  the  last folder  name e.g  /home/../../folder_name - >  get  only the  folder_name 
abriged_path  =  lambda  abs_path  : abs_path.split("/")[-1]  
working_dir   =  abriged_path(abs_path_dir_target)   
__fops__      =  None   
def middleware_checker ( 
        start_btn_launcher  :  Gtk.Button ,
        dbox                :  Gtk.Window ,
        entry               :  Gtk.Entry  , 
        )  ->  None   : 

    """ 
    check  the integrity of the folder if  it has all requirements available  
    """  
    global  working_dir  
    global  __fops__  
    working_dir     =  abriged_path(entry.get_text())  
    __fops__        =  FileOps(entry.get_text())  
    main_pb  : Gtk.Window =  Gtk.Window(title=f"{basename}: {working_dir} {pb.WIDTH}x{pb.HEIGHT}")  
    main_pb.set_border_width(pb.BORDER_WIDTH)  
    main_pb.set_default_size(pb.WIDTH , pb.HEIGHT)  
    main_pb.set_resizable(pb.RESIZABLE) 
    
    vbox          : Gtk.Box            =  Gtk.Box (spacing =BOX_SPACING   , orientation =  Gtk.Orientation.VERTICAL ) 
    activity_bar  :  Gtk.ProgressBar   =  Gtk.ProgressBar()
    activity_bar.pulse()  
    trigger  =  True
    
    status: str  =  f"Scanning ... {working_dir}  Directory"  
    activity_bar.set_text(status) 
    activity_bar.set_show_text(True)  
    
    dir_size   =  __fops__.get_size_of_directory()  # 0x64    #  TODO  :  do not forget to import  fileOps . get_size_of_directory    
    print("size -  > " , dir_size )  
    timout_id  =    GLib.timeout_add(
            0x64          ,  # loop call  
            on_timeout    ,  # callbacck 
            trigger       ,  
            activity_bar  ,  
            dir_size      ,
            main_pb       ,      
            dbox
            )  

    logo_label  : Gtk.Label  =  Gtk.Label()  
    logo_label.set_markup("<big> Gen  Assoc  </big>")
    logo_label.set_max_width_chars(78)  
    
    small_status  :Gtk.Label = Gtk.Label() 
    small_status.set_markup("<small> Please Wait ... </small>")  
    small_status.set_max_width_chars(0xa)  
    
    vbox.pack_start(logo_label ,  True , True  , 0  )  
    vbox.pack_start(activity_bar  , True ,True , 0  )
    vbox.pack_start(small_status, True , True ,  0 ) 

    main_pb.add(vbox) 
    show_frame(main_pb) 
     
def kill_frame  (target_frame  :Gtk.Window )  :  
    target_frame.destroy() 
    Gtk.main_quit()  

def switch_sync_inverted ( switch_widget ,  gsecparam ,  ss_widget )  ->  None : 
    """
    switch_sync_inverted  :   make a syncronisation  of 2  switch wiget 
    on/off  
    """
    state  : bool  =  switch_widget.get_active()  
    ss_widget.set_active(not state)  

   
def iter_stores  (  entry_data  ,  storage_input : Gtk.ListStore  )  -> None : 
    for data  in entry_data  : 
        storage_input.append([data])  
             
    
def on_combox_change ( combo_box_wiget  : Gtk.ComboBox  ) -> None  :
    iter_list  =  combo_box_wiget.get_active_iter() 
    if iter_list  is not  None :   
        model      = combo_box_wiget.get_model() 
        file_type  = model[iter_list][0x00] 
        print(f"you selected - >  {file_type}") 


def main_frame  (dbox_frame  : Gtk.Window)  -> None :
    
    kill_frame(dbox_frame) 
    
    w_d  = abriged_path(abs_path_dir_target)
    main_window_frame  : Gtk.Window =  Gtk.Window( title=f"{basename}:{abs_path_dir_target}  {mw.WIDTH}x{mw.HEIGHT}")  
    main_window_frame.set_border_width(mw.BORDER_WIDTH) 
    main_window_frame.set_default_size(mw.WIDTH ,  mw.HEIGHT)  
    main_window_frame.set_resizable(mw.RESIZABLE)

    master_container : Gtk.Box    =  Gtk.Box(spacing=BOX_SPACING  , orientation = Gtk.Orientation.VERTICAL)  
    #  LOGO  TITLE  HEADER  
    logo_label  : Gtk.Label  =  Gtk.Label()  
    logo_label.set_markup("<big> Gen  Assoc  </big>")
    logo_label.set_max_width_chars(78)  
    
    main_container: Gtk.Box    =  Gtk.Box(spacing=BOX_SPACING  , orientation = Gtk.Orientation.HORIZONTAL )  


    file_viewer   : Gtk.Box    =  Gtk.Box(spacing=BOX_SPACING  , orientation = Gtk.Orientation.VERTICAL )
   
    _ff       : Gtk.Frame =  Gtk.Frame(label=f"Current Working Path {w_d}")   
    _ff.set_shadow_type(Gtk.ShadowType.ETCHED_OUT)  #  0x004   
    expander      : Gtk.Expander =  Gtk.Expander(label="-----") #  TODO : replace  wd to  dir name
    current_dir_content   : Gtk.Label  = Gtk.Label(label = abriged_path(current_dir_view(abs_path_dir_target)))  
    expander.add(current_dir_content) 
    _ff.add(expander)  
    file_viewer.pack_start (_ff , True , True , 0 ) 
    
    container_box : Gtk.Box    =  Gtk.Box(spacing=0xA   , orientation = Gtk.Orientation.VERTICAL ) 

    setup_box     : Gtk.Box    =  Gtk.Box(spacing=BOX_SPACING  , orientation = Gtk.Orientation.HORIZONTAL) 
    # setup_box  component
    #  combox box 
    #  TODO  :  add   data  inside combo box    
    ped_files     : List[str]         =  [  abriged_path(f)  for f in  __fops__.list_files("ped") ]  
    map_files     : List[str]         =  [  abriged_path(f)  for f in  __fops__.list_files("map") ] 
    phen_files    : List[str]         =  [  abriged_path(f)  for f in  __fops__.list_files("phen")]   
    # DEBUG  PRINT 
    print("Debug -  < " ,  ped_files )  
    
    #  TODO :   make controlle to ensure  all  required files are present  in the  directory  
    ext_req  :  List [ str ]   =   [  "ped" , "map",  "phen" ]  
    
    not_statified =  False  
    for type_ext ,  F  in   enumerate ([  ped_files ,  map_files ,  phen_files ]):  
        if   F.__len__() == 0  :  
            not_statified  =  True  

    if  not_statified :  
        generic_alert_dialog(
                "warning"  , 
                "Unsatified Files Requierments " ,
                "Files requirements are not  satisfied"
                )
            
    render_text_tooltip_for_ped  :  Gtk.CellRendererText  =  Gtk.CellRendererText() 
    render_text_tooltip_for_map  :  Gtk.CellRendererText  =  Gtk.CellRendererText() 
    render_text_tooltip_for_phen :  Gtk.CellRendererText  =  Gtk.CellRendererText() 

    ped_stores    : Gtk.ListStore     =  Gtk.ListStore(str) 
    map_stores    : Gtk.ListStore     =  Gtk.ListStore(str)  
    phen_stores   : Gtk.ListStore     =  Gtk.ListStore(str) 
    
    iter_stores(ped_files ,  ped_stores) 
    iter_stores(map_files ,  map_stores) 
    iter_stores(phen_files,  phen_stores) 

    
    ped_label     : Gtk.Label         =  Gtk.Label(label="ped :")  
    ped_cb        : Gtk.ComboBoxText  =  Gtk.ComboBox.new_with_model(ped_stores)   
    ped_cb.pack_start(render_text_tooltip_for_ped , True )  
    ped_cb.add_attribute (render_text_tooltip_for_ped ,  "text" ,  0 )  
    

    map_label     : Gtk.Label         =  Gtk.Label(label="map:") 
    map_cb        : Gtk.ComboBoxText  =  Gtk.ComboBox.new_with_model(map_stores) 
    map_cb.pack_start(render_text_tooltip_for_map , True  ) 
    map_cb.add_attribute(render_text_tooltip_for_map , "text" , 0 )  
    
    phen_label    :  Gtk.Label        =  Gtk.Label(label ="phen :") 
    phen_cb       : Gtk.ComboBoxText  =  Gtk.ComboBox.new_with_model(phen_stores)
    phen_cb.pack_start(render_text_tooltip_for_phen , True) 
    phen_cb.add_attribute(render_text_tooltip_for_phen ,  "text" , 0 ) 


    load_btn      : Gtk.Button        =  Gtk.Button(label="Load")  
    
    
    setup_box.pack_start(ped_label , True , True ,  0 )  
    setup_box.pack_start(ped_cb    , True , True ,  0 )  
    setup_box.pack_start(map_label , True , True ,  0 )  
    setup_box.pack_start(map_cb    , True , True ,  0 )  
    setup_box.pack_start(phen_label, True , True ,  0 )  
    setup_box.pack_start(phen_cb   , True , True ,  0 )  
    setup_box.pack_start(load_btn  , True , True ,  0 )

    choose_box    : Gtk.Box    =  Gtk.Box(spacing=BOX_SPACING  , orientation = Gtk.Orientation.HORIZONTAL)  
    # check box  area 
    run_opts   : Dict[str , str ]    =  {  
            "1" :  "Single Marker" ,
            "2" :  "Multiple Marker"
            }  
    single_marker_rbtn       : Gtk.RadioButton  =  Gtk.RadioButton.new_with_label_from_widget(None,f"{run_opts['1']}")  
    single_marker_rbtn.connect("toggled" , on_togglable_widget)
   
    multiple_marker_rbtn     : Gtk.RadioButton  =  Gtk.RadioButton.new_from_widget(single_marker_rbtn)  
    multiple_marker_rbtn.set_label(f"{run_opts['2']}")   
    multiple_marker_rbtn.connect("toggled" , on_togglable_widget)

    run_btn       : Gtk.Button =  Gtk.Button(label="Run Analysis")
  

    choose_box.pack_start(single_marker_rbtn , True, False  , 0  )  
    choose_box.pack_start(multiple_marker_rbtn, True ,False, 0  )
    
    choose_box.pack_start(run_btn  ,  True , True, 0 )   

    tne_box   :  Gtk.Box  = Gtk.Box(spacing  = BOX_SPACING  , orientation = Gtk.Orientation.HORIZONTAL )  
    
    # emperical  label 
 
    # switch  button  to enable  emperical   
    emp_label  : Gtk.Label =  Gtk.Label(label="Enable Emperical : ") 
    enable_emperical : Gtk.Switch()  = Gtk.Switch ()
    # by default  the emperical is desable   
    enable_emperical.set_active(False)    
     
    th_label   : Gtk.Label =  Gtk.Label(label="Enable Theorical")   
    enable_theorical  : Gtk.Switch()   =  Gtk.Switch()  
    enable_theorical.set_active(True)  
    enable_theorical.connect("notify::active" , switch_sync_inverted ,enable_emperical ) 
    enable_emperical.connect("notify::active" , switch_sync_inverted ,enable_theorical )  
     
    tne_box.pack_start(emp_label , True , True , 0 )  
    tne_box.pack_start(enable_emperical , False,False, 0 )  
    tne_box.pack_start(th_label , True , True , 0 )  
    tne_box.pack_start(enable_theorical , False ,False , 0 ) 
    
    marker_n_setarg :  Gtk.Box    =  Gtk.Box(spacing = BOX_SPACING ,  orientation=Gtk.Orientation.HORIZONTAL)  

    marker_frame    :  Gtk.Frame  =   Gtk.Frame(label="Marker Set")   
    
    setup_args_box  :  Gtk.Box    =   Gtk.Box(spacing =0x0F,  orientation= Gtk.Orientation.VERTICAL)  
    
    nsim_box        :  Gtk.Box    =   Gtk.Box(spacing = BOX_SPACING ,  orientation= Gtk.Orientation.HORIZONTAL)  
    ncore_box       :  Gtk.Box    =   Gtk.Box(spacing = BOX_SPACING ,  orientation= Gtk.Orientation.HORIZONTAL)  
    pheno_box       :  Gtk.Box    =   Gtk.Box(spacing = BOX_SPACING ,  orientation= Gtk.Orientation.HORIZONTAL)  
    
    nsim_label      :  Gtk.Label  =   Gtk.Label(label= "Nsims    :")  
    ncore_label      :  Gkt.Label  =   Gtk.Label(label="Nbcores  :") 
    pheno_label     :  Gkt.Label  =   Gtk.Label(label= "Phenotype:")
    
    available_data  :  Gtk.ListStore = Gtk.ListStore(int , int )  

    for    i ,  iA_  in  enumerate( range(0 ,10)) : available_data.append ([i  , iA_])  

    nsim_cb         :  Gtk.ComboBox  = Gtk.ComboBox.new_with_model_and_entry(Gtk.ListStore(available_data))    
    ncore_cb        :  Gtk.ComboBox  = Gtk.ComboBox.new_with_model_and_entry(Gtk.ListStore(available_data))   
    pheno_cb        :  Gtk.ComboBox  = Gtk.ComboBox.new_with_model_and_entry(Gtk.ListStore(available_data))   
    
    nsim_box.pack_start(nsim_label      , True , True , 0 ) 
    nsim_box.pack_start(nsim_cb         , True , True , 0 ) 
    
    ncore_box.pack_start(ncore_label    , True , True , 0 ) 
    ncore_box.pack_start(ncore_cb       , True , True , 0 ) 
    
    pheno_box.pack_start(pheno_label    , True , True , 0 )  
    pheno_box.pack_start(pheno_cb       , True , True , 0 ) 
    
    setup_args_box.pack_start(nsim_box  , True , True , 0  ) 
    setup_args_box.pack_start(ncore_box , True , True , 0  ) 
    setup_args_box.pack_start(pheno_box , True , True , 0  ) 

    marker_n_setarg.pack_start(setup_args_box, False , False , 0  ) 
    marker_n_setarg.pack_start(marker_frame  , True , True , 0  )  
    
    log_container   : Gtk.Box    =  Gtk.Box(spacing=BOX_SPACING  , orientation = Gtk.Orientation.VERTICAL )  

    bottombox       : Gtk.Box    =  Gtk.Box(spacing=BOX_SPACING ,  orientation= Gtk.Orientation.HORIZONTAL)
    quit_bnt        : Gtk.Button =  Gtk.Button(label="Quit")  
    quit_bnt.connect("clicked" , Gtk.main_quit)  
    bottombox.pack_start(quit_bnt ,  True , False,0 )  

    log_frame       :  Gtk.Frame = Gtk.Frame(label=" Output  Log " )  
    
    log_container.pack_start(log_frame, True , True , 0 )   
    
    container_box.pack_start(setup_box       ,  False , False , 0 )  
    container_box.pack_start(choose_box      ,  False , False , 0 ) 
    container_box.pack_start(tne_box         ,  False , False , 0 )
    container_box.pack_start(marker_n_setarg ,  False , False , 0 ) 
    container_box.pack_start(log_container   ,  True  , True  , 0 )   

    main_container.pack_start(file_viewer    , False  , True  , 0 )  
    main_container.pack_start(container_box  , True   , True  , 0 )  
   
    master_container.pack_start(logo_label      , False, True , 0 )
    master_container.pack_start(main_container  , True ,True  , 0 )
    master_container.pack_start(bottombox       , False,True  , 0 )  

    main_window_frame.add(master_container) 
    
    show_frame(main_window_frame)  

def main   ()  -> None :  
     
    dialog_box(main_frame)  


if __name__.__eq__("__main__")  : 
    try  : 
        main()  
    except KeyboardInterrupt  as  brutalExit :  
        sys.stderr.write("{}\n".format(brutalExit)) 

