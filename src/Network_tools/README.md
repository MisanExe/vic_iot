# Network Tools (configuration)

Depending on the Raspberry PI used, there can be multiple Network managers used
for configuration of not eth and wlan.
The configuration process can be quite Jarring.
The tools in this folder are provided to help the user with the configuration 
process.


## Table of Contents

-[Auth_SSID](#installation)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)

## Installation

###Auth_SSID.py
Tool is used to verify that a given wireless ssid is currently accessible
it exits with:
    VALID_SSID = 120,
    INVALID_SSID = -120,
    PROCESS_ERROR = -10,
    FEW_ARGS = -121,
it is meant to be used as a subprocess.

