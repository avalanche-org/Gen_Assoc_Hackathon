const {ipcRenderer} =require("electron") ,
      {log}          = console            , 
      fs             = require("fs")      , 
      {execSync , exec}     = require("child_process")

const term =  document.querySelector("#term")  

log(ipcRenderer) 
__init__  = ( ()=> { 
    term.innerText        =  "▮ "
    term.setEditable      =  false
    writeSpeed            =  0 
    term_display_speed    =  500   //  millisec
   
})()    
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
            setTimeout(write_simulation ,0)  
        }else  
            clearTimeout(write_simulation) 
    })()
}
let tigger  = false 
ipcRenderer.on("log::fail"        , (evt , data)  => {
    term.value = data 
    term.style.color ="red"
    bar_progress.style.backgroundColor = "firebrick"
}) 
ipcRenderer.on("logerr::notfound" , (evt , data)  => {
    term.value = data 
    term.style.color ="red"
}) 
ipcRenderer.on("term::logerr"     , (evt , data)  => {
    term.value = data 
    run_summary.disabled=false 
    term.style.color   ="red"
})  
ipcRenderer.on("log::broken"      , (evt , data)  => {
    term.value = data  
}) 


ipcRenderer.on("term::logout" , ( evt , data ) => {
    term.focus()
    if  ( data  ) {
        term_write(data)
        follow_scrollbar()
    }
})

