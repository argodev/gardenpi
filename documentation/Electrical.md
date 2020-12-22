# Electrical Configuration

The Raspberry Pi and most of the sensors will run off of the 5VDC/2A power supply and take almost no separate consideration. However, the grow-lights are standard 120VAC lights and will be switched on and off via relays controlled by the RPI. Additionally, the valves I selected that control the water flow to the misters use 12VDC which cannot be supplied by the RPI. 

To address these requirements, I selected two Sainsmart 4-port relay boards. I could have used a single 8-port board, but I had some of the 4-port boards lying around and so I used them. With three shelves configured, this leaves an empty/unused port on each relay board.

## 12 VDC Support

I had an old 12VDC/2A power supply lying around so I used it for the irrigation valves. the common/neutral side connected directly to one leg on each of the valves (it doesn't matter which). The "hot" or positive side of the powersupply is connected to the one leg of each of the relays on one of the Sainsmart boards. The "normally open" leg of each of the relays is then connected to the other side of the valve switch. The Sainsmart board is powered with a VCC of 5VDC from the RPI and the individual relays are controlled by a separate GPIO pin from the PI.

## 120 VAC Support

The 120 VAC ("Mains") power support is wired in a similar fashion as the 12VDC version, but rather than wiring the relays directly to the lights, I wired them to outlets in a standard power outlet box. This allows me to to simply plug something in to one of the outlets, and then control it via the relay. See the image below:

![Box](/images/electrical01.jpg)

I am able to control the top/bottom half of the individual outlets independentaly due to having broken the connection tab between the top/bottom outlets and then wiring them separately. The following images show the normal tab as well as it broken to allow independent operation.

![Outlet Tab](/images/outlet01.jpg)

![Outlet No Tab](/images/outlet02.jpg)
