# Copyright 2024 The android_world Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Composite tasks using Android Operating System actions."""

from typing import Any

from android_world.env import interface
from android_world.task_evals import task_eval
from android_world.task_evals.single import system
from android_world.task_evals.utils import schema




class TurnOnWifiAndOpenApp(task_eval.TaskEval):
  """Evals the agent opening an app after turning on Wifi."""

  app_names = ("settings",)
  complexity = 2
  schema = schema.create([schema.string("app_name", is_required=True)])

  template = "Turn on Wifi, then open the {app_name} app"

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_on_wifi_task = system.SystemWifiTurnOn(params={"on_or_off": "on"})
    self.turn_on_wifi_task.initialize_task(env)
    self.open_app_task = system.OpenAppTaskEval(
        params={
            "app_name": self.params["app_name"],
        }
    )
    self.open_app_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    open_app_score = self.open_app_task.is_successful(env)
    return (wifi_score + open_app_score) / 2.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.open_app_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return system.OpenAppTaskEval.generate_random_params()

class TurnOffWifiAndTurnOnBluetooth(task_eval.TaskEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn off WiFi, then enable bluetooth"

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

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    return (wifi_score + bluetooth_score) / 2.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOffWifiAndOpenApp(task_eval.TaskEval):
  """Evals the agent opening an app after turning on Wifi."""

  app_names = ("settings",)
  complexity = 2
  schema = schema.create([schema.string("app_name", is_required=True)])

  template = "Turn off Wifi, then open the {app_name} app"

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_on_wifi_task = system.SystemWifiTurnOn(params={"on_or_off": "off"})
    self.turn_on_wifi_task.initialize_task(env)
    self.open_app_task = system.OpenAppTaskEval(
        params={
            "app_name": self.params["app_name"],
        }
    )
    self.open_app_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    open_app_score = self.open_app_task.is_successful(env)
    return (wifi_score + open_app_score) / 2.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.open_app_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return system.OpenAppTaskEval.generate_random_params()

class TurnOnBlueToothAndOpenApp(task_eval.TaskEval):

  app_names = ("settings",)
  complexity = 2
  schema = schema.create([schema.string("app_name", is_required=True)])

  template = "Turn on bluetooth, then open the {app_name} app"

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_on_bluetooth_task = system.SystemBluetoothTurnOn(params={"on_or_off": "on"})
    self.turn_on_bluetooth_task.initialize_task(env)
    self.open_app_task = system.OpenAppTaskEval(
        params={
            "app_name": self.params["app_name"],
        }
    )
    self.open_app_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    open_app_score = self.open_app_task.is_successful(env)
    return (bluetooth_score + open_app_score) / 2.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.open_app_task.tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return system.OpenAppTaskEval.generate_random_params()

class TurnOffBlueToothAndOpenApp(task_eval.TaskEval):

  app_names = ("settings",)
  complexity = 2
  schema = schema.create([schema.string("app_name", is_required=True)])

  template = "Turn off bluetooth, then open the {app_name} app"

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_off_bluetooth_task = system.SystemBluetoothTurnOff(params={"on_or_off": "off"})
    self.turn_off_bluetooth_task.initialize_task(env)
    self.open_app_task = system.OpenAppTaskEval(
        params={
            "app_name": self.params["app_name"],
        }
    )
    self.open_app_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    open_app_score = self.open_app_task.is_successful(env)
    return (bluetooth_score + open_app_score) / 2.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.open_app_task.tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return system.OpenAppTaskEval.generate_random_params()

class BrightnessMaxAndOpenApp(task_eval.TaskEval):

  app_names = ("settings",)
  complexity = 2
  schema = schema.create([schema.string("app_name", is_required=True)])

  template = "Turn brightness to the max value, then open the {app_name} app"

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_max_brightness_task = system.SystemBrightnessMax(
      params={'max_or_min': 'max'}
    )
    self.turn_max_brightness_task.initialize_task(env)
    self.open_app_task = system.OpenAppTaskEval(
        params={
            "app_name": self.params["app_name"],
        }
    )
    self.open_app_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    brightness_score = self.turn_max_brightness_task.is_successful(env)
    open_app_score = self.open_app_task.is_successful(env)
    return (brightness_score + open_app_score) / 2.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.open_app_task.tear_down(env)
    self.turn_max_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return system.OpenAppTaskEval.generate_random_params()

class BrightnessMinAndOpenApp(task_eval.TaskEval):

  app_names = ("settings",)
  complexity = 2
  schema = schema.create([schema.string("app_name", is_required=True)])

  template = "Turn brightness to the min value, then open the {app_name} app"

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    self.turn_min_brightness_task = system.SystemBrightnessMin(
      params={'max_or_min': 'min'}
    )
    self.turn_min_brightness_task.initialize_task(env)
    self.open_app_task = system.OpenAppTaskEval(
        params={
            "app_name": self.params["app_name"],
        }
    )
    self.open_app_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    brightness_score = self.turn_min_brightness_task.is_successful(env)
    open_app_score = self.open_app_task.is_successful(env)
    return (brightness_score + open_app_score) / 2.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.open_app_task.tear_down(env)
    self.turn_min_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return system.OpenAppTaskEval.generate_random_params()
class TurnOnWifiAndTurnOnBluetooth(task_eval.TaskEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then enable bluetooth"

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

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    return (wifi_score + bluetooth_score) / 2.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOffWifiAndTurnOffBluetooth(task_eval.TaskEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then turn off the bluetooth"

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

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    return (wifi_score + bluetooth_score) / 2.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnWifiAndTurnOffBluetooth(task_eval.TaskEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then turn off bluetooth"

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

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    return (wifi_score + bluetooth_score) / 2.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOffWifiAndBrightnessMin(task_eval.TaskEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn off WiFi, then Turn brightness to the min value"

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

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    return (wifi_score + bright_score) / 2.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_min_brightness_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnWifiAndBrightnessMin(task_eval.TaskEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then Turn brightness to the min value"

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

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    return (wifi_score + bright_score) / 2.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_min_brightness_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOffWifiAndBrightnessMax(task_eval.TaskEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn off WiFi, then Turn brightness to the max value"

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

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    return (wifi_score + bright_score) / 2.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_max_brightness_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnWifiAndBrightnessMax(task_eval.TaskEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then Turn brightness to the max value"

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

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    return (wifi_score + bright_score) / 2.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_max_brightness_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnBluetoothAndBrightnessMin(task_eval.TaskEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Enable bluetooth, then Turn brightness to the min value"

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

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    return (bright_score + bluetooth_score) / 2.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_min_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnBluetoothAndBrightnessMax(task_eval.TaskEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Enable bluetooth, then Turn brightness to the max value"

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

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    return (bright_score + bluetooth_score) / 2.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_max_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOffBluetoothAndBrightnessMax(task_eval.TaskEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn off bluetooth, then Turn brightness to the max value"

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

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    return (bright_score + bluetooth_score) / 2.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_max_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}\

class TurnOffBluetoothAndBrightnessMin(task_eval.TaskEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn off bluetooth, then Turn brightness to the min value"

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

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    return (bright_score + bluetooth_score) / 2.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_min_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnWifiAndTurnOnBluetoothAndBrightnessMax(task_eval.TaskEval):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then enable bluetooth, also Turn brightness to the max value"

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

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)
    self.turn_max_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnWifiAndTurnOnBluetoothAndBrightnessMin(task_eval.TaskEval):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then enable bluetooth, also Turn brightness to the min value"

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

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)
    self.turn_min_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnWifiAndTurnOffBluetoothAndBrightnessMax(task_eval.TaskEval):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then turn off bluetooth, also Turn brightness to the max value"

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

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)
    self.turn_max_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnWifiAndTurnOffBluetoothAndBrightnessMin(task_eval.TaskEval):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then turn off bluetooth, also Turn brightness to the min value"

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

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)
    self.turn_min_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOffWifiAndTurnOnBluetoothAndBrightnessMax(task_eval.TaskEval):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = schema.create([])

  template = "Turn off WiFi, then enable bluetooth, also Turn brightness to the max value"

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

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)
    self.turn_max_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOffWifiAndTurnOnBluetoothAndBrightnessMin(task_eval.TaskEval):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = schema.create([])

  template = "Turn off WiFi, then enable bluetooth, also Turn brightness to the min value"

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

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)
    self.turn_min_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOffWifiAndTurnOffBluetoothAndBrightnessMax(task_eval.TaskEval):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = schema.create([])

  template = "Turn off WiFi, then turn off bluetooth, also Turn brightness to the max value"

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

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)
    self.turn_max_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOffWifiAndTurnOffBluetoothAndBrightnessMin(task_eval.TaskEval):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = schema.create([])

  template = "Turn off WiFi, then turn off bluetooth, also Turn brightness to the min value"

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

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)
    self.turn_min_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnWifiAndTurnOnBluetoothAndOpenApp(task_eval.TaskEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2
  schema = schema.create([schema.string("app_name", is_required=True)])

  template = "Turn on WiFi, then enable bluetooth,also open the {app_name} app"

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
    self.open_app_task = system.OpenAppTaskEval(
      params={
        "app_name": self.params["app_name"],
      }
    )
    self.open_app_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    open_app_score = self.open_app_task.is_successful(env)
    return (wifi_score + bluetooth_score + open_app_score) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)
    self.open_app_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return system.OpenAppTaskEval.generate_random_params()

class TurnOffWifiAndTurnOffBluetoothAndOpenApp(task_eval.TaskEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([schema.string("app_name", is_required=True)])

  template = "Turn on WiFi, then turn off the bluetooth, also open the {app_name} app"

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
    self.open_app_task = system.OpenAppTaskEval(
      params={
        "app_name": self.params["app_name"],
      }
    )
    self.open_app_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    open_app_score = self.open_app_task.is_successful(env)
    return (wifi_score + bluetooth_score+open_app_score) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)
    self.open_app_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return system.OpenAppTaskEval.generate_random_params()

class TurnOffWifiAndTurnOnBluetoothAndOpenApp(task_eval.TaskEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  schema = schema.create([schema.string("app_name", is_required=True)])

  template = "Turn off WiFi, then enable bluetooth,then open the {app_name} app"

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
    self.open_app_task = system.OpenAppTaskEval(
      params={
        "app_name": self.params["app_name"],
      }
    )
    self.open_app_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    open_app_score = self.open_app_task.is_successful(env)
    return (wifi_score + bluetooth_score + open_app_score) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)
    self.open_app_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return system.OpenAppTaskEval.generate_random_params()

class TurnOnWifiAndTurnOffBluetoothAndOpenApp(task_eval.TaskEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  schema = schema.create([schema.string("app_name", is_required=True)])

  template = "Turn on WiFi, then turn off bluetooth,then open the {app_name} app"

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
    self.open_app_task = system.OpenAppTaskEval(
      params={
        "app_name": self.params["app_name"],
      }
    )
    self.open_app_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    open_app_score = self.open_app_task.is_successful(env)
    return (wifi_score + bluetooth_score + open_app_score) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)
    self.open_app_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return system.OpenAppTaskEval.generate_random_params()

class TurnOffWifiAndBrightnessMinAndOpenApp(task_eval.TaskEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  schema = schema.create([schema.string("app_name", is_required=True)])

  template = "Turn off WiFi, then Turn brightness to the min value,then open the {app_name} app"

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
    self.open_app_task = system.OpenAppTaskEval(
      params={
        "app_name": self.params["app_name"],
      }
    )
    self.open_app_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    open_app_score = self.open_app_task.is_successful(env)
    return (wifi_score + bright_score + open_app_score) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_min_brightness_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)
    self.open_app_task.tear_down(env)
  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return system.OpenAppTaskEval.generate_random_params()

class TurnOnWifiAndBrightnessMinAndOpenApp(task_eval.TaskEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  schema = schema.create([schema.string("app_name", is_required=True)])

  template = "Turn on WiFi, then Turn brightness to the min value,then open the {app_name} app"

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
    self.open_app_task = system.OpenAppTaskEval(
      params={
        "app_name": self.params["app_name"],
      }
    )
    self.open_app_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    open_app_score = self.open_app_task.is_successful(env)
    return (wifi_score + bright_score + open_app_score) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_min_brightness_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)
    self.open_app_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return system.OpenAppTaskEval.generate_random_params()

class TurnOffWifiAndBrightnessMaxAndOpenApp(task_eval.TaskEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  schema = schema.create([schema.string("app_name", is_required=True)])

  template = "Turn off WiFi, then Turn brightness to the max value,then open the {app_name} app"

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
    self.open_app_task = system.OpenAppTaskEval(
      params={
        "app_name": self.params["app_name"],
      }
    )
    self.open_app_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    open_app_score = self.open_app_task.is_successful(env)
    return (wifi_score + bright_score + open_app_score) / 3.0
  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_max_brightness_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)
    self.open_app_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return system.OpenAppTaskEval.generate_random_params()

class TurnOnWifiAndBrightnessMaxAndOpenApp(task_eval.TaskEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  schema = schema.create([schema.string("app_name", is_required=True)])

  template = "Turn on WiFi, then Turn brightness to the max value,then open the {app_name} app"

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
    self.open_app_task = system.OpenAppTaskEval(
      params={
        "app_name": self.params["app_name"],
      }
    )
    self.open_app_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    open_app_score = self.open_app_task.is_successful(env)
    return (wifi_score + bright_score + open_app_score) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_max_brightness_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)
    self.open_app_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return system.OpenAppTaskEval.generate_random_params()

class TurnOnBluetoothAndBrightnessMinAndOpenApp(task_eval.TaskEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  schema = schema.create([schema.string("app_name", is_required=True)])

  template = "Enable bluetooth, then Turn brightness to the min value,then open the {app_name} app"

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
    self.open_app_task = system.OpenAppTaskEval(
      params={
        "app_name": self.params["app_name"],
      }
    )
    self.open_app_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    open_app_score = self.open_app_task.is_successful(env)
    return (bright_score + bluetooth_score + open_app_score) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_min_brightness_task.tear_down(env)
    self.open_app_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return system.OpenAppTaskEval.generate_random_params()

class TurnOnBluetoothAndBrightnessMaxAndOpenApp(task_eval.TaskEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  schema = schema.create([schema.string("app_name", is_required=True)])

  template = "Enable bluetooth, then Turn brightness to the max value,then open the {app_name} app"

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
    self.open_app_task = system.OpenAppTaskEval(
      params={
        "app_name": self.params["app_name"],
      }
    )
    self.open_app_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    open_app_score = self.open_app_task.is_successful(env)
    return (bright_score + bluetooth_score + open_app_score) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_max_brightness_task.tear_down(env)
    self.open_app_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return system.OpenAppTaskEval.generate_random_params()

class TurnOffBluetoothAndBrightnessMaxAndOpenApp(task_eval.TaskEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  schema = schema.create([schema.string("app_name", is_required=True)])

  template = "Turn off bluetooth, then Turn brightness to the max value,then open the {app_name} app"

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
    self.open_app_task = system.OpenAppTaskEval(
        params={
            "app_name": self.params["app_name"],
        }
    )
    self.open_app_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    open_app_score = self.open_app_task.is_successful(env)
    return (bright_score + bluetooth_score + open_app_score) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_max_brightness_task.tear_down(env)
    self.open_app_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return system.OpenAppTaskEval.generate_random_params()

class TurnOffBluetoothAndBrightnessMinAndOpenApp(task_eval.TaskEval):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  schema = schema.create([schema.string("app_name", is_required=True)])
  template = "Turn off bluetooth, then Turn brightness to the min value,then open the {app_name} app"

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
    self.open_app_task = system.OpenAppTaskEval(
        params={
            "app_name": self.params["app_name"],
        }
    )
    self.open_app_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    open_app_score = self.open_app_task.is_successful(env)
    return (bright_score + bluetooth_score + open_app_score) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_min_brightness_task.tear_down(env)
    self.open_app_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return system.OpenAppTaskEval.generate_random_params()