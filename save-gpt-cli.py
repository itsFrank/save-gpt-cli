#!/usr/bin/env python3

import re
import argparse


clear_conversation_pattern = re.compile(
    r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} - .*? - (?:INFO|ERROR|WARNING|DEBUG) - Cleared the conversation\."
)
new_session_pattern = re.compile(
    r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} - .*? - (?:INFO|ERROR|WARNING|DEBUG) - Starting a new chat session\."
)


def remove_logging_metadata(input_file_path, output_file_path, start_pattern):
    # Define the regex pattern for the logging metadata
    log_metadata_pattern = re.compile(
        r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} - .*? - (?:INFO|ERROR|WARNING|DEBUG) - "
    )

    # Define the regex pattern for lines starting with "user:" or "assistant:"
    user_line_pattern = re.compile(r"^user:", re.IGNORECASE)
    assistant_line_pattern = re.compile(r"^assistant:", re.IGNORECASE)

    code_block_delimiter_pattern = re.compile(r"```")

    # Read the content of the file
    with open(input_file_path, "r") as infile:
        content = infile.readlines()

    # Find the index to start processing from
    start_index = 0
    for i in range(len(content) - 1, -1, -1):
        if start_pattern.search(content[i]):
            start_index = i + 1
            break

    code_block_delimeter_count = 0

    # Open the output file
    with open(output_file_path, "w") as outfile:
        # Process lines starting from the start index
        for line in content[start_index:]:
            # Remove the logging metadata using the regex pattern
            cleaned_line = log_metadata_pattern.sub("", line)
            if code_block_delimiter_pattern.match(cleaned_line):
                code_block_delimeter_count += 1
            # Check if the cleaned line starts with "user:" or "assistant:"
            if user_line_pattern.match(cleaned_line):
                formatted_line = f"\n\n**>>> {cleaned_line[len('user:'):].strip()}**\n\n"
                # close code blocks if left open
                if code_block_delimeter_count % 2 == 1:
                    formatted_line = "```\n" + formatted_line
                    code_block_delimeter_count += 1
                # Format the line for Markdown, remove the prefix, and bold the line
                outfile.write(formatted_line)
            elif assistant_line_pattern.match(cleaned_line):
                # Remove the "assistant:" prefix
                formatted_line = f"\n===\n\n{cleaned_line[len('assistant:'):].strip()}"
                outfile.write(formatted_line)
            elif not log_metadata_pattern.match(line):
                # Include lines that do not contain log metadata
                outfile.write(cleaned_line)

        # close the final code block if left open
        if code_block_delimeter_count % 2 == 1:
            outfile.write("```")

    print(
        f"Log metadata has been removed and the text has been formatted. Check the Markdown file in '{output_file_path}'."
    )


def main():
    # Create the top-level parser
    parser = argparse.ArgumentParser(description="GPT CLI for processing log files.")
    subparsers = parser.add_subparsers(
        dest="command", required=True, help="sub-command help"
    )

    # Create the parser for the "session" command
    parser_session = subparsers.add_parser("session", help="Process a full session.")
    parser_session.add_argument("input_file", help="Input file to process.")
    parser_session.add_argument(
        "output_file", help="Output file to save the processed data."
    )

    # Create the parser for the "clear" command
    parser_last_clear = subparsers.add_parser(
        "clear", help="Process logs since last clear."
    )
    parser_last_clear.add_argument("input_file", help="Input file to process.")
    parser_last_clear.add_argument(
        "output_file", help="Output file to save the processed data."
    )

    # Parse the arguments
    args = parser.parse_args()

    # Handle the commands
    if args.command == "session":
        handle_session(args.input_file, args.output_file)
    elif args.command == "clear":
        handle_last_clear(args.input_file, args.output_file)


def handle_session(input_file, output_file):
    remove_logging_metadata(input_file, output_file, new_session_pattern)


def handle_last_clear(input_file, output_file):
    remove_logging_metadata(input_file, output_file, clear_conversation_pattern)


if __name__ == "__main__":
    main()
