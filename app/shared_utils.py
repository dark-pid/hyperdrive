
from dark import DarkMap, DarkGateway

# { address : "val"
#   arks : []
# }
 
LIMIAR = 100
MANAGED_ARK_DICT = {}


def get_pid(wallet_addr,dark_map:DarkMap):
    
    try:
        warks = MANAGED_ARK_DICT[wallet_addr]
    except KeyError:
        warks = dark_map.bulk_request_pid_hash()
        MANAGED_ARK_DICT[wallet_addr] = warks


    s = len(warks)
    if s < LIMIAR:
        r = int((LIMIAR- s)/100)
        for i in range(r):
            pids = dark_map.bulk_request_pid_hash()
            warks.extend(pids)
    
    ark_hash = warks.pop(0)
    # dark_map.dpid_db.caller.get(ark_hash)[1]
    return ark_hash
