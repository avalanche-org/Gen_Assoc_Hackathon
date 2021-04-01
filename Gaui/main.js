#!/usr/bin/env  node  

//author  : Umar aka jukoo  j_umar@outlook.com   <github.com/jukoo> 
//__stage__  : {  process.env["STAGE"] = "production"          }  
//__output_r : {  output_result        ="/home/juko/Desktop/Pasteur/Sandbox/H3BioNet/Gen_Assoc_Hackathon/Gaui/sample_results/weighted_res_multilocus.csv"} 
__stage__  : {  process.env["STAGE"] = "development"          }  
const
{ app,  BrowserWindow  , Menu , dialog , ipcMain } =  require('electron') ,  
{   log  }  = console , 
    path    = require("path") ,
    fs      = require("fs") , 
    url     = require("url"), 
    defconf = require("./config.json") , 
{summary_src ,  run_analysis } = defconf["mtdt_pannel"], 
menu        = require("./menu"), 
utils       = require("./utils"),  
htm_static_path      = "index.html"   

let mw  =  null   , tw  = null  

const  mt_load = menu_template  =>  Menu.buildFromTemplate(menu_template)  

const  action_event  =  wi  => {  
    if ( ! wi instanceof BrowserWindow) return  
        ipcMain.on("run::summary" ,   (evt  ,  _data /*_data is object*/ )  =>  {
            const  { paths  , selected_files  }  =  _data 
            const  [pedfile,mapfile,phenfile]  = selected_files 

            utils.rsv_file(`/${paths}/${phenfile}` ,  '\t')
           .then(res => {
               // TODO  : send   event to read stream  ...  
              // utils.Rlog(".logout"  ,  mw) 
               utils.std_ofstream(`Rscript ${summary_src} --pedfile /${paths}/${pedfile} --mapfile /${paths}/${mapfile} --phenfile /${paths}/${phenfile}` ,
                    exit_code => {
                    if  (exit_code == 0x00)  {
                        //wi.webContents.send("end"  , exit_code) 
                        //TODO  : send   signal to  stop printing  ... 
                        //wi.webContents.send("end" , exit_code)
                         
                        fs.readFile(".logout" , "utf8" ,  (e , d ) => {
                            if (e)  wi.webContents.send("log::fail" , e  )   
                            wi.webContents.send("term::logout"  , d )   
                        })
                        wi.webContents.send("load::phenotype"  ,  res-2)   
                    }else {
                        log("fail")  
                        fs.access(".logerr" , fs.constants["F_OK"] , error => {
                            if (error )  wi.webContents.send("logerr::notfound" , error)  
                            fs.readFile('.logerr' , "utf8" , (err , data) =>{
                                if(err) wi.webContents.send("log::broken" ,  error ) 
                                log(data)
                                wi.webContents.send ("term::logerr" , data) 
                            })
                        }) 
                    }
                })
            }) 
        })

        ipcMain.on("run::analysis" , (evt , data) => {
            const { paths  , selected_index  }  = data    
            const {  mm    , sm , ped , map , phen , phenotype_,  nbsim_ , nbcores_ , markerset }  = selected_index  
            let cmdstr = null 
            if (mm && markerset!= null && markerset != '')  {  
                cmdstr =`Rscript ${run_analysis} --pedfile /${paths}/${ped} --mapfile /${paths}/${map} --phenfile /${paths}/${phen} --phen ${phenotype_} --nbsim ${nbsim_} --nbcores ${nbcores_} --markerset ${markerset}` 
            } 
            if  (sm)  {  
                cmdstr =`Rscript ${run_analysis} --pedfile /${paths}/${ped} --mapfile /${paths}/${map} --phenfile /${paths}/${phen} --phen ${phenotype_}  --nbcores ${nbcores_}`
            }

            utils.std_ofstream(cmdstr ,  exit_code  => {
                if(exit_code ==0x00) {
                    log("exit" , exit_code )
                    wi.webContents.send("end"  , exit_code) 
                    fs.readFile(".logout" , "utf8" , (e , d)  => {
                        if  (e)    wi.webContents.send("log::fail" , e  )  
                        log("output result" ,  d) 
                        //mw.webContents.send("run::analysis_result" ,  d  ) 
                        wi.webContents.send("term::logout" ,  d  ) 
                         
                    })
                }else {
                    log("error") 
                    fs.access(".logerr" , fs.constants["F_OK"] , error => {
                        if (error )  wi.webContents.send("logerr::notfound" , error)  
                        fs.readFile('.logerr' , "utf8" , (err , data) =>{
                            if(err) wi.webContents.send("log::broken" ,  error ) 
                            try {  
                            wi.webContents.send ("term::logerr" , data)
                            }catch (err) { }
                        })
                    }) 
                }
            })
        })



}


let tty = false ; 
const   create_window =  (fd , { ...config }  )  => {
    let instance = new BrowserWindow ( { ...config} )  
    instance.loadURL( url.format ( {   
        pathname  : path.join(__dirname ,  fd )  , 
        protocol  : 'file:' ,
        slashes   :  true 
     }))
     return  instance  
}

app.on("ready",  () =>  { 
     try  {    
        mw = create_window ("index.html" , {  ...defconf["main_frame"]})  
            Menu.setApplicationMenu(mt_load(menu))  
            //! TODO : preload  default value    
            const  { cpus_core } = utils 
            ipcMain.on("init" ,  ( evt ,  init_proc  )  => {
                log("initializing  render process " ,  init_proc)  
                const initiate  =  { 
                    logpath_location      :  defconf["mtdt_pannel"]["logpath"] , 
                    available_cpus_core   :  cpus_core() -1 
                }
                log(cpus_core(true)) 
                if  (init_proc == 1 )  initiate["os_detail_info"] =  cpus_core(true)  

                evt.reply("initialization" ,  {  initiate ,  init_proc}  )   
    
            }) 
    action_event(mw)
     
    ipcMain.on("detach::term" ,  (evt , data ) => {
         tty= true  
         terminal("term.htm")  
         setTimeout ( () =>  {  
             tw.webContents.send("term::start" , data) 
         } ,500)  
         action_event(tw)  
     })

 
    
    //mw.once("ready-to-show" , ()=> { mw.show() } ) 
    } catch ( err )  {
        log(err) 
    }
}) 


const  terminal  =   fd  =>  {  
    const  { webPreferences  }  = defconf["main_frame"]  
    tw  = create_window (fd ,  { width:600 ,height: 400 ,  parent:mw , webPreferences  }) 
    if  (  process.argv.includes("-exp")  )  
        tw.setMenu(Menu.buildFromTemplate([])) 
    tw.on("closed" ,  evt =>{ 
        tty=false
        mw.webContents.send("attach::term", null)
        tw = null 
    }) 
    
    __BOUMRANG_EFFECT :  
    ipcMain.on("annoucement"  , (evt , data ) => {tw?.webContents.send("annoucement",data)})
    ipcMain.on("clear::term"  , (evt , data ) => {tw.webContents.send("clear::term",null)})
    ipcMain.on("system::info" , (evt , data ) => {tw.webContents.send('system::info',data)})
}

app.on("close" ,  app_closed  => { 
    mw =  null  //! free memory  
    app.quit()
}) 

process.on("exit" ,  code_status  =>  {
    mw.webContents.send("clean::localStorage" ,  null ) 
    log(`Exit with :${code_status}`)
})
