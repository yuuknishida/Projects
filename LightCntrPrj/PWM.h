#ifndef _PWM_H_
#define _PWM_H_

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
void PWMSetup(void);
void SetPWMDutyCycle(float DutyCyclePercent);


#endif /* _PWM_H_ */
