//! this script make a bridge between  main  process and renderer process 
//! sending event through backend side  
//
//! TODO  : register  loaded data to  local storage   
//        + when user reload the application  
const { ipcRenderer} =require("electron") ,
      {log}          = console            , 
      fs             = require("fs")      , 
      {execSync , exec}     = require("child_process") 

const _ = document 
//!  mapping  DOM Element  
const  [
    ped , map , 
    phen, sm  ,
    mm  , yes ,
    no  , phenotype ,
    nbsim , nbcores ,
    markerset,term  , 
    run_summary,run_analysis
]=[
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
let terminal ,  writeSpeed  
__init__  = ( ()=> { 
    run_analysis.disabled =  true  
    term.innerText        =  "> "
    term.setEditable      =  false
    nbsim.disabled        = true
    markerset.disabled    =  true 
    ipcRenderer.send("init",0x000)
    writeSpeed            =  1  
    term_display_speed    =  500   //  millisec 
})()    
/*
const execute   =  (cmdstr  , tag )  => { 
     exec ( cmdstr  ,  ( error , stdout ,stderr ) => {
         log(stdout) 
         tag.value = stdout
     })
}*/ 

const  follow_scrollbar  =  () => {term.scrollTop =term.scrollHeight}
const  term_write  =  incomming_data => {
    let  c  =  0 ;    
    (function write_simulation () {
        follow_scrollbar()  
        if ( c <  incomming_data.length) { 
            let termbuffer = `${incomming_data.charAt(c)}`  
            if ( c != incomming_data.length -1) 
                termbuffer =`${termbuffer}` 
            term.value +=termbuffer 
            c++ 
            setTimeout(write_simulation , writeSpeed)  
        }else  
            clearTimeout(write_simulation) 
    })()
}

//!TODO  :  SEND ALL  CONFIG REQUIREMENT TO  PROCESS RENDERING ... 
//          ->  cpus core avlailable  
//          ->  where the  log file  is supposed to be  
 
let  logfile  =  null  
ipcRenderer.on("initialization" ,  (evt , data)  =>{
    const  {  nbsim_limite ,  logpath_location,  available_cpus_core } = data  

    logfile  = logpath_location
    for  ( let i of   range(available_cpus_core) ) { 
        const ncores_opt =  _.createElement("option") 
        ncores_opt.text=i 
        nbcores.add(ncores_opt) 
    }
    
    for ( let i of   range(nbsim_limite) ) {
        const nbsim_opt =  _.createElement("option") 
        nbsim_opt.text=i 
        nbsim.add(nbsim_opt) 
    }


})

log(logfile) 
const  get_ext  = args   =>  {
    let  _d  =  args.split(".")  
    return  _d[_d.length -1 ]  
}
const get_prefix_filename =  ( file , separator = ".")  => {
    let file_prefix       =  file.split(separator)  
    return  file_prefix.slice(0 ,-1)  
}

const  is_satisfied  =  needs   => { 
    for  ( need of needs )  
         return !(( need == null ||  need  == ""))   

    return true 
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

ipcRenderer.on("plug" ,  (evt , data ) => {
     log(data) 
})
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
            try  {  
                s_elmt2.options[data_index].selected= true  
            }catch ( no_sync_error )  { /*shuuuttt !!!!*/}
        } 
    })
} 
//!  this section  make a synchronisation  between ped map and  phen file  
sync_select_action(ped , map) /*<--*/;/*-->*/sync_select_action(map, ped)  
sync_select_action(ped , phen)/*<--*/;/*-->*/sync_select_action(map,phen) 
//!--end sync
//
let  p  = 0

const  plugonlog =   () => {   //TODO : do not forget to make the path as argument  ..
    const  cl   = setInterval( function ()  {
        const  plug  =  fs.createReadStream(logfile , encoding="utf8", start=p) 
        plug.on("data"  , data  => {
        if ( data.length != p ) {  
            //follow_scrollbar()
            term.value = data  
            p+=  data.length
        }
    }) 
        ipcRenderer.on("end"  , (evt ,data ) => {
            log("end " ,data ) 
            clearInterval(cl) 
        })
    } , term_display_speed ) 
}

let ped_  = null , 
    map_  = null ,
    phen_ = null   

let summary_already_run =  false 
run_summary.addEventListener("click" , evt => {
    evt.preventDefault()
    term.focus()
    let  annoucement  = "> Processing Summary  ... please wait\n"
    //plugonlog() 
    //setInterval(plugonlog , term_display_speed)    
    
    run_analysis.disabled = true 
    run_summary.disabled  = false   
    const  {
        paths  , 
        selected_files
    }=  gobject ={ 
         paths  : paths_collections ??  null ,  
         selected_files: [ 
              ped.options[ped.selectedIndex]?.value  ??  null ,   
              map.options[map.selectedIndex]?.value  ?? null , 
              phen.options[phen.selectedIndex]?.value ?? null  
         ]
    }
 
    let  done   = is_satisfied (selected_files)  
    if  (!done)  {
        annoucement = "> Missing " 
        run_summary.disabled = false   
    }
    term.value =  ""   //  clean output before 
    term_write(annoucement) 
    if (done) {
        [ped_  , map_ , phen_ ]  =  selected_files 
        summary_already_run = true  
        ipcRenderer.send("run::summary",  gobject ) 
    } 
})
mm.addEventListener("change" , evt => {
    if (evt.target.checked) { 
        markerset.disabled = false 
        nbsim.disabled     = false 
    }
})
sm.addEventListener("change" , evt => {
    if(evt.target.checked) { 
        markerset.disabled = true
        nbsim.disabled     = true 
    } 
})
ipcRenderer.on("load::phenotype" ,  (evt ,  incomming_data ) =>  {
    phenotype.innerHTML = ""  
    for  ( let phen_index  of range(incomming_data )) { 
        const phenotype_opts = _.createElement("option")  
        phenotype_opts.text      =  phen_index  
        phenotype_opts.value     =  phen_index
        phenotype.add(phenotype_opts)   
    }  
})

//! TODO  :  make realtime reading  stdout stream  
ipcRenderer.on("term::logout" , ( evt , data ) => {
    term.focus() 
    if  ( data  ) { 
        //term_write(data) 
        term.value = data
        //run_summary.disabled  =  // summary_already_run
        run_analysis.disabled = !summary_already_run 
    }
})
//! TODO :  [ optional]  style  output error  with red or yellow color  ... 
ipcRenderer.on("log::fail"        , (evt , data)  => {
    term.value = data 
    run_summary.disabled=false  
}) 
ipcRenderer.on("logerr::notfound" , (evt , data)  => {
    term.value = data 
    run_summary.disabled=false 
}) 
ipcRenderer.on("term::logerr"     , (evt , data)  => {
    term.value = data 
    run_summary.disabled=false 
})  
ipcRenderer.on("log::broken"      , (evt , data)  => {
    term.value = data  
    run_summary.disabled = false  
}) 
run_analysis.addEventListener("click" ,  evt => { 
    evt.preventDefault()
    term.focus()
    term_write("> Running Analysis")

    //setInterval(plugonlog , term_display_speed)    
    const  { 
        selected_index
         }  = gobject  =  { 
        paths           :paths_collections ?? null ,
        selected_index  :  { 
            ped        : ped_  ,   
            map        : map_  ,   
            phen       : phen_ ,   
            phenotype_ : phenotype.options[phenotype.selectedIndex].value ?? null  , 
            nbsim_     : nbsim.options[nbsim.selectedIndex].value         ?? null  , 
            nbcores_   : nbcores.options[nbcores.selectedIndex].value     ?? null  ,
            mm         : mm.checked, 
            sm         : sm.checked, 
            markerset  : mm.checked ? markerset.value : null 
        }  
    }
    
    const  {phenotype_, nbsim_, nbcores_}  = selected_index  
    const  require_needed   = [ phenotype_ ,  nbsim_ , nbcores_ ]  
    let  not_statified  = false  
    let  done  =  is_satisfied(require_needed) 
    log(gobject) 
    if   ( !done )  term_write ("> Run analysis  need to be satisfied" )   
    else  {  
        run_analysis.disabled =  true
        ipcRenderer.send("run::analysis" ,  gobject )
    }
})

/*
ipcRenderer.on("run::analysis_result" ,  (evt , data ) => { 
    term_write(data)   
})
*/

/*ipcRenderer.on("data::available"  ,  (evt , data) => {
    term_write(data)  
})*/

