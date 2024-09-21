#include <stdio.h>
#include "../include/gpio_interface.h"


int v_pin(const int pin){
    if(pin >= MIN_PIN && pin <= MAX_PIN){
        return VERIFY_PIN_OK;
    }else{
        return VERIFY_WRONG_PIN;
    }

    return 0;
}

int gpio_set_Mode(int pin, int mode){
    //verify pin
    if(v_pin(pin) == VERIFY_WRONG_PIN){
        return VERIFY_WRONG_PIN;
    }

    //use pigpio lib
    if(gpioSetMode(pin, mode) != PI_GPIO_OK){
        return SET_MODE_ERROR;
    }else{
        return SET_MODE_SUCCESS;
    }


}

int gpio_ON(int pin){
    //verify pin
    if(v_pin(pin) == VERIFY_WRONG_PIN){
        return VERIFY_WRONG_PIN;
    }

    //use pigpio lib
    if(gpioWrite(pin, GPIO_ON) != PI_GPIO_OK){
        return WRITE_ERROR;
    }else{
        return WRITE_SUCCESS;
    }

    return 0;
}

int gpio_OFF(int pin){
    //verify pin
    if(v_pin(pin) == VERIFY_WRONG_PIN){
        return VERIFY_WRONG_PIN;
    }

    //use pigpio lib
    if(gpioWrite(pin, GPIO_OFF) != PI_GPIO_OK){
        return WRITE_ERROR;
    }else{
        return WRITE_SUCCESS;
    }

    return 0;
}


int gpio_Read_State(int pin){
    //verify pin
    if(v_pin(pin) == VERIFY_WRONG_PIN){
        return VERIFY_WRONG_PIN;
    }

    int read = gpioRead(pin);
    if (read == PI_BAD_GPIO){
        printf("Error occurred\n");
        return READ_ERROR;
    }else{
        return read;
    }
    return 0;
}


int initGpio(){
    int read = gpioInitialise();
    if(read == PI_INIT_FAILED){
        return FAILED_TO_INIT;
    }
    else{
        return read;
    }

    return 0;
}

void forcedExit(){
    gpioTerminate();
}
