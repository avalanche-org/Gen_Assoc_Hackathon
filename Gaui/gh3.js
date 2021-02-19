#!/usr/bin/env  node  

//author  : Umar aka jukoo  j_umar@outlook.com   <github.com/jukoo> 
__stage__  : {  process.env["STAGE"] = "development"          }  
__kernel__ : {  core                 = require("./kernel")    } 
__static__ : {  htm_static_path      = "template/index.html"  } 
const
{   log  }  = console , 
{   path , 
    fs   , 
    ps   ,
    url  , 
    _ejs_
}         = core["@node_module"] , 
{defconf} = core["@config"], 
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
        mw  =  new BrowserWindow({...defconf})
        const { tfile  , mt_load }  =  _start 
        //mw.loadURL(direct_link) //'https://teranga.pasteur.sn/reception/')
        mw.loadURL(url.format(tfile(htm_static_path)))
        Menu.setApplicationMenu(mt_load(menu))  
        //! TODO : preload  default value  
        const  { cpus_core } = utils 
        ipcMain.on("init" ,  ( evt , data )  => {
            log(data) 
            evt.reply("cpus::core" ,  cpus_core())   
        })
    
        //ipcMain.on("wc" ,  (e,d) => log(e , "=" , d) ) 
    }
    
}

app.on("ready",  main_frame)  
app.on("close" ,  app_closed  => { 
    mw =  null  //! free memory  
    app.quit()
})  
process.on("exit" ,  code_status  =>  log(`Exit with :${code_status}`))
