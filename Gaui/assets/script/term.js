const {ipcRenderer} =require("electron") ,
      {log}          = console            , 
      fs             = require("fs")      , 
      {execSync , exec}     = require("child_process"), 
      {fromCharCode }= String 


const term =  document.querySelector("#term")  
__init__  = ( ()=> { 
    term.innerText       =  ""
    term.focus() 
    term.setAttribute("readonly", true) 
    writeSpeed            =  0 
    term_display_speed    =  500   //  millisec
   
})()
/*
 * []  simulat  typing 
 * []  set allowed command  
 * */
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

ipcRenderer.on("term::start",  ( evt , data ) => { term.value = data})
let tigger  = false 
//* ipc  event  listener  -
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
ipcRenderer.on("log::broken"   , (evt , data) => {term.value = data })
ipcRenderer.on("annoucement"   , (evt , data) => {term.value = data })
ipcRenderer.on("clear::term"   , (evt , data) => {term.value = ""   }) 
ipcRenderer.on ("system::info" , (evt , data) => {term.value = "" ; term_write(data) }) 
ipcRenderer.on("term::logout"  , ( evt, data) => {
    term.focus()
    if  ( data  ) {
        term_write(data)
        follow_scrollbar()
    }
})

const skbmap =  {   
    "edition" : 0x5 , 
    "enter_or_return" : 0xD 
} , 
allowed_command  =   {
    "show" :  () => {}  , 
    "help" :  () => {
         let hint =  `\n
         show  File -> to show the content of loaded file \n  
         help print this help \n 
         clear to  clear the terminal \n
         history show history\n
         \n
        `
        term_write(hint) 
    }  , 
    "clear":  () =>  {
        term.value=""
    }, 
    "history" : () => { 
        if( history.length >  0 )  
        {
            let a = "" 
            let h_index = 0  
            for ( let previous_cmd  of history ) 
            {
                h_index++ 
                a +=  `\n${h_index} ${previous_cmd} \n`
            }
            term_write(a) 
        }       
        else term_write("\nno history found\n") 
    }

}

let buffer_register  =  []      ,
    history          =  []      ,
    edition_mode     =  -2   

term.addEventListener("keypress" ,   evt => {
    if  ( evt.keyCode  == skbmap.edition )   
    {
        edition_mode= ~edition_mode 
        switch ( edition_mode ) 
        {
            case  1 :
                notify("Terminal" , { body: "Edition mode on"} )
                term.removeAttribute("readonly") 
                break
            case  -2  : 
                notify("Terminal" , { body: "Edition mode off"} ) 
                term.setAttribute("readonly", true)  
                break  
        } 
    } 
    if  (!Object.values(skbmap).includes(evt.keyCode)) buffer_register.push(fromCharCode(evt.keyCode))
    
    if ( evt.keyCode  ==  skbmap.enter_or_return )  
    {
        let  constitued_cmd =  buffer_register.join("")
        history.push(constitued_cmd) 
        if  (!Object.keys(allowed_command).includes(constitued_cmd))
        {
            buffer_register =  []  
            term_write(`\nCommand  ${constitued_cmd} not found\n` )  
             
        }else 
            allowed_command[constitued_cmd]() 
        
        buffer_register =  []  
    }
})

