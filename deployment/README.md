# Instructions for Production Deployment

Deploying the gardenpi as a service that runs every time the Raspberry Pi boots is quite straight-forward and only requires a few steps, detailed below:

1. Ensure you have created your own `settings.ini` file (copied and modified from `settings.sample.ini`).
1. Review and edit `gardenpi.service`. Be certain to adjust the paths both for `WorkingDirectory` and `ExecStart` for your system.
1. Be certain that the paths above are in the same directory as your modified `settings.ini` file
1. Copy the file to the `/lib/systemd/system/` directory
1. Tell the OS to re-scan that directory via `sudo systemctl daemon-reload`
1. Enable the service (auto start) via `sudo systemctl enable gardenpi`
1. Start the service: `sudo systemctl start gardenpi`
1. Check if everything is ok: `sudo systemctl status gardenpi`