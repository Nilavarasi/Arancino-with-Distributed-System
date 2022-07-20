import os
from web3 import Web3, HTTPProvider
from interface import ContractInterface

w3 = Web3(HTTPProvider('http://127.0.0.1:8545'))

contract_dir = os.path.abspath('./contracts/')
greeter_interface = ContractInterface(w3, 'StoreSensorData', contract_dir)
greeter_interface.compile_source_files()
greeter_interface.deploy_contract()
instance = greeter_interface.get_instance()
