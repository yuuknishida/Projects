
#ifndef _UARTCOMM_H_
#define _UARTCOMM_H_

/***********************
* Includes             *
***********************/
#include <stdint.h>
#include <stdbool.h>


/***********************
* Public Types         *
***********************/

/***********************
* Public Macros        *
***********************/


/***********************
* Public Defines       *
***********************/


/***********************
* Public Constants     *
***********************/


/***********************
* Public Variables     *
***********************/


/***********************
* Public Functions     *
***********************/
void GetUARTInputNumber(void);
void SendUARTDataOut(uint32_t value1, uint32_t value2, uint32_t value3);


#endif /* _UARTCOMM_H_ */

