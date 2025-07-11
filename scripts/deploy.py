from ape import accounts, project
from ape.cli import ConnectedProviderCommand
import click


@click.command(cls=ConnectedProviderCommand)
@click.option("--sender", default=None, help="Deployer account alias (defaults to first local account).")
def cli(sender: str, ecosystem, network, provider):
    """
    Deploys TokenA, TokenB, and CPAMM contracts in sequence.
    """

    click.echo(f"Connected to {ecosystem.name}:{network.name} using provider '{provider.name}'.")

    deployer = sender if sender else accounts.test_accounts[0]
    print(deployer.balance)

    print(f"Deploying contracts using: {deployer.address}")

    # Deploy TokenA
    print("Deploying TokenA...")
    token_a = project.TokenA.deploy(sender=deployer, ecosystem=ecosystem, network=network, provider=provider)
    print(f"TokenA deployed at: {token_a.address}")

    # Deploy TokenB
    print("Deploying TokenB...")
    token_b = project.TokenB.deploy(sender=deployer, ecosystem=ecosystem, network=network, provider=provider)
    print(f"TokenB deployed at: {token_b.address}")

    # Deploy CPAMM using the deployed token addresses
    print("Deploying CPAMM liquidity pool...")
    cpamm = project.CPAMM.deploy(
        token_a.address, token_b.address, sender=deployer, ecosystem=ecosystem, network=network, provider=provider
    )
    print(f"CPAMM deployed at: {cpamm.address}")

    # Final report
    print("\nDeployment Summary:")
    print(f"TokenA: {token_a.address}")
    print(f"TokenB: {token_b.address}")
    print(f"CPAMM:  {cpamm.address}")
