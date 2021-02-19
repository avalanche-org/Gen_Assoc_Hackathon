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
                ped_opts.value  = data  
                ped.add(ped_opts)  
                break ; 
            case  "map" : 
                const  map_opts =  _.createElement("option") 
                map_opts.text   = data  
                map_opts.value  = data  
                map.add(map_opts)  
                break ; 
            case  "phen" : 
                const  phen_opts =  _.createElement("option") 
                phen_opts.text   = data  
                phen_opts.value  = data  
                phen.add(phen_opts)   
                break;  
        }
     })
})
const get_prefix_filename =  ( file , separator = ".")  => {
    let  file_prefix  = file.split(separator)  
    return  file_prefix.slice(0 ,-1)  
}
//! sync select action  between  ped and maps
const sync_select_action =  (s_elmt1 , s_elmt2) => {
    s_elmt1.addEventListener("change" , evt =>{ 
        const  file_name      = get_prefix_filename(evt.target.value)  
        let    map_elmts_opts =  [...s_elmt2.options]  
        map_elmts_opts        =  map_elmts_opts.map(opts =>  opts.value)  
        const  match          = map_elmts_opts.filter( element => {
            let f_prefix =  get_prefix_filename(element)  
            if (file_name[0]  == f_prefix[0] )  return  element  
        })
        if (match) {
            let data_index  = map_elmts_opts.indexOf(match[0])  
            s_elmt2.options[data_index].selected= true  
        } 
    })
}
sync_select_action(ped , map);sync_select_action(map, ped)  
