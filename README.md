# UGV
This is a personal project where I take a ready made Unmannged Ground Vehicle (UGV) and make it do cool things.

## Cool things
### PS4 Remote Control
I have build a system that takes inputs from a bluetooth PS4 controller, and controls the UGV, alloying for speed control, and effective turning using the analogue sticks.

[insert gif here]

### AI Animal Detection
Under Construction.

[insert gif here]

### LiDAR Adaptive Cruise Control
TBD

[insert gif here]


### TBD

## Credits
This UGV is a product from Waveshare (waveshare.com). I take no credit for the underlying ESP32 RTOS, or the contents of `base_ctrl.py`, which allows me to communicate with the ESP32 using a Raspberry Pi.

## Setup

For setup instructions, see the instructions at https://github.com/waveshareteam/ugv_rpi as well as the Waveshare wiki: https://www.waveshare.com/wiki/UGV01#Introduction.

### Setup Notes

* I followed the setup steps in the above link, and then used the created virtual environment to operate the code in this repository.
* pyPS4Controller has a bug which affects performance (see here: https://github.com/ArturSpirin/pyPS4Controller/issues/28). Author doesn't seem to be responding to pull requests.