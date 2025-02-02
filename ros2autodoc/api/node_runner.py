import os
import signal
import subprocess
import sys

from ros2pkg.api import PackageNotFound
from ros2run.api import MultipleExecutables, get_executable_path


class NodeRunner:
    def __init__(self):
        self.process = None

    def start(self, package_name, executable_name=None, launch_file=None):
        """Start a node either using ros2 run or ros2 launch."""
        if executable_name:
            try:
                path = get_executable_path(
                    package_name=package_name, executable_name=executable_name
                )
            except PackageNotFound:
                raise RuntimeError(f"Package '{package_name}' not found")
            except MultipleExecutables as e:
                msg = "Multiple executables found:"
                for p in e.paths:
                    msg += f"\n- {p}"
                raise RuntimeError(msg)
            if path is None:
                return "No executable found"

            cmd = [path]

            # on Windows Python scripts are invocable through the interpreter
            if os.name == "nt" and path.endswith(".py"):
                cmd.insert(0, sys.executable)

        elif launch_file:
            cmd = ["ros2", "launch", package_name, launch_file]

        self.process = subprocess.Popen(
            cmd, shell=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

    def stop(self):
        self.process.send_signal(signal.SIGINT)
