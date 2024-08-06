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

"""Tasks for the camera app."""

from typing import Any
import subprocess
from absl import logging
from android_world.env import adb_utils
from android_world.env import device_constants
from android_world.env import interface
from android_world.task_evals import task_eval
from android_world.utils import file_utils


class _Camera(task_eval.TaskEval):
  """Base class for Camera tasks."""

  app_names = ("camera",)

  def _clear_app_data(self, env: interface.AsyncEnv) -> None:
    """Clears the app data."""
    file_utils.clear_directory(device_constants.PHOTOS_DATA, env.base_env)
    file_utils.clear_directory(device_constants.VIDEOS_DATA, env.base_env)

  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    self._clear_app_data(env)

  def tear_down(self, env: interface.AsyncEnv):
    super().tear_down(env)
    self._clear_app_data(env)


class CameraTakeVideo(_Camera):
  """Task for checking that one single video has been taken."""

  complexity = 1
  schema = {
      "type": "object",
      "properties": {},
      "required": [],
  }
  template = "Take one video."

  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    contents = adb_utils.issue_generic_request(
        ["shell", "ls", device_constants.VIDEOS_DATA],
        env.base_env,
    )
    logging.info("before_videos: %s", contents.generic.output.decode())
    self.before_videos = set(contents.generic.output.decode().split("\n"))
    logging.info("num before_videos: %s", self.before_videos)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    contents = adb_utils.issue_generic_request(
        ["shell", "ls", device_constants.VIDEOS_DATA],
        env.base_env,
    )
    logging.info("before_videos: %s", contents.generic.output.decode())
    after_videos = set(contents.generic.output.decode().split("\n"))
    logging.info("num after_videos: %s", after_videos)
    logging.info(
        "number of after_videos - number of before_videos: %s",
        len(after_videos - self.before_videos),
    )

    return 1.0 if len(after_videos - self.before_videos) == 1 else 0.0

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class CameraTakeVideos(_Camera):
  """Task for checking that one single video has been taken."""

  complexity = 2
  schema = {
      "type": "object",
      "properties": {},
      "required": [],
  }
  template = "Take two videos."

  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    contents = adb_utils.issue_generic_request(
        ["shell", "ls", device_constants.VIDEOS_DATA],
        env.base_env,
    )
    logging.info("before_videos: %s", contents.generic.output.decode())
    self.before_videos = set(contents.generic.output.decode().split("\n"))
    logging.info("num before_videos: %s", self.before_videos)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    contents = adb_utils.issue_generic_request(
        ["shell", "ls", device_constants.VIDEOS_DATA],
        env.base_env,
    )
    logging.info("before_videos: %s", contents.generic.output.decode())
    after_videos = set(contents.generic.output.decode().split("\n"))
    logging.info("num after_videos: %s", after_videos)
    logging.info(
        "number of after_videos - number of before_videos: %s",
        len(after_videos - self.before_videos),
    )

    return 1.0 if len(after_videos - self.before_videos) == 2 else 0.0

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class CameraTakePhoto(_Camera):
  """Task for checking that one single photo has been taken."""

  complexity = 1
  schema = {
      "type": "object",
      "properties": {},
      "required": [],
  }
  template = "Take one photo."

  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    contents = adb_utils.issue_generic_request(
        ["shell", "ls", device_constants.PHOTOS_DATA], env.base_env
    )
    logging.info("before_photos: %s", contents.generic.output.decode())
    self.before_photos = set(contents.generic.output.decode().split("\n"))
    logging.info("num before_photos: %s", self.before_photos)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    contents = adb_utils.issue_generic_request(
        ["shell", "ls", device_constants.PHOTOS_DATA], env.base_env
    )
    logging.info("after_photos: %s", contents.generic.output.decode())
    after_photos = set(contents.generic.output.decode().split("\n"))
    logging.info("num after_photos: %s", after_photos)
    logging.info(
        "number of after_photos - number of before_photos: %s",
        len(after_photos - self.before_photos),
    )

    return 1.0 if len(after_photos - self.before_photos) == 1 else 0.0

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class CameraTakePhotos(_Camera):
  """Task for checking that three photos has been taken."""

  complexity = 1
  schema = {
      "type": "object",
      "properties": {},
      "required": [],
  }
  template = "Take three photos."

  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    contents = adb_utils.issue_generic_request(
        ["shell", "ls", device_constants.PHOTOS_DATA], env.base_env
    )
    logging.info("before_photos: %s", contents.generic.output.decode())
    self.before_photos = set(contents.generic.output.decode().split("\n"))
    logging.info("num before_photos: %s", self.before_photos)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    contents = adb_utils.issue_generic_request(
        ["shell", "ls", device_constants.PHOTOS_DATA], env.base_env
    )
    logging.info("after_photos: %s", contents.generic.output.decode())
    after_photos = set(contents.generic.output.decode().split("\n"))
    logging.info("num after_photos: %s", after_photos)
    logging.info(
        "number of after_photos - number of before_photos: %s",
        len(after_photos - self.before_photos),
    )

    return 1.0 if len(after_photos - self.before_photos) == 3 else 0.0

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class CameraTakePhotoAndVideo(_Camera):
  """Task for checking that one single photo and one single video has been taken."""

  complexity = 2
  schema = {
      "type": "object",
      "properties": {},
      "required": [],
  }
  template = "Take one photo and one video."

  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    contents_photo = adb_utils.issue_generic_request(
        ["shell", "ls", device_constants.PHOTOS_DATA], env.base_env
    )
    logging.info("before_photos: %s", contents_photo.generic.output.decode())
    self.before_photos = set(contents_photo.generic.output.decode().split("\n"))
    logging.info("num before_photos: %s", self.before_photos)
    contents_video = adb_utils.issue_generic_request(
        ["shell", "ls", device_constants.VIDEOS_DATA],
        env.base_env,
    )
    logging.info("before_videos: %s", contents_video.generic.output.decode())
    self.before_videos = set(contents_video.generic.output.decode().split("\n"))
    logging.info("num before_videos: %s", self.before_videos)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    contents_photo = adb_utils.issue_generic_request(
        ["shell", "ls", device_constants.PHOTOS_DATA], env.base_env
    )
    logging.info("after_photos: %s", contents_photo.generic.output.decode())
    after_photos = set(contents_photo.generic.output.decode().split("\n"))
    logging.info("num after_photos: %s", after_photos)
    logging.info(
        "number of after_photos - number of before_photos: %s",
        len(after_photos - self.before_photos),
    )

    contents_video = adb_utils.issue_generic_request(
        ["shell", "ls", device_constants.VIDEOS_DATA],
        env.base_env,
    )
    logging.info("before_videos: %s", contents_video.generic.output.decode())
    after_videos = set(contents_video.generic.output.decode().split("\n"))
    logging.info("num after_videos: %s", after_videos)
    logging.info(
        "number of after_videos - number of before_videos: %s",
        len(after_videos - self.before_videos),
    )
    return 1.0 if len(after_photos - self.before_photos) == 1 and len(after_videos-self.before_videos) == 1 else 0.0

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}

class CameraTakePhotosAndVideos(_Camera):
  """Task for checking that one single photo and one single video has been taken."""

  complexity = 3
  schema = {
      "type": "object",
      "properties": {},
      "required": [],
  }
  template = "Take five photos and two videos."

  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    contents_photo = adb_utils.issue_generic_request(
        ["shell", "ls", device_constants.PHOTOS_DATA], env.base_env
    )
    logging.info("before_photos: %s", contents_photo.generic.output.decode())
    self.before_photos = set(contents_photo.generic.output.decode().split("\n"))
    logging.info("num before_photos: %s", self.before_photos)
    contents_video = adb_utils.issue_generic_request(
        ["shell", "ls", device_constants.VIDEOS_DATA],
        env.base_env,
    )
    logging.info("before_videos: %s", contents_video.generic.output.decode())
    self.before_videos = set(contents_video.generic.output.decode().split("\n"))
    logging.info("num before_videos: %s", self.before_videos)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    contents_photo = adb_utils.issue_generic_request(
        ["shell", "ls", device_constants.PHOTOS_DATA], env.base_env
    )
    logging.info("after_photos: %s", contents_photo.generic.output.decode())
    after_photos = set(contents_photo.generic.output.decode().split("\n"))
    logging.info("num after_photos: %s", after_photos)
    logging.info(
        "number of after_photos - number of before_photos: %s",
        len(after_photos - self.before_photos),
    )

    contents_video = adb_utils.issue_generic_request(
        ["shell", "ls", device_constants.VIDEOS_DATA],
        env.base_env,
    )
    logging.info("before_videos: %s", contents_video.generic.output.decode())
    after_videos = set(contents_video.generic.output.decode().split("\n"))
    logging.info("num after_videos: %s", after_videos)
    logging.info(
        "number of after_videos - number of before_videos: %s",
        len(after_videos - self.before_videos),
    )
    return 1.0 if len(after_photos - self.before_photos) == 5 and len(after_videos-self.before_videos) == 2 else 0.0

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    return {}
class CameraOpen(_Camera):
    """Task for opening Camera."""

    complexity = 1
    schema = {}
    template = (
        "Open Camera App"
    )

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        adb_command = "adb shell dumpsys window windows"
        result = subprocess.run(adb_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # print(result)
        result = result.stdout.split('    ')
        for i in range(len(result)):
            if len(result[i]) > len("mActivityRecord") and result[i][:len("mActivityRecord")] == "mActivityRecord":
                print(result[i])
                part = result[i].split(" ")[2].split('/')
                if part[0] == "com.android.camera2":
                    return 1
                else:
                    return 0



    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        return {}