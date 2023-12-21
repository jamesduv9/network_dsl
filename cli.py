"""
Author: James Duvall
Purpose: CLI interaction with yaml files, creates ConfigInterface objects
 and sends commands if specified
Notes: This will eventually be called by gitlab CI/CD to start the process
"""

from pathlib import Path
import click
from configuration_models.ios_xe.configinterface import ConfigInterface

BASE_DIR = Path(__file__).resolve().parent


@click.group()
def menu():
    """
    Just the menu to combine other click commands
    """


@click.command(name="build_model_directory")
@click.option("--debug", help="Enable debug on ncclient operations", is_flag=True)
@click.option(
    "--directory", help="Path to directory where all configs live", required=True
)
@click.option(
    "--environment",
    help="Select which environment to send the configs to",
    type=click.Choice(["prod", "lab"]),
    required=True,
)
def build_model_directory(directory: str, debug: bool, environment: str) -> None:
    """
    Accepts a directory and creates configuration objects for each, followed by
    sending configuration to the device specified in the yaml
    """
    direct = Path(directory)
    # NETCONF doesn't complete all configs on first run... doubling up
    for _ in range(2):
        print(_)
        threads = []  # List to keep track of threads

        for file in direct.resolve().iterdir():
            if str(file).endswith(".yml"):
                # Define the thread's target function inside the loop
                interface = ConfigInterface(file_=file, base_dir=BASE_DIR)
                    # print(interface.print_config())
                interface.send_config(
                    config=interface.print_config(),
                    host=interface.config.get("device").get(f"device_{environment}_ip"),
                    debug=debug,
                )

                # Create and start a new thread for each file
                # thread = threading.Thread(target=thread_function, args=(file, debug))
                # thread.start()
                # threads.append(thread)

        # # Wait for all threads to complete
        # for thread in threads:
        #     thread.join()


@click.command(name="build_model_solo")
@click.option("--file", help="path to yaml file", required=True)
@click.option("--send_command", help="Send edit-rpc to specified device", is_flag=True)
@click.option(
    "--multi_stage",
    help="Send one ncclient operation at a time instead of one big RPC",
    is_flag=True,
)
@click.option("--debug", help="Enable debug on ncclient operations", is_flag=True)
def build_model_solo(
    file: str, send_command: bool, multi_stage: bool, debug: bool
) -> None:
    """
    Takes yaml file input and create subordinate python models
    """
    test = ConfigInterface(file_=file, base_dir=BASE_DIR)
    if send_command:
        if multi_stage:
            for config in test.config_objects.values():
                for _ in range(2):
                    test.send_config(
                        config=config.print_config(),
                        host=test.config.get("device").get("device_lab_ip"),
                        debug=debug,
                    )
        else:
            for _ in range(2):
                test.send_config(
                    config=test.final_rpc,
                    host=test.config.get("device").get("device_lab_ip"),
                    debug=debug,
                )


if __name__ == "__main__":
    menu.add_command(build_model_directory)
    menu.add_command(build_model_solo)
    menu()
