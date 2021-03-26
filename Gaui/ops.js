//!  author  :  Umar aka  jukoo   < github.com/Jukoo  ||  j_umar@outlook.fr  
//
//
const  { random, floor } = Math 

function AssertionError ( message ) {   this.message =  message  }  
AssertionError.prototyp =  Error.prototype 

Object.prototype["range"]  = v_   =>   { 
        let [ t , i ]  = [[] , 0] 
        if  (v_ < 1  ||  v_ == undefined) return null  
        if  (v_ == 1 )  return  [v_] 
        while ( i < v_ )  { 
            i++ 
            t.push(i) 
        }  
        return [...t]   

} 
const notify                      =  ( title , {...props } ) =>  new  Notification ( title , { ...props})  
const check_network_connectivity  =  ()                      =>  window.navigator.onLine 
const rand                        =  ( min , max=0 )         =>  max? random() * (max-min) + min : floor(random() * floor(min)) // however when one arg was set it's defined as max  
const display_speed               =  hertz_frequency         =>  (1000/hertz_frequency) * 1 
