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
import  multiprocessing  

from time import sleep 
from  typing  import List , Dict , Tuple  
from  collections import  namedtuple

from  fileOps  import  FileOps 
from  utils    import Utils 


basename  :  str  = f"mTDT {__stage__} v{__version__}" 
PRODUCTION_READY  =   False  

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
        True       ,     #  RESIZABLE
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
NSIM_LIMIT         : int  = 0x00B
NCORES_AVAILABLE   : int  = multiprocessing.cpu_count()  

#TODO  : figure out this function  to make  it  more  adptable for each os  
def  current_dir_view ( actual_path  )  :   
    if sys.platform.__eq__("linux") :  
        p =  os.popen(f"tree {actual_path}").read()  
        return  p 


def generic_alert_dialog  (level_warning ,  mesg   , second_mesg  =   None   ) -> Gtk.ResponseType :  
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
            transient_for =  None,  
            flags         =  0x00 , 
            message_type  =  iweq[level_warning]["message_type"] , 
            buttons       =  iweq[level_warning]["buttons"],
            text          =  iweq[level_warning]["text"]  
            )
    if  second_mesg  is not None  :  dbmesg.format_secondary_text(second_mesg) 
    resp  =  dbmesg.run()
    if   resp.__eq__(Gtk.ResponseType.OK)  :  
        print("oK Clicked ")  
        
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
is_mm_set  :  bool  =   False   

def on_togglable_widget ( w_togglable , field_entry  : Gtk.Entry ) ->   None :  
    """ 
    rbtn_on_toggle  :  get  the state  of radio button  on toggle event  
    @param    : 
    rbt_wiget :   Gtk.RadioButton  
    @return   :  
    None  
    """ 
    global state  
    global is_mm_set  
    state  =   (w_togglable.get_label() , w_togglable.get_label()) [w_togglable.get_active()]
    if state.lower().__eq__("multiple marker")  :   
        is_mm_set = True  
        field_entry.set_editable(True)   
    if state.lower().__eq__("single marker")    : 
        is_mm_set  = False  
        field_entry.set_editable(False)    
 

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
    if  PRODUCTION_READY : dir_size  = int( dir_size)  
    else : dir_size = 1   
    trigger   =  (True , False)[call_count  >=  dir_size ]  
    if trigger : activity_bar.pulse() 
    else  :  
        activity_bar.set_text("laoding data ")  
        activity_bar.set_show_text(True)  
        #sleep(2) 
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
    # TODO  : Looking require files before 
    
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

def switch_sync_inverted (  
        switch_widget ,  
        gsecparam ,  
        ss_widget ,  
        plist_nsim  :  Gtk.ListStore ,  
        plist_ncore :  Gtk.ListStore ,  
        th_turn_off = False , 
        )  ->  None : 
    """
    switch_sync_inverted  :   make a syncronisation  of 2  switch wiget 
    on/off  
    """
    state  : bool  =  switch_widget.get_active()  
    state_ : bool  =  ss_widget.get_active()   
    #ss_widget.set_active(not state) 

    if  th_turn_off.__eq__(False) : 
        ss_widget.set_active(False)
        state=  False  

    if state.__eq__(True) and  th_turn_off : 
        ss_widget.set_active(False)  
        iter_stores ( range(1  , NSIM_LIMIT)  ,  plist_nsim)   
        iter_stores (
                range(1  , NCORES_AVAILABLE)  if  NCORES_AVAILABLE  > 1  else   range(1,NCORES_AVAILABLE+1)  ,
                plist_ncore
                )
    else  : 
        plist_nsim.clear() 
        plist_ncore.clear() 
   
   
def iter_stores  (  entry_data  ,  storage_input : Gtk.ListStore  )  -> None : 
    for data  in entry_data  : 
        storage_input.append([data])  
             
 
pmp  = namedtuple("pmp",  [
    "selected_pedfile",
    "selected_mapfile",
    "selected_phenfile"
    ])

_pmp_ =  pmp( 
        selected_pedfile = None  ,  
        selected_mapfile = None  , 
        selected_phenfile= None  
        )  
def sync_ped_to_map_vice_versa   (file_data_type)  :
    # autodetect  extention   
    allowed_ext      : List[str,str] =  [".ped" , ".map"]  
    filename_no_ext  :str  =    file_data_type[:-4]   
    ext              :str  =    file_data_type[-4:]
    assert  allowed_ext.__contains__(ext) 
    if ext.__eq__(allowed_ext[0])   :   filename_no_ext+=allowed_ext[1]  
    if ext.__eq__(allowed_ext[1])   :   filename_no_ext+=allowed_ext[0] 
    return  filename_no_ext  
    

ped_data      =  str () 
map_data      =  str () 
phen_data     =  str () 
nsims_chosed  =  int ()  
ncores_chosed =  int ()
phen_chosed   =  int ()  

def on_combox_change ( 
        combo_box_wiget  : Gtk.ComboBox,    
        load_btn_widget  : Gtk.Button =  None,  
        payload      =  None  , 
        sync_cb      =  None  , 
        nsim_select  =  False , 
        ncore_select =  False , 
        phen_select  =  False   
        ) -> str  :

    global ped_data 
    global map_data 
    global phen_data    
    global nsims_chosed  
    global ncores_chosed
    global phen_chosed 
     
    actual_dir   : str  = abs_path_dir_target  
    iter_list  =  combo_box_wiget.get_active_iter() 
    if iter_list  is not  None :   
        model      = combo_box_wiget.get_model() 
        file_type  = model[iter_list][0x00]
        _ext       = str () 
        if  type(payload) is not None and type(file_type) is not int: _ext  =  file_type.split(chr(0x2e))[1]
        else         :  
            #@NOTE :  file type here  is  int  
            if  nsim_select  :  nsims_chosed    =  file_type  
            if  ncore_select :  ncores_chosed   =  file_type  
            if  phen_select  :  phen_chosed     =  file_type  

        if _ext.__eq__("map")   : 
            map_data = file_type
            pedfile_name   : str  =  sync_ped_to_map_vice_versa(map_data)  
            if os.path.exists (f"{actual_dir}/{pedfile_name}")   and  sync_cb: 
                equivalent_pos_index =   payload.index(pedfile_name)  
                sync_cb.set_active(equivalent_pos_index) 
                
        if _ext.__eq__("ped")   :  
            ped_data = file_type
            mapfile_name   : str  =  sync_ped_to_map_vice_versa(ped_data)  
            if os.path.exists (f"{actual_dir}/{mapfile_name}")  and sync_cb:
                equivalent_pos_index  =  payload.index(mapfile_name)  
                sync_cb.set_active(equivalent_pos_index)  
        
        if _ext.__eq__("phen")  :  phen_data= file_type

        if  load_btn_widget and  phen_data  and  ped_data  and map_data  : 
            load_btn_widget.set_sensitive(True)
        else  :    
            if  load_btn_widget  :
                load_btn_widget.set_sensitive(False)
                


def main_frame  (dbox_frame  : Gtk.Window)  -> None :
    
    kill_frame(dbox_frame) 
    # load  utils   libs  
    _u_  =  Utils()  

    w_d  = abriged_path(abs_path_dir_target)
    main_window_frame  : Gtk.Window =  Gtk.Window( title=f"{basename}:{abs_path_dir_target}  {mw.WIDTH}x{mw.HEIGHT}")  
    main_window_frame.set_border_width(mw.BORDER_WIDTH) 
    main_window_frame.set_default_size(mw.WIDTH ,  mw.HEIGHT)  
    main_window_frame.set_resizable(mw.RESIZABLE)

    #  HEADER BAR  
    headB  : Gtk.HeaderBar  = Gtk.HeaderBar()  
    headB.set_show_close_button(True) 
    headB.props.title= f"{basename}:{abs_path_dir_target}  {mw.WIDTH}x{mw.HEIGHT}"
    main_window_frame.set_titlebar(headB)  

    master_container : Gtk.Box    =  Gtk.Box(spacing=BOX_SPACING  , orientation = Gtk.Orientation.VERTICAL)  
    #  LOGO  TITLE  HEADER  
    logo_label  : Gtk.Label  =  Gtk.Label()  
    logo_label.set_markup("<big> Gen  Assoc  </big>")
    logo_label.set_max_width_chars(78)  
    
    main_container: Gtk.Box    =  Gtk.Box(spacing=BOX_SPACING  , orientation = Gtk.Orientation.HORIZONTAL )  

    file_viewer   : Gtk.Box    =  Gtk.Box(spacing=BOX_SPACING  , orientation = Gtk.Orientation.VERTICAL )
   
    _ff       : Gtk.Frame =  Gtk.Frame(label=f"Current Working Path {w_d}")   
    _ff.set_shadow_type(Gtk.ShadowType.ETCHED_OUT)  #  0x004   
    expander      : Gtk.Expander =  Gtk.Expander(label="-----")
    current_dir_content   : Gtk.Label  = Gtk.Label(label = abriged_path(current_dir_view(abs_path_dir_target)))  
    expander.add(current_dir_content) 
    _ff.add(expander)  
    file_viewer.pack_start (_ff , True , True , 0 ) 
    
    container_box : Gtk.Box    =  Gtk.Box(spacing=0xA   , orientation = Gtk.Orientation.VERTICAL ) 

    setup_box     : Gtk.Box    =  Gtk.Box(spacing=BOX_SPACING  , orientation = Gtk.Orientation.HORIZONTAL) 
    # setup_box  component
    #  combox box 
    #  TODO  :  add   data  inside combo box   
    files_requirements  = [
            ped_files     ,  
            map_files     , 
            phen_files     
            ]=(
                    [  abriged_path(f)  for f in  __fops__.list_files("ped") ]  , 
                    [  abriged_path(f)  for f in  __fops__.list_files("map") ]  ,
                    [  abriged_path(f)  for f in  __fops__.list_files("phen")] 
                    ) 

    # DEBUG  PRINT 
    print("Debug -  < " ,  ped_files )  
    #  TODO :   make controlle to ensure  all  required files are present  in the  directory  
    ext_req  :  List [ str ]   =   [  "ped" , "map",  "phen" ]  
    
    not_statified =  False  
    for type_ext ,  F  in   enumerate(files_requirements):   
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

    load_btn      : Gtk.Button        =  Gtk.Button(label="Load") 
    load_btn.set_sensitive(False) 
    
    ped_label     : Gtk.Label         =  Gtk.Label(label="ped :")  
    ped_cb        : Gtk.ComboBoxText  =  Gtk.ComboBox.new_with_model(ped_stores)   
    ped_cb.pack_start(render_text_tooltip_for_ped , True )  
    ped_cb.add_attribute (render_text_tooltip_for_ped ,  "text" ,  0 )  

    map_label     : Gtk.Label         =  Gtk.Label(label="map:") 
    map_cb        : Gtk.ComboBoxText  =  Gtk.ComboBox.new_with_model(map_stores) 
    map_cb.pack_start(render_text_tooltip_for_map , True  ) 
    map_cb.add_attribute(render_text_tooltip_for_map , "text" , 0 ) 
    # TODO  :  syncronise   ped and  map   
    
    map_cb.connect("changed" ,  on_combox_change  ,load_btn, ped_files , ped_cb)  
    ped_cb.connect("changed" ,on_combox_change    ,load_btn, map_files , map_cb)  
    
    phen_label    :  Gtk.Label        =  Gtk.Label(label ="phen :") 
    phen_cb       : Gtk.ComboBoxText  =  Gtk.ComboBox.new_with_model(phen_stores)
    phen_cb.pack_start(render_text_tooltip_for_phen , True) 
    phen_cb.add_attribute(render_text_tooltip_for_phen ,  "text" , 0 ) 
    phen_cb.connect("changed" ,  on_combox_change , load_btn)

    setup_box.pack_start(ped_label , True , True ,  0 )  
    setup_box.pack_start(ped_cb    , True , True ,  0 )  
    setup_box.pack_start(map_label , True , True ,  0 )  
    setup_box.pack_start(map_cb    , True , True ,  0 )  
    setup_box.pack_start(phen_label, True , True ,  0 )  
    setup_box.pack_start(phen_cb   , True , True ,  0 )  
    setup_box.pack_start(load_btn  , True , True ,  0 )

    choose_box    : Gtk.Box    =  Gtk.Box(spacing=BOX_SPACING  , orientation = Gtk.Orientation.HORIZONTAL)  

    #  the radio button  is related  to  marker set  entry  point 
    marker_payload  :  Gtk.ListStore =  Gtk.ListStore(int) 
    marker_label    :  Gtk.Label     = Gtk.Label(label="MarkerSet :")  
    marker_set      :  Gtk.Entry     = Gtk.Entry()  # Gtk.ComboBox.new_with_model_and_entry(marker_payload)
    marker_set.set_editable(False)  
    #marker_set.set_text()
    # marker_set.connect("changed"   , on_combox_change)  
    # check box  area 
    run_opts   : Dict[str , str ]    =  {  
            "1" :  "Single Marker" ,
            "2" :  "Multiple Marker"
            }  
    single_marker_rbtn       : Gtk.RadioButton  =  Gtk.RadioButton.new_with_label_from_widget(None,f"{run_opts['1']}")  
    single_marker_rbtn.connect("toggled" , on_togglable_widget  , marker_set)
   
    multiple_marker_rbtn     : Gtk.RadioButton  =  Gtk.RadioButton.new_from_widget(single_marker_rbtn)  
    multiple_marker_rbtn.set_label(f"{run_opts['2']}")   
    multiple_marker_rbtn.connect("toggled" , on_togglable_widget , marker_set)

    choose_box.pack_start(single_marker_rbtn , True, False  , 0 )  
    choose_box.pack_start(multiple_marker_rbtn, True ,False, 0)
    
    #choose_box.pack_start(run_btn  ,  True , True, 0 )   

    tne_box   :  Gtk.Box  = Gtk.Box(spacing  = BOX_SPACING  , orientation = Gtk.Orientation.HORIZONTAL )  
    
    # emperical  label 
 
    # switch  button  to enable  emperical   
    emp_label  : Gtk.Label =  Gtk.Label(label="Enable Emperical : ") 
    enable_emperical : Gtk.Switch()  = Gtk.Switch ()
    # by default  the emperical is desable   
    enable_emperical.set_active(False)    
     
    th_label   : Gtk.Label =  Gtk.Label(label="Enable Theorical :")   
    enable_theorical  : Gtk.Switch()   =  Gtk.Switch()  
    enable_theorical.set_active(True)  
    
    nsim_preset_list :    Gtk.ListStore = Gtk.ListStore(int)   
    ncore_preset_list:    Gtk.ListStore = Gtk.ListStore(int)  
   
    enable_theorical.connect(
            "notify::active" , 
            switch_sync_inverted ,
            enable_emperical,
            nsim_preset_list ,  
            ncore_preset_list
            ) 
    
    enable_emperical.connect(
            "notify::active", 
            switch_sync_inverted ,
            enable_theorical , 
            nsim_preset_list , 
            ncore_preset_list,
            True
            )   
     
    tne_box.pack_start(emp_label , True, True , 0 )  
    tne_box.pack_start(enable_emperical ,False , True, 0 )  
    tne_box.pack_start(th_label , True , True , 0 )  
    tne_box.pack_start(enable_theorical , False,  True , 0 ) 
    
    marker_n_setarg :  Gtk.Box    =  Gtk.Box(spacing = 0x00F ,  orientation=Gtk.Orientation.HORIZONTAL)  

    #  TODO  : 
    #  preload  marker  if they are available  
    marker_zone     :  Gtk.Box    = Gtk.Box(spacing  = 0x00f  , orientation=Gtk.Orientation.HORIZONTAL)
    analysis_zone   :  Gtk.Box    = Gtk.Box(spacing  = 0x00f  , orientation=Gtk.Orientation.HORIZONTAL) 
    

    
    marker_zone.pack_start(marker_label  , False , True ,  0 )  
    marker_zone.pack_start(marker_set    , True , True ,  0 )
    
    run_btn            : Gtk.Button =  Gtk.Button(label="Run Analysis")
    run_btn.set_sensitive(False) 
    
    analysis_zone.pack_start(run_btn ,True , False  , 0 )
    
    run_n_marker_zone  : Gtk.Box    =  Gtk.Box( spacing = 0x00f , orientation = Gtk.Orientation.VERTICAL) 
    run_n_marker_zone.pack_start(marker_zone   , True , True  ,  0 ) 
    run_n_marker_zone.pack_start(analysis_zone , True , False   ,  0 ) 


    setup_args_box  :  Gtk.Box    =   Gtk.Box(spacing =0x0F,  orientation= Gtk.Orientation.VERTICAL)  
    
    nsim_box        :  Gtk.Box    =   Gtk.Box(spacing = BOX_SPACING ,  orientation= Gtk.Orientation.HORIZONTAL)  
    ncore_box       :  Gtk.Box    =   Gtk.Box(spacing = BOX_SPACING ,  orientation= Gtk.Orientation.HORIZONTAL)  
    pheno_box       :  Gtk.Box    =   Gtk.Box(spacing = BOX_SPACING ,  orientation= Gtk.Orientation.HORIZONTAL)  
    
    nsim_label      :  Gtk.Label  =   Gtk.Label(label="Nsims    :")  
    ncore_label     :  Gkt.Label  =   Gtk.Label(label="Nbcores  :") 
    pheno_label     :  Gkt.Label  =   Gtk.Label(label="Phenotype:")
    

    pheno_preset_list:    Gtk.ListStore = Gtk.ListStore(int)  
     
    scrollog        : Gtk.ScrolledWindow = Gtk.ScrolledWindow() 
    logview         : Gkt.TextView  = Gtk.TextView()
    logview.set_editable(False) 
    logbuffering    : Gtk.TextBuffer = Gtk.TextBuffer() 
    progressive_iter  =  logbuffering.get_end_iter()
    #logbuffering.insert(progressive_iter , "this is a simple log" )  
    #logbuffering.set_text("this  is  a log ") 
    logview.set_buffer(logbuffering) 
    scrollog.add(logview) 

    def launch_summary   (  
            widget         : Gtk.Button      ,  
            b_log          : Gtk.TextBuffer  , 
            run_btn_widget : Gtk.Button      , 
            plist          : Gtk.ListStore
            ): 
        # TODO  : ADD CONTROL  TO ENSURE   ALL 3 VARIABLE ARE  NOT EMPTY
        # TODO  : MAKE STATIC PATH  FOR  SUMMARY.R SCRIPT
        
        source  = f"{abs_path_dir_target}/summary.R" 
        ped_  = f"{abs_path_dir_target}/{ped_data}" 
        map_  = f"{abs_path_dir_target}/{map_data}" 
        phen_ = f"{abs_path_dir_target}/{phen_data}" 
        
        exec =  _u_.stream_stdout(f"Rscript  {source} --pedfile {ped_} --mapfile {map_}  --phenfile {phen_}")
                
        b_log.insert(progressive_iter ,exec) 
        # TODO  : Chech if  some errors are not occured to generate alert message 
        # if everything  is Ok  enable  the run_btn_widget 
        # otherwise  , maintain the  disable state  
       
        # auto fill phenotype cbox  on load 
        phenotype_rowcol = __fops__.phen_rowcol(f"{abs_path_dir_target}/{phen_data}")  
        iter_stores ( range(1 ,  phenotype_rowcol.__len__() -0x001)  ,plist)   
        run_btn_widget.set_sensitive(True)   

    
    #iter_stores ( range(0   , 1003)  ,pheno_preset_list)   
    load_btn.connect("clicked" , launch_summary ,  logbuffering  , run_btn,  pheno_preset_list )  #  ...) 
    
    render_text_tooltip_for_nsim    : Gtk.CellRendererText  =  Gtk.CellRendererText() 
    render_text_tooltip_for_ncore   : Gtk.CellRendererText  =  Gtk.CellRendererText() 
    render_text_tooltip_for_pheno   : Gtk.CellRendererText  =  Gtk.CellRendererText()

    nsim_cb         :  Gtk.ComboBoxText  = Gtk.ComboBox.new_with_model(nsim_preset_list)    
    nsim_cb.pack_start(render_text_tooltip_for_nsim , True )  
    nsim_cb.add_attribute(render_text_tooltip_for_nsim,   "text" ,  0 ) 
    nsim_cb.connect("changed" ,  on_combox_change  , None,None , None , True) 
    
    ncore_cb        :  Gtk.ComboBoxText  = Gtk.ComboBox.new_with_model(ncore_preset_list)  
    ncore_cb.pack_start(render_text_tooltip_for_ncore , True )  
    ncore_cb.add_attribute(render_text_tooltip_for_ncore , "text" , 0 ) 
    ncore_cb.connect("changed" ,  on_combox_change  ,None, None , None , False , True) 
    
    pheno_cb        :  Gtk.ComboBoxText  = Gtk.ComboBox.new_with_model(pheno_preset_list)  
    pheno_cb.pack_start(render_text_tooltip_for_pheno , True ) 
    pheno_cb.add_attribute(render_text_tooltip_for_pheno , "text" , 0 )  
    pheno_cb.connect("changed" ,  on_combox_change  ,None, None , None  ,False , False  , True ) 
    
    
    nsim_box.pack_start(nsim_label      , True , True , 0 ) 
    nsim_box.pack_start(nsim_cb         , True , True , 0 ) 
    
    ncore_box.pack_start(ncore_label    , True , True , 0 ) 
    ncore_box.pack_start(ncore_cb       , True , True , 0 )  
        
    
    pheno_box.pack_start(pheno_label    , True , True , 0 )  
    pheno_box.pack_start(pheno_cb       , True , True , 0 ) 
    
    setup_args_box.pack_start(nsim_box  , True , True , 0  ) 
    setup_args_box.pack_start(ncore_box , True , True , 0  ) 
    setup_args_box.pack_start(pheno_box , True , True , 0  ) 

    marker_n_setarg.pack_start(setup_args_box, True , True  , 0 ) 
    
    marker_n_setarg.pack_start(run_n_marker_zone, True , True  , 0 ) 
    
    log_container   : Gtk.Box    =  Gtk.Box(spacing=BOX_SPACING  , orientation = Gtk.Orientation.VERTICAL )  
    
    def run_analysis  ( wiget : Gtk.Button  , b_log  : Gtk.TextBuffer )   : 
        source  = f"{abs_path_dir_target}/run_analysis.R" 
        ped_    = f"{abs_path_dir_target}/{ped_data}" 
        map_    = f"{abs_path_dir_target}/{map_data}" 
        phen_   = f"{abs_path_dir_target}/{phen_data}"  
        
        cmd  = f"Rscript   {source} --pedfile  {ped_} --mapfile {map_}  --phenfile {phen_} --nbsim {nsims_chosed} --nbcores {ncores_chosed}"  
        
        print("ms txt "  , marker_set.get_text() )  

        exec = _u_.stream_stdout(cmd)  
        b_log.insert(progressive_iter, exec) 


    run_btn.connect ("clicked" ,  run_analysis  ,  logbuffering )  

    bottombox       : Gtk.Box    =  Gtk.Box(spacing=BOX_SPACING ,  orientation= Gtk.Orientation.HORIZONTAL)
    quit_bnt        : Gtk.Button =  Gtk.Button(label="Quit")  
    quit_bnt.connect("clicked" , Gtk.main_quit)  
    bottombox.pack_start(quit_bnt ,  True , False,0 )  

    log_frame       :  Gtk.Frame = Gtk.Frame(label="CONSOLE" )   
    log_frame.add(scrollog)  
    
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

