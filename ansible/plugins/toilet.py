# callback_plugins/toilet_play.py

from ansible.plugins.callback import CallbackBase
from ansible.utils.display import Display
import subprocess

display = Display()

class CallbackModule(CallbackBase):
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'stdout'
    CALLBACK_NAME = 'toilet_play'

    def _toilet(self, text):
        try:
            return subprocess.check_output(
                ["toilet", "-f", "future", "--metal", text],
                text=True
            )
        except Exception:
            return text

    # Только PLAY через toilet
    def v2_playbook_on_play_start(self, play):
        if play.get_name():
            msg = f"PLAY [{play.get_name()}]"
            display.display(self._toilet(msg))

    # Всё остальное выводим стандартно
    def v2_playbook_on_task_start(self, task, is_conditional):
        display.display(f"TASK [{task.get_name()}]")

    def v2_runner_on_ok(self, result):
        display.display(f"ok: [{result._host.get_name()}]")

    def v2_runner_on_failed(self, result, ignore_errors=False):
        display.display(f"failed: [{result._host.get_name()}]")

    def v2_runner_on_changed(self, result):
        display.display(f"changed: [{result._host.get_name()}]")

    def v2_runner_on_skipped(self, result):
        display.display(f"skipped: [{result._host.get_name()}]")