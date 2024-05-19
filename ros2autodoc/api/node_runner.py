from ros2pkg.api import PackageNotFound
from ros2run.api import MultipleExecutables, get_executable_path, run_executable


class NodeRunner:
    def __init__(self):
        pass

    def run(self, package_name, executable_name):
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
        return run_executable(path=path, argv=[])
