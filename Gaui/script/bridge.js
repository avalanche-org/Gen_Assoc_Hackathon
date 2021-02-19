//! this script make a bridge between  main  process and renderer process 
//! sending event through backend side  
//

const { ipcRenderer} = require("electron") ,
      {log}          = console  

const _ = document 
//!  mapping  DOM Element  
const  [
    ped , map , 
    phen, sm  ,
    mm  , yes ,
    no  , phenotype ,
    nbsim , nbcores ,
    markerset ]=[
        _.querySelector("#ped"),   
        _.querySelector("#map")  ,
        _.querySelector("#phen") , 
        _.querySelector("#single_marker") , 
        _.querySelector("#multi_marker") ,  
        _.querySelector("#yes"), 
        _.querySelector("#no"), 
        _.querySelector("#phenotype") , 
        _.querySelector("#nbsim") , 
        _.querySelector("#nbcores"),
        _.querySelector("#marker_set") 
    ] 
ipcRenderer.send("init",0) 

ipcRenderer.on("cpus::core" ,  (evt , data)  =>{
    for  ( let i of   range(data-1) ) { 
        const ncores_opt =  _.createElement("option") 
        ncores_opt.text=i 
        nbcores.add(ncores_opt) 
    }
   
})

ipcRenderer.on("Browse",  (evt ,browse_data)  => {
     browse_data.forEach(data => {
        let _d  = data.split(".") 
        let ext = _d[_d.length -1]  
        log(ext) 
        switch  (ext) { 
            case  "ped" : 
                const  ped_opts =  _.createElement("option") 
                ped_opts.text   = data  
                ped.add(ped_opts)  
                break ; 
            case  "map" : 
                const  map_opts =  _.createElement("option") 
                map_opts.text   = data  
                map.add(map_opts)  
                break ; 
            case  "phen" : 
                const  phen_opts =  _.createElement("option") 
                phen_opts.text   = data  
                phen.add(phen_opts)   
                break;  
        }
     })
})


