
from typing import Any

from android_world.env import interface
from android_world.task_evals import task_eval
from android_world.task_evals.single import system
from android_world.task_evals.utils import schema
from android_world.task_evals.single import  clock
from absl import logging




class _System(task_eval.TaskEval):
  """Base class for clock tasks."""

  app_names = ("settings",)

class TurnOffWifiAndTurnOnBluetoothAndClockTimerEntry(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {
      "type": "object",
      "properties": {
          "hours": {"type": "integer"},
          "minutes": {"type": "integer"},
          "seconds": {"type": "integer"},
      },
      "required": ["hours", "minutes", "seconds"],
  }

  template = ("Turn off WiFi, then enable bluetooth,  then "
              "Create a timer with {hours} hours, {minutes} minutes, and {seconds}"
                " seconds. Do not start the timer.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_off_wifi_task = system.SystemWifiTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_wifi_task.initialize_task(env)
    self.turn_on_bluetooth_task = system.SystemBluetoothTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_bluetooth_task.initialize_task(env)
    self.clock_task = clock.ClockTimerEntry(
       params={"hours": self.params["hours"],
                    "minutes": self.params["minutes"],
                    "seconds": self.params["seconds"]
                    }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (wifi_score + bluetooth_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        clock_params = clock.ClockTimerEntry.generate_random_params()
        return clock_params

class TurnOnWifiAndTurnOnBluetoothAndClockTimerEntry(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {
      "type": "object",
      "properties": {
          "hours": {"type": "integer"},
          "minutes": {"type": "integer"},
          "seconds": {"type": "integer"},
      },
      "required": ["hours", "minutes", "seconds"],
  }

  template = ("Turn on WiFi, then enable bluetooth, then "
              "Create a timer with {hours} hours, {minutes} minutes, and {seconds}"
                " seconds. Do not start the timer.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_off_wifi_task = system.SystemWifiTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_off_wifi_task.initialize_task(env)
    self.turn_on_bluetooth_task = system.SystemBluetoothTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_bluetooth_task.initialize_task(env)
    self.clock_task = clock.ClockTimerEntry(
       params={"hours": self.params["hours"],
                    "minutes": self.params["minutes"],
                    "seconds": self.params["seconds"]
                    }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (wifi_score + bluetooth_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        clock_params = clock.ClockTimerEntry.generate_random_params()
        return clock_params

class TurnOffWifiAndTurnOffBluetoothAndClockTimerEntry(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {
      "type": "object",
      "properties": {
          "hours": {"type": "integer"},
          "minutes": {"type": "integer"},
          "seconds": {"type": "integer"},
      },
      "required": ["hours", "minutes", "seconds"],
  }

  template = ("Turn on WiFi, then turn off the bluetooth, then "
              "Create a timer with {hours} hours, {minutes} minutes, and {seconds}"
                " seconds. Do not start the timer.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_off_wifi_task = system.SystemWifiTurnOff(
        params={"on_or_off": "on"}
    )
    self.turn_off_wifi_task.initialize_task(env)
    self.turn_on_bluetooth_task = system.SystemBluetoothTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_on_bluetooth_task.initialize_task(env)
    self.clock_task = clock.ClockTimerEntry(
       params={"hours": self.params["hours"],
                    "minutes": self.params["minutes"],
                    "seconds": self.params["seconds"]
                    }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (wifi_score + bluetooth_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        clock_params = clock.ClockTimerEntry.generate_random_params()
        return clock_params

class TurnOnWifiAndTurnOffBluetoothAndClockTimerEntry(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {
      "type": "object",
      "properties": {
          "hours": {"type": "integer"},
          "minutes": {"type": "integer"},
          "seconds": {"type": "integer"},
      },
      "required": ["hours", "minutes", "seconds"],
  }

  template = ("Turn on WiFi, then turn off bluetooth,and  then "
              "Create a timer with {hours} hours, {minutes} minutes, and {seconds}"
                " seconds. Do not start the timer.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_on_wifi_task = system.SystemWifiTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_wifi_task.initialize_task(env)
    self.turn_on_bluetooth_task = system.SystemBluetoothTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_on_bluetooth_task.initialize_task(env)
    self.clock_task = clock.ClockTimerEntry(
       params={"hours": self.params["hours"],
                    "minutes": self.params["minutes"],
                    "seconds": self.params["seconds"]
                    }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (wifi_score + bluetooth_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        clock_params = clock.ClockTimerEntry.generate_random_params()
        return clock_params

class TurnOffWifiAndBrightnessMinAndClockTimerEntry(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {
      "type": "object",
      "properties": {
          "hours": {"type": "integer"},
          "minutes": {"type": "integer"},
          "seconds": {"type": "integer"},
      },
      "required": ["hours", "minutes", "seconds"],
  }

  template = ("Turn off WiFi, then Turn brightness to the min value, then "
              "Create a timer with {hours} hours, {minutes} minutes, and {seconds}"
                " seconds. Do not start the timer.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_off_wifi_task = system.SystemWifiTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_wifi_task.initialize_task(env)
    self.turn_min_brightness_task = system.SystemBrightnessMin(
      params={'max_or_min': 'min'}
    )
    self.turn_min_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockTimerEntry(
       params={"hours": self.params["hours"],
                    "minutes": self.params["minutes"],
                    "seconds": self.params["seconds"]
                    }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (wifi_score + bright_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_min_brightness_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        clock_params = clock.ClockTimerEntry.generate_random_params()
        return clock_params

class TurnOnWifiAndBrightnessMinAndClockTimerEntry(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {
      "type": "object",
      "properties": {
          "hours": {"type": "integer"},
          "minutes": {"type": "integer"},
          "seconds": {"type": "integer"},
      },
      "required": ["hours", "minutes", "seconds"],
  }

  template = ("Turn on WiFi, then Turn brightness to the min value, then "
              "Create a timer with {hours} hours, {minutes} minutes, and {seconds}"
                " seconds. Do not start the timer.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_on_wifi_task = system.SystemWifiTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_wifi_task.initialize_task(env)
    self.turn_min_brightness_task = system.SystemBrightnessMin(
      params={'max_or_min': 'min'}
    )
    self.turn_min_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockTimerEntry(
       params={"hours": self.params["hours"],
                    "minutes": self.params["minutes"],
                    "seconds": self.params["seconds"]
                    }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (wifi_score + bright_score) + clock_success / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_min_brightness_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        clock_params = clock.ClockTimerEntry.generate_random_params()
        return clock_params

class TurnOffWifiAndBrightnessMaxAndClockTimerEntry(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {
      "type": "object",
      "properties": {
          "hours": {"type": "integer"},
          "minutes": {"type": "integer"},
          "seconds": {"type": "integer"},
      },
      "required": ["hours", "minutes", "seconds"],
  }

  template = ("Turn off WiFi, then Turn brightness to the max value, then "
              "Create a timer with {hours} hours, {minutes} minutes, and {seconds}"
                " seconds. Do not start the timer.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_off_wifi_task = system.SystemWifiTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_wifi_task.initialize_task(env)
    self.turn_max_brightness_task = system.SystemBrightnessMax(
      params={'max_or_min': 'max'}
    )
    self.turn_max_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockTimerEntry(
       params={"hours": self.params["hours"],
                    "minutes": self.params["minutes"],
                    "seconds": self.params["seconds"]
                    }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (wifi_score + bright_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_max_brightness_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        clock_params = clock.ClockTimerEntry.generate_random_params()
        return clock_params

class TurnOnWifiAndBrightnessMaxAndClockTimerEntry(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {
      "type": "object",
      "properties": {
          "hours": {"type": "integer"},
          "minutes": {"type": "integer"},
          "seconds": {"type": "integer"},
      },
      "required": ["hours", "minutes", "seconds"],
  }

  template = ("Turn on WiFi, then Turn brightness to the max value,  then "
              "Create a timer with {hours} hours, {minutes} minutes, and {seconds}"
                " seconds. Do not start the timer.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_on_wifi_task = system.SystemWifiTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_wifi_task.initialize_task(env)
    self.turn_max_brightness_task = system.SystemBrightnessMax(
      params={'max_or_min': 'max'}
    )
    self.turn_max_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockTimerEntry(
       params={"hours": self.params["hours"],
                    "minutes": self.params["minutes"],
                    "seconds": self.params["seconds"]
                    }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (wifi_score + bright_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_max_brightness_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        clock_params = clock.ClockTimerEntry.generate_random_params()
        return clock_params

class TurnOnBluetoothAndBrightnessMinAndClockTimerEntry(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {
      "type": "object",
      "properties": {
          "hours": {"type": "integer"},
          "minutes": {"type": "integer"},
          "seconds": {"type": "integer"},
      },
      "required": ["hours", "minutes", "seconds"],
  }

  template = ("Enable bluetooth, then Turn brightness to the min value, then "
              "Create a timer with {hours} hours, {minutes} minutes, and {seconds}"
                " seconds. Do not start the timer.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_min_brightness_task = system.SystemBrightnessMin(
      params={'max_or_min': 'min'}
    )
    self.turn_min_brightness_task.initialize_task(env)
    self.turn_on_bluetooth_task = system.SystemBluetoothTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_bluetooth_task.initialize_task(env)
    self.clock_task = clock.ClockTimerEntry(
       params={"hours": self.params["hours"],
                    "minutes": self.params["minutes"],
                    "seconds": self.params["seconds"]
                    }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (bluetooth_score + bright_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_min_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        clock_params = clock.ClockTimerEntry.generate_random_params()
        return clock_params

class TurnOnBluetoothAndBrightnessMaxAndClockTimerEntry(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {
      "type": "object",
      "properties": {
          "hours": {"type": "integer"},
          "minutes": {"type": "integer"},
          "seconds": {"type": "integer"},
      },
      "required": ["hours", "minutes", "seconds"],
  }

  template = ("Enable bluetooth, then Turn brightness to the max value, then "
              "Create a timer with {hours} hours, {minutes} minutes, and {seconds}"
                " seconds. Do not start the timer.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_max_brightness_task = system.SystemBrightnessMax(
      params={'max_or_min': 'max'}
    )
    self.turn_max_brightness_task.initialize_task(env)
    self.turn_on_bluetooth_task = system.SystemBluetoothTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_bluetooth_task.initialize_task(env)
    self.clock_task = clock.ClockTimerEntry(
       params={"hours": self.params["hours"],
                    "minutes": self.params["minutes"],
                    "seconds": self.params["seconds"]
                    }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (bright_score + bright_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_max_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        clock_params = clock.ClockTimerEntry.generate_random_params()
        return clock_params

class TurnOffBluetoothAndBrightnessMaxAndClockTimerEntry(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {
      "type": "object",
      "properties": {
          "hours": {"type": "integer"},
          "minutes": {"type": "integer"},
          "seconds": {"type": "integer"},
      },
      "required": ["hours", "minutes", "seconds"],
  }

  template = ("Turn off bluetooth, then Turn brightness to the max value "
            " then Create a timer with {hours} hours, {minutes} minutes, and {seconds}"
                " seconds. Do not start the timer.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_max_brightness_task = system.SystemBrightnessMax(
      params={'max_or_min': 'max'}
    )
    self.turn_max_brightness_task.initialize_task(env)
    self.turn_off_bluetooth_task = system.SystemBluetoothTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_bluetooth_task.initialize_task(env)
    self.clock_task = clock.ClockTimerEntry(
       params={"hours": self.params["hours"],
                    "minutes": self.params["minutes"],
                    "seconds": self.params["seconds"]
                    }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (bluetooth_score + bright_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_max_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        clock_params = clock.ClockTimerEntry.generate_random_params()
        return clock_params\

class TurnOffBluetoothAndBrightnessMinAndClockTimerEntry(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {
      "type": "object",
      "properties": {
          "hours": {"type": "integer"},
          "minutes": {"type": "integer"},
          "seconds": {"type": "integer"},
      },
      "required": ["hours", "minutes", "seconds"],
  }

  template = ("Turn off bluetooth, then Turn brightness to the min value  then "
              "Create a timer with {hours} hours, {minutes} minutes, and {seconds}"
                " seconds. Do not start the timer.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_min_brightness_task = system.SystemBrightnessMin(
      params={'max_or_min': 'min'}
    )
    self.turn_min_brightness_task.initialize_task(env)
    self.turn_off_bluetooth_task = system.SystemBluetoothTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_bluetooth_task.initialize_task(env)
    self.clock_task = clock.ClockTimerEntry(
       params={"hours": self.params["hours"],
                    "minutes": self.params["minutes"],
                    "seconds": self.params["seconds"]
                    }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (bluetooth_score + bright_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_min_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        clock_params = clock.ClockTimerEntry.generate_random_params()
        return clock_params

class TurnOnWifiAndTurnOnBluetoothAndBrightnessMaxAndClockTimerEntry(_System,clock._ClockEval):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {
      "type": "object",
      "properties": {
          "hours": {"type": "integer"},
          "minutes": {"type": "integer"},
          "seconds": {"type": "integer"},
      },
      "required": ["hours", "minutes", "seconds"],
  }

  template = ("Turn on WiFi, then enable bluetooth, also Turn brightness to the max value, then "
              "Create a timer with {hours} hours, {minutes} minutes, and {seconds}"
                " seconds. Do not start the timer.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_on_wifi_task = system.SystemWifiTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_wifi_task.initialize_task(env)
    self.turn_on_bluetooth_task = system.SystemBluetoothTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_bluetooth_task.initialize_task(env)
    self.turn_max_brightness_task = system.SystemBrightnessMax(
      params={'max_or_min': 'max'}
    )
    self.turn_max_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockTimerEntry(
       params={"hours": self.params["hours"],
                    "minutes": self.params["minutes"],
                    "seconds": self.params["seconds"]
                    }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +clock_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)
    self.turn_max_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        clock_params = clock.ClockTimerEntry.generate_random_params()
        return clock_params

class TurnOnWifiAndTurnOnBluetoothAndBrightnessMinAndClockTimerEntry(_System,clock._ClockEval):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {
      "type": "object",
      "properties": {
          "hours": {"type": "integer"},
          "minutes": {"type": "integer"},
          "seconds": {"type": "integer"},
      },
      "required": ["hours", "minutes", "seconds"],
  }

  template = ("Turn on WiFi, then enable bluetooth, also Turn brightness to the min value,  then "
              "Create a timer with {hours} hours, {minutes} minutes, and {seconds}"
                " seconds. Do not start the timer.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_on_wifi_task = system.SystemWifiTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_wifi_task.initialize_task(env)
    self.turn_on_bluetooth_task = system.SystemBluetoothTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_bluetooth_task.initialize_task(env)
    self.turn_min_brightness_task = system.SystemBrightnessMin(
      params={'max_or_min': 'min'}
    )
    self.turn_min_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockTimerEntry(
       params={"hours": self.params["hours"],
                    "minutes": self.params["minutes"],
                    "seconds": self.params["seconds"]
                    }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +clock_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)
    self.turn_min_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        clock_params = clock.ClockTimerEntry.generate_random_params()
        return clock_params

class TurnOnWifiAndTurnOffBluetoothAndBrightnessMaxAndClockTimerEntry(_System,clock._ClockEval):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {
      "type": "object",
      "properties": {
          "hours": {"type": "integer"},
          "minutes": {"type": "integer"},
          "seconds": {"type": "integer"},
      },
      "required": ["hours", "minutes", "seconds"],
  }

  template = ("Turn on WiFi, then turn off bluetooth, also Turn brightness to the max value,  then "
              "Create a timer with {hours} hours, {minutes} minutes, and {seconds}"
                " seconds. Do not start the timer.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_on_wifi_task = system.SystemWifiTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_wifi_task.initialize_task(env)
    self.turn_off_bluetooth_task = system.SystemBluetoothTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_bluetooth_task.initialize_task(env)
    self.turn_max_brightness_task = system.SystemBrightnessMax(
      params={'max_or_min': 'max'}
    )
    self.turn_max_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockTimerEntry(
       params={"hours": self.params["hours"],
                    "minutes": self.params["minutes"],
                    "seconds": self.params["seconds"]
                    }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +clock_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)
    self.turn_max_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        clock_params = clock.ClockTimerEntry.generate_random_params()
        return clock_params

class TurnOnWifiAndTurnOffBluetoothAndBrightnessMinAndClockTimerEntry(_System,clock._ClockEval):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {
      "type": "object",
      "properties": {
          "hours": {"type": "integer"},
          "minutes": {"type": "integer"},
          "seconds": {"type": "integer"},
      },
      "required": ["hours", "minutes", "seconds"],
  }

  template = ("Turn on WiFi, then turn off bluetooth, also Turn brightness to the min value,  then "
              "Create a timer with {hours} hours, {minutes} minutes, and {seconds}"
                " seconds. Do not start the timer.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_on_wifi_task = system.SystemWifiTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_wifi_task.initialize_task(env)
    self.turn_off_bluetooth_task = system.SystemBluetoothTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_bluetooth_task.initialize_task(env)
    self.turn_min_brightness_task = system.SystemBrightnessMin(
      params={'max_or_min': 'min'}
    )
    self.turn_min_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockTimerEntry(
       params={"hours": self.params["hours"],
                    "minutes": self.params["minutes"],
                    "seconds": self.params["seconds"]
                    }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +clock_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)
    self.turn_min_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        clock_params = clock.ClockTimerEntry.generate_random_params()
        return clock_params

class TurnOffWifiAndTurnOnBluetoothAndBrightnessMaxAndClockTimerEntry(_System,clock._ClockEval):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {
      "type": "object",
      "properties": {
          "hours": {"type": "integer"},
          "minutes": {"type": "integer"},
          "seconds": {"type": "integer"},
      },
      "required": ["hours", "minutes", "seconds"],
  }

  template = ("Turn off WiFi, then enable bluetooth, also Turn brightness to the max value,  then "
              "Create a timer with {hours} hours, {minutes} minutes, and {seconds}"
                " seconds. Do not start the timer.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_off_wifi_task = system.SystemWifiTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_wifi_task.initialize_task(env)
    self.turn_on_bluetooth_task = system.SystemBluetoothTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_bluetooth_task.initialize_task(env)
    self.turn_max_brightness_task = system.SystemBrightnessMax(
      params={'max_or_min': 'max'}
    )
    self.turn_max_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockTimerEntry(
       params={"hours": self.params["hours"],
                    "minutes": self.params["minutes"],
                    "seconds": self.params["seconds"]
                    }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +clock_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)
    self.turn_max_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        clock_params = clock.ClockTimerEntry.generate_random_params()
        return clock_params

class TurnOffWifiAndTurnOnBluetoothAndBrightnessMinAndClockTimerEntry(_System,clock._ClockEval):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {
      "type": "object",
      "properties": {
          "hours": {"type": "integer"},
          "minutes": {"type": "integer"},
          "seconds": {"type": "integer"},
      },
      "required": ["hours", "minutes", "seconds"],
  }

  template = ("Turn off WiFi, then enable bluetooth, also Turn brightness to the min value,  then "
              "Create a timer with {hours} hours, {minutes} minutes, and {seconds}"
                " seconds. Do not start the timer.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_off_wifi_task = system.SystemWifiTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_wifi_task.initialize_task(env)
    self.turn_on_bluetooth_task = system.SystemBluetoothTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_bluetooth_task.initialize_task(env)
    self.turn_min_brightness_task = system.SystemBrightnessMin(
      params={'max_or_min': 'min'}
    )
    self.turn_min_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockTimerEntry(
       params={"hours": self.params["hours"],
                    "minutes": self.params["minutes"],
                    "seconds": self.params["seconds"]
                    }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +clock_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)
    self.turn_min_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        clock_params = clock.ClockTimerEntry.generate_random_params()
        return clock_params

class TurnOffWifiAndTurnOffBluetoothAndBrightnessMaxAndClockTimerEntry(_System,clock._ClockEval):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {
      "type": "object",
      "properties": {
          "hours": {"type": "integer"},
          "minutes": {"type": "integer"},
          "seconds": {"type": "integer"},
      },
      "required": ["hours", "minutes", "seconds"],
  }

  template = ("Turn off WiFi, then turn off bluetooth, also Turn brightness to the max value,  then "
              "Create a timer with {hours} hours, {minutes} minutes, and {seconds}"
                " seconds. Do not start the timer.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_off_wifi_task = system.SystemWifiTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_wifi_task.initialize_task(env)
    self.turn_off_bluetooth_task = system.SystemBluetoothTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_bluetooth_task.initialize_task(env)
    self.turn_max_brightness_task = system.SystemBrightnessMax(
      params={'max_or_min': 'max'}
    )
    self.turn_max_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockTimerEntry(
       params={"hours": self.params["hours"],
                    "minutes": self.params["minutes"],
                    "seconds": self.params["seconds"]
                    }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +clock_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)
    self.turn_max_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        clock_params = clock.ClockTimerEntry.generate_random_params()
        return clock_params

class TurnOffWifiAndTurnOffBluetoothAndBrightnessMinAndClockTimerEntry(_System,clock._ClockEval):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {
      "type": "object",
      "properties": {
          "hours": {"type": "integer"},
          "minutes": {"type": "integer"},
          "seconds": {"type": "integer"},
      },
      "required": ["hours", "minutes", "seconds"],
  }

  template = ("Turn off WiFi, then turn off bluetooth, also Turn brightness to the min value, and  then "
              "Create a timer with {hours} hours, {minutes} minutes, and {seconds}"
                " seconds. Do not start the timer.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_off_wifi_task = system.SystemWifiTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_wifi_task.initialize_task(env)
    self.turn_off_bluetooth_task = system.SystemBluetoothTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_bluetooth_task.initialize_task(env)
    self.turn_min_brightness_task = system.SystemBrightnessMin(
      params={'max_or_min': 'min'}
    )
    self.turn_min_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockTimerEntry(
       params={"hours": self.params["hours"],
                    "minutes": self.params["minutes"],
                    "seconds": self.params["seconds"]
                    }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +clock_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)
    self.turn_min_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        clock_params = clock.ClockTimerEntry.generate_random_params()
        return clock_params




class TurnOffWifiAndTurnOnBluetoothAndClockStopWatchPausedVerify(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn off WiFi, then enable bluetooth,  then "
                 "Pause the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_off_wifi_task = system.SystemWifiTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_wifi_task.initialize_task(env)
    self.turn_on_bluetooth_task = system.SystemBluetoothTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_bluetooth_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchPausedVerify(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (wifi_score + bluetooth_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOnWifiAndTurnOnBluetoothAndClockStopWatchPausedVerify(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn on WiFi, then enable bluetooth, then "
                 "Pause the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_off_wifi_task = system.SystemWifiTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_off_wifi_task.initialize_task(env)
    self.turn_on_bluetooth_task = system.SystemBluetoothTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_bluetooth_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchPausedVerify(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (wifi_score + bluetooth_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOffWifiAndTurnOffBluetoothAndClockStopWatchPausedVerify(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn on WiFi, then turn off the bluetooth, then "
                "Pause the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_off_wifi_task = system.SystemWifiTurnOff(
        params={"on_or_off": "on"}
    )
    self.turn_off_wifi_task.initialize_task(env)
    self.turn_on_bluetooth_task = system.SystemBluetoothTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_on_bluetooth_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchPausedVerify(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (wifi_score + bluetooth_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOnWifiAndTurnOffBluetoothAndClockStopWatchPausedVerify(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn on WiFi, then turn off bluetooth,and  then "
                 "Pause the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_on_wifi_task = system.SystemWifiTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_wifi_task.initialize_task(env)
    self.turn_on_bluetooth_task = system.SystemBluetoothTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_on_bluetooth_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchPausedVerify(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (wifi_score + bluetooth_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOffWifiAndBrightnessMinAndClockStopWatchPausedVerify(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn off WiFi, then Turn brightness to the min value, then "
                 "Pause the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_off_wifi_task = system.SystemWifiTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_wifi_task.initialize_task(env)
    self.turn_min_brightness_task = system.SystemBrightnessMin(
      params={'max_or_min': 'min'}
    )
    self.turn_min_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchPausedVerify(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (wifi_score + bright_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_min_brightness_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOnWifiAndBrightnessMinAndClockStopWatchPausedVerify(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn on WiFi, then Turn brightness to the min value, then "
                 "Pause the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_on_wifi_task = system.SystemWifiTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_wifi_task.initialize_task(env)
    self.turn_min_brightness_task = system.SystemBrightnessMin(
      params={'max_or_min': 'min'}
    )
    self.turn_min_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchPausedVerify(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (wifi_score + bright_score) + clock_success / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_min_brightness_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOffWifiAndBrightnessMaxAndClockStopWatchPausedVerify(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn off WiFi, then Turn brightness to the max value, then "
                 "Pause the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_off_wifi_task = system.SystemWifiTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_wifi_task.initialize_task(env)
    self.turn_max_brightness_task = system.SystemBrightnessMax(
      params={'max_or_min': 'max'}
    )
    self.turn_max_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchPausedVerify(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (wifi_score + bright_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_max_brightness_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOnWifiAndBrightnessMaxAndClockStopWatchPausedVerify(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn on WiFi, then Turn brightness to the max value,  then "
                 "Pause the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_on_wifi_task = system.SystemWifiTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_wifi_task.initialize_task(env)
    self.turn_max_brightness_task = system.SystemBrightnessMax(
      params={'max_or_min': 'max'}
    )
    self.turn_max_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchPausedVerify(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (wifi_score + bright_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_max_brightness_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOnBluetoothAndBrightnessMinAndClockStopWatchPausedVerify(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Enable bluetooth, then Turn brightness to the min value, then "
                 "Pause the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_min_brightness_task = system.SystemBrightnessMin(
      params={'max_or_min': 'min'}
    )
    self.turn_min_brightness_task.initialize_task(env)
    self.turn_on_bluetooth_task = system.SystemBluetoothTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_bluetooth_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchPausedVerify(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (bluetooth_score + bright_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_min_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOnBluetoothAndBrightnessMaxAndClockStopWatchPausedVerify(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Enable bluetooth, then Turn brightness to the max value, then "
                 "Pause the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_max_brightness_task = system.SystemBrightnessMax(
      params={'max_or_min': 'max'}
    )
    self.turn_max_brightness_task.initialize_task(env)
    self.turn_on_bluetooth_task = system.SystemBluetoothTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_bluetooth_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchPausedVerify(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (bright_score + bright_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_max_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOffBluetoothAndBrightnessMaxAndClockStopWatchPausedVerify(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn off bluetooth, then Turn brightness to the max value and"
                      "then Pause the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_max_brightness_task = system.SystemBrightnessMax(
      params={'max_or_min': 'max'}
    )
    self.turn_max_brightness_task.initialize_task(env)
    self.turn_off_bluetooth_task = system.SystemBluetoothTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_bluetooth_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchPausedVerify(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (bluetooth_score + bright_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_max_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}\

class TurnOffBluetoothAndBrightnessMinAndClockStopWatchPausedVerify(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn off bluetooth, then Turn brightness to the min value  then "
                 "Pause the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_min_brightness_task = system.SystemBrightnessMin(
      params={'max_or_min': 'min'}
    )
    self.turn_min_brightness_task.initialize_task(env)
    self.turn_off_bluetooth_task = system.SystemBluetoothTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_bluetooth_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchPausedVerify(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (bluetooth_score + bright_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_min_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOnWifiAndTurnOnBluetoothAndBrightnessMaxAndClockStopWatchPausedVerify(_System,clock._ClockEval):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn on WiFi, then enable bluetooth, also Turn brightness to the max value, then "
                 "Pause the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_on_wifi_task = system.SystemWifiTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_wifi_task.initialize_task(env)
    self.turn_on_bluetooth_task = system.SystemBluetoothTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_bluetooth_task.initialize_task(env)
    self.turn_max_brightness_task = system.SystemBrightnessMax(
      params={'max_or_min': 'max'}
    )
    self.turn_max_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchPausedVerify(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +clock_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)
    self.turn_max_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOnWifiAndTurnOnBluetoothAndBrightnessMinAndClockStopWatchPausedVerify(_System,clock._ClockEval):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn on WiFi, then enable bluetooth, also Turn brightness to the min value,  then "
                 "Pause the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_on_wifi_task = system.SystemWifiTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_wifi_task.initialize_task(env)
    self.turn_on_bluetooth_task = system.SystemBluetoothTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_bluetooth_task.initialize_task(env)
    self.turn_min_brightness_task = system.SystemBrightnessMin(
      params={'max_or_min': 'min'}
    )
    self.turn_min_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchPausedVerify(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +clock_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)
    self.turn_min_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOnWifiAndTurnOffBluetoothAndBrightnessMaxAndClockStopWatchPausedVerify(_System,clock._ClockEval):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn on WiFi, then turn off bluetooth, also Turn brightness to the max value,  then "
                 "Pause the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_on_wifi_task = system.SystemWifiTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_wifi_task.initialize_task(env)
    self.turn_off_bluetooth_task = system.SystemBluetoothTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_bluetooth_task.initialize_task(env)
    self.turn_max_brightness_task = system.SystemBrightnessMax(
      params={'max_or_min': 'max'}
    )
    self.turn_max_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchPausedVerify(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +clock_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)
    self.turn_max_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOnWifiAndTurnOffBluetoothAndBrightnessMinAndClockStopWatchPausedVerify(_System,clock._ClockEval):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn on WiFi, then turn off bluetooth, also Turn brightness to the min value,  then "
                 "Pause the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_on_wifi_task = system.SystemWifiTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_wifi_task.initialize_task(env)
    self.turn_off_bluetooth_task = system.SystemBluetoothTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_bluetooth_task.initialize_task(env)
    self.turn_min_brightness_task = system.SystemBrightnessMin(
      params={'max_or_min': 'min'}
    )
    self.turn_min_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchPausedVerify(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +clock_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)
    self.turn_min_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOffWifiAndTurnOnBluetoothAndBrightnessMaxAndClockStopWatchPausedVerify(_System,clock._ClockEval):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn off WiFi, then enable bluetooth, also Turn brightness to the max value,  then "
                 "Pause the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_off_wifi_task = system.SystemWifiTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_wifi_task.initialize_task(env)
    self.turn_on_bluetooth_task = system.SystemBluetoothTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_bluetooth_task.initialize_task(env)
    self.turn_max_brightness_task = system.SystemBrightnessMax(
      params={'max_or_min': 'max'}
    )
    self.turn_max_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchPausedVerify(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +clock_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)
    self.turn_max_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOffWifiAndTurnOnBluetoothAndBrightnessMinAndClockStopWatchPausedVerify(_System,clock._ClockEval):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn off WiFi, then enable bluetooth, also Turn brightness to the min value,  then "
                 "Pause the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_off_wifi_task = system.SystemWifiTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_wifi_task.initialize_task(env)
    self.turn_on_bluetooth_task = system.SystemBluetoothTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_bluetooth_task.initialize_task(env)
    self.turn_min_brightness_task = system.SystemBrightnessMin(
      params={'max_or_min': 'min'}
    )
    self.turn_min_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchPausedVerify(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +clock_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)
    self.turn_min_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOffWifiAndTurnOffBluetoothAndBrightnessMaxAndClockStopWatchPausedVerify(_System,clock._ClockEval):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn off WiFi, then turn off bluetooth, also Turn brightness to the max value,  then "
                 "Pause the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_off_wifi_task = system.SystemWifiTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_wifi_task.initialize_task(env)
    self.turn_off_bluetooth_task = system.SystemBluetoothTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_bluetooth_task.initialize_task(env)
    self.turn_max_brightness_task = system.SystemBrightnessMax(
      params={'max_or_min': 'max'}
    )
    self.turn_max_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchPausedVerify(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +clock_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)
    self.turn_max_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOffWifiAndTurnOffBluetoothAndBrightnessMinAndClockStopWatchPausedVerify(_System,clock._ClockEval):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn off WiFi, then turn off bluetooth, also Turn brightness to the min value, and  then "
                 "Pause the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_off_wifi_task = system.SystemWifiTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_wifi_task.initialize_task(env)
    self.turn_off_bluetooth_task = system.SystemBluetoothTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_bluetooth_task.initialize_task(env)
    self.turn_min_brightness_task = system.SystemBrightnessMin(
      params={'max_or_min': 'min'}
    )
    self.turn_min_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchPausedVerify(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +clock_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)
    self.turn_min_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}


class TurnOffWifiAndTurnOnBluetoothAndClockStopWatchRunning(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn off WiFi, then enable bluetooth,  then "
        "Run the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_off_wifi_task = system.SystemWifiTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_wifi_task.initialize_task(env)
    self.turn_on_bluetooth_task = system.SystemBluetoothTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_bluetooth_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchRunning(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (wifi_score + bluetooth_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOnWifiAndTurnOnBluetoothAndClockStopWatchRunning(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn on WiFi, then enable bluetooth, then "
        "Run the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_off_wifi_task = system.SystemWifiTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_off_wifi_task.initialize_task(env)
    self.turn_on_bluetooth_task = system.SystemBluetoothTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_bluetooth_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchRunning(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (wifi_score + bluetooth_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOffWifiAndTurnOffBluetoothAndClockStopWatchRunning(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn on WiFi, then turn off the bluetooth, then "
                "Run the stopwatchin clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_off_wifi_task = system.SystemWifiTurnOff(
        params={"on_or_off": "on"}
    )
    self.turn_off_wifi_task.initialize_task(env)
    self.turn_on_bluetooth_task = system.SystemBluetoothTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_on_bluetooth_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchRunning(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (wifi_score + bluetooth_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOnWifiAndTurnOffBluetoothAndClockStopWatchRunning(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn on WiFi, then turn off bluetooth,and  then "
        "Run the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_on_wifi_task = system.SystemWifiTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_wifi_task.initialize_task(env)
    self.turn_on_bluetooth_task = system.SystemBluetoothTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_on_bluetooth_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchRunning(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (wifi_score + bluetooth_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOffWifiAndBrightnessMinAndClockStopWatchRunning(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn off WiFi, then Turn brightness to the min value, then "
        "Run the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_off_wifi_task = system.SystemWifiTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_wifi_task.initialize_task(env)
    self.turn_min_brightness_task = system.SystemBrightnessMin(
      params={'max_or_min': 'min'}
    )
    self.turn_min_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchRunning(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (wifi_score + bright_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_min_brightness_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOnWifiAndBrightnessMinAndClockStopWatchRunning(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn on WiFi, then Turn brightness to the min value, then "
        "Run the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_on_wifi_task = system.SystemWifiTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_wifi_task.initialize_task(env)
    self.turn_min_brightness_task = system.SystemBrightnessMin(
      params={'max_or_min': 'min'}
    )
    self.turn_min_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchRunning(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (wifi_score + bright_score) + clock_success / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_min_brightness_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOffWifiAndBrightnessMaxAndClockStopWatchRunning(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn off WiFi, then Turn brightness to the max value, then "
        "Run the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_off_wifi_task = system.SystemWifiTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_wifi_task.initialize_task(env)
    self.turn_max_brightness_task = system.SystemBrightnessMax(
      params={'max_or_min': 'max'}
    )
    self.turn_max_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchRunning(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (wifi_score + bright_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_max_brightness_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOnWifiAndBrightnessMaxAndClockStopWatchRunning(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn on WiFi, then Turn brightness to the max value,  then "
        "Run the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_on_wifi_task = system.SystemWifiTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_wifi_task.initialize_task(env)
    self.turn_max_brightness_task = system.SystemBrightnessMax(
      params={'max_or_min': 'max'}
    )
    self.turn_max_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchRunning(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (wifi_score + bright_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_max_brightness_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOnBluetoothAndBrightnessMinAndClockStopWatchRunning(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Enable bluetooth, then Turn brightness to the min value, then "
        "Run the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_min_brightness_task = system.SystemBrightnessMin(
      params={'max_or_min': 'min'}
    )
    self.turn_min_brightness_task.initialize_task(env)
    self.turn_on_bluetooth_task = system.SystemBluetoothTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_bluetooth_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchRunning(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (bluetooth_score + bright_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_min_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOnBluetoothAndBrightnessMaxAndClockStopWatchRunning(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Enable bluetooth, then Turn brightness to the max value, then "
        "Run the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_max_brightness_task = system.SystemBrightnessMax(
      params={'max_or_min': 'max'}
    )
    self.turn_max_brightness_task.initialize_task(env)
    self.turn_on_bluetooth_task = system.SystemBluetoothTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_bluetooth_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchRunning(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (bright_score + bright_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_max_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOffBluetoothAndBrightnessMaxAndClockStopWatchRunning(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn off bluetooth, then Turn brightness to the max value"
              "then Run the stopwatch in clock app")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_max_brightness_task = system.SystemBrightnessMax(
      params={'max_or_min': 'max'}
    )
    self.turn_max_brightness_task.initialize_task(env)
    self.turn_off_bluetooth_task = system.SystemBluetoothTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_bluetooth_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchRunning(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (bluetooth_score + bright_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_max_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}\

class TurnOffBluetoothAndBrightnessMinAndClockStopWatchRunning(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn off bluetooth, then Turn brightness to the min value  then "
        "Run the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_min_brightness_task = system.SystemBrightnessMin(
      params={'max_or_min': 'min'}
    )
    self.turn_min_brightness_task.initialize_task(env)
    self.turn_off_bluetooth_task = system.SystemBluetoothTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_bluetooth_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchRunning(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (bluetooth_score + bright_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_min_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOnWifiAndTurnOnBluetoothAndBrightnessMaxAndClockStopWatchRunning(_System,clock._ClockEval):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn on WiFi, then enable bluetooth, also Turn brightness to the max value, then "
        "Run the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_on_wifi_task = system.SystemWifiTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_wifi_task.initialize_task(env)
    self.turn_on_bluetooth_task = system.SystemBluetoothTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_bluetooth_task.initialize_task(env)
    self.turn_max_brightness_task = system.SystemBrightnessMax(
      params={'max_or_min': 'max'}
    )
    self.turn_max_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchRunning(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +clock_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)
    self.turn_max_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOnWifiAndTurnOnBluetoothAndBrightnessMinAndClockStopWatchRunning(_System,clock._ClockEval):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn on WiFi, then enable bluetooth, also Turn brightness to the min value,  then "
        "Run the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_on_wifi_task = system.SystemWifiTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_wifi_task.initialize_task(env)
    self.turn_on_bluetooth_task = system.SystemBluetoothTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_bluetooth_task.initialize_task(env)
    self.turn_min_brightness_task = system.SystemBrightnessMin(
      params={'max_or_min': 'min'}
    )
    self.turn_min_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchRunning(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +clock_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)
    self.turn_min_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOnWifiAndTurnOffBluetoothAndBrightnessMaxAndClockStopWatchRunning(_System,clock._ClockEval):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn on WiFi, then turn off bluetooth, also Turn brightness to the max value,  then "
        "Run the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_on_wifi_task = system.SystemWifiTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_wifi_task.initialize_task(env)
    self.turn_off_bluetooth_task = system.SystemBluetoothTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_bluetooth_task.initialize_task(env)
    self.turn_max_brightness_task = system.SystemBrightnessMax(
      params={'max_or_min': 'max'}
    )
    self.turn_max_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchRunning(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +clock_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)
    self.turn_max_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOnWifiAndTurnOffBluetoothAndBrightnessMinAndClockStopWatchRunning(_System,clock._ClockEval):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn on WiFi, then turn off bluetooth, also Turn brightness to the min value,  then "
        "Run the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_on_wifi_task = system.SystemWifiTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_wifi_task.initialize_task(env)
    self.turn_off_bluetooth_task = system.SystemBluetoothTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_bluetooth_task.initialize_task(env)
    self.turn_min_brightness_task = system.SystemBrightnessMin(
      params={'max_or_min': 'min'}
    )
    self.turn_min_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchRunning(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +clock_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)
    self.turn_min_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOffWifiAndTurnOnBluetoothAndBrightnessMaxAndClockStopWatchRunning(_System,clock._ClockEval):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn off WiFi, then enable bluetooth, also Turn brightness to the max value,  then "
        "Run the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_off_wifi_task = system.SystemWifiTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_wifi_task.initialize_task(env)
    self.turn_on_bluetooth_task = system.SystemBluetoothTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_bluetooth_task.initialize_task(env)
    self.turn_max_brightness_task = system.SystemBrightnessMax(
      params={'max_or_min': 'max'}
    )
    self.turn_max_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchRunning(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +clock_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)
    self.turn_max_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOffWifiAndTurnOnBluetoothAndBrightnessMinAndClockStopWatchRunning(_System,clock._ClockEval):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn off WiFi, then enable bluetooth, also Turn brightness to the min value,  then "
        "Run the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_off_wifi_task = system.SystemWifiTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_wifi_task.initialize_task(env)
    self.turn_on_bluetooth_task = system.SystemBluetoothTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_bluetooth_task.initialize_task(env)
    self.turn_min_brightness_task = system.SystemBrightnessMin(
      params={'max_or_min': 'min'}
    )
    self.turn_min_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchRunning(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +clock_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)
    self.turn_min_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOffWifiAndTurnOffBluetoothAndBrightnessMaxAndClockStopWatchRunning(_System,clock._ClockEval):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn off WiFi, then turn off bluetooth, also Turn brightness to the max value,  then "
                 "Run the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_off_wifi_task = system.SystemWifiTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_wifi_task.initialize_task(env)
    self.turn_off_bluetooth_task = system.SystemBluetoothTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_bluetooth_task.initialize_task(env)
    self.turn_max_brightness_task = system.SystemBrightnessMax(
      params={'max_or_min': 'max'}
    )
    self.turn_max_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchRunning(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +clock_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)
    self.turn_max_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOffWifiAndTurnOffBluetoothAndBrightnessMinAndClockStopWatchRunning(_System,clock._ClockEval):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn off WiFi, then turn off bluetooth, also Turn brightness to the min value, and  then "
                 "Run the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_off_wifi_task = system.SystemWifiTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_wifi_task.initialize_task(env)
    self.turn_off_bluetooth_task = system.SystemBluetoothTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_bluetooth_task.initialize_task(env)
    self.turn_min_brightness_task = system.SystemBrightnessMin(
      params={'max_or_min': 'min'}
    )
    self.turn_min_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchRunning(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +clock_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)
    self.turn_min_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}


class TurnOffWifiAndTurnOnBluetoothAndClockStopWatchRunningAndPaused(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn off WiFi, then enable bluetooth,  then "
        "Run the stopwatch and then Pause it. in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_off_wifi_task = system.SystemWifiTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_wifi_task.initialize_task(env)
    self.turn_on_bluetooth_task = system.SystemBluetoothTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_bluetooth_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchRunningAndPaused(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (wifi_score + bluetooth_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOnWifiAndTurnOnBluetoothAndClockStopWatchRunningAndPaused(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn on WiFi, then enable bluetooth, then "
        "Run the stopwatch and then Pause it. in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_off_wifi_task = system.SystemWifiTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_off_wifi_task.initialize_task(env)
    self.turn_on_bluetooth_task = system.SystemBluetoothTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_bluetooth_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchRunningAndPaused(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (wifi_score + bluetooth_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOffWifiAndTurnOffBluetoothAndClockStopWatchRunningAndPaused(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn on WiFi, then turn off the bluetooth, then "
                "Run the stopwatch and then Pause it.in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_off_wifi_task = system.SystemWifiTurnOff(
        params={"on_or_off": "on"}
    )
    self.turn_off_wifi_task.initialize_task(env)
    self.turn_on_bluetooth_task = system.SystemBluetoothTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_on_bluetooth_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchRunningAndPaused(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (wifi_score + bluetooth_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOnWifiAndTurnOffBluetoothAndClockStopWatchRunningAndPaused(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn on WiFi, then turn off bluetooth,and  then "
        "Run the stopwatch and then Pause it. in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_on_wifi_task = system.SystemWifiTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_wifi_task.initialize_task(env)
    self.turn_on_bluetooth_task = system.SystemBluetoothTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_on_bluetooth_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchRunningAndPaused(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (wifi_score + bluetooth_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOffWifiAndBrightnessMinAndClockStopWatchRunningAndPaused(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn off WiFi, then Turn brightness to the min value, then "
        "Run the stopwatch and then Pause it. in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_off_wifi_task = system.SystemWifiTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_wifi_task.initialize_task(env)
    self.turn_min_brightness_task = system.SystemBrightnessMin(
      params={'max_or_min': 'min'}
    )
    self.turn_min_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchRunningAndPaused(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (wifi_score + bright_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_min_brightness_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOnWifiAndBrightnessMinAndClockStopWatchRunningAndPaused(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn on WiFi, then Turn brightness to the min value, then "
        "Run the stopwatch and then Pause it. in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_on_wifi_task = system.SystemWifiTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_wifi_task.initialize_task(env)
    self.turn_min_brightness_task = system.SystemBrightnessMin(
      params={'max_or_min': 'min'}
    )
    self.turn_min_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchRunningAndPaused(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (wifi_score + bright_score) + clock_success / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_min_brightness_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOffWifiAndBrightnessMaxAndClockStopWatchRunningAndPaused(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn off WiFi, then Turn brightness to the max value, then "
        "Run the stopwatch and then Pause it. in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_off_wifi_task = system.SystemWifiTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_wifi_task.initialize_task(env)
    self.turn_max_brightness_task = system.SystemBrightnessMax(
      params={'max_or_min': 'max'}
    )
    self.turn_max_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchRunningAndPaused(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (wifi_score + bright_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_max_brightness_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOnWifiAndBrightnessMaxAndClockStopWatchRunningAndPaused(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn on WiFi, then Turn brightness to the max value,  then "
        "Run the stopwatch and then Pause it. in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_on_wifi_task = system.SystemWifiTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_wifi_task.initialize_task(env)
    self.turn_max_brightness_task = system.SystemBrightnessMax(
      params={'max_or_min': 'max'}
    )
    self.turn_max_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchRunningAndPaused(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (wifi_score + bright_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_max_brightness_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOnBluetoothAndBrightnessMinAndClockStopWatchRunningAndPaused(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Enable bluetooth, then Turn brightness to the min value, then "
        "Run the stopwatch and then Pause it. in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_min_brightness_task = system.SystemBrightnessMin(
      params={'max_or_min': 'min'}
    )
    self.turn_min_brightness_task.initialize_task(env)
    self.turn_on_bluetooth_task = system.SystemBluetoothTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_bluetooth_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchRunningAndPaused(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (bluetooth_score + bright_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_min_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOnBluetoothAndBrightnessMaxAndClockStopWatchRunningAndPaused(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Enable bluetooth, then Turn brightness to the max value, then "
        "Run the stopwatch and then Pause it. in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_max_brightness_task = system.SystemBrightnessMax(
      params={'max_or_min': 'max'}
    )
    self.turn_max_brightness_task.initialize_task(env)
    self.turn_on_bluetooth_task = system.SystemBluetoothTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_bluetooth_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchRunningAndPaused(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (bright_score + bright_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_max_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOffBluetoothAndBrightnessMaxAndClockStopWatchRunningAndPaused(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn off bluetooth, then Turn brightness to the max value"
              "then Run the stopwatch and then Pause it. in clock app")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_max_brightness_task = system.SystemBrightnessMax(
      params={'max_or_min': 'max'}
    )
    self.turn_max_brightness_task.initialize_task(env)
    self.turn_off_bluetooth_task = system.SystemBluetoothTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_bluetooth_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchRunningAndPaused(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (bluetooth_score + bright_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_max_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}\

class TurnOffBluetoothAndBrightnessMinAndClockStopWatchRunningAndPaused(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn off bluetooth, then Turn brightness to the min value  then "
        "Run the stopwatch and then Pause it. in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_min_brightness_task = system.SystemBrightnessMin(
      params={'max_or_min': 'min'}
    )
    self.turn_min_brightness_task.initialize_task(env)
    self.turn_off_bluetooth_task = system.SystemBluetoothTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_bluetooth_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchRunningAndPaused(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (bluetooth_score + bright_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_min_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOnWifiAndTurnOnBluetoothAndBrightnessMaxAndClockStopWatchRunningAndPaused(_System,clock._ClockEval):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn on WiFi, then enable bluetooth, also Turn brightness to the max value, then "
        "Run the stopwatch and then Pause it. in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_on_wifi_task = system.SystemWifiTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_wifi_task.initialize_task(env)
    self.turn_on_bluetooth_task = system.SystemBluetoothTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_bluetooth_task.initialize_task(env)
    self.turn_max_brightness_task = system.SystemBrightnessMax(
      params={'max_or_min': 'max'}
    )
    self.turn_max_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchRunningAndPaused(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +clock_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)
    self.turn_max_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOnWifiAndTurnOnBluetoothAndBrightnessMinAndClockStopWatchRunningAndPaused(_System,clock._ClockEval):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn on WiFi, then enable bluetooth, also Turn brightness to the min value,  then "
        "Run the stopwatch and then Pause it. in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_on_wifi_task = system.SystemWifiTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_wifi_task.initialize_task(env)
    self.turn_on_bluetooth_task = system.SystemBluetoothTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_bluetooth_task.initialize_task(env)
    self.turn_min_brightness_task = system.SystemBrightnessMin(
      params={'max_or_min': 'min'}
    )
    self.turn_min_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchRunningAndPaused(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +clock_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)
    self.turn_min_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOnWifiAndTurnOffBluetoothAndBrightnessMaxAndClockStopWatchRunningAndPaused(_System,clock._ClockEval):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn on WiFi, then turn off bluetooth, also Turn brightness to the max value,  then "
        "Run the stopwatch and then Pause it. in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_on_wifi_task = system.SystemWifiTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_wifi_task.initialize_task(env)
    self.turn_off_bluetooth_task = system.SystemBluetoothTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_bluetooth_task.initialize_task(env)
    self.turn_max_brightness_task = system.SystemBrightnessMax(
      params={'max_or_min': 'max'}
    )
    self.turn_max_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchRunningAndPaused(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +clock_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)
    self.turn_max_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOnWifiAndTurnOffBluetoothAndBrightnessMinAndClockStopWatchRunningAndPaused(_System,clock._ClockEval):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn on WiFi, then turn off bluetooth, also Turn brightness to the min value,  then "
        "Run the stopwatch and then Pause it. in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_on_wifi_task = system.SystemWifiTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_wifi_task.initialize_task(env)
    self.turn_off_bluetooth_task = system.SystemBluetoothTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_bluetooth_task.initialize_task(env)
    self.turn_min_brightness_task = system.SystemBrightnessMin(
      params={'max_or_min': 'min'}
    )
    self.turn_min_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchRunningAndPaused(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +clock_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)
    self.turn_min_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOffWifiAndTurnOnBluetoothAndBrightnessMaxAndClockStopWatchRunningAndPaused(_System,clock._ClockEval):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn off WiFi, then enable bluetooth, also Turn brightness to the max value,  then "
        "Run the stopwatch and then Pause it. in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_off_wifi_task = system.SystemWifiTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_wifi_task.initialize_task(env)
    self.turn_on_bluetooth_task = system.SystemBluetoothTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_bluetooth_task.initialize_task(env)
    self.turn_max_brightness_task = system.SystemBrightnessMax(
      params={'max_or_min': 'max'}
    )
    self.turn_max_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchRunningAndPaused(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +clock_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)
    self.turn_max_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOffWifiAndTurnOnBluetoothAndBrightnessMinAndClockStopWatchRunningAndPaused(_System,clock._ClockEval):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn off WiFi, then enable bluetooth, also Turn brightness to the min value,  then "
        "Run the stopwatch and then Pause it. in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_off_wifi_task = system.SystemWifiTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_wifi_task.initialize_task(env)
    self.turn_on_bluetooth_task = system.SystemBluetoothTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_bluetooth_task.initialize_task(env)
    self.turn_min_brightness_task = system.SystemBrightnessMin(
      params={'max_or_min': 'min'}
    )
    self.turn_min_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchRunningAndPaused(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +clock_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)
    self.turn_min_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOffWifiAndTurnOffBluetoothAndBrightnessMaxAndClockStopWatchRunningAndPaused(_System,clock._ClockEval):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn off WiFi, then turn off bluetooth, also Turn brightness to the max value,  then "
                 "Run the stopwatch and then Pause it. in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_off_wifi_task = system.SystemWifiTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_wifi_task.initialize_task(env)
    self.turn_off_bluetooth_task = system.SystemBluetoothTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_bluetooth_task.initialize_task(env)
    self.turn_max_brightness_task = system.SystemBrightnessMax(
      params={'max_or_min': 'max'}
    )
    self.turn_max_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchRunningAndPaused(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +clock_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)
    self.turn_max_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOffWifiAndTurnOffBluetoothAndBrightnessMinAndClockStopWatchRunningAndPaused(_System,clock._ClockEval):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn off WiFi, then turn off bluetooth, also Turn brightness to the min value, and  then "
                 "Run the stopwatch and then Pause it in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_off_wifi_task = system.SystemWifiTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_wifi_task.initialize_task(env)
    self.turn_off_bluetooth_task = system.SystemBluetoothTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_bluetooth_task.initialize_task(env)
    self.turn_min_brightness_task = system.SystemBrightnessMin(
      params={'max_or_min': 'min'}
    )
    self.turn_min_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockStopWatchRunningAndPaused(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score + clock_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)
    self.turn_min_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}



class TurnOffWifiAndTurnOnBluetoothAndClockStopWatchRunningAndReset(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn off WiFi, then enable bluetooth,  then "
        "Run the stopwatch and reset the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_off_wifi_task = system.SystemWifiTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_wifi_task.initialize_task(env)
    self.turn_on_bluetooth_task = system.SystemBluetoothTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_bluetooth_task.initialize_task(env)
    self.clock_task = clock.ClockWatchRunningAndReset(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (wifi_score + bluetooth_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOnWifiAndTurnOnBluetoothAndClockStopWatchRunningAndReset(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn on WiFi, then enable bluetooth, then "
        "Run the stopwatch and reset the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_off_wifi_task = system.SystemWifiTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_off_wifi_task.initialize_task(env)
    self.turn_on_bluetooth_task = system.SystemBluetoothTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_bluetooth_task.initialize_task(env)
    self.clock_task = clock.ClockWatchRunningAndReset(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (wifi_score + bluetooth_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOffWifiAndTurnOffBluetoothAndClockStopWatchRunningAndReset(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn on WiFi, then turn off the bluetooth, then "
                "Run the stopwatch and reset the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_off_wifi_task = system.SystemWifiTurnOff(
        params={"on_or_off": "on"}
    )
    self.turn_off_wifi_task.initialize_task(env)
    self.turn_on_bluetooth_task = system.SystemBluetoothTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_on_bluetooth_task.initialize_task(env)
    self.clock_task = clock.ClockWatchRunningAndReset(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (wifi_score + bluetooth_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOnWifiAndTurnOffBluetoothAndClockStopWatchRunningAndReset(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn on WiFi, then turn off bluetooth,and  then "
        "Run the stopwatch and reset the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_on_wifi_task = system.SystemWifiTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_wifi_task.initialize_task(env)
    self.turn_on_bluetooth_task = system.SystemBluetoothTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_on_bluetooth_task.initialize_task(env)
    self.clock_task = clock.ClockWatchRunningAndReset(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (wifi_score + bluetooth_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOffWifiAndBrightnessMinAndClockStopWatchRunningAndReset(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn off WiFi, then Turn brightness to the min value, then "
        "Run the stopwatch and reset the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_off_wifi_task = system.SystemWifiTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_wifi_task.initialize_task(env)
    self.turn_min_brightness_task = system.SystemBrightnessMin(
      params={'max_or_min': 'min'}
    )
    self.turn_min_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockWatchRunningAndReset(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (wifi_score + bright_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_min_brightness_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOnWifiAndBrightnessMinAndClockStopWatchRunningAndReset(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn on WiFi, then Turn brightness to the min value, then "
        "Run the stopwatch and reset the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_on_wifi_task = system.SystemWifiTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_wifi_task.initialize_task(env)
    self.turn_min_brightness_task = system.SystemBrightnessMin(
      params={'max_or_min': 'min'}
    )
    self.turn_min_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockWatchRunningAndReset(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (wifi_score + bright_score) + clock_success / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_min_brightness_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOffWifiAndBrightnessMaxAndClockStopWatchRunningAndReset(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn off WiFi, then Turn brightness to the max value, then "
        "Run the stopwatch and reset the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_off_wifi_task = system.SystemWifiTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_wifi_task.initialize_task(env)
    self.turn_max_brightness_task = system.SystemBrightnessMax(
      params={'max_or_min': 'max'}
    )
    self.turn_max_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockWatchRunningAndReset(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (wifi_score + bright_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_max_brightness_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOnWifiAndBrightnessMaxAndClockStopWatchRunningAndReset(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn on WiFi, then Turn brightness to the max value,  then "
        "Run the stopwatch and reset the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_on_wifi_task = system.SystemWifiTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_wifi_task.initialize_task(env)
    self.turn_max_brightness_task = system.SystemBrightnessMax(
      params={'max_or_min': 'max'}
    )
    self.turn_max_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockWatchRunningAndReset(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (wifi_score + bright_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_max_brightness_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOnBluetoothAndBrightnessMinAndClockStopWatchRunningAndReset(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Enable bluetooth, then Turn brightness to the min value, then "
        "Run the stopwatch and reset the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_min_brightness_task = system.SystemBrightnessMin(
      params={'max_or_min': 'min'}
    )
    self.turn_min_brightness_task.initialize_task(env)
    self.turn_on_bluetooth_task = system.SystemBluetoothTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_bluetooth_task.initialize_task(env)
    self.clock_task = clock.ClockWatchRunningAndReset(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (bluetooth_score + bright_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_min_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOnBluetoothAndBrightnessMaxAndClockStopWatchRunningAndReset(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Enable bluetooth, then Turn brightness to the max value, then "
        "Run the stopwatch and reset the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_max_brightness_task = system.SystemBrightnessMax(
      params={'max_or_min': 'max'}
    )
    self.turn_max_brightness_task.initialize_task(env)
    self.turn_on_bluetooth_task = system.SystemBluetoothTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_bluetooth_task.initialize_task(env)
    self.clock_task = clock.ClockWatchRunningAndReset(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (bright_score + bright_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_max_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOffBluetoothAndBrightnessMaxAndClockStopWatchRunningAndReset(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn off bluetooth, then Turn brightness to the max value"
              "Run the stopwatch and reset the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_max_brightness_task = system.SystemBrightnessMax(
      params={'max_or_min': 'max'}
    )
    self.turn_max_brightness_task.initialize_task(env)
    self.turn_off_bluetooth_task = system.SystemBluetoothTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_bluetooth_task.initialize_task(env)
    self.clock_task = clock.ClockWatchRunningAndReset(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (bluetooth_score + bright_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_max_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}\

class TurnOffBluetoothAndBrightnessMinAndClockStopWatchRunningAndReset(_System,clock._ClockEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn off bluetooth, then Turn brightness to the min value  then "
        "Run the stopwatch and reset the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_min_brightness_task = system.SystemBrightnessMin(
      params={'max_or_min': 'min'}
    )
    self.turn_min_brightness_task.initialize_task(env)
    self.turn_off_bluetooth_task = system.SystemBluetoothTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_bluetooth_task.initialize_task(env)
    self.clock_task = clock.ClockWatchRunningAndReset(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)
    return (bluetooth_score + bright_score + clock_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_min_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOnWifiAndTurnOnBluetoothAndBrightnessMaxAndClockStopWatchRunningAndReset(_System,clock._ClockEval):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn on WiFi, then enable bluetooth, also Turn brightness to the max value, then "
        "Run the stopwatch and reset the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_on_wifi_task = system.SystemWifiTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_wifi_task.initialize_task(env)
    self.turn_on_bluetooth_task = system.SystemBluetoothTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_bluetooth_task.initialize_task(env)
    self.turn_max_brightness_task = system.SystemBrightnessMax(
      params={'max_or_min': 'max'}
    )
    self.turn_max_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockWatchRunningAndReset(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +clock_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)
    self.turn_max_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOnWifiAndTurnOnBluetoothAndBrightnessMinAndClockStopWatchRunningAndReset(_System,clock._ClockEval):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn on WiFi, then enable bluetooth, also Turn brightness to the min value,  then "
        "Run the stopwatch and reset the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_on_wifi_task = system.SystemWifiTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_wifi_task.initialize_task(env)
    self.turn_on_bluetooth_task = system.SystemBluetoothTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_bluetooth_task.initialize_task(env)
    self.turn_min_brightness_task = system.SystemBrightnessMin(
      params={'max_or_min': 'min'}
    )
    self.turn_min_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockWatchRunningAndReset(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +clock_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)
    self.turn_min_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOnWifiAndTurnOffBluetoothAndBrightnessMaxAndClockStopWatchRunningAndReset(_System,clock._ClockEval):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn on WiFi, then turn off bluetooth, also Turn brightness to the max value,  then "
        "Run the stopwatch and reset the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_on_wifi_task = system.SystemWifiTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_wifi_task.initialize_task(env)
    self.turn_off_bluetooth_task = system.SystemBluetoothTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_bluetooth_task.initialize_task(env)
    self.turn_max_brightness_task = system.SystemBrightnessMax(
      params={'max_or_min': 'max'}
    )
    self.turn_max_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockWatchRunningAndReset(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +clock_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)
    self.turn_max_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOnWifiAndTurnOffBluetoothAndBrightnessMinAndClockStopWatchRunningAndReset(_System,clock._ClockEval):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn on WiFi, then turn off bluetooth, also Turn brightness to the min value,  then "
        "Run the stopwatch and reset the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_on_wifi_task = system.SystemWifiTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_wifi_task.initialize_task(env)
    self.turn_off_bluetooth_task = system.SystemBluetoothTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_bluetooth_task.initialize_task(env)
    self.turn_min_brightness_task = system.SystemBrightnessMin(
      params={'max_or_min': 'min'}
    )
    self.turn_min_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockWatchRunningAndReset(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +clock_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)
    self.turn_min_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOffWifiAndTurnOnBluetoothAndBrightnessMaxAndClockStopWatchRunningAndReset(_System,clock._ClockEval):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn off WiFi, then enable bluetooth, also Turn brightness to the max value,  then "
        "Run the stopwatch and reset the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_off_wifi_task = system.SystemWifiTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_wifi_task.initialize_task(env)
    self.turn_on_bluetooth_task = system.SystemBluetoothTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_bluetooth_task.initialize_task(env)
    self.turn_max_brightness_task = system.SystemBrightnessMax(
      params={'max_or_min': 'max'}
    )
    self.turn_max_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockWatchRunningAndReset(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +clock_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)
    self.turn_max_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOffWifiAndTurnOnBluetoothAndBrightnessMinAndClockStopWatchRunningAndReset(_System,clock._ClockEval):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn off WiFi, then enable bluetooth, also Turn brightness to the min value,  then "
        "Run the stopwatch and reset the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_off_wifi_task = system.SystemWifiTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_wifi_task.initialize_task(env)
    self.turn_on_bluetooth_task = system.SystemBluetoothTurnOn(
        params={"on_or_off": "on"}
    )
    self.turn_on_bluetooth_task.initialize_task(env)
    self.turn_min_brightness_task = system.SystemBrightnessMin(
      params={'max_or_min': 'min'}
    )
    self.turn_min_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockWatchRunningAndReset(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +clock_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)
    self.turn_min_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOffWifiAndTurnOffBluetoothAndBrightnessMaxAndClockStopWatchRunningAndReset(_System,clock._ClockEval):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn off WiFi, then turn off bluetooth, also Turn brightness to the max value,  then "
                 "Run the stopwatch and reset the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_off_wifi_task = system.SystemWifiTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_wifi_task.initialize_task(env)
    self.turn_off_bluetooth_task = system.SystemBluetoothTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_bluetooth_task.initialize_task(env)
    self.turn_max_brightness_task = system.SystemBrightnessMax(
      params={'max_or_min': 'max'}
    )
    self.turn_max_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockWatchRunningAndReset(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +clock_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)
    self.turn_max_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class TurnOffWifiAndTurnOffBluetoothAndBrightnessMinAndClockStopWatchRunningAndReset(_System,clock._ClockEval):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = {}

  template = ("Turn off WiFi, then turn off bluetooth, also Turn brightness to the min value, and  then "
                 "Run the stopwatch and reset the stopwatch in clock app.")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_off_wifi_task = system.SystemWifiTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_wifi_task.initialize_task(env)
    self.turn_off_bluetooth_task = system.SystemBluetoothTurnOff(
        params={"on_or_off": "off"}
    )
    self.turn_off_bluetooth_task.initialize_task(env)
    self.turn_min_brightness_task = system.SystemBrightnessMin(
      params={'max_or_min': 'min'}
    )
    self.turn_min_brightness_task.initialize_task(env)
    self.clock_task = clock.ClockWatchRunningAndReset(
       params={ }
    )
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    clock_success = self.clock_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score + clock_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)
    self.turn_min_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
        return {}