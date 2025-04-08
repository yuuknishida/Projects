#include <stdint.h>
#include <stdbool.h>
#include "inc/tm4c123gh6pm.h"
#include "inc/hw_memmap.h"
#include "inc/hw_types.h"
#include "driverlib/sysctl.h"
#include "driverlib/interrupt.h"
#include "driverlib/gpio.h"
#include "inc/hw_gpio.h"
#include "driverlib/i2c.h"
#include "driverlib/pin_map.h"


void TMP102Setup(void)
{
    //Turn on clock to GPIOB and I2C0
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOB);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_I2C0);
    while(!SysCtlPeripheralReady(SYSCTL_PERIPH_I2C0))
    {}

    //Configure GPIOB pins to be used by I2C0
    GPIOPinConfigure(GPIO_PB2_I2C0SCL);
    GPIOPinConfigure(GPIO_PB3_I2C0SDA);
    GPIOPinTypeI2CSCL(GPIO_PORTB_BASE, GPIO_PIN_2);
    GPIOPinTypeI2C(GPIO_PORTB_BASE, GPIO_PIN_3);

    //Set the Launcpad as the I2C master with the slow clock 100 Kbps
    I2CMasterInitExpClk(I2C0_BASE, SysCtlClockGet(), false);

}

int32_t ReadTMP102(void)
{
    uint32_t frame_value, assemble, temp_celsius;
    int32_t temperature;
    //Set the address to the TMP102. First byte sent to the TMP102 for each read.
    //*Set this value correctly***************************************/

    I2CMasterSlaveAddrSet(I2C0_BASE, 0x48, true);  //This value is the top 7 MSB's

    I2CMasterControl(I2C0_BASE, I2C_MASTER_CMD_BURST_RECEIVE_START); //Outputs first byte(address) and receives top 8 bits of temperature
    while(I2CMasterBusy(I2C0_BASE))  //Wait for I2CO master to finish receiving
    {}
    frame_value = I2CMasterDataGet(I2C0_BASE); //Get the top 8 bits, MSB's, of the temperature from I2C hardware
    assemble = frame_value << 24;


    I2CMasterControl(I2C0_BASE, I2C_MASTER_CMD_BURST_RECEIVE_FINISH);   //Receives the bottom 4 bits of the temperature
    while(I2CMasterBusy(I2C0_BASE))  //Wait for I2CO master to finish receiving
    {}
    frame_value = I2CMasterDataGet(I2C0_BASE); //Get the bottom 4 bits, MSB's, of the temperature from the I2C hardware
    frame_value = (frame_value << 16) & 0x00F00000;
    assemble = assemble | frame_value;
    temperature = assemble;
    temperature = temperature >> 20;
    temp_celsius = temperature * 0.0625;

    return temp_celsius;
}
