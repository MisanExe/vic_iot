
#include <iostream>
#include "../include/app.h"

int main(int argc, char **argv){


    GPIO::Gpio *gpio = new GPIO::Gpio();
    

    try{
        gpio->SetPinMode(11, GPIO::GpioMode_e::OUTPUT);

    }catch(...){
        std::cout<<"Something went wrong"<<std::endl;
    }

    
    unsigned int input = 1;
    while(input == 1){
        std::cout<<"Enter 1 to  toogle : \t"<<std::endl;
        std::cin >> input;

        if(input){

            try{
                if(gpio->ReadSinglePin(17)){
                    gpio->WritePin(17, false);
                }else{
                    gpio->WritePin(17, true);
                }
            }catch(...){
                std::cout<<"something went wrong \n"<<std::endl;
            }
        }
    }

    

}