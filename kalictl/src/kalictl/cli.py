#!/usr/bin/env python3

from typing import Optional
import typer
import os
from kalictl import __app_name__, __version__, config, ERRORS
from kalictl.handler import DockerHandler

app = typer.Typer()
handler = DockerHandler()

@app.command()
def init(
    username: str = typer.Option(
        str(os.getenv('USER')),
        '--username',
        '-u',
        prompt="Enter Username of Kali Container"
    )
) -> None:
    """
    Initializes the config file for future references
    """
    app_init_error = config.init_app(username)
    if app_init_error:
        typer.secho(
            f'Creating config file failed with "{ERRORS[app_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"Config file written at {config.CONFIG_FILE_PATH}", fg=typer.colors.GREEN)

@app.command()
def start() -> None:
    """
    Starts the stack
    """
    handler.start_stack()

@app.command()
def stop() -> None:
    """
    Stops the stack
    """
    handler.stop_stack()

@app.command()
def restart() -> None:
    """
    Restarts the stack
    """
    handler.restart_stack()

@app.command()
def build() -> None:
    """
    Builds the Docker images in the stack
    """
    handler.build_stack()

@app.command()
def status() -> None:
    """
    Shows the status of the stack
    """
    handler.get_stack_state()

@app.command()
def exec(
    command: str = typer.Argument(
        ...,
        help="Command to execute in the container"
    ),
    container_name: str = typer.Option(
        'kali',
        '--container',
        '-c',
        help="Container to execute command in"
    )
) -> None:
    """
    Executes a command in the container
    """
    handler.exec_in_stack(command, container_name)

@app.command()
def cp(
    src_path: str = typer.Argument(
        ...,
        help="Source path to copy from"
    ),
    dest_path: str = typer.Argument(
        ...,
        help="Destination path to copy to"
    ),
    container_name: str = typer.Option(
        'kali',
        '--container',
        '-c',
        help="Container to copy from"
    ),
    reverse: bool = typer.Option(
        False,
        '--reverse',
        '-r',
        help="Copy from container to host instead of host to container"
    )
) -> None:
    """
    Copies files from the host to the container or vice versa
    """
    if reverse:
        handler.copy_from_stack(src_path, dest_path, container_name)
    else:
        handler.copy_to_stack(src_path, dest_path, container_name)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()

@app.callback()
def main(
        version: Optional[bool] = typer.Option(
            None,
            "--version",
            "-v",
            help="Show the Application's version and exit",
            callback=_version_callback,
            is_eager=True
        )
) -> None:
    return