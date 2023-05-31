import services
from protocolbuffers import Consts_pb2, UI_pb2

def moneycheat(command, _connection=None):
    try:
        try:
            active_sim = services.get_active_sim()
        except Exception as e:
            return "Error: {}".format(str(e))
        #! webney | money amount
        #! 0        1[-1]
        try:
            cheat_amount = int(command.split(".")[-1])
        except:
            return "Invalid amount."
        
        if active_sim is None:
            return "No active Sim. Are you in gameplay mode?"
        else:
            money_in_inventory = active_sim.family_funds.money
            if cheat_amount <= -1:
                cheat_amount
                output = active_sim.family_funds._update_money(max(cheat_amount, 0) - money_in_inventory, Consts_pb2.TELEMETRY_MONEY_CHEAT, active_sim, None, True, True)
            else:
                output = active_sim.family_funds._update_money(cheat_amount, Consts_pb2.TELEMETRY_MONEY_CHEAT, active_sim, None, True, True)
            if output == None:
                return "Household funds modified."
    except Exception as e:
        return "Unknown error: {}".format(str(e))

def process_command(command):
    if command.startswith('webney.money'):
        moneycheat(command)
    else:
        return "Invalid command {}".format(command)