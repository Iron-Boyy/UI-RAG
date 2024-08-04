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

"""Tasks for the file manager app."""

import os
import random
from typing import Any
import datetime
from android_world.env import device_constants
from android_world.env import interface
from android_world.task_evals import task_eval
from android_world.task_evals.common_validators import file_validators
from android_world.task_evals.utils import user_data_generation
from android_world.utils import file_utils

class FilesMoveFile(task_eval.TaskEval):
  """Task for checking that a file has been moved."""

  app_names = ("files",)
  complexity = 2
  schema = file_validators.MoveFile.schema
  template = (
      "Move the file {file_name} from {source_folder} within the"
      " sdk_gphone_x86_64 storage area to the {destination_folder} within the"
      " same sdk_gphone_x86_64 storage area in the Android filesystem."
  )

  def __init__(self, params: dict[str, Any]):
    super().__init__(params)
    self.move_file_task = file_validators.MoveFile(
        params, device_constants.EMULATOR_DATA
    )

  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    self.move_file_task.initialize_task(env)

  def tear_down(self, env: interface.AsyncEnv) -> None:
    super().tear_down(env)
    self.move_file_task.tear_down(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    return self.move_file_task.is_successful(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    source_folder = random.choice(
        list(user_data_generation.EMULATOR_DIRECTORIES.keys())
    )
    destination_folder = random.choice([
        folder
        for folder in user_data_generation.EMULATOR_DIRECTORIES
        if folder != source_folder
    ])
    noise_candidates = user_data_generation.EMULATOR_DIRECTORIES[source_folder]

    destination_candidates = user_data_generation.EMULATOR_DIRECTORIES[
        destination_folder
    ]
    file_name = random.choice(destination_candidates)

    return {
        "file_name": file_name,
        "source_folder": source_folder,
        "destination_folder": destination_folder,
        "noise_candidates": noise_candidates,
    }

class FilesDeleteFile(task_eval.TaskEval):
  """Task for checking that a file has been deleted."""

  app_names = ("files",)
  complexity = 1
  schema = file_validators.DeleteFile.schema
  template = (
      "Delete the file {file_name} from the Android filesystem located in the"
      " {subfolder} folder within the sdk_gphone_x86_64 storage area."
  )

  def __init__(self, params: dict[str, Any]):
    super().__init__(params)
    self.delete_file_task = file_validators.DeleteFile(
        params, device_constants.EMULATOR_DATA
    )

  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    self.delete_file_task.initialize_task(env)

  def tear_down(self, env: interface.AsyncEnv) -> None:
    super().tear_down(env)
    self.delete_file_task.tear_down(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    return self.delete_file_task.is_successful(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    subfolder = random.choice(
        list(user_data_generation.EMULATOR_DIRECTORIES.keys())
    )
    noise_candidates = user_data_generation.EMULATOR_DIRECTORIES[subfolder]
    _, ext_part = os.path.splitext(noise_candidates[0])
    file_name = user_data_generation.generate_random_file_name() + ext_part
    return {
        "file_name": file_name,
        "subfolder": subfolder,
        "noise_candidates": noise_candidates,
    }

class FilesMoveFileAndDelete(task_eval.TaskEval):
  """Task for checking that a file has been moved."""

  app_names = ("files",)
  complexity = 2
  schema = file_validators.MoveFile.schema
  template = (
      "Move the file {file_name} from {source_folder} within the"
      " sdk_gphone_x86_64 storage area to the {destination_folder} within the"
      " same sdk_gphone_x86_64 storage area in the Android filesystem. then delete it"
  )

  def __init__(self, params: dict[str, Any]):
    super().__init__(params)
    self.move_file_task = file_validators.MoveFile(
        params, device_constants.EMULATOR_DATA
    )
    self.delete_file_task = file_validators.DeleteFile(
        params, device_constants.EMULATOR_DATA
    )

  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    self.move_file_task.initialize_task(env)

  def tear_down(self, env: interface.AsyncEnv) -> None:
    super().tear_down(env)
    self.delete_file_task.tear_down(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    return self.delete_file_task.is_successful(env)

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    source_folder = random.choice(
        list(user_data_generation.EMULATOR_DIRECTORIES.keys())
    )
    destination_folder = random.choice([
        folder
        for folder in user_data_generation.EMULATOR_DIRECTORIES
        if folder != source_folder
    ])
    noise_candidates = user_data_generation.EMULATOR_DIRECTORIES[source_folder]

    destination_candidates = user_data_generation.EMULATOR_DIRECTORIES[
        destination_folder
    ]
    file_name = random.choice(destination_candidates)

    return {
        "file_name": file_name,
        "source_folder": source_folder,
        "destination_folder": destination_folder,
        "noise_candidates": noise_candidates,
    }

class FilesCreateFolder(task_eval.TaskEval):
  """Task for checking that a new folder in Markor has been created with a specific name."""
  app_names = ("files",)
  complexity = 2
  schema = {
      "type": "object",
      "properties": {
          "folder_name": {"type": "string"},
      },
      "required": ["folder_name"],
  }
  template = "Create a new folder named {folder_name} in the files app. "

  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)


  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    folder_name = self.params["folder_name"]
    exists = file_utils.check_file_or_folder_exists(
        self.params["folder_name"],  device_constants.DOWNLOAD_DATA, env.base_env
    )
    if not exists:
      return 0.0

    return 1.0

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
    random_folder_name = "folder_" + str(
        datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    )
    return {"folder_name": random_folder_name}