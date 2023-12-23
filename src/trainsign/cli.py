import os
import sys

import fire


class TrainSignCLI:
    def __init__(self, config_path: os.PathLike = "./trainsign.yml"):
        self._config_path = config_path

    def start_sign(self):
        raise NotImplementedError()

    def systemd(self) -> str:
        unit_template = """[Unit]
Description=trainsign

[Service]
ExecStart="{interpreter} {script} -c {config} run_sign"

[Install]
WantedBy=multi-user.target"""
        this_script = os.path.realpath(__file__)

        return unit_template.format(
            interpreter=sys.executable,
            script=os.path.realpath(__file__),
            config=self._config_path,
        ).strip()


def main():
    fire.Fire(TrainSignCLI)


if __name__ == "__main__":
    main()
