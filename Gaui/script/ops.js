//!  author  :  Umar aka  jukoo   
Object.prototype["range"]  = v_   =>   { 
        let [ t , i ]  = [[] , 0] 
        if  (v_ <= 1  ||  v_ == undefined) return null  
        while ( i < v_ )  { 
            i++ 
            t.push(i) 
        }  
        return [...t]   
}

Object.prototype["createTag"] =  (htm_tag , txt , cb=false/* cb should be a  function*/   _=documen) => {
    const  new_elmt =  _.createElement(htm_tag)   
    if ( new_elmt.ELEMENT_NODE !=  Node.ElEMENT_NODE) throw new  Error("not allowed to create this tag")
    new_elmt.text =  txt  ||  ""   
    if  (cb) cb(new_elmt) 
    return  new_elmt  
}
