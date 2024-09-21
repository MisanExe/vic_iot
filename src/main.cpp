
#include <iostream>
#include <fcntl.h>
#include <unistd.h>
#include <cstdlib>
#include <thread>
#include "../include/app.h"
#include <sys/stat.h> 

//Listen to requests
void incomingRequest(){


}
//spawn wlan_edit
std::string wlan_edit_call(){

    std::string fifoPath = "../pipes/lan_config_fifo";
    

    auto lan_script = system("sudo python3 ../src/wlan_edit.py");
    
    if( lan_script >= 0){
        std::cout<<"called wlan config script sucessfully"<<std::endl;
    }else{
        std::cout<<"failed to call lan :"<<lan_script<<std::endl;
        return "Error";
    }

    //open fifo
    mkfifo(fifoPath.c_str(), 0777);
    
    int fifo = open(fifoPath.c_str(), O_RDONLY);
    if(fifo == -1){
        std::cout<<"Error opening fifo error num :"+fifo<<std::endl;
        return "Error";
    }

 

    char buffer[1024];
    while (true)
    {
        ssize_t byteRead = read(fifo, buffer, sizeof(buffer) -1);
        if(byteRead > 0){
            //std::cout<<buffer<<std::endl;
        }else if(byteRead == 0){
            break;
        }else{
            std::cout<<"Error reading fifo"<<std::endl;
            break;
        }
        
    }

    close(fifo);
    
    std::string ret(buffer);
    return ret;
}


int main(int argc, char **argv){

    //thread to listen for request
    std::cout<<wlan_edit_call()<<std::endl;


    return 0;
}
