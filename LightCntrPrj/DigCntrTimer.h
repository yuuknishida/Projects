#ifndef _DIGCNTRTIMER_H_
#define _DIGCNTRTIMER_H_

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
void DigCntrTimerSetup(void);
void SetDigCntrTimerRate(uint32_t update_rate);


#endif /* _DIGCNTRTIMER_H_ */

