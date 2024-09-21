
#include "../include/app.h"
#include "../include/pi_exceptions.h"

GPIO::Gpio::Gpio(){
    unsigned int ret = initGpio();
    if(ret == FAILED_TO_INIT){
        throw GPIO_EXCEPTIONS::FailedToInit();
    }
    this->_version = ret;
    std::cout<<"Created GPIO object --\nPIGPIO verison : "<<this->getVersion()<<std::endl;
}

GPIO::Gpio::~Gpio(){
    
}

int GPIO::Gpio::SetPinMode(unsigned const int &pin, GpioMode_e mode){

    if(v_pin(pin) == VERIFY_WRONG_PIN){
        throw GPIO_EXCEPTIONS::WrongPinNumber();
    }

    switch(mode){
        OUTPUT:
            if(gpio_set_Mode(pin, PI_OUTPUT) == WRITE_ERROR){
                throw GPIO_EXCEPTIONS::SetModeError();
            }
            break;

        INPUT:
            if(gpio_set_Mode(pin, PI_INPUT) == WRITE_ERROR){
                throw GPIO_EXCEPTIONS::SetModeError();
            }        
            break;

        ALTERNATE:
            if(gpio_set_Mode(pin, PI_ALT0) == WRITE_ERROR){
                throw GPIO_EXCEPTIONS::SetModeError();
            }
            break;
        default:
            mode = OUTPUT;
            break;
    }

    return 0;
}


int GPIO::Gpio::WritePin(unsigned int pin, bool state){
    if(v_pin(pin) == VERIFY_WRONG_PIN){
        throw GPIO_EXCEPTIONS::WrongPinNumber();
    }

    if (state){
        if(gpio_ON(pin) == WRITE_ERROR){
            throw GPIO_EXCEPTIONS::WriteError();
        }
    }else{
        if(gpio_OFF(pin) == WRITE_ERROR){
            throw GPIO_EXCEPTIONS::WriteError();
        }
    }

    return WRITE_SUCCESS;
}


int GPIO::Gpio::WritePin(std::vector<unsigned int> &pins, unsigned const int mode){

}

bool GPIO::Gpio::ReadSinglePin(unsigned const int &pin){
    if(v_pin(pin) == VERIFY_WRONG_PIN){
        throw GPIO_EXCEPTIONS::WrongPinNumber();
    }

    int ret = gpio_Read_State(pin);

    if(ret == READ_ERROR){
        throw GPIO_EXCEPTIONS::ReadError();
    }else{
        if(ret == 1){
            return true;
        }else if(ret == 0){
            return false;
        }
    }

    return false;
}

std::vector<unsigned int> GPIO::Gpio::ReadMultiplePins(std::vector<unsigned int> &pins){

}

std::string GPIO::Gpio::getVersion(){
    return std::to_string(this->_version);
}