# OctoPrint-EnclosureHeaterCommand

This plugin listens for custom G-code commands starting with `@ENCLOSUREHEATER` and sends corresponding JSON payloads to a fixed API endpoint.

Supported commands:

- `@ENCLOSUREHEATER-ON`  
  → Sends: `{"HeaterArmed": true}`

- `@ENCLOSUREHEATER-OFF`  
  → Sends: `{"HeaterArmed": false}`

- `@ENCLOSUREHEATER-ON Ttt`  
  → Sends: `{"HeaterArmed": true, "setpoint": tt}`

- `@ENCLOSUREHEATER-SET <json-data>`  
  → Sends the provided JSON payload

The API endpoint is fixed by default but can be changed in the plugin settings if needed.
# OctoPrint-EnclosureHeaterCommand
