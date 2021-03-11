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

let mw  =  null  

const  mt_load = menu_template  =>  Menu.buildFromTemplate(menu_template)  

app.on("ready",  () =>  {
    
        mw  =  new BrowserWindow({...defconf["main_frame"]})
        //mw.setIcon(path.join(__dirname ,"/assets/icons/linux/icon.png"))
        //mw.loadURL(direct_link) //'https://teranga.pasteur.sn/reception/')
        mw.loadURL(url.format( { 
               pathname:  path.join(__dirname, "index.html") , 
               protocol: 'file:',
               slashes :  true

        } ))

        Menu.setApplicationMenu(mt_load(menu))  
        //! TODO : preload  default value  
        const  { cpus_core } = utils 
        ipcMain.on("init" ,  ( evt , data )  => {
            log("initializing  render process " ,  data)  
            const initiate  =  { 
                nbsim_limite          :  defconf["mtdt_pannel"]["limite_nbsims"], 
                logpath_location      :  defconf["mtdt_pannel"]["logpath"] , 
                available_cpus_core   :  cpus_core() -1 
            } 
            evt.reply("initialization" ,  initiate)   
        })
   
        ipcMain.on("run::summary" ,   (evt  ,  _data /*_data is object*/ )  =>  {
            const  { paths  , selected_files  }  =  _data 
            const  [pedfile,mapfile,phenfile]  = selected_files 

            utils.rsv_file(`/${paths}/${phenfile}` ,  '\t')
           .then(res => {
               // TODO  : send   event to read stream  ...  
               utils.Rlog(".logout"  ,  mw) 
               utils.std_ofstream(`Rscript ${summary_src} --pedfile /${paths}/${pedfile} --mapfile /${paths}/${mapfile} --phenfile /${paths}/${phenfile}` ,
                    exit_code => {
                    if  (exit_code == 0x00)  {
                        mw.webContents.send("end"  , exit_code) 
                        //TODO  : send   signal to  stop printing  ... 
                        mw.webContents.send("end" , exit_code)
                         
                        fs.readFile(".logout" , "utf8" ,  (e , d ) => {
                            if (e)  mw.webContents.send("log::fail" , e  )   
                            mw.webContents.send("term::logout"  , d )   
                        })
                        mw.webContents.send("load::phenotype"  ,  res-2)   
                    }else {
                        log("fail")  
                        fs.access(".logerr" , fs.constants["F_OK"] , error => {
                            if (error )  mw.webContents.send("logerr::notfound" , error)  
                            fs.readFile('.logerr' , "utf8" , (err , data) =>{
                                if(err) mw.webContents.send("log::broken" ,  error ) 
                                log(data)
                                mw.webContents.send ("term::logerr" , data) 
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
                    mw.webContents.send("end"  , exit_code) 
                    fs.readFile(".logout" , "utf8" , (e , d)  => {
                        if  (e)    mw.webContents.send("log::fail" , e  )  
                        log("output result" ,  d) 
                        //mw.webContents.send("run::analysis_result" ,  d  ) 
                        mw.webContents.send("term::logout" ,  d  ) 
                         
                    })
                }else {
                    log("error") 
                    fs.access(".logerr" , fs.constants["F_OK"] , error => {
                        if (error )  mw.webContents.send("logerr::notfound" , error)  
                        fs.readFile('.logerr' , "utf8" , (err , data) =>{
                            if(err) mw.webContents.send("log::broken" ,  error )  
                            mw.webContents.send ("term::logerr" , data) 
                        })
                    }) 
                }
            })
        })
     mw.once("ready-to-show" , ()=> { mw.show() } ) 
     
})  
app.on("close" ,  app_closed  => { 
    mw =  null  //! free memory  
    app.quit()
})  
process.on("exit" ,  code_status  =>  log(`Exit with :${code_status}`))
