#!/usr/bin/env python3

from sys import argv
from command import CMD
from ui import UI
from ui import print_error, promt_missing_files, print_help


class APP:
    def run(self):
        try:
            cmd = CMD(" ".join(argv[1:]))
        except ValueError as err:
            print_error(err)
            print_help()
            
        else:
            ui = UI(cmd)
            try:
                cmd.compile()
            except Exception as err:
                missing_files = promt_missing_files()
                try:
                    cmd.compile(missing_files)
                except Exception as err:
                    print_error(err)
                    cmd.cleanup()
                else:
                    ui.raport()
                    cmd.cleanup()
            else:
                ui.raport()
                cmd.cleanup()


if __name__ == "__main__":
    app = APP()
    app.run()

# TODO
# help
# tests