'''
Exercise : Check the available context (localised and downstream information) that Feeder area agent has.

todo: context for switch and secondary area 


Before Running:
- Set os.environ['GRIDAPPSD_ADDRESS'] to the ipaddress of the system running GridAPPS-D platform before running example.
'''

import os
from pathlib import Path
import time

import gridappsd.field_interface.agents.agents as agents_mod
from cimgraph.data_profile import CIM_PROFILE
from gridappsd.field_interface.agents import SwitchAreaAgent
from gridappsd.field_interface.interfaces import MessageBusDefinition

from typing import Dict

cim_profile = CIM_PROFILE.RC4_2021.value

agents_mod.set_cim_profile(cim_profile)

cim = agents_mod.cim

os.environ['GRIDAPPSD_ADDRESS'] = 'localhost'

config_folder = 'config_files_ieee13'

class SampleSwitchAreaAgent(SwitchAreaAgent):

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

    feeder_message_bus_def = MessageBusDefinition.load(f"{config_folder}/feeder-message-bus.yml")
    switch_area_message_bus_def = MessageBusDefinition.load(f"{config_folder}/switch_area_message_bus_1.yml")
    
    print("Creating switch area agent ")
    switch_area_agent = SampleSwitchAreaAgent(feeder_message_bus_def,
                                              switch_area_message_bus_def,
                                              agent_config)

    print("\n Addressable equipments in switch area: \n")
    for equipment_id in switch_area_agent.switch_area.addressable_equipment:
        print(f"{type(switch_area_agent.switch_area.addressable_equipment[equipment_id]).__name__} : {equipment_id}")

    print("\n Connectivity nodes: \n")
    for conn_node in switch_area_agent.switch_area.connectivity_nodes:
        print(f"{type(switch_area_agent.switch_area.connectivity_nodes[conn_node]).__name__} : {conn_node}")
    

    print("\n Secondary Areas: \n")
    for sec_area in switch_area_agent.switch_area.secondary_areas:
        print(f"{sec_area.area_id}")

    print("\n Unaddressable equipments: \n")
    for equipment_id in switch_area_agent.switch_area.unaddressable_equipment:
        print(f"{switch_area_agent.switch_area.unaddressable_equipment[equipment_id].name} : {equipment_id}")

    
if __name__ == "__main__":
    _main()