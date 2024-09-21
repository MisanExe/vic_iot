#ifndef GPIO_C_INTERFACE
#define GPIO_C_INTERFACE

#include <pigpio.h>

//pin range 
#define MAX_PIN 45
#define MIN_PIN 0
//pin state
#define GPIO_ON     1
#define GPIO_OFF    0
//pin mode



/*
    Error Codes 
*/
#define PI_GPIO_OK 0
#define WRITE_SUCCESS 2
#define WRITE_ERROR -2
#define READ_SUCCESS 3
#define READ_ERROR -3
#define VERIFY_PIN_OK 4
#define VERIFY_WRONG_PIN -4
#define FAILED_TO_INIT -5
#define SET_MODE_ERROR 6
#define SET_MODE_SUCCESS -6


/**
 * @brief Stores the init state of the library
 */
static int isInit = 0;

/**
 * @brief Verifys the GPIO pin entered
 * @param int pin
 * @return VERIFY_PIN_OK(pin number is valid), VERIFY_WRONG_PIN(wrong pin entered)
 */
int v_pin(const int pin);

/**
 * @brief initalizes gpio library
 * @param None
 * @return returns FAILED_TO_INIT or PI_GPIO_OK
 */
int initGpio();

/**
 * @brief Sets pin mode to OUTPUT,INPUT or ALTERNATE MODE
 * @param int pin(ranging between MAX_PIN and MIN_PIN)
 *        int mode(PI_INPUT,PI_OUTPUT, PI_ALT0)
 * @return VERIFY_WRONG_PIN(wrong pin entered) , WRITE_ERROR(Unable to perform Write), WRITE_SUCCESS(Write successful)
 */
int gpio_set_Mode(int pin, int mode);

/**
 * @brief Sets pin OUTPUT HIGH
 * @param int pin(ranging between MAX_PIN and MIN_PIN)
 * @return VERIFY_WRONG_PIN(wrong pin entered) , WRITE_ERROR(Unable to perform Write), WRITE_SUCCESS(Write successful)
 */
int gpio_ON(int pin);

/**
 * @brief Sets pin OUTPUT LOW
 * @param int pin(ranging between MAX_PIN and MIN_PIN)
 * @return VERIFY_WRONG_PIN(wrong pin entered) , WRITE_ERROR(Unable to perform Write), WRITE_SUCCESS(Write successful)
 */
int gpio_OFF(int pin);

/**
 * @brief Reads the pin state
 * @param int pin (output pin number ranging from MIN_PIN to MAX_PIN)
 * @return VERIFY_WRONG_PIN (wrong pin number entered), READ_ERROR(unable to read), GPIO_ON(1), GPIO_OFF(0)
 */
int gpio_Read_State(int pin);


void forcedExit();

#endif