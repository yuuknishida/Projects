#include <stdint.h>
#include <stdbool.h>

#include "GlobalsAndDefines.h"
#include "PWM.h"


void PIUpdate(uint32_t ADC_value)
{
    float e0, u0;
    static float e1=0.0, u1=0.0;



    //Calculate the current error for the PID algorithm
    e0 = (float)g_UARTInputNumber - (float)ADC_value;


    //PI difference equation.  Only P and I terms are used.
    u0 = u1 + 0.002*e0 - 0.0*e1;
//    u0 = u1 + 0.192*e0 - 0.168*e1;
//    u0 = u1 + 0.0241*e0 - 0.0*e1;

    //Limit output to be between 1% and 99%.
    if (u0 > 99.0)
        u0 = 99.0;
    else if (u0 < 1.0)
        u0 = 1.0;


    //Save the current output and error into the old output and error
    u1 = u0;
    e1 = e0;


    //Output the PI pulse width to the PWM module
    //The PID output goes from 1 to 99 after being limited above.
    SetPWMDutyCycle(u0);
}

