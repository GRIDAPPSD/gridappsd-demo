'''
Exercise: Create a basic distributed agent at Feeder area level 

Before Running:
- Set os.environ['GRIDAPPSD_ADDRESS'] to the ipaddress of the system running GridAPPS-D platform before running example.
'''

import os
from pathlib import Path
import time
import yaml

import gridappsd.field_interface.agents.agents as agents_mod
from cimgraph.data_profile import CIM_PROFILE
from gridappsd.field_interface.agents import FeederAgent
from gridappsd.field_interface.interfaces import MessageBusDefinition

from typing import Dict

cim_profile = CIM_PROFILE.RC4_2021.value

agents_mod.set_cim_profile(cim_profile)

cim = agents_mod.cim

os.environ['GRIDAPPSD_ADDRESS'] = 'localhost'

config_folder = 'config_files_ieee123'

class SampleFeederAgent(FeederAgent):

    def __init__(self,
                 upstream_message_bus_def: MessageBusDefinition,
                 downstream_message_bus_def: MessageBusDefinition,
                 agent_config):

        super().__init__(upstream_message_bus_def, downstream_message_bus_def,
                         agent_config, None, None)

def _main():

    agent_config = {
        "app_id": "demo_app",
        "description": "This is a GridAPPS-D demo distributed application"
    }

    system_message_bus_def = MessageBusDefinition.load(f"{config_folder}/system-message-bus.yml")
    feeder_message_bus_def = MessageBusDefinition.load(f"{config_folder}/feeder-message-bus.yml")

    print("Creating feeder area agent " +str(feeder_message_bus_def.id))
    feeder_agent = SampleFeederAgent(system_message_bus_def,
                                     feeder_message_bus_def, 
                                     agent_config)
    
if __name__ == "__main__":
    _main()