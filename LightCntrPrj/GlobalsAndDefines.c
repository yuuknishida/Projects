
/***********************
* Includes             *
***********************/
#include <stdint.h>
#include <stdbool.h>


/***********************
* Type Definitions     *
***********************/

/***********************
* Macros               *
***********************/

/***********************
* Defines              *
***********************/

/***********************
* Constants            *
***********************/

/***********************
* Calibrations         *
***********************/

/***********************
* Global Variables     *
***********************/

//Flag for user inputting a number.
//False if  no new input.
//True if new number is in the process of being inputted.
bool g_InputFlag = false;

//Number received from keyboard
uint32_t g_UARTInputNumber = 750;

/***********************
* File Scope Variables *
***********************/

/***********************
* Function Prototypes  *
***********************/


/***********************
* Function Definitions *
***********************/
