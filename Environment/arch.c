/** 
 * \  help to know the architecture of the machine ! 
 */
#include <stdio.h> 
#include <stdlib.h> 

#define  BASE_BITS   0B1000 
#define  ARCH       ( BASE_BITS * sizeof(void*) ) 

int 
main () {
    fprintf(stdout ,  "you system architecture is %d bits %c"  , ARCH , 0xa)  ; 
    return EXIT_SUCCESS ; 
}
