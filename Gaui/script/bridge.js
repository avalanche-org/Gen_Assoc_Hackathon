//! this script make a bridge between  main  process and renderer process 
//! sending event through backend side  
//
//! TODO  : register  loaded data to  local storage   
//        + when user reload the application  
console.log ("loaded")
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
    markerset,term  , 
    run_summary,run_analysis]=[
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
        _.querySelector("#marker_set"), 
        _.querySelector("#term") , 
        _.querySelector("#run_summary"), 
        _.querySelector("#run_analysis") 
    ] 
 
run_analysis.disabled =  true  
term.innerText = "[Gen Assoc@ABC:]$"
term.setEditable =  false 
ipcRenderer.send("init",0x000) 

ipcRenderer.on("cpus::core" ,  (evt , data)  =>{
    for  ( let i of   range(data) ) { 
        const ncores_opt =  _.createElement("option") 
        ncores_opt.text=i 
        nbcores.add(ncores_opt) 
    }
})
const  get_ext  = args   =>  {
    let  _d  =  args.split(".")  
    return  _d[_d.length -1 ]  
}
const get_prefix_filename =  ( file , separator = ".")  => {
    let file_prefix       =  file.split(separator)  
    return  file_prefix.slice(0 ,-1)  
}

const  optsfeed  =  gdata   => {
    gdata.forEach(data => {
        let ext = get_ext(data)  
        switch  (ext) { 
            case  "ped" : 
                const  ped_opts =  _.createElement("option") 
                ped_opts.text   = data  
                ped_opts.value  = data  
                ped_opts.title  = data  
                ped.add(ped_opts)  
                break ; 
            case  "map" : 
                const  map_opts =  _.createElement("option") 
                map_opts.text   = data  
                map_opts.value  = data
                map_opts.title  = data
                map.add(map_opts)  
                break ; 
            case  "phen" : 
                const  phen_opts =  _.createElement("option") 
                phen_opts.text   = data  
                phen_opts.value  = data 
                phen_opts.title  = data 
                phen.add(phen_opts)   
                break;  
        }
     })

}
let 
[paths_collections  , files_collections] = [ [] , [] ]  


ipcRenderer.on("Browse::single"   , (evt ,  { main_root , files}) =>   { 
    paths_collections =  main_root  
    files_collections =  files 
    optsfeed(files)
}) 

ipcRenderer.on("Browse::multiple" , (evt , mbrowse_data )  =>{
    const request_files =  Object.keys(mbrowse_data)   
    for ( let  htm_elmt  of  [ ped  , map , phen ]  )  htm_elmt.innerHTML= ""    
    optsfeed(request_files)
})
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
sync_select_action(ped , map) /*< --*/;/*-->*/sync_select_action(map, ped)
sync_select_action(ped , phen)        ;       sync_select_action(map,phen) 


run_summary.addEventListener("click" , evt => {
    evt.preventDefault() 
    //TODO  : run   summary
    term.innerText =  "Processing  Summary ... please wait"
    run_analysis.disabled = true  
    const gobject =    { 
         paths  : paths_collections ??  null ,  
         selected_files: [ 
              ped.options[ped.selectedIndex].value , 
              map.options[map.selectedIndex].value , 
              phen.options[phen.selectedIndex].value  
         ]
    }

    ipcRenderer.send("run::summary",  gobject )  
})

ipcRenderer.on("load::phenotype" ,  (evt ,  incomming_data ) =>  {
    log(incomming_data)
     //!TODO  : CLEAN  PHENOTYPE BEFORE
    phenotype.innerHTML = ""  
    for  ( let phen_index  of range(incomming_data )) { 
        const phenotype_opts = _.createElement("option")  
        phenotype_opts.text      =  phen_index  
        phenotype_opts.value     =  phen_index
        phenotype.add(phenotype_opts)   
    }  
    
    //!TODO   : enable  run analysis  button    " by  default  the run  analysis  is disabled 
})

ipcRenderer.on("term::logout" , ( evt , data ) => {
    if  ( data  ) {
    term.innerText        = data   
    run_analysis.disabled = false 
    run_summary.disabled  = true
    }
})


run_analysis.addEventListener("click" ,  evt => { 

    //! GET   ALL   VALUE   TO ALL  SELEECT FIELD 
    const gobject  =  { 
        paths           :paths_collections ?? null ,
        selected_index  :[  
            ped.options[ped.selectedIndex].value , 
            map.options[map.selectedIndex].value , 
            phen.options[phen.selectedIndex].value , 
            phenotype.options[phenotype.selectedIndex].value , 
            nbsim.options[nbsim.selectedIndex].value , 
            nbcores.options[nbcores.selectedIndex].value  
        
        ]
    }
    
    ipcRenderer.send("run::analysis" ,  gobject )

})


