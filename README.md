# USER GUIDE
## SETUP

### Docker desktop
Project uses docker desktop, which can be downloaded through microsoft store.<br>
You might need to restart your computer to complete the configuration.

### UV
Project uses a virtual environment for python managed with uv, Astrals manager for virtual environments.<br>
Download link: [here](https://docs.astral.sh/uv/getting-started/installation/#installation-methods)

When installed run the following commands in the root folder of the directory:<br>
`uv venv`<br>
`.venv/scripts/activate`<br>
`uv sync`<br>

## Running the microkernel
### Running the venv
Make sure the virtual environment is running, if not run `.venv/scripts/activate` again

### Running the MQTT broker
Launch Docker desktop. <br>
After it is running run `docker compose up` inside the terminal with the virtual environment active

### Running the microkernel
Open another terminal window with the virtual environment active. then run `uv run main.py`

## Enjoy the application
The project should work when run in this way, and should automatically run any and all plugins in micro-kernel/configs/app_configs.json<br>
To add another plugin, create another directory in the plugins folder, and create a plugin class inheriting the AbstractPlugin class <br>
Then add any functionality you want and subscribe to the topics you need. If you want communication accross different plugins, have several subscribe to the same topics.