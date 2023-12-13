# save-gpt-cli

Utility to preserve AI conversations using [gpt-cli](https://github.com/kharvd/gpt-cli)

### Features

- Saves as cleaned up Markdown document
- Save up to the start of the last session, or since the last time you cleared
- Remove all the logging metadata from the output
- Improve readability by better identifying user input from agent response
  - First line of user input is bolded and begins with `>>>`
  - White space and `===` added between end of user input and start of agent
  response
  - Close unfinished code blocks due to aborting agent response with `ctrl-c`

### Requirements

1. Install gpt-cli
1. Download and save `save-gpt-cli.py` somewhere on your file system
   ([instructions](https://github.com/kharvd/gpt-cli/blob/main/README.md#installation))
1. Use a log file (with the `--log_file` option or by setting the `log_file`
   setting in the [config
yaml](https://github.com/kharvd/gpt-cli/blob/main/README.md#Configuration))

### Usage

```shell
py save-gpt-cli.py {session,clear} [-h] input_file output_file
```

Commands:

- `session` save up to the start for the last session
- `clear` save up to the last time you cleared the conversation
