from pathlib import Path
from os import listdir
from os.path import exists

import subprocess


class CMD:
    def __init__(self, cmd: str):
        self.args = {
            "source_file": "",
            "test_file": "",
        }
        self.flags = {
            "raport": False,
            "errors": False,
        }
        self.validate(cmd)

    def validate(self, cmd: str):
        command_parts = cmd.strip().split()
        if len(command_parts) < 2:
            raise ValueError("To few arguments")
        for arg in command_parts:
            if arg == "--raport" or arg == "-r":
                self.flags["raport"] = True
            elif arg == "--error" or arg == "-e":
                self.flags["errors"] = True
            elif arg.startswith("--") or arg.startswith("-"):
                raise ValueError(f"The `{arg}` flag does not exist")
            elif not exists(Path(arg)):
                raise ValueError(f"`{arg}` is not a valid path")
            else:
                if not self.args["source_file"]:
                    self.args["source_file"] = Path(arg)
                elif not self.args["test_file"]:
                    self.args["test_file"] = Path(arg)
                else:
                    raise ValueError(f"Too many arguments, the source file is `{self.args.get('source_file')}` and the test file is `{self.args.get('test_file')}`")

    def compile(self, extra_files=[]):
        command = [
            "g++", 
            "-fprofile-arcs", 
            "-ftest-coverage",
            "-o",
            "cov",
            self.args["source_file"],
            self.args["test_file"],
            *extra_files,
        ]

        if self.flags["errors"]:
            subprocess.run(command)
        else:
            subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

        subprocess.run([
            "./cov"
        ])
        
        file_name = str(self.args['source_file']).split("/")[-1]
        subprocess.run([
                "gcov",
                f"cov-{file_name}"
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
        )

    def cleanup(self):
        files_to_delete = [file for file in listdir() if file.endswith(".gcda") or file.endswith(".gcno") or file.endswith(".gcov")]
        files_to_delete.append("cov")
        if self.flags["raport"]:
            file_name = str(self.args['source_file']).split("/")[-1]
            try:
                files_to_delete.remove(f"{file_name}.gcov")
            except ValueError:
                pass

        for file in files_to_delete:
            subprocess.run([
                "rm",
                file,
            ])
