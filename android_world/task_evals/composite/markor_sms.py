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

"""Tasks that involve Markor and SMS."""

import random
import dataclasses
from absl import logging
from android_world.env import interface
from android_world.env import device_constants
from android_world.task_evals.common_validators import sms_validators
from android_world.task_evals.single import markor
from android_world.task_evals.single import sms
from android_world.task_evals.utils import user_data_generation
from android_world.task_evals import task_eval
from android_world.utils import file_utils

@dataclasses.dataclass(frozen=True)
class _Note:
  name: str
  content: str


generate_random_sentence = lambda: random.choice(
    user_data_generation.RANDOM_SENTENCES
)


def _generate_random_note() -> _Note:
  """Generates a random note."""
  extensions = [".md", ".txt"]
  random_file_name = (
      user_data_generation.generate_random_file_name()
      + random.choice(extensions)
  )
  return _Note(random_file_name, generate_random_sentence())

class MarkorAndSms(task_eval.TaskEval):
  app_names = ("markor","simple sms messenger")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    file_utils.clear_directory(device_constants.MARKOR_DATA, env.base_env)

  def tear_down(self, env: interface.AsyncEnv) -> None:
    super().tear_down(env)
    file_utils.clear_directory(device_constants.MARKOR_DATA, env.base_env)

class MarkorCreateNoteAndSms(markor.Markor):
  """Task for checking that a new note in Markor has been created and then an SMS has been sent."""

  app_names = ("markor", "simple sms messenger")
  complexity = 2
  schema = {
      "type": "object",
      "properties": {
          "file_name": {"type": "string"},
          "text": {"type": "string"},
          "number": {"type": "string"},
      },
      "required": ["file_name", "text", "number"],
  }

  template = (
      "Create a new note in Markor named {file_name} with the following text:"
      " {text}. Share the entire content of the note with the phone number"
      " {number} via SMS using Simple SMS Messenger"
  )

  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    self.markor_task = markor.MarkorCreateNote(
        params={
            "file_name": self.params["file_name"],
            "text": self.params["text"],
        }
    )
    self.markor_task.initialize_task(env)

    self.sms_task = sms_validators.SimpleSMSSendSms(
        params={"number": self.params["number"], "message": self.params["text"]}
    )
    self.sms_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    markor_success = self.markor_task.is_successful(env)
    logging.info("Markor success: %s", markor_success)

    sms_success = self.sms_task.is_successful(env)
    logging.info("SMS success: %s", sms_success)

    return (markor_success + sms_success) / 2.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.markor_task.tear_down(env)
    self.sms_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
    markor_params = markor.MarkorCreateNote.generate_random_params()
    sms_params = sms_validators.SimpleSMSSendSms.generate_random_params()

    compound_params = {
        "file_name": markor_params["file_name"],
        "text": markor_params["text"],
        "number": sms_params["number"],
    }

    return compound_params

class MarkorCreateNoteAndSmsRelpy(markor.Markor):
  """Task for checking that a new note in Markor has been created and then an SMS has been sent."""

  app_names = ("markor", "simple sms messenger")
  complexity = 2
  schema = {
      "type": "object",
      "properties": {
          "file_name": {"type": "string"},
          "text": {"type": "string"},
          "number": {"type": "string"},
      },
      "required": ["file_name", "text", "number"],
  }

  template = (
      "Create a new note in Markor named {file_name} with the following text:"
      " {text}. Reply to {number} with the entire content of the note "
      " via SMS using Simple SMS Messenger"
  )

  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    self.markor_task = markor.MarkorCreateNote(
        params={
            "file_name": self.params["file_name"],
            "text": self.params["text"],
        }
    )
    self.markor_task.initialize_task(env)

    self.sms_task = sms.SimpleSmsReply(
        params={"number": self.params["number"], "message": self.params["text"]}
    )
    self.sms_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    markor_success = self.markor_task.is_successful(env)
    logging.info("Markor success: %s", markor_success)

    sms_success = self.sms_task.is_successful(env)
    logging.info("SMS success: %s", sms_success)

    return (markor_success + sms_success) / 2.0

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self.markor_task.tear_down(env)
    self.sms_task.tear_down(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
    markor_params = markor.MarkorCreateNote.generate_random_params()
    sms_params = sms_validators.SimpleSMSSendSms.generate_random_params()

    compound_params = {
        "file_name": markor_params["file_name"],
        "text": markor_params["text"],
        "number": sms_params["number"],
    }

    return compound_params




