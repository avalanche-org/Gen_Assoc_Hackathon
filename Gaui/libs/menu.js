#!/usr/bin/env node 

__Menu_Template__ :  

is_osx   = process.platform === "darwin" 
module
["exports"]  =   [ 
    { 
        label : "File",
        submenu   : [
            { 
                label : "Open new Folder" , 
                clik() {}  , 
            } , 
            is_osx? {role :"close" } : {role:"quit"} 
        ]
    },  
    {
        label : "Edit"  , 
        submenu  : [ 
            {role : "undo"} , 
            {role : "redo"} , 
            {type : "separator"} , 
            {role : "cut"}  ,
            {role : "copy"} , 
            {role : "paste"},
        ] 
    
    } ,
    {
        label :  "View" ,
        submenu : [  
            {role : "reload"} , 
            {role : "forceReload"} , 
            ...process.env?.["STAGE"] !== "production" ?  [
                {
                    label : "Toggle DevTools",  
                    accelerator : is_osx ? "Command+I" :"Ctrl+I" , 
                    click (it_ , wintarget )  {
                        wintarget?.toggleDevTools()
                    }
                },   
            ] : {}, 
            {type: "separator"} , 
            {role : "resetZoom"} , 
            {role : "zoomIn"} , 
            {role : "zoomOut"} ,
            {type : "separator"} , 
            {role : "togglefullscreen"}  
        ]
    },  

    {
        label   : "Window" ,  
        submenu : [ 
                {role : "minimize"} ,
                {role : "zoom"}, 
                {type : "separator"}, 
                {role : "window"} 
        ]

    }, 
    
    {
        role: "help" , 
        submenu : [
            {
                label  : "About",
                click() {} , 
            }
        ]
    }

]
