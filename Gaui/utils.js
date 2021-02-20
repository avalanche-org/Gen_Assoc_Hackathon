#!/usr/bin/env node 
//author  : Umar aka jukoo  j_umar@outlook.com   <github.com/jukoo> 

const    
    fs =  require("fs") , 
    os =  require("os") ,  
    {execSync ,exec , spawn}  = require("child_process"), 
    {fromCharCode}            = String 

module
["exports"]  =  {
    //! TODO  : improve this function to manage correctly  csv or tsv  file ...  
    rsv_file :  (  file  , default_delimiter = "," )  => {
        return new Promise  ( (resolve , reject )  => {
            fs.readFile(file ,  "utf8" , (e , file_data ) => {
                if (e) reject(e.code)
                const headers = []  
                const endcc   =  fromCharCode(0xa)   
                for ( head  of  file_data.split(default_delimiter))  {
                    if (head.includes(endcc))  {
                        let last_head =  head.split(endcc)[0] 
                        headers.push(last_head) 
                        break 
                    }
                    headers.push(head)
                }

            console.log(headers)  
            resolve(headers.length)  
        })  
      
        
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
   
    execmd  : (main_cmd  ,  ...options)=> {
        const  output_ =  spawn(main_cmd , options)   
        return  new Promise( (resolve ,  reject)   => {
            output_.stdout.on("data"  ,  data      => resolve(data.toString())) 
            output_.stderr.on("data"  ,  e_data    => reject(e_data.toString()))
            output_.on("error"        ,  err       => reject(err.message))  
            output_.on("close"        ,  exit_code =>  console.log(`exited with ${exit_code}`)) 
        }) 
      }, 
   execmd_ :  command => {
       const  buffer  =  execSync(command)  
       return buffer.toString()  
   }
}
__TEST_MODULE__:  

//console.log(module.exports.execmd_("ls -la")) 
module.exports.execmd("ls" ,"-la").then(res  => console.log(res))
console.log(module.exports.rsv_file('/home/juko/final.csv'))  
module.exports.rsv_file("/home/juko/Desktop/Pasteur/Sandbox/H3BioNet/Gen_Assoc_Hackathon/test/sample.phen" ,  "\t")
.then(res => console.log(res)) 
//console.log(module.exports.cpus_core(true)) 
//module.exports.scan_directory( "/home/juko/Desktop/Pasteur/Sandbox/Gen_Assoc/test","ped","map", "phen") 
//.then ( res => console.log(res)) 
