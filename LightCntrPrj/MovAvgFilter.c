#include <stdint.h>
#include <stdbool.h>
#include "inc/tm4c123gh6pm.h"
#include "inc/hw_memmap.h"
#include "inc/hw_types.h"
#include "driverlib/sysctl.h"


static int32_t fifo[16];        //array to hold FIFO data (global)

//FIFO function for moving average filter
int32_t push_front_pop_back(int32_t push_value)
{
    static uint32_t current_fifo_index=0;
    uint32_t pop_value;

    pop_value=fifo[current_fifo_index];
    fifo[current_fifo_index]=push_value;
    if(current_fifo_index==15)
        current_fifo_index=0;
    else
        current_fifo_index++;
    return pop_value;
}

//Recursive implementation of moving average filter
//Must use integer math or round off errors will occur
uint32_t MovAvgFilter(uint32_t input_value)
{
    uint32_t current_sum=0, prev_sum=0, i, average=0, popped_value;
    popped_value=push_front_pop_back(input_value);

    for(i=0;i<16;i++)
    {
        current_sum+=fifo[i];
    }
    if(prev_sum==0)
    {
        average=current_sum/16;
    }
    else{
        current_sum=prev_sum - popped_value+input_value;
        average=current_sum/16;
    }
    prev_sum=current_sum;
    current_sum=0;
    return average;
}

