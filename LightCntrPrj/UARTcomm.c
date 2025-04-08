
#include <stdint.h>
#include <stdbool.h>
#include "inc/tm4c123gh6pm.h"
#include "inc/hw_memmap.h"
#include "driverlib/uart.h"
#include "utils/uartstdio.h"

#include "GlobalsAndDefines.h"



// standard ASCII symbols
#define CR   0x0D
#define LF   0x0A
#define BS   0x7F
#define ESC  0x1B
#define SP   0x20
#define DEL  0x7F


//------------UART_InChar------------
// Input: none
// Output: ASCII code for key typed
char UART0_InChar(void){
    return((char)(UARTCharGet(UART0_BASE)));
}


//------------UART_OutChar------------
// Output 8-bit to serial port
// Input: letter is an 8-bit ASCII character to be transferred
// Output: none
void UART0_OutChar(char data){
    UARTCharPut(UART0_BASE, data);
}

void UART0_OutCRLF(void){
  UART0_OutChar(CR);
  UART0_OutChar(LF);
}

//Function to get user input from the keyboard
//Returns an unsigned 32 bit integer
//The function does not update the global variable until the user presses enter
//A flag is set if a number is being inputted
//False no new input.
//True new number is being inputted.
void GetUARTInputNumber()
{
    char character;
    static uint32_t number=0, length=0;

    character = UART0_InChar();

    if (character == CR)  //enter pressed update variables and return number
    {
        if (number < 1 || number > 3000){
            UART0_OutCRLF();
            UARTprintf("Enter number between 1 and 3000\n");
            number = 0;
        }
        else {
            UART0_OutCRLF();
            UARTprintf("Set Point = %d ADC counts\n", number);
            g_UARTInputNumber = number;
            g_InputFlag = false;
            number =0;
            length = 0;
        }
    }
    else if ((character>='0') && (character<='9')) //char is number append to value
    {
        g_InputFlag = true;
        number = 10*number+(character-'0');   // this line overflows if above 4294967295
        length++;
        UART0_OutChar(character);
    }
    else if ((character==BS) && length > 0)  //back space pressed
    {
        g_InputFlag = true;
        number /= 10;
        length--;
        UART0_OutChar(BS);
    }
    else //Default condition
    {
        g_InputFlag = true;
    }
}


//Function to send out data to the UART for display
void SendUARTDataOut(uint32_t value1, uint32_t value2, uint32_t value3)
{

    //If the user is not in the process of inputting a temperature set point send data out to the UART
    if (g_InputFlag == false)
    {
        UARTprintf(" %d   %d\n", value1, value2);
        UARTprintf("Temperature: %d degrees\n", value3);

    }
}


