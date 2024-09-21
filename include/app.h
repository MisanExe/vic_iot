#pragma once


#ifdef __cplusplus
    extern "C"
    {
#endif
    #include "../include/gpio_interface.h"
#ifdef __cplusplus
}
#endif

#include <vector>
#include <string>


namespace GPIO{

    enum GpioMode_e{
        OUTPUT,
        INPUT,
        ALTERNATE,
    };

    class Gpio{
        public :
            /**
             * @brief initalizes a GPIO object used to interact with the pigpio library
             * @exception FailedToInit
             * @param
             * @return
             */
            Gpio();
            ~Gpio();

            /**
             * @brief set pin mode to Output, Input or Alternate
             * @param unsigned int pin(pin number), GpioMode_e mode(mode type specifying the to be used)
             * @return int 
             */
            int SetPinMode(unsigned const int &pin, GpioMode_e mode);

            /**
             * @brief
             */
            int WritePin(unsigned int, bool state);

            /**
             * @brief
             */
            int WritePin(std::vector<unsigned int> &pins, unsigned const int mode);

            /**
             * @brief
             */
            bool ReadSinglePin(unsigned const int &pin);
            /**
             * @brief
             */
            std::vector<unsigned int> ReadMultiplePins(std::vector<unsigned int> &pins);

            std::string getVersion();

            private:
            /**
             * @version
             */
            unsigned int _version = 0;
            





    };
    
}


