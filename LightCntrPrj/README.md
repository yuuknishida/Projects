
# LightCntrPrj (TM4C123 Microcontroller Firmware)

## Overview
Firmware for a Texas Instruments TM4C123 (Tiva C) microcontroller implementing light control and monitoring functions. It exercises common peripherals: ADC for sensing, PWM for output modulation, timers/counters for scheduling, UART for diagnostics, and I2C (via TMP102 temperature sensor driver).

## Features
- Analog sampling through `ADC0` for sensor inputs.
- PWM signal generation for brightness or actuator control.
- Moving average filtering to smooth sensor data (`MovAvgFilter.c`).
- Digital counters and timing utilities (`DigCntrTimer.c`, `PICntr.c`).
- Temperature acquisition using TMP102 (`TMP102.c`).
- UART communication for status/debug output (`UARTcomm.c`, `UARTSetup.c`).

## Key Source Files
- `main.c` – Application entry, high-level orchestration.
- `initialization.c` – Peripheral setup routines.
- `ADC0.c` / `ADC0.h` – ADC driver implementation.
- `PWM.c` / `PWM.h` – PWM configuration and update logic.
- `UARTcomm.c` / `UARTSetup.c` – UART send/receive and initialization.
- `MovAvgFilter.c` – Filter utility for smoothing sampled data.
- `TMP102.c` – I2C temperature sensor driver.
- `tm4c123gh6pm_startup_ccs.c` – Startup vector table and low-level init.

## Build
Recommended to use Code Composer Studio (CCS):
1. Import the project directory into CCS.
2. Ensure device target is TM4C123GH6PM.
3. Build (Project > Build).

Alternative (ARM GCC toolchain):
You may craft a Makefile referencing the provided linker script `tm4c123gh6pm.cmd` and startup file. (Not included here; CCS artifacts present.)

## Flash & Debug
Use the onboard ICDI debugger or an external JTAG adapter:
1. Connect LaunchPad.
2. In CCS click Debug, then Run.
3. Monitor UART output with a serial terminal (baud configured in UART setup file).

## Data Processing
ADC readings are filtered using a moving average to reduce noise before PWM adjustments or logic decisions. Timing modules coordinate sampling intervals and output refresh.

## Possible Enhancements
- Add interrupt-driven ADC sampling.
- Implement low-power modes.
- Include CRC or checksum on UART packets.
- Expand sensor suite (light, humidity with additional I2C drivers).

## Learning Focus
Showcases embedded C modular design, peripheral configuration, and simple signal conditioning techniques.

