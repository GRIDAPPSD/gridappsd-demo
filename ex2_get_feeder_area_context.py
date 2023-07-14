'''
Exercise : Check the available context (localised and downstream information) that Feeder area agent has.

Before Running:
- Set os.environ['GRIDAPPSD_ADDRESS'] to the ipaddress of the system running GridAPPS-D platform before running example.
'''

import os
from pathlib import Path
import time

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
    
    
    print("\n Addressable equipments: \n")
    for equipment_id in feeder_agent.feeder_area.addressable_equipment:
        print(f"{type(feeder_agent.feeder_area.addressable_equipment[equipment_id]).__name__} : {equipment_id}")


    print("\n Connectivity nodes: \n")
    for conn_node in feeder_agent.feeder_area.connectivity_nodes:
        print(f"{type(feeder_agent.feeder_area.connectivity_nodes[conn_node]).__name__} : {conn_node}")
    
    print("\n Switch Areas: \n")
    for switch_area in feeder_agent.feeder_area.switch_areas:
        print(f"{switch_area.area_id} : {switch_area.boundary_switches}")

    print("\n Unaddressable equipments: \n")
    Path("output.txt").write_text(str(feeder_agent.feeder_area.unaddressable_equipment))
    for equipment_id in feeder_agent.feeder_area.unaddressable_equipment:
        print(f"{feeder_agent.feeder_area.unaddressable_equipment[equipment_id].name} : {equipment_id}")
    
if __name__ == "__main__":
    _main()