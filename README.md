# LinkedIn Toggler

This project is a Selenium based automation that aims to help programming repetitive LinkedIn tasks. To do that, a script with the Selenium routines is provided together with a Dockerfile with a simple image that executes a crontab. For now, a single script has been implemented to turn on/off the #OpenToWork frame.

Please feel free to fork or contribute to this project. Keep in mind this is a personal project, feedback is more than welcome.

## Getting started

Please follow the next steps to call the script in your system:

### Setup local

1. Open a terminal and clone the repository using: `git clone https://github.com/mbalos16/linkedin_toggler.git`
2. Navigate to the cloned folder using the `cd` command.
3. Create a new file with the name `secrets.json` in the root of the repository where you will add your LinkedIn credentials:

```
{
    "email" : "<LinkedIn email>",
    "pass" : "<LinkedIn password>"
}
```

4. Create a new python environment using the following command: `python -m venv .venv`
5. Activate the python environment with `source .venv/bin/activate`
6. Install the requirements by using `pip install -r requirements.txt`

#### Example of local run

Set your LinkedIn as #OpenToWork:

```
python main.py --open
```

Turn down #OpenToWork:

```
python main.py --close
```

### Setup Docker

1. Build the image with the following command: `docker build -t <image_tag> .`
2. Run a container with the image by using: `docker run -it -v $(pwd/logs):/app/logs <image_tag>`

### Adjust schedules

To modify the open and close schedules edit the crontab configuration in `configure_crontabs.sh`.

## Contribution

Pull requests and issues are welcome.

## Licence

This repository is licensed under CC0. More info in the LICENSE file.

Copyright (c) 2024 Maria Magdalena Balos
