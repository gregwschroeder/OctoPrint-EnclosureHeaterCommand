# coding=utf-8
from __future__ import absolute_import
import octoprint.plugin
import requests
import json

class EnclosureHeaterCommandPlugin(octoprint.plugin.StartupPlugin,
                                   octoprint.plugin.SettingsPlugin,
                                   octoprint.plugin.TemplatePlugin):

    def on_atcommand_queuing(self, comm, phase, command, parameters, tags=None, *args, **kwargs):
        # Process only during the queuing phase.
        if phase != "queuing":
            return
        # Only process commands that start with ENCLOSUREHEATER.
        if not command.startswith("ENCLOSUREHEATER"):
            return

        self._logger.info("Enclosure Heater @ command detected in queuing phase: %s with parameters: %s", command, parameters)
        payload = None

        if command == "ENCLOSUREHEATER-ON":
            payload = {"HeaterArmed": True}
            # If parameters begin with "T", assume it's a temperature.
            if parameters.strip().upper().startswith("T"):
                try:
                    temp_value = float(parameters.strip()[1:])
                    payload["setpoint"] = int(temp_value)
                except ValueError:
                    self._logger.error("Invalid temperature value in parameters: %s", parameters)
        elif command == "ENCLOSUREHEATER-OFF":
            payload = {"HeaterArmed": False}
        elif command == "ENCLOSUREHEATER-SET":
            try:
                payload = json.loads(parameters)
            except Exception as e:
                self._logger.error("Error parsing JSON for ENCLOSUREHEATER-SET: %s", e)
                payload = None
        else:
            self._logger.warn("Unknown ENCLOSUREHEATER command: %s", command)

        if payload is not None:
            # Retrieve the API URL from settings, or use our default.
            api_url = self._settings.get(["api_url"]) or "http://fileserver5.localnet:1880/api/v1/enclosureheater/setparams"
            self._logger.info("Sending API request to %s with payload: %s", api_url, payload)
            try:
                response = requests.post(api_url, json=payload, timeout=5)
                self._logger.info("API response: %s %s", response.status_code, response.text)
            except Exception as e:
                self._logger.error("Error sending API request: %s", e)
        return

    def get_settings_defaults(self):
        return {
            "api_url": "http://fileserver5.localnet:1880/api/v1/enclosureheater/setparams"
        }

    def get_template_configs(self):
        return [dict(type="settings", custom_bindings=False)]

    def on_after_startup(self):
        self._logger.info("Enclosure Heater Command Plugin started (AT Command Queuing Hook)")

    def get_update_information(self):
        return {
            "enclosureheatercommand": {
                "displayName": "Enclosure Heater Command Plugin",
                "displayVersion": self._plugin_version,
                "type": "github_release",
                "user": "gregwschroeder",         
                "repo": "https://github.com/gregwschroeder/OctoPrint-EnclosureHeaterCommand",
                "current": self._plugin_version,
                "pip": "https://github.com/your_github_username/OctoPrint-EnclosureHeaterCommand/archive/{target_version}.zip"
            }
        }

__plugin_name__ = "Enclosure Heater Command Plugin"
__plugin_pythoncompat__ = ">=2.7,<4"
__plugin_implementation__ = EnclosureHeaterCommandPlugin()

# Register our hook for the atcommand.queuing phase with priority -100 so it runs early.
__plugin_hooks__ = {
    "octoprint.comm.protocol.atcommand.queuing": (__plugin_implementation__.on_atcommand_queuing, -100)
}
