#!/usr/bin/env node 


const  [ 
    fs =  require("fs")  
]  = process.argv.splice(0b11) 


module
["exports"]  =  {
    // TODO  :  read  file  and extrate data ... 
    ["ascii_extraction"]  :  (  file  , default_delimiter = "," )   => {
        fs.readFile(file ,  "utf8" , (e , d ) => {
            if (e)  throw e   
            return  d.split(default_delimiter) 
        })  
    } 
    //! TODO :  collect how many cpu  are available   
    //! TODO :  check all requierment inside the directory file  [ ped map phen 
    //! TODO :  check file extsion ped map phen  ->  menu.js
} 

