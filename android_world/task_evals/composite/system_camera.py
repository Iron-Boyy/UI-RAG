from typing import Any

from android_world.env import interface
from android_world.task_evals import task_eval
from android_world.task_evals.single import system
from android_world.task_evals.utils import schema
from android_world.task_evals.single import  camera
from absl import logging

class _System(task_eval.TaskEval):
  """Base class for Camera tasks."""

  app_names = ("settings",)

class TurnOffWifiAndTurnOnBluetoothAndTakeVideo(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn off WiFi, then enable bluetooth,then Take one video"

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
    self.camera_task = camera.CameraTakeVideo(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (wifi_score + bluetooth_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnWifiAndTurnOnBluetoothAndTakeVideo(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then enable bluetooth,then Take one video"

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
    self.camera_task = camera.CameraTakeVideo(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (wifi_score + bluetooth_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOffWifiAndTurnOffBluetoothAndTakeVideo(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then turn off the bluetooth,then Take one video"

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
    self.camera_task = camera.CameraTakeVideo(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (wifi_score + bluetooth_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnWifiAndTurnOffBluetoothAndTakeVideo(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then turn off bluetooth,and then take one video"

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
    self.camera_task = camera.CameraTakeVideo(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (wifi_score + bluetooth_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOffWifiAndBrightnessMinAndTakeVideo(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn off WiFi, then Turn brightness to the min value,then Take one video"

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
    self.camera_task = camera.CameraTakeVideo(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (wifi_score + bright_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_min_brightness_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnWifiAndBrightnessMinAndTakeVideo(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then Turn brightness to the min value,then Take one video"

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
    self.camera_task = camera.CameraTakeVideo(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (wifi_score + bright_score) + camera_success / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_min_brightness_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOffWifiAndBrightnessMaxAndTakeVideo(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn off WiFi, then Turn brightness to the max value,then Take one video"

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
    self.camera_task = camera.CameraTakeVideo(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (wifi_score + bright_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_max_brightness_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnWifiAndBrightnessMaxAndTakeVideo(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then Turn brightness to the max value, then Take one video"

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
    self.camera_task = camera.CameraTakeVideo(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (wifi_score + bright_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_max_brightness_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnBluetoothAndBrightnessMinAndTakeVideo(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Enable bluetooth, then Turn brightness to the min value,then take one video"

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
    self.camera_task = camera.CameraTakeVideo(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (bluetooth_score + bright_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_min_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnBluetoothAndBrightnessMaxAndTakeVideo(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Enable bluetooth, then Turn brightness to the max value,then take one video"

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
    self.camera_task = camera.CameraTakeVideo(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (bright_score + bright_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_max_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOffBluetoothAndBrightnessMaxAndTakeVideo(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn off bluetooth, then Turn brightness to the max value and take one video"

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
    self.camera_task = camera.CameraTakeVideo(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (bluetooth_score + bright_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_max_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}\

class TurnOffBluetoothAndBrightnessMinAndTakeVideo(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn off bluetooth, then Turn brightness to the min value then take one video"

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
    self.camera_task = camera.CameraTakeVideo(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (bluetooth_score + bright_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_min_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnWifiAndTurnOnBluetoothAndBrightnessMaxAndTakeVideo(_System,camera._Camera):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then enable bluetooth, also Turn brightness to the max value,then take one video"

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
    self.camera_task = camera.CameraTakeVideo(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +camera_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)
    self.turn_max_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnWifiAndTurnOnBluetoothAndBrightnessMinAndTakeVideo(_System,camera._Camera):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then enable bluetooth, also Turn brightness to the min value, then take one video"

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
    self.camera_task = camera.CameraTakeVideo(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +camera_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)
    self.turn_min_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnWifiAndTurnOffBluetoothAndBrightnessMaxAndTakeVideo(_System,camera._Camera):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then turn off bluetooth, also Turn brightness to the max value, then take one video"

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
    self.camera_task = camera.CameraTakeVideo(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +camera_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)
    self.turn_max_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnWifiAndTurnOffBluetoothAndBrightnessMinAndTakeVideo(_System,camera._Camera):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then turn off bluetooth, also Turn brightness to the min value, then take one video"

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
    self.camera_task = camera.CameraTakeVideo(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +camera_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)
    self.turn_min_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOffWifiAndTurnOnBluetoothAndBrightnessMaxAndTakeVideo(_System,camera._Camera):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = schema.create([])

  template = "Turn off WiFi, then enable bluetooth, also Turn brightness to the max value, then take one video"

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
    self.camera_task = camera.CameraTakeVideo(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +camera_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)
    self.turn_max_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOffWifiAndTurnOnBluetoothAndBrightnessMinAndTakeVideo(_System,camera._Camera):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = schema.create([])

  template = "Turn off WiFi, then enable bluetooth, also Turn brightness to the min value, then take one video"

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
    self.camera_task = camera.CameraTakeVideo(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +camera_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)
    self.turn_min_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOffWifiAndTurnOffBluetoothAndBrightnessMaxAndTakeVideo(_System,camera._Camera):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = schema.create([])

  template = "Turn off WiFi, then turn off bluetooth, also Turn brightness to the max value, then take one video"

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
    self.camera_task = camera.CameraTakeVideo(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +camera_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)
    self.turn_max_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOffWifiAndTurnOffBluetoothAndBrightnessMinAndTakeVideo(_System,camera._Camera):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = schema.create([])

  template = "Turn off WiFi, then turn off bluetooth, also Turn brightness to the min value, and then take one video"

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
    self.camera_task = camera.CameraTakeVideo(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +camera_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)
    self.turn_min_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOffWifiAndTurnOnBluetoothAndTakeVideos(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn off WiFi, then enable bluetooth,then Take two videos"

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
    self.camera_task = camera.CameraTakeVideos(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (wifi_score + bluetooth_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnWifiAndTurnOnBluetoothAndTakeVideos(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then enable bluetooth,then Take two videos"

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
    self.camera_task = camera.CameraTakeVideos(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (wifi_score + bluetooth_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOffWifiAndTurnOffBluetoothAndTakeVideos(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then turn off the bluetooth,then Take two videos"

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
    self.camera_task = camera.CameraTakeVideos(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (wifi_score + bluetooth_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnWifiAndTurnOffBluetoothAndTakeVideos(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then turn off bluetooth,then Take two videos"

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
    self.camera_task = camera.CameraTakeVideos(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (wifi_score + bluetooth_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOffWifiAndBrightnessMinAndTakeVideos(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn off WiFi, then Turn brightness to the min value,then Take two videos"

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
    self.camera_task = camera.CameraTakeVideos(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (wifi_score + bright_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_min_brightness_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnWifiAndBrightnessMinAndTakeVideos(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then Turn brightness to the min value, then Take two videos"

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
    self.camera_task = camera.CameraTakeVideos(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (wifi_score + bright_score) + camera_success / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_min_brightness_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOffWifiAndBrightnessMaxAndTakeVideos(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn off WiFi, then Turn brightness to the max value,then Take two videos"

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
    self.camera_task = camera.CameraTakeVideos(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (wifi_score + bright_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_max_brightness_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnWifiAndBrightnessMaxAndTakeVideos(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then Turn brightness to the max value, then Take two videos"

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
    self.camera_task = camera.CameraTakeVideos(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (wifi_score + bright_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_max_brightness_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnBluetoothAndBrightnessMinAndTakeVideos(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Enable bluetooth, then Turn brightness to the min value,then Take two videos"

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
    self.camera_task = camera.CameraTakeVideos(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (bluetooth_score + bright_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_min_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnBluetoothAndBrightnessMaxAndTakeVideos(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Enable bluetooth, then Turn brightness to the max value,then Take two videos"

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
    self.camera_task = camera.CameraTakeVideos(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (bright_score + bright_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_max_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOffBluetoothAndBrightnessMaxAndTakeVideos(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn off bluetooth, then Turn brightness to the max value,then Take two videos"

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
    self.camera_task = camera.CameraTakeVideos(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (bluetooth_score + bright_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_max_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}\

class TurnOffBluetoothAndBrightnessMinAndTakeVideos(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn off bluetooth, then Turn brightness to the min value then Take two videos"

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
    self.camera_task = camera.CameraTakeVideos(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (bluetooth_score + bright_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_min_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnWifiAndTurnOnBluetoothAndBrightnessMaxAndTakeVideos(_System,camera._Camera):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then enable bluetooth, also Turn brightness to the max value,then Take two videos"

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
    self.camera_task = camera.CameraTakeVideos(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +camera_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)
    self.turn_max_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnWifiAndTurnOnBluetoothAndBrightnessMinAndTakeVideos(_System,camera._Camera):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then enable bluetooth, also Turn brightness to the min value, then Take two videos"

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
    self.camera_task = camera.CameraTakeVideos(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +camera_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)
    self.turn_min_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnWifiAndTurnOffBluetoothAndBrightnessMaxAndTakeVideos(_System,camera._Camera):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then turn off bluetooth, also Turn brightness to the max value, then Take two videos"

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
    self.camera_task = camera.CameraTakeVideos(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score + camera_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)
    self.turn_max_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnWifiAndTurnOffBluetoothAndBrightnessMinAndTakeVideos(_System,camera._Camera):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then turn off bluetooth, also Turn brightness to the min value,then Take two videos"

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
    self.camera_task = camera.CameraTakeVideos(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score + camera_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)
    self.turn_min_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOffWifiAndTurnOnBluetoothAndBrightnessMaxAndTakeVideos(_System,camera._Camera):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = schema.create([])

  template = "Turn off WiFi, then enable bluetooth, also Turn brightness to the max value, then Take two videos"

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
    self.camera_task = camera.CameraTakeVideos(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score + camera_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)
    self.turn_max_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOffWifiAndTurnOnBluetoothAndBrightnessMinAndTakeVideos(_System,camera._Camera):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = schema.create([])

  template = "Turn off WiFi, then enable bluetooth, also Turn brightness to the min value,then Take two videos"

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
    self.camera_task = camera.CameraTakeVideos(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +camera_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)
    self.turn_min_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOffWifiAndTurnOffBluetoothAndBrightnessMaxAndTakeVideos(_System,camera._Camera):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = schema.create([])

  template = "Turn off WiFi, then turn off bluetooth, also Turn brightness to the max value, then Take two videos"

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
    self.camera_task = camera.CameraTakeVideos(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score + camera_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)
    self.turn_max_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOffWifiAndTurnOffBluetoothAndBrightnessMinAndTakeVideos(_System,camera._Camera):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = schema.create([])

  template = "Turn off WiFi, then turn off bluetooth, also Turn brightness to the min value, and then Take two videos"

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
    self.camera_task = camera.CameraTakeVideos(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score + camera_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)
    self.turn_min_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}



class TurnOffWifiAndTurnOnBluetoothAndTakePhoto(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn off WiFi, then enable bluetooth,then Take one photo"

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
    self.camera_task = camera.CameraTakePhoto(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    logging.info("camera success: %s", wifi_score)
    logging.info("camera success: %s", bluetooth_score)
    return (wifi_score + bluetooth_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnWifiAndTurnOnBluetoothAndTakePhoto(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then enable bluetooth,then Take one Photo"

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
    self.camera_task = camera.CameraTakePhoto(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (wifi_score + bluetooth_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOffWifiAndTurnOffBluetoothAndTakePhoto(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then turn off the bluetooth,then Take one Photo"

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
    self.camera_task = camera.CameraTakePhoto(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (wifi_score + bluetooth_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnWifiAndTurnOffBluetoothAndTakePhoto(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then turn off bluetooth,and then take one Photo"

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
    self.camera_task = camera.CameraTakePhoto(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (wifi_score + bluetooth_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOffWifiAndBrightnessMinAndTakePhoto(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn off WiFi, then Turn brightness to the min value,then Take one Photo"

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
    self.camera_task = camera.CameraTakePhoto(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (wifi_score + bright_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_min_brightness_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnWifiAndBrightnessMinAndTakePhoto(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then Turn brightness to the min value,then Take one Photo"

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
    self.camera_task = camera.CameraTakePhoto(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (wifi_score + bright_score) + camera_success / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_min_brightness_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOffWifiAndBrightnessMaxAndTakePhoto(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn off WiFi, then Turn brightness to the max value,then Take one Photo"

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
    self.camera_task = camera.CameraTakePhoto(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (wifi_score + bright_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_max_brightness_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnWifiAndBrightnessMaxAndTakePhoto(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then Turn brightness to the max value, then Take one Photo"

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
    self.camera_task = camera.CameraTakePhoto(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (wifi_score + bright_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_max_brightness_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnBluetoothAndBrightnessMinAndTakePhoto(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Enable bluetooth, then Turn brightness to the min value,then take one Photo"

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
    self.camera_task = camera.CameraTakePhoto(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (bluetooth_score + bright_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_min_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnBluetoothAndBrightnessMaxAndTakePhoto(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Enable bluetooth, then Turn brightness to the max value,then take one Photo"

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
    self.camera_task = camera.CameraTakePhoto(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (bright_score + bright_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_max_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOffBluetoothAndBrightnessMaxAndTakePhoto(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn off bluetooth, then Turn brightness to the max value and take one Photo"

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
    self.camera_task = camera.CameraTakePhoto(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (bluetooth_score + bright_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_max_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}\

class TurnOffBluetoothAndBrightnessMinAndTakePhoto(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn off bluetooth, then Turn brightness to the min value then take one Photo"

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
    self.camera_task = camera.CameraTakePhoto(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (bluetooth_score + bright_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_min_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnWifiAndTurnOnBluetoothAndBrightnessMaxAndTakePhoto(_System,camera._Camera):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then enable bluetooth, also Turn brightness to the max value,then take one Photo"

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
    self.camera_task = camera.CameraTakePhoto(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +camera_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)
    self.turn_max_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnWifiAndTurnOnBluetoothAndBrightnessMinAndTakePhoto(_System,camera._Camera):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then enable bluetooth, also Turn brightness to the min value, then take one Photo"

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
    self.camera_task = camera.CameraTakePhoto(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +camera_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)
    self.turn_min_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnWifiAndTurnOffBluetoothAndBrightnessMaxAndTakePhoto(_System,camera._Camera):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then turn off bluetooth, also Turn brightness to the max value, then take one Photo"

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
    self.camera_task = camera.CameraTakePhoto(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +camera_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)
    self.turn_max_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnWifiAndTurnOffBluetoothAndBrightnessMinAndTakePhoto(_System,camera._Camera):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then turn off bluetooth, also Turn brightness to the min value, then take one Photo"

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
    self.camera_task = camera.CameraTakePhoto(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +camera_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)
    self.turn_min_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOffWifiAndTurnOnBluetoothAndBrightnessMaxAndTakePhoto(_System,camera._Camera):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = schema.create([])

  template = "Turn off WiFi, then enable bluetooth, also Turn brightness to the max value, then take one Photo"

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
    self.camera_task = camera.CameraTakePhoto(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +camera_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)
    self.turn_max_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOffWifiAndTurnOnBluetoothAndBrightnessMinAndTakePhoto(_System,camera._Camera):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = schema.create([])

  template = "Turn off WiFi, then enable bluetooth, also Turn brightness to the min value, then take one Photo"

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
    self.camera_task = camera.CameraTakePhoto(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +camera_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)
    self.turn_min_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOffWifiAndTurnOffBluetoothAndBrightnessMaxAndTakePhoto(_System,camera._Camera):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = schema.create([])

  template = "Turn off WiFi, then turn off bluetooth, also Turn brightness to the max value, then take one Photo"

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
    self.camera_task = camera.CameraTakePhoto(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +camera_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)
    self.turn_max_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOffWifiAndTurnOffBluetoothAndBrightnessMinAndTakePhoto(_System,camera._Camera):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = schema.create([])

  template = "Turn off WiFi, then turn off bluetooth, also Turn brightness to the min value, and then take one Photo"

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
    self.camera_task = camera.CameraTakePhoto(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +camera_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)
    self.turn_min_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}


class TurnOffWifiAndTurnOnBluetoothAndTakePhotos(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn off WiFi, then enable bluetooth,then Take three photos"

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
    self.camera_task = camera.CameraTakePhotoss(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (wifi_score + bluetooth_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnWifiAndTurnOnBluetoothAndTakePhotos(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then enable bluetooth,then Take three Photos"

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
    self.camera_task = camera.CameraTakePhotos(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (wifi_score + bluetooth_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOffWifiAndTurnOffBluetoothAndTakePhotos(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then turn off the bluetooth,then Take three Photos"

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
    self.camera_task = camera.CameraTakePhotos(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (wifi_score + bluetooth_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnWifiAndTurnOffBluetoothAndTakePhotos(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then turn off bluetooth,and then Take three Photos"

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
    self.camera_task = camera.CameraTakePhotos(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (wifi_score + bluetooth_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOffWifiAndBrightnessMinAndTakePhotos(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn off WiFi, then Turn brightness to the min value,then Take three Photos"

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
    self.camera_task = camera.CameraTakePhotos(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (wifi_score + bright_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_min_brightness_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnWifiAndBrightnessMinAndTakePhotos(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then Turn brightness to the min value,then Take three Photos"

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
    self.camera_task = camera.CameraTakePhotos(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (wifi_score + bright_score) + camera_success / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_min_brightness_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOffWifiAndBrightnessMaxAndTakePhotos(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn off WiFi, then Turn brightness to the max value,then Take three Photos"

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
    self.camera_task = camera.CameraTakePhotos(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (wifi_score + bright_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_max_brightness_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnWifiAndBrightnessMaxAndTakePhotos(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then Turn brightness to the max value, then Take three Photos"

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
    self.camera_task = camera.CameraTakePhotos(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (wifi_score + bright_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_max_brightness_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnBluetoothAndBrightnessMinAndTakePhotos(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Enable bluetooth, then Turn brightness to the min value,then Take three Photos"

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
    self.camera_task = camera.CameraTakePhotos(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (bluetooth_score + bright_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_min_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnBluetoothAndBrightnessMaxAndTakePhotos(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Enable bluetooth, then Turn brightness to the max value,then Take three Photos"

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
    self.camera_task = camera.CameraTakePhotos(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (bright_score + bright_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_max_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOffBluetoothAndBrightnessMaxAndTakePhotos(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn off bluetooth, then Turn brightness to the max value and Take three Photos"

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
    self.camera_task = camera.CameraTakePhotos(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (bluetooth_score + bright_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_max_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}\

class TurnOffBluetoothAndBrightnessMinAndTakePhotos(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn off bluetooth, then Turn brightness to the min value then Take three Photos"

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
    self.camera_task = camera.CameraTakePhotos(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (bluetooth_score + bright_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_min_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnWifiAndTurnOnBluetoothAndBrightnessMaxAndTakePhotos(_System,camera._Camera):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then enable bluetooth, also Turn brightness to the max value,then Take three Photos"

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
    self.camera_task = camera.CameraTakePhotos(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +camera_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)
    self.turn_max_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnWifiAndTurnOnBluetoothAndBrightnessMinAndTakePhotos(_System,camera._Camera):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then enable bluetooth, also Turn brightness to the min value, then Take three Photos"

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
    self.camera_task = camera.CameraTakePhotos(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +camera_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)
    self.turn_min_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnWifiAndTurnOffBluetoothAndBrightnessMaxAndTakePhotos(_System,camera._Camera):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then turn off bluetooth, also Turn brightness to the max value, then Take three Photos"

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
    self.camera_task = camera.CameraTakePhotos(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +camera_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)
    self.turn_max_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnWifiAndTurnOffBluetoothAndBrightnessMinAndTakePhotos(_System,camera._Camera):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then turn off bluetooth, also Turn brightness to the min value, then Take three Photos"

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
    self.camera_task = camera.CameraTakePhotos(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +camera_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)
    self.turn_min_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOffWifiAndTurnOnBluetoothAndBrightnessMaxAndTakePhotos(_System,camera._Camera):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = schema.create([])

  template = "Turn off WiFi, then enable bluetooth, also Turn brightness to the max value, then Take three Photos"

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
    self.camera_task = camera.CameraTakePhotos(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +camera_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)
    self.turn_max_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOffWifiAndTurnOnBluetoothAndBrightnessMinAndTakePhotos(_System,camera._Camera):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = schema.create([])

  template = "Turn off WiFi, then enable bluetooth, also Turn brightness to the min value, then Take three Photos"

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
    self.camera_task = camera.CameraTakePhotos(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +camera_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)
    self.turn_min_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOffWifiAndTurnOffBluetoothAndBrightnessMaxAndTakePhotos(_System,camera._Camera):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = schema.create([])

  template = "Turn off WiFi, then turn off bluetooth, also Turn brightness to the max value, then Take three Photos"

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
    self.camera_task = camera.CameraTakePhotos(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +camera_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)
    self.turn_max_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOffWifiAndTurnOffBluetoothAndBrightnessMinAndTakePhotos(_System,camera._Camera):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = schema.create([])

  template = "Turn off WiFi, then turn off bluetooth, also Turn brightness to the min value, and then Take three Photos"

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
    self.camera_task = camera.CameraTakePhotos(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +camera_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)
    self.turn_min_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOffWifiAndTurnOnBluetoothAndTakePhotoAndVideo(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = schema.create([])

  template = "Turn off WiFi, then enable bluetooth,then Take one photo and one video."

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
    self.camera_task = camera.CameraTakePhotoAndVideo(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (wifi_score + bluetooth_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnWifiAndTurnOnBluetoothAndTakePhotoAndVideo(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then enable bluetooth,then Take one photo and one video."

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
    self.camera_task = camera.CameraTakePhotoAndVideo(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (wifi_score + bluetooth_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOffWifiAndTurnOffBluetoothAndTakePhotoAndVideo(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then turn off the bluetooth,then Take one photo and one video."

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
    self.camera_task = camera.CameraTakePhotoAndVideo(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (wifi_score + bluetooth_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnWifiAndTurnOffBluetoothAndTakePhotoAndVideo(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then turn off bluetooth,and then Take one photo and one video."

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
    self.camera_task = camera.CameraTakePhotoAndVideo(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (wifi_score + bluetooth_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOffWifiAndBrightnessMinAndTakePhotoAndVideo(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn off WiFi, then Turn brightness to the min value,then Take one photo and one video."

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
    self.camera_task = camera.CameraTakePhotoAndVideo(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (wifi_score + bright_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_min_brightness_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnWifiAndBrightnessMinAndTakePhotoAndVideo(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then Turn brightness to the min value,then Take one photo and one video."

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
    self.camera_task = camera.CameraTakePhotoAndVideo(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (wifi_score + bright_score) + camera_success / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_min_brightness_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOffWifiAndBrightnessMaxAndTakePhotoAndVideo(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn off WiFi, then Turn brightness to the max value,then Take one photo and one video."

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
    self.camera_task = camera.CameraTakePhotoAndVideo(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (wifi_score + bright_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_max_brightness_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnWifiAndBrightnessMaxAndTakePhotoAndVideo(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then Turn brightness to the max value, then Take one photo and one video."

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
    self.camera_task = camera.CameraTakePhotoAndVideo(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (wifi_score + bright_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_max_brightness_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnBluetoothAndBrightnessMinAndTakePhotoAndVideo(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Enable bluetooth, then Turn brightness to the min value,then Take one photo and one video."

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
    self.camera_task = camera.CameraTakePhotoAndVideo(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (bluetooth_score + bright_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_min_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnBluetoothAndBrightnessMaxAndTakePhotoAndVideo(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Enable bluetooth, then Turn brightness to the max value,then Take one photo and one video."

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
    self.camera_task = camera.CameraTakePhotoAndVideo(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (bright_score + bright_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_max_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOffBluetoothAndBrightnessMaxAndTakePhotoAndVideo(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn off bluetooth, then Turn brightness to the max value and Take one photo and one video."

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
    self.camera_task = camera.CameraTakePhotoAndVideo(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (bluetooth_score + bright_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_max_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}\

class TurnOffBluetoothAndBrightnessMinAndTakePhotoAndVideo(_System,camera._Camera):
  """Evals the agent turning off WiFi and enabling bluetooth."""

  app_names = ("settings",)
  complexity = 2

  # No parameters.
  schema = schema.create([])

  template = "Turn off bluetooth, then Turn brightness to the min value then Take one photo and one video."

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
    self.camera_task = camera.CameraTakePhotoAndVideo(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)
    return (bluetooth_score + bright_score + camera_success) / 3.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_min_brightness_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnWifiAndTurnOnBluetoothAndBrightnessMaxAndTakePhotoAndVideo(_System,camera._Camera):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then enable bluetooth, also Turn brightness to the max value,then Take one photo and one video."

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
    self.camera_task = camera.CameraTakePhotoAndVideo(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +camera_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)
    self.turn_max_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnWifiAndTurnOnBluetoothAndBrightnessMinAndTakePhotoAndVideo(_System,camera._Camera):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then enable bluetooth, also Turn brightness to the min value, then Take one photo and one video."

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
    self.camera_task = camera.CameraTakePhotoAndVideo(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +camera_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)
    self.turn_min_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnWifiAndTurnOffBluetoothAndBrightnessMaxAndTakePhotoAndVideo(_System,camera._Camera):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then turn off bluetooth, also Turn brightness to the max value, then Take one photo and one video."

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
    self.camera_task = camera.CameraTakePhotoAndVideo(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +camera_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)
    self.turn_max_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOnWifiAndTurnOffBluetoothAndBrightnessMinAndTakePhotoAndVideo(_System,camera._Camera):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = schema.create([])

  template = "Turn on WiFi, then turn off bluetooth, also Turn brightness to the min value, then Take one photo and one video."

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
    self.camera_task = camera.CameraTakePhotoAndVideo(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_on_wifi_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +camera_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_on_wifi_task.tear_down(env)
    self.turn_min_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOffWifiAndTurnOnBluetoothAndBrightnessMaxAndTakePhotoAndVideo(_System,camera._Camera):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = schema.create([])

  template = "Turn off WiFi, then enable bluetooth, also Turn brightness to the max value, then Take one photo and one video."

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
    self.camera_task = camera.CameraTakePhotoAndVideo(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +camera_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)
    self.turn_max_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOffWifiAndTurnOnBluetoothAndBrightnessMinAndTakePhotoAndVideo(_System,camera._Camera):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = schema.create([])

  template = "Turn off WiFi, then enable bluetooth, also Turn brightness to the min value, then Take one photo and one video."

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
    self.camera_task = camera.CameraTakePhotoAndVideo(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_on_bluetooth_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +camera_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_on_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)
    self.turn_min_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOffWifiAndTurnOffBluetoothAndBrightnessMaxAndTakePhotoAndVideo(_System,camera._Camera):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = schema.create([])

  template = "Turn off WiFi, then turn off bluetooth, also Turn brightness to the max value, then Take one photo and one video."

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
    self.camera_task = camera.CameraTakePhotoAndVideo(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    bright_score = self.turn_max_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +camera_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)
    self.turn_max_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class TurnOffWifiAndTurnOffBluetoothAndBrightnessMinAndTakePhotoAndVideo(_System,camera._Camera):

  app_names = ("settings",)
  complexity = 3

  # No parameters.
  schema = schema.create([])

  template = "Turn off WiFi, then turn off bluetooth, also Turn brightness to the min value, and then Take one photo and one video."

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
    self.camera_task = camera.CameraTakePhotoAndVideo(
        params={}
    )
    self.camera_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    wifi_score = self.turn_off_wifi_task.is_successful(env)
    bluetooth_score = self.turn_off_bluetooth_task.is_successful(env)
    bright_score = self.turn_min_brightness_task.is_successful(env)
    camera_success = self.camera_task.is_successful(env)
    return (wifi_score + bluetooth_score + bright_score +camera_success) / 4.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.turn_off_bluetooth_task.tear_down(env)
    self.turn_off_wifi_task.tear_down(env)
    self.turn_min_brightness_task.tear_down((env))

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}