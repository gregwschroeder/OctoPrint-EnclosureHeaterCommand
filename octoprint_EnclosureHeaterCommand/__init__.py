# coding=utf-8
from __future__ import absolute_import
import octoprint.plugin
import requests
import json

class EnclosureHeaterCommandPlugin(octoprint.plugin.StartupPlugin,
                                   octoprint.plugin.SettingsPlugin,
                                   octoprint.plugin.TemplatePlugin):

    def on_gcode_received(self, comm, line, parsed):
        stripped = line.strip()
        if stripped.startswith("@ENCLOSUREHEATER"):
            self._logger.info("Enclosure Heater command detected: %s", stripped)
            payload = None
            try:
                # Handle @ENCLOSUREHEATER-ON [optional T<temperature>]
                if stripped.startswith("@ENCLOSUREHEATER-ON"):
                    payload = {"HeaterArmed": True}
                    parts = stripped.split()
                    # Look for an extra token starting with 'T'
                    if len(parts) > 1:
                        for part in parts[1:]:
                            if part.upper().startswith("T"):
                                try:
                                    temp_value = float(part[1:])
                                    payload["setpoint"] = int(temp_value)  # or use float(temp_value) if needed
                                except ValueError:
                                    self._logger.error("Invalid temperature value in command: %s", part)
                                break

                # Handle @ENCLOSUREHEATER-OFF
                elif stripped.startswith("@ENCLOSUREHEATER-OFF"):
                    payload = {"HeaterArmed": False}

                # Handle @ENCLOSUREHEATER-SET <json-data>
                elif stripped.startswith("@ENCLOSUREHEATER-SET"):
                    json_part = stripped[len("@ENCLOSUREHEATER-SET"):].strip()
                    try:
                        payload = json.loads(json_part)
                    except Exception as e:
                        self._logger.error("Error parsing JSON from @ENCLOSUREHEATER-SET: %s", e)
                        payload = None
                else:
                    self._logger.warn("Unknown Enclosure Heater command: %s", stripped)
                
                if payload is not None:
                    api_url = self._settings.get(["api_url"], "http://fileserver5.localnet:1880/api/v1/enclosureheater/setparams")
                    self._logger.info("Sending API request to %s with payload: %s", api_url, payload)
                    response = requests.post(api_url, json=payload, timeout=5)
                    self._logger.info("API response: %s %s", response.status_code, response.text)
            except Exception as e:
                self._logger.error("Error processing Enclosure Heater command: %s", e)
        return line

    def get_settings_defaults(self):
        return {
            "api_url": "http://fileserver5.localnet:1880/api/v1/enclosureheater/setparams"
        }

    def get_template_configs(self):
        return [dict(type="settings", custom_bindings=False)]

    def on_after_startup(self):
        self._logger.info("Enclosure Heater Command Plugin started")

    ##-- Software Update Information (optional)
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

# Use the "received" hook with a lower (earlier) priority (e.g. -10)
__plugin_hooks__ = {
    "octoprint.comm.protocol.gcode.received": (__plugin_implementation__.on_gcode_received, -10)
}
