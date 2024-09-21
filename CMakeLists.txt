cmake_minimum_required(VERSION 3.18.4)

project(gpio VERSION 1.0 LANGUAGES C CXX)
set(CMAKE_C_STANDARD 99)
set(CMAKE_CXX_STANDARD 17)


include_directories(${PROJECT_SOURCE_DIR}/src)

add_executable( gpio_exe
                src/gpio/app.cpp
                src/gpio/gpio_interface.c
                src/main.cpp
                include/gpio_interface.h
                include/pi_exceptions.h
                include/app.h)

target_include_directories(gpio_exe PRIVATE ${CMAKE_SOURCE_DIR}/include)

target_link_libraries(gpio_exe pigpio pthread)

