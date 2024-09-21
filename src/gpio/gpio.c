#include <stdio.h>
#include <stdlib.h>
#include <pigpio.h>
#include "../include/gpio_interface.h"



int main(int argc, char** argv){

	atexit(forcedExit);

	initGpio();
	int input =0;
	while(1){

		printf("Enter 1 character to toogle pin: \t");
		scanf("%d", &input);
		
		if(input == 1){
			if(gpio_Read_State(17) == GPIO_ON){
				gpio_OFF(17);
			}else if (gpio_Read_State(17) != GPIO_ON){
				gpio_ON(17);
			}
			
		}else{
			printf("Exiting ......\n");
			gpioTerminate();
			break;
		}
	}	


	return 0;
}
