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

        # Run in its own process group so any children it spawns (e.g. a
        # component container and the nodes loaded into it by a launch file)
        # can be signaled together and don't outlive the launch process.
        popen_kwargs = {}
        if os.name == "nt":
            popen_kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
        else:
            popen_kwargs["start_new_session"] = True

        self.process = subprocess.Popen(
            cmd,
            shell=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            **popen_kwargs,
        )
        return self

    def stop(self):
        if self.process is None:
            return
        self._signal_group(signal.CTRL_BREAK_EVENT if os.name == "nt" else signal.SIGINT)
        try:
            self.process.wait(timeout=5.0)
        except subprocess.TimeoutExpired:
            self._kill_group()
            self.process.wait()
        self.process = None

    def _signal_group(self, sig):
        if os.name == "nt":
            self.process.send_signal(sig)
        else:
            try:
                os.killpg(os.getpgid(self.process.pid), sig)
            except ProcessLookupError:
                pass

    def _kill_group(self):
        if os.name == "nt":
            self.process.kill()
        else:
            try:
                os.killpg(os.getpgid(self.process.pid), signal.SIGKILL)
            except ProcessLookupError:
                pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.stop()
        return False
