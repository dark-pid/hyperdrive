import os
import configparser

from dark import DarkMap, DarkGateway

##
# configuring dARK GW
##

bc_config = configparser.ConfigParser()
deployed_contracts_config = configparser.ConfigParser()

# bc configuration
PROJECT_ROOT = "./"
bc_config.read(os.path.join(PROJECT_ROOT, "config.ini"))
# deployed contracts config
deployed_contracts_config.read(os.path.join(PROJECT_ROOT, "deployed_contracts.ini"))


class BlockChainManager:
    _instance = None

    def __new__(cls, user_pk=None, *args, **kwargs):
        if not cls._instance:
            if user_pk:
                dark_gw = DarkGateway(bc_config, deployed_contracts_config, account_private_key=user_pk)
            else:
                dark_gw = DarkGateway(bc_config, deployed_contracts_config)
            dark_map = DarkMap(dark_gw)

            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance.dark_gw = dark_gw
            cls._instance.dark_map = dark_map

        return cls._instance