#include <stdint.h>
#include <stdbool.h>
#include "inc/tm4c123gh6pm.h"
#include "inc/hw_memmap.h"
#include "driverlib/sysctl.h"
#include "driverlib/gpio.h"
#include "driverlib/adc.h"


void ADC0Setup(void)
{

    /***********************
    * ADC0                 *
    ***********************/
    //Enable ADC0
    SysCtlPeripheralEnable(SYSCTL_PERIPH_ADC0);
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_ADC0))
    {}

    //Enable PORTB
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOB);
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_GPIOB))
    {}

    //Configure PORT pins for analog input
    //PB5 analog input CH11
    GPIOPinTypeADC(GPIO_PORTB_BASE, GPIO_PIN_5);

    //ADC will use sequencer 3 for one sample mode
    ADCSequenceConfigure(ADC0_BASE, 3, ADC_TRIGGER_PROCESSOR, 0);
//    ADCSequenceStepConfigure(ADC0_BASE,3,0,ADC_CTL_TS|ADC_CTL_IE|ADC_CTL_END);    //Internal Temperature Sensor
    ADCSequenceStepConfigure(ADC0_BASE,3,0,ADC_CTL_CH11|ADC_CTL_IE|ADC_CTL_END);   //Analog Input PB5
    ADCSequenceEnable(ADC0_BASE, 3);

}

uint32_t ReadADC0(void)
{
    uint32_t ADC_value;
    ADCIntClear(ADC0_BASE, 3);

    //Start conversion sequence
    ADCProcessorTrigger(ADC0_BASE, 3);
    while(!ADCIntStatus(ADC0_BASE, 3, false))
    {
    }

    //Get the ADC value
    ADCSequenceDataGet(ADC0_BASE, 3, &ADC_value);

    return ADC_value;
}

