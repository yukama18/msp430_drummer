FILE=unfiltered

OBJECTS=$(FILE).c
DEVICE=msp430g2553
INSTALL_DIR=$(HOME)/ti/msp430_gcc

GCC_DIR = $(INSTALL_DIR)/bin
SUPPORT_FILE_DIRECTORY = $(INSTALL_DIR)/include

CC      = $(GCC_DIR)/msp430-elf-gcc
GDB     = $(GCC_DIR)/msp430-elf-gdb

CFLAGS = -I $(SUPPORT_FILE_DIRECTORY) -mmcu=$(DEVICE) -Os
LFLAGS = -L $(SUPPORT_FILE_DIRECTORY) -T $(DEVICE).ld

elf: ${OBJECTS}
	$(CC) $(CFLAGS) $(LFLAGS) $? -g -o $(FILE).elf
#asm: 
#	$(CC) $(CFLAGS) $(LFLAGS) $? -S $(FILE).c

clean: 
	rm *.o *.elf *.s


debug: all
	$(GDB) $(FILE).elf
