#include <stdio.h>
#include <errno.h>
#include "oled.h"
#include <wiringPiI2C.h>


/*
 
available gpio function

int wiringPiI2C Setup(int devId);
int wiringPiI2CRead(int fd);
int wiringPiI2CWrite(int fd,int data);
int wiringPiI2cWriteReg8(int fd, int reg, int data);
int wiringPiI2CWriteReg16(int fd,int reg, int data);
int wiringPiI2CReadReg8(int fd,int reg);
int wiringPiI2CReadReg16(int fd,int reg);

 */
