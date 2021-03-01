#!/usr/bin/env node 
//author  : Umar ak jukoo  j_umar@outlook.com   <github.com/jukoo> const {dialog  ,  ipcMain } = require("electron") ,

const { dialog ,  ipcMain } =  require("electron") , 
    fs                      = require("fs") ,
    utils                   = require("./utils")


__Menu_Template__ :  

is_osx           = process.platform === "darwin" 
slash_orientaion = process.platform  == "win32" ? "\\" : "/"

module
["exports"]  =   [  
    { 
        label : "File",
        submenu   : [
            { 
                label : "Open new Folder" ,  
                accelerator : is_osx  ?  "Command+O"  : "Ctrl+O" , 
                click(it_ ,  wintarget) {
                    dialog.showOpenDialog( wintarget  ,  { 
                        title  : "open dir" ,
                        filters : [ 
                            {name : "All Files" , extensions:["ped" , "map","phen"] }
                        ],
                        buttonLabel :  "Choose" , 
                        properties  : [  
                            "openFile",  
                            "openDirectiory", 
                            "multiSelections" 
                        ] 
                    })
                    .then( res =>{  
                        //res?.canceled
                        const  actions  =  res?.filePaths
                        //! when user choose one file  it related to path  
                        if  ( actions.length == 1 )  {
                            let  abs_path =  actions[0].split(slash_orientaion)
                            //! TODO : don't forget to use ipc rendering  to send path  
  
                            abs_path = abs_path.slice(1 , -1).join(slash_orientaion)
                            //! TODO :  load  all required file  ped map phen 
                            console.log("-> " , abs_path) 
                            const { scan_directory} = utils 
                            scan_directory(`${slash_orientaion}${abs_path}` , "ped","map","phen")
                            .then(res => {
                                wintarget.webContents.send("Browse::single",  { 
                                    main_root : abs_path  , 
                                    files     :  res  
                                }) 
                            })
                            .catch(err => console.log(err)) 
                        }
                        //!  when user  decide to  request multiple choice  .... 
                        if  (actions.length > 1  ) {
                            let  path_location     = []   
                            let files_collections  = [...actions.map(file  =>   { 
                                let path_explode   = file.split(slash_orientaion)
                                let root_path      = path_explode.slice(1 , -1).join(slash_orientaion)
                                path_location.push(root_path)  
                                return path_explode[path_explode.length -1 ] 
                            
                            })] 
                            const tree_signature  = {} 
                            files_collections.forEach((file, index) =>{ tree_signature[file] = path_location[index]})
                            console.log(tree_signature) //console.log(path_location) console.log(files_collections)  
                            //!  send  the related data  to renderer process 
                            wintarget.webContents.send("Browse::multiple" ,  tree_signature) 

                        }
                        
                    })
                    .catch  (err => console.log(err))  
                }  
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

if ( is_osx) module.exports.unshift({})
if (process.env["STAGE"] != "production") {
    module.exports[2].submenu.push({
        label : "Toggle DevTools",  
        accelerator : is_osx ? "Command+I" :"Ctrl+I" , 
        click (it_ , wintarget )  {
            wintarget?.toggleDevTools()
        }
    })
}
