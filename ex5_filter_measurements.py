'''
Exercise: Filter measurements for a device 

Before Running:
- Execute ./setup_environment.sh with provided ipaddress of the system running GridAPPS-D platform.
- Set the simulation_id below to the provided running simulation id in the GridAPPS-D platform
'''

import json
import os
from pathlib import Path
import time

import gridappsd.field_interface.agents.agents as agents_mod
from cimgraph.data_profile import CIM_PROFILE
from gridappsd.field_interface.agents import FeederAgent, SwitchAreaAgent, SecondaryAreaAgent
from gridappsd.field_interface.interfaces import MessageBusDefinition

from typing import Dict

cim_profile = CIM_PROFILE.RC4_2021.value

agents_mod.set_cim_profile(cim_profile)

cim = agents_mod.cim

simulation_id = '198927053'

config_folder = 'config_files_ieee13'

class SampleFeederAgent(FeederAgent):

    def __init__(self,
                 upstream_message_bus_def: MessageBusDefinition,
                 downstream_message_bus_def: MessageBusDefinition,
                 agent_config, simulation_id):

        super().__init__(upstream_message_bus_def, downstream_message_bus_def,
                         agent_config, None, simulation_id)
        
    def on_measurement(self, headers: Dict, message) -> None:
        with open("feeder_measurements.txt", "a") as fp:
            fp.write(json.dumps(message))

class SampleSwitchAreaAgent(SwitchAreaAgent):

    def __init__(self,
                 upstream_message_bus_def: MessageBusDefinition,
                 downstream_message_bus_def: MessageBusDefinition,
                 agent_config, simulation_id):

        super().__init__(upstream_message_bus_def, downstream_message_bus_def,
                         agent_config, None, simulation_id)
    
    def on_measurement(self, headers: Dict, message) -> None:
        with open(f"{self.switch_area.area_id}_measurements.txt", "a") as fp:
            fp.write(json.dumps(message))

class SampleSecondaryAreaAgent(SecondaryAreaAgent):

    def __init__(self,
                 upstream_message_bus_def: MessageBusDefinition,
                 downstream_message_bus_def: MessageBusDefinition,
                 agent_config, simulation_id):

        super().__init__(upstream_message_bus_def, downstream_message_bus_def,
                         agent_config, None, simulation_id)
        
        self.get_measurement_ids()
        

    def get_measurement_ids(self):

        self.measurement_ids = []
        network_area = self.secondary_area
        if cim.PowerElectronicsConnection in network_area.typed_catalog:
            network_area.get_all_attributes(cim.PowerElectronicsConnection)
            network_area.get_all_attributes(cim.PowerElectronicsConnectionPhase)
            network_area.get_all_attributes(cim.Terminal)
            network_area.get_all_attributes(cim.Analog)

            for pec in network_area.typed_catalog[cim.PowerElectronicsConnection].values():
                for meas in pec.Measurements:
                    print('Measurement: ', meas.name, meas.mRID)
                    print('type:', meas.measurementType, 'phases:', meas.phases)
                    self.measurement_ids.append(meas.mRID)


    def on_measurement(self, headers: Dict, message):
        for measurement_id in message.keys():
            if measurement_id in self.measurement_ids:
                print(f"\n\n Received measurements at secondary agent {self.secondary_area.area_id}: \n{message}")
                with open("secondary.txt", "a") as fp:
                    fp.write(json.dumps(message))

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
                                     agent_config,
                                     simulation_id)
    

    for switch_index, switch_area in enumerate(feeder_agent.feeder_area.switch_areas):
        switch_area_message_bus_def = MessageBusDefinition.load(f"{config_folder}/switch_area_message_bus_{switch_index}.yml")
        print("Creating switch area agent " +str(switch_area.area_id))
        switch_area_agent = SampleSwitchAreaAgent(feeder_message_bus_def,
                                                  switch_area_message_bus_def,
                                                  agent_config,
                                                  simulation_id)
        

        for sec_index, secondary_area in enumerate(switch_area_agent.switch_area.secondary_areas):
            secondary_area_message_bus_def = MessageBusDefinition.load(f"{config_folder}/secondary_area_message_bus_{switch_index}_{sec_index}.yml")
            print("Creating secondary area agent " +str(secondary_area.area_id))
            secondary_area_agent = SampleSecondaryAreaAgent(switch_area_message_bus_def, 
                                                            secondary_area_message_bus_def,
                                                            agent_config,
                                                            simulation_id)
        

    while True:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            print("Exiting sample")
            break


if __name__ == "__main__":
    _main()