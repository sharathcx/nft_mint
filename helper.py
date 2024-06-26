from brownie import network, config, accounts

def get_account():
    if network.show_active() == "development":
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])