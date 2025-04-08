#include <stdint.h>
#include <stdbool.h>
#include "inc/tm4c123gh6pm.h"
#include "inc/hw_memmap.h"
#include "driverlib/sysctl.h"
#include "driverlib/interrupt.h"
#include "driverlib/timer.h"
#include "utils/uartstdio.h"

#include "GlobalsAndDefines.h"
#include "UARTcomm.h"


//Timing for data output
void Timer0_Handler(void)
{

}

/***************************************************************
* TIMER2A is used for setting the data output rate to the UART *
***************************************************************/
void DigCntrTimerSetup(void)
{

}

//Function to set data output rate
void SetDigCntrTimerRate(uint32_t update_rate)
{

}
