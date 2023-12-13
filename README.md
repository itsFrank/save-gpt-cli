# save-gpt-cli

Utility to preserve AI conversations using [gpt-cli](https://github.com/kharvd/gpt-cli)

### requirements

1. install gpt-cli
1. download and save `save-gpt-cli.py` somewhere on your file system
   ([instructions](https://github.com/kharvd/gpt-cli/blob/main/README.md#installation))
1. Use a log file (with the `--log_file` option or by setting the `log_file`
   setting in the [config
yaml](https://github.com/kharvd/gpt-cli/blob/main/README.md#Configuration))

### usage

```shell
py save-gpt-cli.py {session,clear} [-h] input_file output_file
```

Commands:

- `session` save up to the start for the last session
- `clear` save up to the last time you cleared the conversation
