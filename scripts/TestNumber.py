from ape import accounts, project

tokenA = accounts.test_accounts[0]
tokenB = accounts.test_accounts[1]
account = accounts.test_accounts[2]
contract = project.CPAMM.deploy(tokenA, tokenB, sender=account)

# Transaction: Invoke the `set_number()` function, which costs Ether
receipt = contract.set_number(34, sender=account)
assert not receipt.failed

# The receipt contains data such as `gas_used`.
print(receipt.gas_used)
print(contract.testNumber())
