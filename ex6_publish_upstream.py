'''
Exercise: Filter measurements for a device 

Before Running:
- Execute ./setup_environment.sh with provided ipaddress of the system running GridAPPS-D platform.
'''

import json
import os
from pathlib import Path
import time

import gridappsd.field_interface.agents.agents as agents_mod
from cimgraph.data_profile import CIM_PROFILE
from gridappsd.field_interface.agents import FeederAgent, SwitchAreaAgent, SecondaryAreaAgent
from gridappsd.field_interface.interfaces import MessageBusDefinition

from gridappsd import topics

from typing import Dict

cim_profile = CIM_PROFILE.RC4_2021.value

agents_mod.set_cim_profile(cim_profile)

cim = agents_mod.cim

simulation_id = '1703223889'

config_folder = 'config_files_ieee13'

os

class SampleSwitchAreaAgent(SwitchAreaAgent):

    def __init__(self,
                 upstream_message_bus_def: MessageBusDefinition,
                 downstream_message_bus_def: MessageBusDefinition,
                 agent_config):

        super().__init__(upstream_message_bus_def, downstream_message_bus_def,
                         agent_config, None, None)
        
    def on_downstream_message(self, headers: Dict, message) -> None:
        print(f"recieved message from secondary agent: {message}")
        
        
class SampleSecondaryAreaAgent(SecondaryAreaAgent):

    def __init__(self,
                 upstream_message_bus_def: MessageBusDefinition,
                 downstream_message_bus_def: MessageBusDefinition,
                 agent_config):

        super().__init__(upstream_message_bus_def, downstream_message_bus_def,
                         agent_config, None, None)
            
    def on_upstream_message(self, headers: Dict, message) -> None:
        pass

def _main():

    agent_config = {
        "app_id": "demo_app",
        "description": "This is a GridAPPS-D demo distributed application"
    }

    feeder_message_bus_def = MessageBusDefinition.load(f"{config_folder}/feeder-message-bus.yml")
    switch_area_message_bus_def = MessageBusDefinition.load(f"{config_folder}/switch_area_message_bus_4.yml")
    secondary_area_message_bus_def = MessageBusDefinition.load(f"{config_folder}/secondary_area_message_bus_4_0.yml")
    
        
    print("Creating switch area agent ")
    switch_area_agent = SampleSwitchAreaAgent(feeder_message_bus_def,
                                                switch_area_message_bus_def,
                                                agent_config)
    
    print("Creating secondary area agent ")
    secondary_area_agent = SampleSecondaryAreaAgent(switch_area_message_bus_def, 
                                                    secondary_area_message_bus_def,
                                                    agent_config)

    secondary_area_agent.publish_upstream(message={"message":"this is a test meesage"})
            
            

    while True:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            print("Exiting sample")
            break


if __name__ == "__main__":
    _main()