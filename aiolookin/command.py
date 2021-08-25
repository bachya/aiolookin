"""Define endpoints to manage commands and their data."""
from typing import Any, Awaitable, Callable, Dict, List, Optional, cast

from .errors import CommandError


class Command:
    """Define a command data object."""

    def __init__(self, async_request: Callable[..., Awaitable]) -> None:
        """Initialize."""
        self._async_request = async_request

    async def async_get_command_list(self) -> List[str]:
        """Get the list of commands supported by the device."""
        commands = await self._async_request("get", "commands")
        return cast(List[str], commands)

    async def async_get_command_action_list(self, command: str) -> List[str]:
        """Get the list of actions that a command can trigger."""
        actions = await self._async_request("get", f"commands/{command}")
        return cast(List[str], actions)

    async def async_send_command(
        self, command: str, action: str, *, operand: Optional[str] = None
    ) -> Dict[str, Any]:
        """Send a command/action (plus optional parameter)."""
        command_list = await self.async_get_command_list()
        if command not in command_list:
            raise CommandError(f"Unknown command: {command}")

        action_list = await self.async_get_command_action_list(command)
        if action not in action_list:
            raise CommandError(f'Unknown action for command "{command}": {action}')

        response = await self._async_request(
            "post",
            "commands",
            json={"command": command, "action": action, "operand": operand},
        )
        return cast(Dict[str, Any], response)
