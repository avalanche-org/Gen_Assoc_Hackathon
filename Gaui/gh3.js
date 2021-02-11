#!/usr/bin/env  node  
//author  :  Umar  aka jukoo 

__kernel__ : {  core  = require("./kernel") }  

const
{   log  }  = console , 
{   path , 
    fs   , 
    ps   ,
    url  , 
    _ejs_
} = core["@node_module"] , 

{defconf} = core["@config"]

const 
{ app , BrowserWindow } = _ejs_  

const  {  
    main_frame  
} = _start =  {
    
    ["tfile"]  : filepath => {  
       fs.access(filepath , fs.constants["F_OK"] ,  error => {if (error) process.exit()})
           return   {  
               ["pathname"]:  path.join(__dirname,filepath) , 
               ["protocol"]: 'file:',
               ["slashes "]:  true
           }  

    } , 
    ["main_frame"]  :  ()  => {    
        const  mw  =  new BrowserWindow({...defconf})
        const { tfile }  =  _start 
        //mw.loadURL(direct_link) //'https://teranga.pasteur.sn/reception/')
        mw.loadURL(url.format(tfile("template/mw_template.html")))
        
    }
} 

app.on("ready",  main_frame) 
process.on("exit" ,  code_status  =>  log(`Brutal exit :${code_status}`))
