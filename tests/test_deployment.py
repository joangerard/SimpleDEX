import pytest
from ape import accounts, project


@pytest.fixture
def deployer():
    return accounts.test_accounts[0]


@pytest.fixture
def deployed_contracts(deployer):
    token_a = project.TokenA.deploy(sender=deployer)
    token_b = project.TokenB.deploy(sender=deployer)
    cpamm = project.CPAMM.deploy(token_a.address, token_b.address, sender=deployer)
    return token_a, token_b, cpamm


def test_tokens_supply(deployed_contracts, deployer):
    token_a, token_b, _ = deployed_contracts
    assert token_a.totalSupply() == 10_000 * 10**18
    assert token_b.totalSupply() == 10_000 * 10**18
    assert token_a.balanceOf(deployer) == token_a.totalSupply()
    assert token_b.balanceOf(deployer) == token_b.totalSupply()


def test_cpamm_token_addresses(deployed_contracts):
    token_a, token_b, cpamm = deployed_contracts
    assert cpamm.tokenA() == token_a.address
    assert cpamm.tokenB() == token_b.address
