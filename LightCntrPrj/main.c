
#include <stdint.h>
#include <stdbool.h>

#include "driverlib/sysctl.h"

#include "GlobalsAndDefines.h"
#include "initialization.h"

#include "driverlib/uart.h"
#include "utils/uartstdio.h"

#include "UARTcomm.h"
#include "ADC0.h"

#include "PICntr.h"
#include "PWM.h"

#include "MovAvgFilter.h"

#include "TMP102.h"





int main()
{
    uint32_t i;

    initialization();


    while(1)
    {
        uint32_t ADC_value, Filtered_ADC_value = 0,Temp;

//        //Toggle blue LED for round robin loop timing profile
//        PF2 ^= 0x04;

        //SetPWMDutyCycle(g_UARTInputNumber);

        ADC_value = ReadADC0();

        //PI Control
        PIUpdate(ADC_value);

        //Moving average filter
        Filtered_ADC_value = MovAvgFilter(ADC_value);

        //TMP102
        Temp = ReadTMP102();


        //Display Data on UART
        SendUARTDataOut(ADC_value, Filtered_ADC_value,Temp);

        //Delay Loop
        for(i=0; i<500000; i++){}
    }
}

