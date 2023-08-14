# CliServer
An API that turns your shell into a powerful and customisable backend with just one simple configuration file.

## Deployment and configuration
### Requirements

- *nix or windows system
- Python 3.6+ 
- 30 MB of free RAM (but depends on the amount of ram used by called programs and the used WSGI server)
- 1 CPU core (depending on the programs that are called)

### Usage
To start the program, run `python cliserver.py /path/to/config/file.json`

To start the program using docker, run `docker run -p 9999:9999 -v /path/to/config/file.json:/config.json ghcr.io/nekoluka/cliserver:main`

### Configuration

#### Example:
```json
{
    "host": "0.0.0.0",
    "port": 9999,
    "routes": {
        "/hello": {
            "method": "GET",
            "params": ["message"],
            "return_stdout": true,
            "commands": [
                {
                    "command": "echo {message}",
                    "pipe_to_stdin": true,
                    "expected_return_code": 0,
                    "return_stderr_on_error": true
                },
                {
                    "command": "base64"
                }
            ]
        },
        "/date": {
            "method": "GET",
            "commands": [
                {
                  "command": "date"
                }
            ]
        }
    },
    "default_responses": {
        "404": {
          "type": "string",
          "text": "This path was not found :)"
        }
    }
}
```
The first command is equal to `echo {message} | base64`.

#### General options  

- host (str): The hostname to listen on when using the builtin WSGI server (default: 0.0.0.0).
- port (int): The port to listen on when using the builtin WSGI server (default: 9999).
- routes (obj): An object with keys being the endpoint url, e.g '/hello' and as value the configuration of what the endpoint should do (at least one route is required).
- default_responses (obj): An object with the keys being an HTTP response code and the values being what to put as the body when the status codes are used.

#### Routes options

- method (str): What HTTP method this route listens to (default: GET).
- params (list): A list of strings which are keys found in either the query string or request body (supported content types: JSON), whose value is passed to the command (note: values from duplicate keys are concatenated with spaces).
- return_stdout (bool): If the output of STDOUT should be returned when the command chain finishes successfully (default: true).
- commands (list): A list of objects containing the definitions for the commands that need to be executed (at least one route is required).

#### Commands options

- command (str): The command to execute (required).
- stdin (string): The name of the parameter that should be piped to STDIN (don't use if you used pipe_to_stdin in the previous command).
- pipe_to_stdin (bool): Signal if STDOUT from the current command should be piped to STDIN of the next command (default: false).
- expected_return_code (int): The expected return code to check against if the command failed or not (default: 0).
- return_stderr_on_err (bool): If the output of STDERR should be returned when the command fails (default: true).

#### Default response options

- type (string): A string literal that identifies to use the 'text' field to generate output for the code (required).
- text (str): The text that is put in the response body (required).

## Testing
To run all tests, run `python tests.py`

## Roadmap

- Put the program into a docker image.
- Add more accepted request body types.
- Add files for accepted default responses.
- Support to run commands as different users on the system.
- Sanitize input to prevent command injections.
- Add possible authentication to endpoints
- Add testing cases
- Add ctrl+C exit functionality
- Static file serving
