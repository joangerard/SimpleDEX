from ape import accounts, project


def main():
    tokenA = accounts.test_accounts[0]
    tokenB = accounts.test_accounts[1]
    account = accounts.test_accounts[2]
    contract = project.CPAMM.deploy(tokenA, tokenB, sender=account)
