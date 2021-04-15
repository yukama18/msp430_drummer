#include  "msp430.h"

#define     LED1                  BIT0                      // P1.0 red LED
#define     TXD                   BIT2                      // TXD on P1.2
#define     RXD                   BIT1                      // RXD on P1.1

unsigned char amp;
  
void setup(void);

void main(void)
{
    WDTCTL = WDTPW + WDTHOLD;       // Stop WDT
    
    // set up ADC on P1.5
    ADC10CTL0 = ADC10SHT_2 + ADC10ON;     // ADC10ON
    ADC10CTL1 = INCH_5;                   // input A1
    ADC10AE0 |= 0x20;                     // PA.1 ADC option select

    // set up LED1
    P1DIR |= LED1;
    P1OUT &= ~(LED1);

    // set up UART hardware
    P1DIR |= TXD;
    P1OUT |= TXD;

    // set up output and input to SR04
    P1DIR &= ~(BIT5);               // P 1.5 input = 0x20

    setup();                        // set up timer related stuff
  
  /* Main Application Loop */
  while(1)
  {
      ADC10CTL0 |= ENC + ADC10SC;
      while (ADC10CTL1 &ADC10BUSY);
      
      amp = (unsigned char) ADC10MEM;
      
      if ((amp > 200) && (amp < 260)) {
          continue;
      }
      
      UCA0TXBUF = 1;   // send volume as a byte to serial port
      
      P1OUT ^= LED1;              // toggle light for measurement

    __delay_cycles(40000);      // wait 100ms before collecting data again
      
      P1OUT ^= LED1;
  }
}

void setup(void)
{
    /* next three lines to use internal calibrated 1MHz clock: */
    BCSCTL1 = CALBC1_1MHZ;                    // Set range
    DCOCTL = CALDCO_1MHZ;
    BCSCTL2 &= ~(DIVS_3);                     // SMCLK = DCO = 1MHz

    /* these next two lines configure the ACLK signal to come from
    a secondary oscillator source, called VLO */
    BCSCTL1 |= DIVA_1;             // ACLK is half the speed of the source (VLO)
    BCSCTL3 |= LFXT1S_2;           // ACLK = VLO

    /* here we're setting up a timer to fire an interrupt periodically.
    When the timer 1 hits its limit, the interrupt will toggle the lights
    We're using ACLK as the timer source, since it lets us go into LPM3
    (where SMCLK and MCLK are turned off). */
    // not sure why we need to include this, but when removed, definitely stopped program from working
    TACCR0 = 1200;                 //  period
    TACTL = TASSEL_1 | MC_1;       // TACLK = ACLK, Up mode.
    TACCTL1 = CCIE + OUTMOD_3;     // TACCTL1 Capture Compare
    TACCR1 = 600;                  // duty cycle

    /* Configure hardware UART */
    P1SEL = BIT1 + BIT2 ; // P1.1 = RXD, P1.2=TXD
    P1SEL2 = BIT1 + BIT2 ; // P1.1 = RXD, P1.2=TXD
    UCA0CTL1 |= UCSSEL_2; // Use SMCLK
    UCA0BR0 = 104; // Set baud rate to 9600 with 1MHz clock (Data Sheet 15.3.13)
    UCA0BR1 = 0; // Set baud rate to 9600 with 1MHz clock
    UCA0MCTL = UCBRS0; // Modulation UCBRSx = 1
    UCA0CTL1 &= ~UCSWRST; // Initialize USCI state machine
}
