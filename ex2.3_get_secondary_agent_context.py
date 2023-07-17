'''
Exercise : Check the available context (localised and downstream information) that Secondary area agent has.

Before Running:
- Execute ./setup_environment.sh with provided ipaddress of the system running GridAPPS-D platform.
'''

import os
from pathlib import Path
import time

import gridappsd.field_interface.agents.agents as agents_mod
from cimgraph.data_profile import CIM_PROFILE
from gridappsd.field_interface.agents import SecondaryAreaAgent
from gridappsd.field_interface.interfaces import MessageBusDefinition

from typing import Dict

cim_profile = CIM_PROFILE.RC4_2021.value

agents_mod.set_cim_profile(cim_profile)

cim = agents_mod.cim


config_folder = 'config_files_ieee13'

class SampleSecondaryAreaAgent(SecondaryAreaAgent):

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

    switch_area_message_bus_def = MessageBusDefinition.load(f"{config_folder}/switch_area_message_bus_4.yml")
    secondary_area_message_bus_def = MessageBusDefinition.load(f"{config_folder}/secondary_area_message_bus_4_0.yml")
    
    secondary_area_agent = SampleSecondaryAreaAgent(switch_area_message_bus_def, 
                                                    secondary_area_message_bus_def,
                                                    agent_config)
    
    print("\n Addressable equipments in switch area: \n")
    for equipment_id in secondary_area_agent.secondary_area.addressable_equipment:
        print(f"{type(secondary_area_agent.secondary_area.addressable_equipment[equipment_id]).__name__} : {equipment_id}")

    print("\n Connectivity nodes: \n")
    for conn_node in secondary_area_agent.secondary_area.connectivity_nodes:
        print(f"{type(secondary_area_agent.secondary_area.connectivity_nodes[conn_node]).__name__} : {conn_node}")
    
    print("\n Unaddressable equipments: \n")
    for equipment_id in secondary_area_agent.secondary_area.unaddressable_equipment:
        print(f"{secondary_area_agent.secondary_area.unaddressable_equipment[equipment_id].name} : {equipment_id}")
    
    
if __name__ == "__main__":
    _main()