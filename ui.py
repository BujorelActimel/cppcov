from command import CMD
from rich.progress import Progress, TextColumn, BarColumn, TimeRemainingColumn

import rich

class ProgressBar(Progress):
    def get_time(self):
        return ""


class UI:
    def __init__(self, cmd: CMD):
        self.cmd = cmd

    def raport(self):
        total_lines = 0
        executed_lines = 0
        file_name = str(self.cmd.args['source_file']).split("/")[-1]
        with open(f"{file_name}.gcov") as f:
            lines = f.readlines()
            for line in lines:
                if line.strip()[0].isdigit():
                    total_lines += 1
                    executed_lines += 1
                elif line.strip().startswith("#####"):
                    total_lines += 1

        coverage = round((executed_lines/total_lines) * 100, 2)

        if coverage > 80:
            color = "green"
        else:
            color = "red"

        rich.print(f"Coverage for [bold cyan]`{file_name}`[/bold cyan]: [bold {color}]{coverage}%[/bold {color}]")
        rich.print(f"[bold {color}]{executed_lines} lines covered out of {total_lines}[/bold {color}]")
        with ProgressBar(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=50), # ??? if it looks like shit, do bar_width=None
            "[progress.percentage]{task.percentage:>3.0f}%",
        ) as progress:
            task = progress.add_task(f"[{color}]Test Coverage", total=total_lines)

            progress.update(task, completed=executed_lines)


def print_error(err: Exception):
    rich.print(f"[bold red]ERROR\n{err}[/bold red]")


def promt_missing_files():
    rich.print("[bold red]There might be missing imports, do you want to continue?(Y/n)", end=" ")
    option = input()
    if option.strip().lower() == "y":
        files = input("Missing files: ").strip().split()
        return files
    else:
        rich.print("[bold red]Aborted")
        exit()


def print_help():
    print("Usage: cppcov [options] <source_file> <test_file>")
    print("Options:")
    print("  --raport/-r: Generate a coverage report")
    print("Example:")
    print("  cppcov -r path/to/source/src_file.cpp path/to/tests/test_file.cpp")