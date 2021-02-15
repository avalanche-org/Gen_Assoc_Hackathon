#!/usr/bin/env  node  
//author  :  Umar  aka jukoo 
__stage__  : { process.env["STAGE"] = "development" }  
__kernel__ : {  core  = require("./kernel") }  

const
{   log  }  = console , 
{   path , 
    fs   , 
    ps   ,
    url  , 
    _ejs_
}         = core["@node_module"] , 
{defconf} = core["@config"], 
{menu}    = core["@libs"] 

const 
{ app , BrowserWindow  , Menu , dialog } = _ejs_  

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
        const  mw  =  new BrowserWindow({...defconf})
        const { tfile  , mt_load }  =  _start 
        //mw.loadURL(direct_link) //'https://teranga.pasteur.sn/reception/')
        mw.loadURL(url.format(tfile("template/mw_template.html")))
        Menu.setApplicationMenu(mt_load(menu))  
    }
}

app.on("ready",  main_frame)  
app.on("close" ,  app_closed  => app.quit())  
process.on("exit" ,  code_status  =>  log(`Exit with :${code_status}`))