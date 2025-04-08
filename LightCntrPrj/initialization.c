

#include <stdint.h>
#include <stdbool.h>
#include "inc/tm4c123gh6pm.h"
#include "inc/hw_memmap.h"
#include "inc/hw_types.h"
#include "driverlib/pin_map.h"
#include "driverlib/sysctl.h"
#include "driverlib/interrupt.h"
#include "driverlib/gpio.h"

#include "ADC0.h"
#include "UARTSetup.h"

#include "DigCntrTimer.h"
#include "PWM.h"

#include "TMP102.h"



void initialization(void)
{

    /***********************
    * Bus Clock            *
    ***********************/
    //Set system clock to 80MHz
    SysCtlClockSet(SYSCTL_SYSDIV_2_5|SYSCTL_USE_PLL|SYSCTL_XTAL_16MHZ|SYSCTL_OSC_MAIN);



    /***********************
    * PortF                *
    ***********************/
    //Enable PORTF
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF);  //Enable clock on GPIO PORTF
    GPIOPinTypeGPIOOutput(GPIO_PORTF_BASE, GPIO_PIN_1|GPIO_PIN_2|GPIO_PIN_3);  //Sets pins 1,2,3 as outputs



    /******************************
    *     Project Peripherals     *
    ******************************/
    UART0Setup();
    ADC0Setup();

    DigCntrTimerSetup();
    PWMSetup();

    TMP102Setup();


    /*************************
    * Master Interrupt Enable*
    *************************/
    IntMasterEnable();
}



