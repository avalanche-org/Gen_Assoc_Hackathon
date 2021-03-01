#!/usr/bin/env  node  

//author  : Umar aka jukoo  j_umar@outlook.com   <github.com/jukoo> 
__stage__  : {  process.env["STAGE"] = "development"          }  
//__stage__  : {  process.env["STAGE"] = "production"          }  
__kernel__ : {  core                 = require("./kernel")    } 
__static__ : {  htm_static_path      = "template/proposal.html"  }
//NOTE:  the summary  should be  present in your system path ... 
const
{   log  }  = console , 
{   path , 
    fs   , 
    ps   ,
    url  , 
    _ejs_
}         = core["@node_module"] , 
{defconf} = core["@config"],
{summary_src ,  run_analysis } = defconf["mtdt_pannel"], 
{menu ,  utils}    = core["@libs"] 

const 
{ app , BrowserWindow  , Menu , dialog , ipcMain } = _ejs_  

let mw  =  null  
const  {  
    main_frame , 
    ctrl 
} = _start =  {  
    ["ctrl"]  : {
        ["file?"] : file  => {
             return new Promise((resolve ,reject) => {
                 fs.access(file , fs.constants["F_OK"]  , error =>  { 
                     error? reject(false) : resolve(true)  
                 }) 
             }) 
        }
    },
    ["tfile"]  : filepath => {
        ctrl["file?"](filepath)
        .catch(error => process.exit()) 
        return {  
               ["pathname"]:  path.join(__dirname,filepath) , 
               ["protocol"]: 'file:',
               ["slashes "]:  true
           } 
    } ,
    ["mt_load"] :   menu_template  =>  Menu.buildFromTemplate(menu_template)  , 
    
    ["box_dialog"] :  (options ,  with_check_Box =  false)  => { 
       const  defopts =  {  
           type          : options?.type     || "error" , 
           buttons       : options?.buttons  || ["cancel", "ok"] ,    
           default       : 2 , 
           title         : options?.title    || "Error", 
           message       : options?.message  || "An Error was occured",
           detail        : options?.detail   || "Error Exception" 
       }  
       if  (with_check_Box)  { 
           defopts["checkboxLabel"]   = options?.checkboxLabel   || "" 
           defopts["checkboxChecked"] = options?.checkboxChecked || with_check_Box  
           dialog.showMessageBox(null ,  defopts ,    ( res ,  cb )  => {
               log(res)  
               log(cb) 
           })
       }else  {
           dialog.showMessageBox(null ,  defopts)
       }
       
    },
    ["main_frame"]  :  ()  => {    
        mw  =  new BrowserWindow({...defconf["main_frame"]})
        mw.setIcon(path.join(__dirname ,"/assets/icons/linux/icon.png"))
        const { tfile  , mt_load }  =  _start 
        //mw.loadURL(direct_link) //'https://teranga.pasteur.sn/reception/')
        mw.loadURL(url.format(tfile(htm_static_path)))
        Menu.setApplicationMenu(mt_load(menu))  
        //! TODO : preload  default value  
        const  { cpus_core } = utils 
        ipcMain.on("init" ,  ( evt , data )  => {
            log("initializing  render process " ,  data)  
            const initiate  =  { 
                nbsim_limite          :  defconf["mtdt_pannel"]["limite_nbsims"], 
                available_cpus_core   :  cpus_core() -1
            } 
            evt.reply("cpus::core" ,  initiate)   
        })
   
        ipcMain.on("run::summary" ,   (evt  ,  _data /*_data is object*/ )  =>  {
            const  { paths  , selected_files  }  =  _data 
            const  [pedfile,mapfile,phenfile]  = selected_files 
            //! TODO :  Build respective complete path  for  ped map phen ...  
            //!      :+ each file should have   own path   

            utils.rsv_file(`/${paths}/${phenfile}` ,  '\t')
           .then(res => {
               utils.std_ofstream(`Rscript ${summary_src} --pedfile /${paths}/${pedfile} --mapfile /${paths}/${mapfile} --phenfile /${paths}/${phenfile}` ,
                    exit_code => {
                    if  (exit_code == 0x00)  { 
                        fs.readFile(".logout" , "utf8" ,  (e , d ) => {
                            /*sending data  to renderer  process */
                            if (e)  mw.webContents.send("log::fail" , e  )   
                            mw.webContents.send("term::logout"  , d )   
                        })
                        mw.webContents.send("load::phenotype"  ,  res-2)   
                    }else { 
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
        })

        ipcMain.on("run::analysis" , (evt , data) => {
            const { paths  , selected_index  }  = data    
            const {  mm    , sm , ped , map , phen , phenotype ,  nbsim , nbcores , markerset }  = selected_index  
            let cmdstr = null 
            if (mm && markerset!= null && markerset != '')  {  
                cmdstr =`Rscript ${run_analysis} --pedfile /${paths}/${ped} --mapfile /${paths}/${map} --phenfile /${paths}/${phen} --phen ${phenotype} --nbsim ${nbsim} --nbcores ${nbcores} --markerset ${markerset}` 
            } 
            if  (sm)  {  
                cmdstr =`Rscript ${run_analysis} --pedfile /${paths}/${ped} --mapfile /${paths}/${map} --phenfile /${paths}/${phen} --phen ${phenotype} --nbsim ${nbsim} --nbcores ${nbcores}`
            }

            utils.std_ofstream(cmdstr ,  exit_code  => {
                if(exit_code ==0x00) {
                    log("success") 
                    fs.readFile(".logout" , "utf8" , (e , d)  => {
                        if  (e)    mw.webContents.send("log::fail" , e  )  
                        log("output result" ,  d)  
                        mw.webContents.send("run::analysis_result" ,  d  ) 
                    })
                }else {
                    log (cmdstr) 
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
    }   
}

app.on("ready",  main_frame)  
app.on("close" ,  app_closed  => { 
    mw =  null  //! free memory  
    app.quit()
})  
process.on("exit" ,  code_status  =>  log(`Exit with :${code_status}`))
