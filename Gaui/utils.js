#!/usr/bin/env node 
//author  : Umar aka jukoo  j_umar@outlook.com   <github.com/jukoo> 

const    
    fs =  require("fs") , 
    os =  require("os")  

module
["exports"]  =  {
    // TODO  :  read  file  and extrate data ... 
    rsv_file :  (  file  , default_delimiter = "," )   => {  // rsv_file  aka  read separed value file like csv  , tsv  ...
        fs.readFile(file ,  "utf8" , (e , d ) => {
            if (e)  throw e   
            return  d.split(default_delimiter) 
        })  
    },  
    //! TODO  [x] :  collect how many cpu  are available   
    cpus_core  : (with_detail_object = false)   =>  {  
        if  (with_detail_object) {  
          return   { 
              core_cpus_available  : os.cpus().length , 
              core_cpus_detail     : os.cpus()
          }
        }
       return  os.cpus().length 
    },   
    //! TODO :  check all requierment inside the directory file  [ ped map phen] 
    scan_directory  : (  dir_root_location , ...filter_extension  )  =>  {
       return   new Promise ( ( resolve , reject ) => {
           fs.readdir ( dir_root_location , (err ,  dir_contents)=> {
               if  (err)  reject(err)    
               const files =  []  
               if  (filter_extension  &&  dir_contents) {
                   dir_contents.forEach( file  => {
                       let spread_filename  = file.split(".") 
                       let file_extention   = spread_filename[spread_filename.length -1 ]
                       if  (filter_extension.includes(file_extention) ) files.push(file)
                   }) 
                    
               }
               resolve(files.length ?  files : dir_contents) 
           })
       
       })
    } ,
   
    //!  TODO  :  execute shell statement  ...   
    execute_cmd  : () => {} 
    //! TODO :  check file extsion ped map phen  ->  menu.js
}

//console.log(module.exports.cpus_core(true)) 
//module.exports.scan_directory( "/home/juko/Desktop/Pasteur/Sandbox/Gen_Assoc/test","ped","map", "phen") 
//.then ( res => console.log(res)) 
