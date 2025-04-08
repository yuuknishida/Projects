
#ifndef _GLOBALSANDDEFINES_H_
#define _GLOBALSANDDEFINES_H_

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

//PORTF LED pins
#define PF2  (*((volatile uint32_t *)0x40025010))
#define PF3  (*((volatile uint32_t *)0x40025020))
#define PF4  (*((volatile uint32_t *)0x40025040))

//Bus Clock
#define BUS_Clk 80000000  //This is set in initialization()

//Sample Rate in Hz
#define Sample_Rate 10

//PWM Divider
#define PWM_Divider 1  //also change in PWM setup

//PWM Clock
#define PWM_Clk BUS_Clk/PWM_Divider

//PWM Frequency in Hz
#define PWM_FREQUENCY 10000

//PWM Period in counts
#define PWM_Period PWM_Clk/PWM_FREQUENCY



/***********************
* Public Constants     *
***********************/


/***********************
* Public Variables     *
***********************/

//Flag for user inputting a number.
//False no new input.
//True new number is being inputted.
extern bool g_InputFlag;

//Number received from keyboard
extern uint32_t g_UARTInputNumber;



/***********************
* Public Functions     *
***********************/


#endif /* _GLOBALSANDDEFINES_H_ */

