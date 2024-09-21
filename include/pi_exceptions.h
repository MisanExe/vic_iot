#pragma once

#include <exception>
#include <iostream>



namespace GPIO_EXCEPTIONS{

    class FailedToInit : public std::exception{

        public:
        const char* what() const noexcept override{
            return "GPIO Initalization : Initalization error\n";
        }

    };

    class WriteError : public std::exception{

        public:
        const char* what() const noexcept override{
            return "GPIO Write Error : Attempt to write to pin failed\n";
        }

    };

    class ReadError : public std::exception{

        public:
        const char* what() const noexcept override{
            return "GPIO Read Error : Attempt to read pin failed\n";
        }

    };

    class  WrongPinNumber : public std::exception{

        public:
        const char* what() const noexcept override{
            return "GPIO Wrong pin: PIN Number entered is Wrong.\nEnter PIN Number ranging from MAX_PIN to MIN_PIN\n";
        }

    };

    class  SetModeError : public std::exception{

        public:
        const char* what() const noexcept override{
            return "GPIO Set pin Mode: Error setting pin mode\n";
        }

    };
}
