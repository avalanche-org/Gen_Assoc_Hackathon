#!/usr/bin/env node 
//author  : Umar aka jukoo  j_umar@outlook.com   <github.com/jukoo>

const   
    {readFile , createWriteStream , readdir , access ,  constants  , createReadStream}=  require("fs") , 
    os =  require("os") ,  
    {execSync ,exec , spawn}  = require("child_process"), 
    {fromCharCode}            = String , 
    {log}                     = console,  
    { fstdout , fstderr , fserror} =  require("./config")["io_fstream"]  
 
module
["exports"]  =  {
    //! TODO  : improve this function to manage correctly  csv or tsv  file ...  
    rsv_file :  (  file  , default_delimiter = "," )  => {
        return new Promise  ( (resolve , reject )  => {
            readFile(file ,  "utf8" , (e , file_data ) => {
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

                resolve(headers.length)  
            })  
        
        }) 
      },  
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
           readdir ( dir_root_location , (err ,  dir_contents)=> {
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
    },
    execmd  : (main_cmd  ,  ...options)=> {
        const  output_ =  spawn(main_cmd , options) 
        log(...options)
        console.log(`${main_cmd}` , ...options)
        return  new Promise( (resolve ,  reject)   => {
            output_.stdout.on("data"  ,  data      =>  { 
                log (data.toString()) 
                resolve(data.toString())
            }) 
            output_.stderr.on("data"  ,  e_data    => reject(e_data.toString()))
            output_.on("error"        ,  err       => reject(err.message))  
            output_.on("close"        ,  exit_code =>  console.log(`exited with ${exit_code}`)) 
        }) 
      }, 
    execmd_ :  command => {
       const  buffer  =  execSync(command)  
       return buffer.toString()  
    }, 
    
    std_ofstream   : (command ,  callback )=> {
        const   cmd    = exec(command)
        const stdout = createWriteStream(fstdout) 
        const stderr = createWriteStream(fstderr) 
        cmd.stdout.pipe(stdout)  
        cmd.stderr.pipe(stderr)   

        cmd.on("close" , exit_code =>  {
            callback(exit_code) 
            process.stdout.write(`exiting with code ${exit_code}`)
        })
    } ,  
    Rlog :  ( logfile ,  mw_ ) => {  // Rlog  aka   realtime readable log 
         access( logfile  , constants["F_OK"] , error => {   
             if  (error) log("Unable  to access file or permission denied!") 
             if  (!error) log("ok  streaming  out -> "  ,logfile)  
         })
        const  plug  =  createReadStream(logfile)
        plug.on("data"  , data  => {
             mw_?.webContents?.send("plug"  , data )  
        }) 
    }
    
}

//module.exports.std_ofstream("Rscript summary.R --pedfile sample.ped  --mapfile sample.map  --phenfile sample.phen")  
//console.log(module.exports.rsv_file('/home/juko/final.csv'))  
//module.exports.rsv_file("/home/juko/Desktop/Pasteur/Sandbox/H3BioNet/Gen_Assoc_Hackathon/test/sample.phen" ,  "\t")
//.then(res => console.log(res)) 
