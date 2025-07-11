import pytest
from ape import accounts, project


@pytest.fixture
def deployer():
    return accounts.test_accounts[0]


@pytest.fixture
def user():
    return accounts.test_accounts[1]


@pytest.fixture
def setup(deployer, user):
    # Deploy tokens
    tokenA = project.TokenA.deploy(sender=deployer)
    tokenB = project.TokenB.deploy(sender=deployer)

    # Deploy CPAMM
    cpamm = project.CPAMM.deploy(tokenA.address, tokenB.address, sender=deployer)

    # Transfer tokens to user
    tokenA.transfer(user, 1_000 * 10**18, sender=deployer)
    tokenB.transfer(user, 1_000 * 10**18, sender=deployer)

    # Approve CPAMM to spend tokens for both accounts
    tokenA.approve(cpamm.address, 2**256 - 1, sender=user)
    tokenB.approve(cpamm.address, 2**256 - 1, sender=user)

    tokenA.approve(cpamm.address, 2**256 - 1, sender=deployer)
    tokenB.approve(cpamm.address, 2**256 - 1, sender=deployer)

    return tokenA, tokenB, cpamm


def test_add_liquidity(setup, user):
    tokenA, tokenB, cpamm = setup

    tx = cpamm.addLiquidity(100 * 10**18, 200 * 10**18, sender=user)

    assert cpamm.totalSupply() > 0
    assert cpamm.balanceOf(user) > 0
    assert cpamm.reserveA() == 100 * 10**18
    assert cpamm.reserveB() == 200 * 10**18


def test_swap_A_for_B(setup, user):
    tokenA, tokenB, cpamm = setup
    cpamm.addLiquidity(100 * 10**18, 200 * 10**18, sender=user)

    bal_before = tokenB.balanceOf(user)
    amount_out = cpamm.swapAforB(10 * 10**18, sender=user)

    assert tokenB.balanceOf(user) > bal_before
    assert tokenA.balanceOf(user) < 990 * 10**18  # spent tokenA


def test_swap_B_for_A(setup, user):
    tokenA, tokenB, cpamm = setup
    cpamm.addLiquidity(100 * 10**18, 200 * 10**18, sender=user)

    bal_before = tokenA.balanceOf(user)
    amount_out = cpamm.swapBforA(20 * 10**18, sender=user)

    assert tokenA.balanceOf(user) > bal_before
    assert tokenB.balanceOf(user) < 980 * 10**18


def test_remove_liquidity(setup, user):
    tokenA, tokenB, cpamm = setup
    cpamm.addLiquidity(100 * 10**18, 100 * 10**18, sender=user)

    shares = cpamm.balanceOf(user)

    balA_before = tokenA.balanceOf(user)
    balB_before = tokenB.balanceOf(user)

    cpamm.removeLiquidity(shares, sender=user)

    balA_after = tokenA.balanceOf(user)
    balB_after = tokenB.balanceOf(user)

    assert balA_after > balA_before
    assert balB_after > balB_before
    assert cpamm.totalSupply() == 0
    assert cpamm.balanceOf(user) == 0


def test_get_prices(setup, user):
    tokenA, tokenB, cpamm = setup
    cpamm.addLiquidity(100 * 10**18, 200 * 10**18, sender=user)

    priceA = cpamm.getPriceTokenA()
    priceB = cpamm.getPriceTokenB()

    assert priceA == 2 * 10**18  # tokenB/tokenA = 2
    assert priceB == 0.5 * 10**18  # tokenA/tokenB = 0.5
