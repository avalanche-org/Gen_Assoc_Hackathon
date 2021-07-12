/**!  web Tcp  server  socket   
 *    for  synchronous exchange    
 *    ----
 *    author  :   Umar aka < jukoo >  @  github.com/jukoo  
 */ 

__kernel_file__          : { core  = require("./kernel")  }  
__kernel_file_props__    : { 
        nm    = core["@node_module"] ,
        cfg   = core["@config"]      ,
        xtra  = core["@extra"]       
} 

const  [
    { log }  = console                   , 
    {Server} = require("http")           ,
    {createReadStream} =nm["fs"]         , 
    xpress   = xtra["xpress"]            , 
    ios      = xtra["io_socket"].Server
] = process.argv.slice(0xa) 


__setup__  :  
xapp   = xpress()
server = Server(xapp) 
socket =  new ios(server)   //  binding  
gateways=4000 

xapp
.use(xpress.static(__dirname+"/assets")) 

const __wtcp__ =  {  

    wtcp_server  : () => {

        xapp
        ["get"] ("/" , ( rx , tx  )  =>    { 
            createReadStream(__dirname  + "/index.html").pipe(tx)  
        })
        ["use"]((rx , tx  , next )   =>  tx.redirect("/"))
        server 
        ["listen"](gateways , "0.0.0.0" ,log(`\x1b[1;32m * connected on  ${gateways}\x1b[0m`))
        ["on"]("error" , err         => {  

            switch (err.errno)   
            {
                case  -98  :  //!EADDRINUSE  
                    log (`\x1b[1;33m -*this gatewaye ${gateways} is already used by  \x1b[4m ${process.argv[1]} \x1b[0m`) 
                    process.exit(err.errno) 
                    
            }
        }) 

        socket.on("connection" , sock => {
            //! TODO :  GET FINGER PRINT  USER
            log("let 's rock n roll ") 
            
        })

    }
    
}

__wtcp__.wtcp_server() 
