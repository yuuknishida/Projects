#include <stdint.h>
#include <stdbool.h>
#include "inc/hw_memmap.h"
#include "inc/hw_types.h"
#include "driverlib/sysctl.h"
#include "driverlib/gpio.h"
#include "driverlib/debug.h"
#include "driverlib/pwm.h"
#include "driverlib/pin_map.h"
#include "inc/hw_gpio.h"

#include "GlobalsAndDefines.h"



/************************************************
* PWM1 GEN1 is used to control LED brightness   *
************************************************/
void PWMSetup(void)
{
    uint32_t ui32PWMClock, ui32Load;
    /****************************************************************
    * MODULE1 GEN2 PWM5 is used for distance display on the RED LED *
    ****************************************************************/
    //Set PWM clock to Bus clock
    SysCtlPWMClockSet(SYSCTL_PWMDIV_1);
    //Enable, Turn on clock to PWM1
    SysCtlPeripheralEnable(SYSCTL_PERIPH_PWM1);
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_PWM1))
    {}
    //Configure pin PF1 for PWM output
    GPIOPinTypePWM(GPIO_PORTF_BASE, GPIO_PIN_1);
    GPIOPinConfigure(GPIO_PF1_M1PWM5);
    //Set up PWM Clock
    ui32PWMClock = SysCtlClockGet(); //PWM clock is 80 MHz
    ui32Load = (ui32PWMClock / PWM_FREQUENCY) - 1; //PWM period
    PWMGenConfigure(PWM1_BASE, PWM_GEN_2, PWM_GEN_MODE_DOWN); //Count down mode
    PWMGenPeriodSet(PWM1_BASE, PWM_GEN_2, ui32Load); //Set the PWM period
    PWMPulseWidthSet(PWM1_BASE, PWM_OUT_5, 1000); //Initial pulse width 50%
    PWMOutputState(PWM1_BASE, PWM_OUT_5_BIT, true); //Enable PWM output
    PWMGenEnable(PWM1_BASE, PWM_GEN_2); //Turn PWM1 GEN1 on
}

void SetPWMDutyCycle(float DutyCyclePercent)
{
    PWMPulseWidthSet(PWM1_BASE, PWM_OUT_5, PWM_Period*DutyCyclePercent/100);
}



