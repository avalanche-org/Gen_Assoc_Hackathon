#!/usr/bin/nodejs  
//! author : umar  <jukoo>  << github.com/jukoo >> 

__KERNEL__    :  { core   = require("./kernel") }
__node_mod__  :  {fstream = core["@node_module"]["fs"] }    
__extra__     :  {xapp    = core["@extra"]["xpress"]() }
__config__    :  {dconf = core["@config"]["defconf"] }   

const  { stdout }                  = process , 
       {readFile , readFileSync  } = fstream , 
       { homepage  , index_ , gateways , host , defencode , Etag }  = dconf["web_server"] 

Object.prototype["write"] =  (args , end="\n") =>{stdout.write(args+end) } 

__configure__ : 
xapp 
.set("views" ,"./views")
.set("view  engine" , "ejs") 
.use(core["@extra"]["xpress"].static("assets")) 

//! NOTE:
//to avoid the  navigator cache   304  status code 
if  (!Etag) xapp.disable("etag")
/// END NOTE 

const  __global_start = {
     static_server  :  () => {
         xapp
         ["get"](index_  , ( request  , response  ) => {
             response.setHeader("Content-Type" , "text/html")
             const baseroot  = __dirname +  homepage  
             response.render(baseroot) 
         }) 
         ["use"]( (resquest , response  , next ) =>  response.redirect(index_) ) 
         ["listen"](gateways , host , write(`connected  to  ${gateways}`))
         ["on"]("error" , err => {
             // handeling server error  
             switch(err.errno) 
             {
                 case  -98 :   //  EADDRINUSE  
                     write("Fail : the  port is busy  try  another one ") 
                     process.exit(err.errno)  
                     break
                 //~! implement your own  
             }
         })  
     }
}

__global_start 
["static_server"]() 
