import os
import random
import subprocess
from typing import Any
import dataclasses
import datetime
from android_world.env import device_constants
from android_world.env import interface
from android_world.task_evals import task_eval
from android_world.task_evals.common_validators import file_validators
from android_world.task_evals.utils import user_data_generation
from android_world.utils import file_utils
from android_world.task_evals.single import camera
from android_world.task_evals.single import markor
from absl import logging


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



class MarkorAndCamera(task_eval.TaskEval):
  app_names = ("markor","camera")
  def _clear_app_data(self, env: interface.AsyncEnv) -> None:
    """Clears the app data."""
    file_utils.clear_directory(device_constants.PHOTOS_DATA, env.base_env)
  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    file_utils.clear_directory(device_constants.MARKOR_DATA, env.base_env)
    self._clear_app_data(env)

  def tear_down(self, env: interface.AsyncEnv) -> None:
    super().tear_down(env)
    file_utils.clear_directory(device_constants.MARKOR_DATA, env.base_env)
    self._clear_app_data(env)
    

class MarkorMoveNoteandCreateFolderAndCameraTakeVideo(MarkorAndCamera):
  """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

  complexity = 3
  schema = {
      "type": "object",
      "properties": {
          "file_name": {"type": "string"},
          "source_folder": {"type": "string"},
          "destination_folder": {"type": "string"},
          "folder_name": {"type": "string"},
      },
      "required": ["file_name", "source_folder", "destination_folder", "folder_name"],
  }
  template = (
      "In Markor, move the note {file_name} from {source_folder} to"
      " {destination_folder}. Also, create a new folder named {folder_name} in Markor."
      " then Take one video."
  )

  def __init__(self, params: dict[str, Any]):
    """Initialize the task."""
    super().__init__(params)
    self.move_file_task = markor.MarkorMoveNoteandCreateFolder(
        params={ "file_name": self.params["file_name"],
                 "source_folder":self.params["source_folder"],
                 "destination_folder" : self.params["destination_folder"],
                 "folder_name" : self.params["folder_name"],
                 "noise_candidates" : self.params["noise_candidates"]

        })
    self.camera_task = camera.CameraTakeVideo(params={})
                               



  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    self.move_file_task.initialize_task(env)
    self.camera_task.initialize_task(env)


  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    markor_success = self.move_file_task.is_successful(env)
    logging.info("Markor success: %s", markor_success)

    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)

    return (markor_success + camera_success) / 2.0

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    markor_params = markor.MarkorMoveNoteandCreateFolder.generate_random_params()
    compound_params ={
        "file_name": markor_params["file_name"],
        "source_folder": markor_params["source_folder"],
        "destination_folder": markor_params["destination_folder"],
        "noise_candidates": _NOTE_TITLES,
        "folder_name": markor_params["folder_name"],
    }
    return compound_params

  def tear_down(self, env: interface.AsyncEnv) -> None:
    super().tear_down(env)
    self.move_file_task.tear_down(env)

class MarkorCreateFolderthenCreateNoteAndCameraTakeVideo(MarkorAndCamera):
  """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

  complexity = 3
  schema = {
      "type": "object",
      "properties": {
          "file_name": {"type": "string"},
          "folder_name": {"type": "string"},
      },
      "required": ["folder_name", "file_name",],
  }
  template = (
      "Create a new folder in Markor named {folder_name} and then create a new note named {file_name} in this folder with the following text:"
      " {text}"
      "then Take one video ."

  )

  def __init__(self, params: dict[str, Any]):
    """Initialize the task."""
    super().__init__(params)
    self.markor_task = markor.MarkorCreateFolderthenCreateNote(
        params={ "file_name": self.params["file_name"],
                 "folder_name" : self.params["folder_name"],
                 "text": self.params["text"],

        })
    self.camera_task = camera.CameraTakeVideo(params={})



  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    self.markor_task.initialize_task(env)
    self.camera_task.initialize_task(env)


  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    markor_success = self.markor_task.is_successful(env)
    logging.info("Markor success: %s", markor_success)

    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)

    return (markor_success + camera_success) / 2.0

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    markor_params = markor.MarkorCreateFolderthenCreateNote.generate_random_params()
    compound_params ={
        "file_name": markor_params["file_name"],
        "folder_name": markor_params["folder_name"],
        "text": markor_params["text"],
    }
    return compound_params

  def tear_down(self, env: interface.AsyncEnv) -> None:
    super().tear_down(env)
    self.markor_task.tear_down(env)

class MarkorMoveNoteAndCameraTakeVideo(MarkorAndCamera):
  """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

  complexity = 3
  schema = {
      "type": "object",
      "properties": {
          "file_name": {"type": "string"},
          "source_folder": {"type": "string"},
          "destination_folder": {"type": "string"},
      },
      "required": ["file_name", "source_folder", "destination_folder" ],
  }
  template = (
      "In Markor, move the note {file_name} from {source_folder} to"
      " {destination_folder}."
      "then Take one video."
  )

  def __init__(self, params: dict[str, Any]):
    """Initialize the task."""
    super().__init__(params)
    self.move_file_task = markor.MarkorMoveNote(
        params={ "file_name": self.params["file_name"],
                 "source_folder":self.params["source_folder"],
                 "destination_folder" : self.params["destination_folder"],
                 "noise_candidates" : self.params["noise_candidates"]

        })
    self.camera_task = camera.CameraTakeVideo(params={})



  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    self.move_file_task.initialize_task(env)
    self.camera_task.initialize_task(env)


  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    markor_success = self.move_file_task.is_successful(env)
    logging.info("Markor success: %s", markor_success)

    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)

    return (markor_success + camera_success) / 2.0

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    markor_params = markor.MarkorMoveNote.generate_random_params()
    compound_params ={
        "file_name": markor_params["file_name"],
        "source_folder": markor_params["source_folder"],
        "destination_folder": markor_params["destination_folder"],
        "noise_candidates": _NOTE_TITLES,
    }
    return compound_params

  def tear_down(self, env: interface.AsyncEnv) -> None:
    super().tear_down(env)
    self.move_file_task.tear_down(env)


class MarkorCreateFolderAndCameraTakeVideo(MarkorAndCamera):
  """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

  complexity = 3
  schema = {
      "type": "object",
      "properties": {
          "folder_name": {"type": "string"},
      },
      "required": ["folder_name"],
  }
  template = (
      "Create a new folder in Markor named {folder_name}."
      "then Create a new cameraing in Simple camera Pro. Name it {file_name_camera}. Save it in"
      " the Pictures folder within the sdk_gphone_x86_64 storage area."
      "then Take one video."
  )

  def __init__(self, params: dict[str, Any]):
    """Initialize the task."""
    super().__init__(params)
    self.markor_task = markor.MarkorCreateFolder(
        params={
                 "folder_name" : self.params["folder_name"],
        })
    self.camera_task = camera.CameraTakeVideo(params={})



  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    self.markor_task.initialize_task(env)
    self.camera_task.initialize_task(env)


  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    markor_success = self.markor_task.is_successful(env)
    logging.info("Markor success: %s", markor_success)

    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)

    return (markor_success + camera_success) / 2.0

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    markor_params = markor.MarkorCreateFolder.generate_random_params()
    compound_params ={
        "folder_name": markor_params["folder_name"],
    }
    return compound_params

  def tear_down(self, env: interface.AsyncEnv) -> None:
    super().tear_down(env)
    self.markor_task.tear_down(env)

class MarkorCreateNoteAndCameraTakeVideo(MarkorAndCamera):
  """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

  complexity = 3
  schema = {
      "type": "object",
      "properties": {
          "file_name": {"type": "string"},
          "text": {"type": "string"},
      },
      "required": ["file_name","text"],
  }
  template = (
      "Create a new note in Markor named {file_name} with the following text:"
      " {text}"
      "then Take one video."
  )

  def __init__(self, params: dict[str, Any]):
    """Initialize the task."""
    super().__init__(params)
    self.markor_task = markor.MarkorCreateNote(
        params={
                 "file_name" : self.params["file_name"],
                 "text": self.params["text"]
        })
    self.camera_task = camera.CameraTakeVideo(params={})



  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    self.markor_task.initialize_task(env)
    self.camera_task.initialize_task(env)


  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    markor_success = self.markor_task.is_successful(env)
    logging.info("Markor success: %s", markor_success)

    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)

    return (markor_success + camera_success) / 2.0

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    markor_params = markor.MarkorCreateNote.generate_random_params()
    compound_params ={
        "file_name": markor_params["file_name"],
        "text":  markor_params["text"],
    }
    return compound_params

  def tear_down(self, env: interface.AsyncEnv) -> None:
    super().tear_down(env)
    self.markor_task.tear_down(env)


class MarkorCreateNoteFromClipboardAndCameraTakeVideo(MarkorAndCamera):
  """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

  complexity = 3
  schema = {
      "type": "object",
      "properties": {
          "file_name": {"type": "string"},
          "file_content": {"type": "string"},
      },
      "required": ["file_name","file_content"],
  }
  template = (
      "Create a note in Markor named {file_name}. Perform a paste operation in"
      " the note and save the note."
      "then Take one video."
  )

  def __init__(self, params: dict[str, Any]):
    """Initialize the task."""
    super().__init__(params)
    self.markor_task = markor.MarkorCreateNoteFromClipboard(
        params={
                 "file_name" : self.params["file_name"],
                 "file_content": self.params["file_content"]
        })
    self.camera_task =camera.CameraTakeVideo(params={})



  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    self.markor_task.initialize_task(env)
    self.camera_task.initialize_task(env)


  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    markor_success = self.markor_task.is_successful(env)
    logging.info("Markor success: %s", markor_success)

    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)

    return (markor_success + camera_success) / 2.0

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    markor_params = markor.MarkorCreateNoteFromClipboard.generate_random_params()
    compound_params ={
        "file_name": markor_params["file_name"],
        "file_content": markor_params["file_content"],
    }
    return compound_params

  def tear_down(self, env: interface.AsyncEnv) -> None:
    super().tear_down(env)
    self.markor_task.tear_down(env)


class MarkorMergeNotesAndCameraTakeVideo(MarkorAndCamera):
  """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

  complexity = 3
  schema = {
      "type": "object",
      "properties": {
          "file1_name": {"type": "string"},
          "file2_name": {"type": "string"},
          "file3_name": {"type": "string"},
          "new_file_name": {"type": "string"},
          "file1_content": {"type": "string"},
          "file2_content": {"type": "string"},
          "file3_content": {"type": "string"},

      },
      "required": [   "file1_name",
          "file2_name",
          "file3_name",
          "new_file_name",
          "file1_content",
          "file2_content",
          "file3_content",],
  }
  template = (
      "Merge the contents of Markor notes {file1_name}, {file2_name} and"
      " {file3_name} (in the same order) into a new Markor note named"
      " {new_file_name} and save it. Add a new line between the content of each"
      " note."
      "then Take one video."
  )

  def __init__(self, params: dict[str, Any]):
    """Initialize the task."""
    super().__init__(params)
    self.markor_task = markor.MarkorMergeNotes(
        params={
                 "new_file_name" : self.params["new_file_name"],
                 "file1_name" : self.params["file1_name"],
                 "file2_name": self.params["file2_name"],
                 "file3_name": self.params["file3_name"],
                 "file1_content": self.params["file1_content"],
                 "file2_content": self.params["file2_content"],
                 "file3_content": self.params["file3_content"],

        })
    self.camera_task =camera.CameraTakeVideo(params={})



  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    self.markor_task.initialize_task(env)
    self.camera_task.initialize_task(env)


  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    markor_success = self.markor_task.is_successful(env)
    logging.info("Markor success: %s", markor_success)

    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)

    return (markor_success + camera_success) / 2.0

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    markor_params = markor.MarkorMergeNotes.generate_random_params()
    compound_params ={
        "new_file_name": markor_params["new_file_name"],
        "file1_name": markor_params["file1_name"],
        "file2_name": markor_params["file2_name"],
        "file3_name": markor_params["file3_name"],
        "file1_content": markor_params["file1_content"],
        "file2_content": markor_params["file2_content"],
        "file3_content": markor_params["file3_content"],
    }
    return compound_params

  def tear_down(self, env: interface.AsyncEnv) -> None:
    super().tear_down(env)
    self.markor_task.tear_down(env)



class MarkorChangeNoteContentAndCameraTakeVideo(MarkorAndCamera):
  """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

  complexity = 3
  schema = {
      "type": "object",
      "properties": {
          "original_name": {"type": "string"},
          "new_name": {"type": "string"},
          "updated_content": {"type": "string"},

      },
      "required": ["original_name", "new_name", "updated_content"],
  }
  template = (
      'Update the content of {original_name} to "{updated_content}" in Markor'
      " and change its name to {new_name}."
      "then Take one video."
  )

  def __init__(self, params: dict[str, Any]):
    """Initialize the task."""
    super().__init__(params)
    self.markor_task = markor.MarkorChangeNoteContent(
        params={
                 "original_name" : self.params["original_name"],
                 "new_name" : self.params["new_name"],
                 "updated_content": self.params["updated_content"],

        })
    self.camera_task =camera.CameraTakeVideo(params={})



  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    self.markor_task.initialize_task(env)
    self.camera_task.initialize_task(env)


  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    markor_success = self.markor_task.is_successful(env)
    logging.info("Markor success: %s", markor_success)

    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)

    return (markor_success + camera_success) / 2.0

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    markor_params = markor.MarkorChangeNoteContent.generate_random_params()
    compound_params ={
        "original_name": markor_params["original_name"],
        "new_name": markor_params["new_name"],
        "updated_content": markor_params["updated_content"],

    }
    return compound_params

  def tear_down(self, env: interface.AsyncEnv) -> None:
    super().tear_down(env)
    self.markor_task.tear_down(env)


class MarkorAddNoteHeaderAndCameraTakeVideo(MarkorAndCamera):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "original_name": {"type": "string"},
            "new_name": {"type": "string"},
            "header": {"type": "string"},
            "original_content": {"type": "string"},


        },
        "required": ["original_name", "new_name", "header", "original_content"],
    }
    template = (
        "Update the Markor note {original_name} by adding the following text,"
        ' along with a new blank line before the existing content: "{header}",'
        " and rename it to {new_name}."
        "then Take one video."
    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.markor_task = markor.MarkorAddNoteHeader(
            params={
                "original_name": self.params["original_name"],
                "new_name": self.params["new_name"],
                "header": self.params["header"],
                "original_content": self.params["original_content"],

            })
        self.camera_task = camera.CameraTakeVideo(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (markor_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorAddNoteHeader.generate_random_params()
        compound_params = {
            "original_name": markor_params["original_name"],
            "new_name": markor_params["new_name"],
            "header": markor_params["header"],
            "original_content": markor_params["original_content"],

        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorEditNoteAndCameraTakeVideo(MarkorAndCamera):
  """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

  complexity = 3
  schema = {
      "type": "object",
      "properties": {
          "file_name": {"type": "string"},
          "header": {"type": "string"},
          "footer": {"type": "string"},
          "replace_text": {"type": "string"},
          "edit_type": {
              "type": "string",
              "enum": ["header", "footer", "replace"],
          },


      },
      "required": ["file_name", "edit_type"],
  }
  @property
  def template(self) -> str:
    templates = {
        "header": (
            "Edit {file_name} in Markor. Add to the top of the note {header}"
            "then Take one video."
        ),
        "footer": (
            "Edit {file_name} in Markor. Add to the bottom of the note {footer}"
            "then Take one video."
        ),
        "replace": (
            "Edit {file_name} in Markor. Replace the text with {replace_text}"
            "then Take one video."
        ),
    }

    if "edit_type" not in self.params and "edit_type" not in templates:
      return templates.get(
          self.params.get("edit_type"),
          "Invalid edit_type for {file_name} in Markor.",
      )
    return templates[self.params.get("edit_type")]


  def __init__(self, params: dict[str, Any]):
    """Initialize the task."""
    super().__init__(params)
    markor_params = {
        "file_name": self.params["file_name"],
        "edit_type": self.params["edit_type"],
    }
    if self.params["edit_type"] == "header":
        markor_params["header"]=self.params["header"]
    elif self.params["edit_type"] == "footer":
        markor_params["footer"]=self.params["footer"]
    elif self.params["edit_type"] == "replace":
        markor_params["replace_text"] = self.params["replace_text"]
    self.markor_task = markor.MarkorEditNote(markor_params)
    self.camera_task =camera.CameraTakeVideo(params={})



  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    self.markor_task.initialize_task(env)
    self.camera_task.initialize_task(env)


  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    markor_success = self.markor_task.is_successful(env)
    logging.info("Markor success: %s", markor_success)

    camera_success = self.camera_task.is_successful(env)
    logging.info("camera success: %s", camera_success)

    return (markor_success + camera_success) / 2.0

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    markor_params = markor.MarkorEditNote.generate_random_params()
    compound_params ={
        "file_name": markor_params["file_name"],
        "edit_type": markor_params["edit_type"],

    }
    if markor_params["edit_type"] == "header":
        compound_params["header"]=markor_params["header"]
    elif markor_params["edit_type"] == "footer":
        compound_params["footer"]=markor_params["footer"]
    elif markor_params["edit_type"] == "replace":
        compound_params["replace_text"] = markor_params["replace_text"]

    return compound_params

  def tear_down(self, env: interface.AsyncEnv) -> None:
    super().tear_down(env)
    self.markor_task.tear_down(env)


class MarkorMoveNoteandCreateFolderAndCameraTakeVideos(MarkorAndCamera):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "file_name": {"type": "string"},
            "source_folder": {"type": "string"},
            "destination_folder": {"type": "string"},
            "folder_name": {"type": "string"},
        },
        "required": ["file_name", "source_folder", "destination_folder", "folder_name"],
    }
    template = (
        "In Markor, move the note {file_name} from {source_folder} to"
        " {destination_folder}. Also, create a new folder named {folder_name} in Markor."
        " then Take two videos"
    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.move_file_task = markor.MarkorMoveNoteandCreateFolder(
            params={"file_name": self.params["file_name"],
                    "source_folder": self.params["source_folder"],
                    "destination_folder": self.params["destination_folder"],
                    "folder_name": self.params["folder_name"],
                    "noise_candidates": self.params["noise_candidates"]

                    })
        self.camera_task = camera.CameraTakeVideos(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.move_file_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.move_file_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (markor_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorMoveNoteandCreateFolder.generate_random_params()
        compound_params = {
            "file_name": markor_params["file_name"],
            "source_folder": markor_params["source_folder"],
            "destination_folder": markor_params["destination_folder"],
            "noise_candidates": _NOTE_TITLES,
            "folder_name": markor_params["folder_name"],
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.move_file_task.tear_down(env)


class MarkorCreateFolderthenCreateNoteAndCameraTakeVideos(MarkorAndCamera):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "file_name": {"type": "string"},
            "folder_name": {"type": "string"},
        },
        "required": ["folder_name", "file_name", ],
    }
    template = (
        "Create a new folder in Markor named {folder_name} and then create a new note named {file_name} in this folder with the following text:"
        " {text}"
        " then Take two videos"

    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.markor_task = markor.MarkorCreateFolderthenCreateNote(
            params={"file_name": self.params["file_name"],
                    "folder_name": self.params["folder_name"],
                    "text": self.params["text"],

                    })
        self.camera_task = camera.CameraTakeVideos(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (markor_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorCreateFolderthenCreateNote.generate_random_params()
        compound_params = {
            "file_name": markor_params["file_name"],
            "folder_name": markor_params["folder_name"],
            "text": markor_params["text"],
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorMoveNoteAndCameraTakeVideos(MarkorAndCamera):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "file_name": {"type": "string"},
            "source_folder": {"type": "string"},
            "destination_folder": {"type": "string"},
        },
        "required": ["file_name", "source_folder", "destination_folder"],
    }
    template = (
        "In Markor, move the note {file_name} from {source_folder} to"
        " {destination_folder}."
        "then Take two videos"
    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.move_file_task = markor.MarkorMoveNote(
            params={"file_name": self.params["file_name"],
                    "source_folder": self.params["source_folder"],
                    "destination_folder": self.params["destination_folder"],
                    "noise_candidates": self.params["noise_candidates"]

                    })
        self.camera_task = camera.CameraTakeVideos(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.move_file_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.move_file_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (markor_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorMoveNote.generate_random_params()
        compound_params = {
            "file_name": markor_params["file_name"],
            "source_folder": markor_params["source_folder"],
            "destination_folder": markor_params["destination_folder"],
            "noise_candidates": _NOTE_TITLES,
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.move_file_task.tear_down(env)


class MarkorCreateFolderAndCameraTakeVideos(MarkorAndCamera):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "folder_name": {"type": "string"},
        },
        "required": ["folder_name"],
    }
    template = (
        "Create a new folder in Markor named {folder_name}."
        "then Create a new cameraing in Simple camera Pro. Name it {file_name_camera}. Save it in"
        " the Pictures folder within the sdk_gphone_x86_64 storage area."
        "then Take two videos"
    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.markor_task = markor.MarkorCreateFolder(
            params={
                "folder_name": self.params["folder_name"],
            })
        self.camera_task = camera.CameraTakeVideos(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (markor_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorCreateFolder.generate_random_params()
        compound_params = {
            "folder_name": markor_params["folder_name"],
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorCreateNoteAndCameraTakeVideos(MarkorAndCamera):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "file_name": {"type": "string"},
            "text": {"type": "string"},
        },
        "required": ["file_name", "text"],
    }
    template = (
        "Create a new note in Markor named {file_name} with the following text:"
        " {text}"
        "then Take two videos"
    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.markor_task = markor.MarkorCreateNote(
            params={
                "file_name": self.params["file_name"],
                "text": self.params["text"]
            })
        self.camera_task = camera.CameraTakeVideos(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (markor_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorCreateNote.generate_random_params()
        compound_params = {
            "file_name": markor_params["file_name"],
            "text": markor_params["text"],
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorCreateNoteFromClipboardAndCameraTakeVideos(MarkorAndCamera):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "file_name": {"type": "string"},
            "file_content": {"type": "string"},
        },
        "required": ["file_name", "file_content"],
    }
    template = (
        "Create a note in Markor named {file_name}. Perform a paste operation in"
        " the note and save the note."
        "then Take two videos"
    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.markor_task = markor.MarkorCreateNoteFromClipboard(
            params={
                "file_name": self.params["file_name"],
                "file_content": self.params["file_content"]
            })
        self.camera_task = camera.CameraTakeVideos(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (markor_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorCreateNoteFromClipboard.generate_random_params()
        compound_params = {
            "file_name": markor_params["file_name"],
            "file_content": markor_params["file_content"],
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorMergeNotesAndCameraTakeVideos(MarkorAndCamera):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "file1_name": {"type": "string"},
            "file2_name": {"type": "string"},
            "file3_name": {"type": "string"},
            "new_file_name": {"type": "string"},
            "file1_content": {"type": "string"},
            "file2_content": {"type": "string"},
            "file3_content": {"type": "string"},

        },
        "required": ["file1_name",
                     "file2_name",
                     "file3_name",
                     "new_file_name",
                     "file1_content",
                     "file2_content",
                     "file3_content", ],
    }
    template = (
        "Merge the contents of Markor notes {file1_name}, {file2_name} and"
        " {file3_name} (in the same order) into a new Markor note named"
        " {new_file_name} and save it. Add a new line between the content of each"
        " note."
        "then Take two videos"
    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.markor_task = markor.MarkorMergeNotes(
            params={
                "new_file_name": self.params["new_file_name"],
                "file1_name": self.params["file1_name"],
                "file2_name": self.params["file2_name"],
                "file3_name": self.params["file3_name"],
                "file1_content": self.params["file1_content"],
                "file2_content": self.params["file2_content"],
                "file3_content": self.params["file3_content"],

            })
        self.camera_task = camera.CameraTakeVideos(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (markor_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorMergeNotes.generate_random_params()
        compound_params = {
            "new_file_name": markor_params["new_file_name"],
            "file1_name": markor_params["file1_name"],
            "file2_name": markor_params["file2_name"],
            "file3_name": markor_params["file3_name"],
            "file1_content": markor_params["file1_content"],
            "file2_content": markor_params["file2_content"],
            "file3_content": markor_params["file3_content"],
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorChangeNoteContentAndCameraTakeVideos(MarkorAndCamera):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "original_name": {"type": "string"},
            "new_name": {"type": "string"},
            "updated_content": {"type": "string"},

        },
        "required": ["original_name", "new_name", "updated_content"],
    }
    template = (
        'Update the content of {original_name} to "{updated_content}" in Markor'
        " and change its name to {new_name}."
        "then Take two videos"
    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.markor_task = markor.MarkorChangeNoteContent(
            params={
                "original_name": self.params["original_name"],
                "new_name": self.params["new_name"],
                "updated_content": self.params["updated_content"],

            })
        self.camera_task = camera.CameraTakeVideos(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (markor_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorChangeNoteContent.generate_random_params()
        compound_params = {
            "original_name": markor_params["original_name"],
            "new_name": markor_params["new_name"],
            "updated_content": markor_params["updated_content"],

        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorAddNoteHeaderAndCameraTakeVideos(MarkorAndCamera):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "original_name": {"type": "string"},
            "new_name": {"type": "string"},
            "header": {"type": "string"},
            "original_content": {"type": "string"},

        },
        "required": ["original_name", "new_name", "header", "original_content"],
    }
    template = (
        "Update the Markor note {original_name} by adding the following text,"
        ' along with a new blank line before the existing content: "{header}",'
        " and rename it to {new_name}."
        "then Take two videos"
    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.markor_task = markor.MarkorAddNoteHeader(
            params={
                "original_name": self.params["original_name"],
                "new_name": self.params["new_name"],
                "header": self.params["header"],
                "original_content": self.params["original_content"],

            })
        self.camera_task = camera.CameraTakeVideos(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (markor_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorAddNoteHeader.generate_random_params()
        compound_params = {
            "original_name": markor_params["original_name"],
            "new_name": markor_params["new_name"],
            "header": markor_params["header"],
            "original_content": markor_params["original_content"],

        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorEditNoteAndCameraTakeVideos(MarkorAndCamera):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "file_name": {"type": "string"},
            "header": {"type": "string"},
            "footer": {"type": "string"},
            "replace_text": {"type": "string"},
            "edit_type": {
                "type": "string",
                "enum": ["header", "footer", "replace"],
            },

        },
        "required": ["file_name", "edit_type"],
    }

    @property
    def template(self) -> str:
        templates = {
            "header": (
                "Edit {file_name} in Markor. Add to the top of the note {header}"
                "then Take two videos"
            ),
            "footer": (
                "Edit {file_name} in Markor. Add to the bottom of the note {footer}"
                "then Take two videos"
            ),
            "replace": (
                "Edit {file_name} in Markor. Replace the text with {replace_text}"
                "then Take two videos"
            ),
        }

        if "edit_type" not in self.params and "edit_type" not in templates:
            return templates.get(
                self.params.get("edit_type"),
                "Invalid edit_type for {file_name} in Markor.",
            )
        return templates[self.params.get("edit_type")]

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        markor_params = {
            "file_name": self.params["file_name"],
            "edit_type": self.params["edit_type"],
        }
        if self.params["edit_type"] == "header":
            markor_params["header"] = self.params["header"]
        elif self.params["edit_type"] == "footer":
            markor_params["footer"] = self.params["footer"]
        elif self.params["edit_type"] == "replace":
            markor_params["replace_text"] = self.params["replace_text"]
        self.markor_task = markor.MarkorEditNote(markor_params)
        self.camera_task = camera.CameraTakeVideos(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (markor_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorEditNote.generate_random_params()
        compound_params = {
            "file_name": markor_params["file_name"],
            "edit_type": markor_params["edit_type"],

        }
        if markor_params["edit_type"] == "header":
            compound_params["header"] = markor_params["header"]
        elif markor_params["edit_type"] == "footer":
            compound_params["footer"] = markor_params["footer"]
        elif markor_params["edit_type"] == "replace":
            compound_params["replace_text"] = markor_params["replace_text"]

        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorMoveNoteandCreateFolderAndCameraTakePhoto(MarkorAndCamera):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "file_name": {"type": "string"},
            "source_folder": {"type": "string"},
            "destination_folder": {"type": "string"},
            "folder_name": {"type": "string"},
        },
        "required": ["file_name", "source_folder", "destination_folder", "folder_name"],
    }
    template = (
        "In Markor, move the note {file_name} from {source_folder} to"
        " {destination_folder}. Also, create a new folder named {folder_name} in Markor."
        " then Take one Photo"
    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.move_file_task = markor.MarkorMoveNoteandCreateFolder(
            params={"file_name": self.params["file_name"],
                    "source_folder": self.params["source_folder"],
                    "destination_folder": self.params["destination_folder"],
                    "folder_name": self.params["folder_name"],
                    "noise_candidates": self.params["noise_candidates"]

                    })
        self.camera_task = camera.CameraTakePhoto(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.move_file_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.move_file_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (markor_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorMoveNoteandCreateFolder.generate_random_params()
        compound_params = {
            "file_name": markor_params["file_name"],
            "source_folder": markor_params["source_folder"],
            "destination_folder": markor_params["destination_folder"],
            "noise_candidates": _NOTE_TITLES,
            "folder_name": markor_params["folder_name"],
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.move_file_task.tear_down(env)


class MarkorCreateFolderthenCreateNoteAndCameraTakePhoto(MarkorAndCamera):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "file_name": {"type": "string"},
            "folder_name": {"type": "string"},
        },
        "required": ["folder_name", "file_name", ],
    }
    template = (
        "Create a new folder in Markor named {folder_name} and then create a new note named {file_name} in this folder with the following text:"
        " {text}"
        " then Take one Photo"

    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.markor_task = markor.MarkorCreateFolderthenCreateNote(
            params={"file_name": self.params["file_name"],
                    "folder_name": self.params["folder_name"],
                    "text": self.params["text"],

                    })
        self.camera_task = camera.CameraTakePhoto(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (markor_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorCreateFolderthenCreateNote.generate_random_params()
        compound_params = {
            "file_name": markor_params["file_name"],
            "folder_name": markor_params["folder_name"],
            "text": markor_params["text"],
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorMoveNoteAndCameraTakePhoto(MarkorAndCamera):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "file_name": {"type": "string"},
            "source_folder": {"type": "string"},
            "destination_folder": {"type": "string"},
        },
        "required": ["file_name", "source_folder", "destination_folder"],
    }
    template = (
        "In Markor, move the note {file_name} from {source_folder} to"
        " {destination_folder}."
        "then Take one Photo"
    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.move_file_task = markor.MarkorMoveNote(
            params={"file_name": self.params["file_name"],
                    "source_folder": self.params["source_folder"],
                    "destination_folder": self.params["destination_folder"],
                    "noise_candidates": self.params["noise_candidates"]

                    })
        self.camera_task = camera.CameraTakePhoto(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.move_file_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.move_file_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (markor_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorMoveNote.generate_random_params()
        compound_params = {
            "file_name": markor_params["file_name"],
            "source_folder": markor_params["source_folder"],
            "destination_folder": markor_params["destination_folder"],
            "noise_candidates": _NOTE_TITLES,
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.move_file_task.tear_down(env)


class MarkorCreateFolderAndCameraTakePhoto(MarkorAndCamera):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "folder_name": {"type": "string"},
        },
        "required": ["folder_name"],
    }
    template = (
        "Create a new folder in Markor named {folder_name}."
        "then Create a new cameraing in Simple camera Pro. Name it {file_name_camera}. Save it in"
        " the Pictures folder within the sdk_gphone_x86_64 storage area."
        "then Take one Photo"
    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.markor_task = markor.MarkorCreateFolder(
            params={
                "folder_name": self.params["folder_name"],
            })
        self.camera_task = camera.CameraTakePhoto(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (markor_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorCreateFolder.generate_random_params()
        compound_params = {
            "folder_name": markor_params["folder_name"],
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorCreateNoteAndCameraTakePhoto(MarkorAndCamera):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "file_name": {"type": "string"},
            "text": {"type": "string"},
        },
        "required": ["file_name", "text"],
    }
    template = (
        "Create a new note in Markor named {file_name} with the following text:"
        " {text}"
        "then Take one Photo"
    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.markor_task = markor.MarkorCreateNote(
            params={
                "file_name": self.params["file_name"],
                "text": self.params["text"]
            })
        self.camera_task = camera.CameraTakePhoto(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (markor_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorCreateNote.generate_random_params()
        compound_params = {
            "file_name": markor_params["file_name"],
            "text": markor_params["text"],
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorCreateNoteFromClipboardAndCameraTakePhoto(MarkorAndCamera):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "file_name": {"type": "string"},
            "file_content": {"type": "string"},
        },
        "required": ["file_name", "file_content"],
    }
    template = (
        "Create a note in Markor named {file_name}. Perform a paste operation in"
        " the note and save the note."
        "then Take one Photo"
    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.markor_task = markor.MarkorCreateNoteFromClipboard(
            params={
                "file_name": self.params["file_name"],
                "file_content": self.params["file_content"]
            })
        self.camera_task = camera.CameraTakePhoto(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (markor_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorCreateNoteFromClipboard.generate_random_params()
        compound_params = {
            "file_name": markor_params["file_name"],
            "file_content": markor_params["file_content"],
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorMergeNotesAndCameraTakePhoto(MarkorAndCamera):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "file1_name": {"type": "string"},
            "file2_name": {"type": "string"},
            "file3_name": {"type": "string"},
            "new_file_name": {"type": "string"},
            "file1_content": {"type": "string"},
            "file2_content": {"type": "string"},
            "file3_content": {"type": "string"},

        },
        "required": ["file1_name",
                     "file2_name",
                     "file3_name",
                     "new_file_name",
                     "file1_content",
                     "file2_content",
                     "file3_content", ],
    }
    template = (
        "Merge the contents of Markor notes {file1_name}, {file2_name} and"
        " {file3_name} (in the same order) into a new Markor note named"
        " {new_file_name} and save it. Add a new line between the content of each"
        " note."
        "then Take one Photo"
    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.markor_task = markor.MarkorMergeNotes(
            params={
                "new_file_name": self.params["new_file_name"],
                "file1_name": self.params["file1_name"],
                "file2_name": self.params["file2_name"],
                "file3_name": self.params["file3_name"],
                "file1_content": self.params["file1_content"],
                "file2_content": self.params["file2_content"],
                "file3_content": self.params["file3_content"],

            })
        self.camera_task = camera.CameraTakePhoto(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (markor_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorMergeNotes.generate_random_params()
        compound_params = {
            "new_file_name": markor_params["new_file_name"],
            "file1_name": markor_params["file1_name"],
            "file2_name": markor_params["file2_name"],
            "file3_name": markor_params["file3_name"],
            "file1_content": markor_params["file1_content"],
            "file2_content": markor_params["file2_content"],
            "file3_content": markor_params["file3_content"],
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorChangeNoteContentAndCameraTakePhoto(MarkorAndCamera):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "original_name": {"type": "string"},
            "new_name": {"type": "string"},
            "updated_content": {"type": "string"},

        },
        "required": ["original_name", "new_name", "updated_content"],
    }
    template = (
        'Update the content of {original_name} to "{updated_content}" in Markor'
        " and change its name to {new_name}."
        "then Take one Photo"
    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.markor_task = markor.MarkorChangeNoteContent(
            params={
                "original_name": self.params["original_name"],
                "new_name": self.params["new_name"],
                "updated_content": self.params["updated_content"],

            })
        self.camera_task = camera.CameraTakePhoto(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (markor_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorChangeNoteContent.generate_random_params()
        compound_params = {
            "original_name": markor_params["original_name"],
            "new_name": markor_params["new_name"],
            "updated_content": markor_params["updated_content"],

        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorAddNoteHeaderAndCameraTakePhoto(MarkorAndCamera):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "original_name": {"type": "string"},
            "new_name": {"type": "string"},
            "header": {"type": "string"},
            "original_content": {"type": "string"},

        },
        "required": ["original_name", "new_name", "header", "original_content"],
    }
    template = (
        "Update the Markor note {original_name} by adding the following text,"
        ' along with a new blank line before the existing content: "{header}",'
        " and rename it to {new_name}."
        "then Take one Photo"
    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.markor_task = markor.MarkorAddNoteHeader(
            params={
                "original_name": self.params["original_name"],
                "new_name": self.params["new_name"],
                "header": self.params["header"],
                "original_content": self.params["original_content"],

            })
        self.camera_task = camera.CameraTakePhoto(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (markor_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorAddNoteHeader.generate_random_params()
        compound_params = {
            "original_name": markor_params["original_name"],
            "new_name": markor_params["new_name"],
            "header": markor_params["header"],
            "original_content": markor_params["original_content"],

        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorEditNoteAndCameraTakePhoto(MarkorAndCamera):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "file_name": {"type": "string"},
            "header": {"type": "string"},
            "footer": {"type": "string"},
            "replace_text": {"type": "string"},
            "edit_type": {
                "type": "string",
                "enum": ["header", "footer", "replace"],
            },

        },
        "required": ["file_name", "edit_type"],
    }

    @property
    def template(self) -> str:
        templates = {
            "header": (
                "Edit {file_name} in Markor. Add to the top of the note {header}"
                "then Take one Photo"
            ),
            "footer": (
                "Edit {file_name} in Markor. Add to the bottom of the note {footer}"
                "then Take one Photo"
            ),
            "replace": (
                "Edit {file_name} in Markor. Replace the text with {replace_text}"
                "then Take one Photo"
            ),
        }

        if "edit_type" not in self.params and "edit_type" not in templates:
            return templates.get(
                self.params.get("edit_type"),
                "Invalid edit_type for {file_name} in Markor.",
            )
        return templates[self.params.get("edit_type")]

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        markor_params = {
            "file_name": self.params["file_name"],
            "edit_type": self.params["edit_type"],
        }
        if self.params["edit_type"] == "header":
            markor_params["header"] = self.params["header"]
        elif self.params["edit_type"] == "footer":
            markor_params["footer"] = self.params["footer"]
        elif self.params["edit_type"] == "replace":
            markor_params["replace_text"] = self.params["replace_text"]
        self.markor_task = markor.MarkorEditNote(markor_params)
        self.camera_task = camera.CameraTakePhoto(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (markor_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorEditNote.generate_random_params()
        compound_params = {
            "file_name": markor_params["file_name"],
            "edit_type": markor_params["edit_type"],

        }
        if markor_params["edit_type"] == "header":
            compound_params["header"] = markor_params["header"]
        elif markor_params["edit_type"] == "footer":
            compound_params["footer"] = markor_params["footer"]
        elif markor_params["edit_type"] == "replace":
            compound_params["replace_text"] = markor_params["replace_text"]

        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)



class MarkorMoveNoteandCreateFolderAndCameraTakePhotos(MarkorAndCamera):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "file_name": {"type": "string"},
            "source_folder": {"type": "string"},
            "destination_folder": {"type": "string"},
            "folder_name": {"type": "string"},
        },
        "required": ["file_name", "source_folder", "destination_folder", "folder_name"],
    }
    template = (
        "In Markor, move the note {file_name} from {source_folder} to"
        " {destination_folder}. Also, create a new folder named {folder_name} in Markor."
        " then Take three Photos"
    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.move_file_task = markor.MarkorMoveNoteandCreateFolder(
            params={"file_name": self.params["file_name"],
                    "source_folder": self.params["source_folder"],
                    "destination_folder": self.params["destination_folder"],
                    "folder_name": self.params["folder_name"],
                    "noise_candidates": self.params["noise_candidates"]

                    })
        self.camera_task = camera.CameraTakePhotos(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.move_file_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.move_file_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (markor_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorMoveNoteandCreateFolder.generate_random_params()
        compound_params = {
            "file_name": markor_params["file_name"],
            "source_folder": markor_params["source_folder"],
            "destination_folder": markor_params["destination_folder"],
            "noise_candidates": _NOTE_TITLES,
            "folder_name": markor_params["folder_name"],
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.move_file_task.tear_down(env)


class MarkorCreateFolderthenCreateNoteAndCameraTakePhotos(MarkorAndCamera):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "file_name": {"type": "string"},
            "folder_name": {"type": "string"},
        },
        "required": ["folder_name", "file_name", ],
    }
    template = (
        "Create a new folder in Markor named {folder_name} and then create a new note named {file_name} in this folder with the following text:"
        " {text}"
        " then Take three Photos"

    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.markor_task = markor.MarkorCreateFolderthenCreateNote(
            params={"file_name": self.params["file_name"],
                    "folder_name": self.params["folder_name"],
                    "text": self.params["text"],

                    })
        self.camera_task = camera.CameraTakePhotos(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (markor_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorCreateFolderthenCreateNote.generate_random_params()
        compound_params = {
            "file_name": markor_params["file_name"],
            "folder_name": markor_params["folder_name"],
            "text": markor_params["text"],
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorMoveNoteAndCameraTakePhotos(MarkorAndCamera):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "file_name": {"type": "string"},
            "source_folder": {"type": "string"},
            "destination_folder": {"type": "string"},
        },
        "required": ["file_name", "source_folder", "destination_folder"],
    }
    template = (
        "In Markor, move the note {file_name} from {source_folder} to"
        " {destination_folder}."
        "then Take three Photos"
    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.move_file_task = markor.MarkorMoveNote(
            params={"file_name": self.params["file_name"],
                    "source_folder": self.params["source_folder"],
                    "destination_folder": self.params["destination_folder"],
                    "noise_candidates": self.params["noise_candidates"]

                    })
        self.camera_task = camera.CameraTakePhotos(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.move_file_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.move_file_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (markor_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorMoveNote.generate_random_params()
        compound_params = {
            "file_name": markor_params["file_name"],
            "source_folder": markor_params["source_folder"],
            "destination_folder": markor_params["destination_folder"],
            "noise_candidates": _NOTE_TITLES,
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.move_file_task.tear_down(env)


class MarkorCreateFolderAndCameraTakePhotos(MarkorAndCamera):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "folder_name": {"type": "string"},
        },
        "required": ["folder_name"],
    }
    template = (
        "Create a new folder in Markor named {folder_name}."
        "then Create a new cameraing in Simple camera Pro. Name it {file_name_camera}. Save it in"
        " the Pictures folder within the sdk_gphone_x86_64 storage area."
        "then Take three Photos"
    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.markor_task = markor.MarkorCreateFolder(
            params={
                "folder_name": self.params["folder_name"],
            })
        self.camera_task = camera.CameraTakePhotos(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (markor_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorCreateFolder.generate_random_params()
        compound_params = {
            "folder_name": markor_params["folder_name"],
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorCreateNoteAndCameraTakePhotos(MarkorAndCamera):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "file_name": {"type": "string"},
            "text": {"type": "string"},
        },
        "required": ["file_name", "text"],
    }
    template = (
        "Create a new note in Markor named {file_name} with the following text:"
        " {text}"
        "then Take three Photos"
    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.markor_task = markor.MarkorCreateNote(
            params={
                "file_name": self.params["file_name"],
                "text": self.params["text"]
            })
        self.camera_task = camera.CameraTakePhotos(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (markor_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorCreateNote.generate_random_params()
        compound_params = {
            "file_name": markor_params["file_name"],
            "text": markor_params["text"],
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorCreateNoteFromClipboardAndCameraTakePhotos(MarkorAndCamera):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "file_name": {"type": "string"},
            "file_content": {"type": "string"},
        },
        "required": ["file_name", "file_content"],
    }
    template = (
        "Create a note in Markor named {file_name}. Perform a paste operation in"
        " the note and save the note."
        "then Take three Photos"
    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.markor_task = markor.MarkorCreateNoteFromClipboard(
            params={
                "file_name": self.params["file_name"],
                "file_content": self.params["file_content"]
            })
        self.camera_task = camera.CameraTakePhotos(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (markor_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorCreateNoteFromClipboard.generate_random_params()
        compound_params = {
            "file_name": markor_params["file_name"],
            "file_content": markor_params["file_content"],
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorMergeNotesAndCameraTakePhotos(MarkorAndCamera):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "file1_name": {"type": "string"},
            "file2_name": {"type": "string"},
            "file3_name": {"type": "string"},
            "new_file_name": {"type": "string"},
            "file1_content": {"type": "string"},
            "file2_content": {"type": "string"},
            "file3_content": {"type": "string"},

        },
        "required": ["file1_name",
                     "file2_name",
                     "file3_name",
                     "new_file_name",
                     "file1_content",
                     "file2_content",
                     "file3_content", ],
    }
    template = (
        "Merge the contents of Markor notes {file1_name}, {file2_name} and"
        " {file3_name} (in the same order) into a new Markor note named"
        " {new_file_name} and save it. Add a new line between the content of each"
        " note."
        "then Take three Photos"
    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.markor_task = markor.MarkorMergeNotes(
            params={
                "new_file_name": self.params["new_file_name"],
                "file1_name": self.params["file1_name"],
                "file2_name": self.params["file2_name"],
                "file3_name": self.params["file3_name"],
                "file1_content": self.params["file1_content"],
                "file2_content": self.params["file2_content"],
                "file3_content": self.params["file3_content"],

            })
        self.camera_task = camera.CameraTakePhotos(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (markor_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorMergeNotes.generate_random_params()
        compound_params = {
            "new_file_name": markor_params["new_file_name"],
            "file1_name": markor_params["file1_name"],
            "file2_name": markor_params["file2_name"],
            "file3_name": markor_params["file3_name"],
            "file1_content": markor_params["file1_content"],
            "file2_content": markor_params["file2_content"],
            "file3_content": markor_params["file3_content"],
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorChangeNoteContentAndCameraTakePhotos(MarkorAndCamera):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "original_name": {"type": "string"},
            "new_name": {"type": "string"},
            "updated_content": {"type": "string"},

        },
        "required": ["original_name", "new_name", "updated_content"],
    }
    template = (
        'Update the content of {original_name} to "{updated_content}" in Markor'
        " and change its name to {new_name}."
        "then Take three Photos"
    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.markor_task = markor.MarkorChangeNoteContent(
            params={
                "original_name": self.params["original_name"],
                "new_name": self.params["new_name"],
                "updated_content": self.params["updated_content"],

            })
        self.camera_task = camera.CameraTakePhotos(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (markor_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorChangeNoteContent.generate_random_params()
        compound_params = {
            "original_name": markor_params["original_name"],
            "new_name": markor_params["new_name"],
            "updated_content": markor_params["updated_content"],

        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorAddNoteHeaderAndCameraTakePhotos(MarkorAndCamera):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "original_name": {"type": "string"},
            "new_name": {"type": "string"},
            "header": {"type": "string"},
            "original_content": {"type": "string"},

        },
        "required": ["original_name", "new_name", "header", "original_content"],
    }
    template = (
        "Update the Markor note {original_name} by adding the following text,"
        ' along with a new blank line before the existing content: "{header}",'
        " and rename it to {new_name}."
        "then Take three Photos"
    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.markor_task = markor.MarkorAddNoteHeader(
            params={
                "original_name": self.params["original_name"],
                "new_name": self.params["new_name"],
                "header": self.params["header"],
                "original_content": self.params["original_content"],

            })
        self.camera_task = camera.CameraTakePhotos(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (markor_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorAddNoteHeader.generate_random_params()
        compound_params = {
            "original_name": markor_params["original_name"],
            "new_name": markor_params["new_name"],
            "header": markor_params["header"],
            "original_content": markor_params["original_content"],

        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorEditNoteAndCameraTakePhotos(MarkorAndCamera):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "file_name": {"type": "string"},
            "header": {"type": "string"},
            "footer": {"type": "string"},
            "replace_text": {"type": "string"},
            "edit_type": {
                "type": "string",
                "enum": ["header", "footer", "replace"],
            },

        },
        "required": ["file_name", "edit_type"],
    }

    @property
    def template(self) -> str:
        templates = {
            "header": (
                "Edit {file_name} in Markor. Add to the top of the note {header}"
                "then Take three Photos"
            ),
            "footer": (
                "Edit {file_name} in Markor. Add to the bottom of the note {footer}"
                "then Take three Photos"
            ),
            "replace": (
                "Edit {file_name} in Markor. Replace the text with {replace_text}"
                "then Take three Photos"
            ),
        }

        if "edit_type" not in self.params and "edit_type" not in templates:
            return templates.get(
                self.params.get("edit_type"),
                "Invalid edit_type for {file_name} in Markor.",
            )
        return templates[self.params.get("edit_type")]

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        markor_params = {
            "file_name": self.params["file_name"],
            "edit_type": self.params["edit_type"],
        }
        if self.params["edit_type"] == "header":
            markor_params["header"] = self.params["header"]
        elif self.params["edit_type"] == "footer":
            markor_params["footer"] = self.params["footer"]
        elif self.params["edit_type"] == "replace":
            markor_params["replace_text"] = self.params["replace_text"]
        self.markor_task = markor.MarkorEditNote(markor_params)
        self.camera_task = camera.CameraTakePhotos(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (markor_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorEditNote.generate_random_params()
        compound_params = {
            "file_name": markor_params["file_name"],
            "edit_type": markor_params["edit_type"],

        }
        if markor_params["edit_type"] == "header":
            compound_params["header"] = markor_params["header"]
        elif markor_params["edit_type"] == "footer":
            compound_params["footer"] = markor_params["footer"]
        elif markor_params["edit_type"] == "replace":
            compound_params["replace_text"] = markor_params["replace_text"]

        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)





class MarkorMoveNoteandCreateFolderAndCameraTakePhotoAndVideo(MarkorAndCamera):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "file_name": {"type": "string"},
            "source_folder": {"type": "string"},
            "destination_folder": {"type": "string"},
            "folder_name": {"type": "string"},
        },
        "required": ["file_name", "source_folder", "destination_folder", "folder_name"],
    }
    template = (
        "In Markor, move the note {file_name} from {source_folder} to"
        " {destination_folder}. Also, create a new folder named {folder_name} in Markor."
        " then Take one Photo and one VIdeo"
    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.move_file_task = markor.MarkorMoveNoteandCreateFolder(
            params={"file_name": self.params["file_name"],
                    "source_folder": self.params["source_folder"],
                    "destination_folder": self.params["destination_folder"],
                    "folder_name": self.params["folder_name"],
                    "noise_candidates": self.params["noise_candidates"]

                    })
        self.camera_task = camera.CameraTakePhotoAndVideo(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.move_file_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.move_file_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (markor_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorMoveNoteandCreateFolder.generate_random_params()
        compound_params = {
            "file_name": markor_params["file_name"],
            "source_folder": markor_params["source_folder"],
            "destination_folder": markor_params["destination_folder"],
            "noise_candidates": _NOTE_TITLES,
            "folder_name": markor_params["folder_name"],
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.move_file_task.tear_down(env)


class MarkorCreateFolderthenCreateNoteAndCameraTakePhotoAndVideo(MarkorAndCamera):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "file_name": {"type": "string"},
            "folder_name": {"type": "string"},
        },
        "required": ["folder_name", "file_name", ],
    }
    template = (
        "Create a new folder in Markor named {folder_name} and then create a new note named {file_name} in this folder with the following text:"
        " {text}"
        " then Take one Photo and one VIdeo"

    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.markor_task = markor.MarkorCreateFolderthenCreateNote(
            params={"file_name": self.params["file_name"],
                    "folder_name": self.params["folder_name"],
                    "text": self.params["text"],

                    })
        self.camera_task = camera.CameraTakePhotoAndVideo(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (markor_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorCreateFolderthenCreateNote.generate_random_params()
        compound_params = {
            "file_name": markor_params["file_name"],
            "folder_name": markor_params["folder_name"],
            "text": markor_params["text"],
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorMoveNoteAndCameraTakePhotoAndVideo(MarkorAndCamera):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "file_name": {"type": "string"},
            "source_folder": {"type": "string"},
            "destination_folder": {"type": "string"},
        },
        "required": ["file_name", "source_folder", "destination_folder"],
    }
    template = (
        "In Markor, move the note {file_name} from {source_folder} to"
        " {destination_folder}."
        "then Take one Photo and one VIdeo"
    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.move_file_task = markor.MarkorMoveNote(
            params={"file_name": self.params["file_name"],
                    "source_folder": self.params["source_folder"],
                    "destination_folder": self.params["destination_folder"],
                    "noise_candidates": self.params["noise_candidates"]

                    })
        self.camera_task = camera.CameraTakePhotoAndVideo(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.move_file_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.move_file_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (markor_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorMoveNote.generate_random_params()
        compound_params = {
            "file_name": markor_params["file_name"],
            "source_folder": markor_params["source_folder"],
            "destination_folder": markor_params["destination_folder"],
            "noise_candidates": _NOTE_TITLES,
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.move_file_task.tear_down(env)


class MarkorCreateFolderAndCameraTakePhotoAndVideo(MarkorAndCamera):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "folder_name": {"type": "string"},
        },
        "required": ["folder_name"],
    }
    template = (
        "Create a new folder in Markor named {folder_name}."
        "then Take one Photo and one VIdeo"
    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.markor_task = markor.MarkorCreateFolder(
            params={
                "folder_name": self.params["folder_name"],
            })
        self.camera_task = camera.CameraTakePhotoAndVideo(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (markor_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorCreateFolder.generate_random_params()
        compound_params = {
            "folder_name": markor_params["folder_name"],
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorCreateNoteAndCameraTakePhotoAndVideo(MarkorAndCamera):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "file_name": {"type": "string"},
            "text": {"type": "string"},
        },
        "required": ["file_name", "text"],
    }
    template = (
        "Create a new note in Markor named {file_name} with the following text:"
        " {text}"
        "then Take one Photo and one VIdeo"
    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.markor_task = markor.MarkorCreateNote(
            params={
                "file_name": self.params["file_name"],
                "text": self.params["text"]
            })
        self.camera_task = camera.CameraTakePhotoAndVideo(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (markor_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorCreateNote.generate_random_params()
        compound_params = {
            "file_name": markor_params["file_name"],
            "text": markor_params["text"],
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorCreateNoteFromClipboardAndCameraTakePhotoAndVideo(MarkorAndCamera):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "file_name": {"type": "string"},
            "file_content": {"type": "string"},
        },
        "required": ["file_name", "file_content"],
    }
    template = (
        "Create a note in Markor named {file_name}. Perform a paste operation in"
        " the note and save the note."
        "then Take one Photo and one VIdeo"
    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.markor_task = markor.MarkorCreateNoteFromClipboard(
            params={
                "file_name": self.params["file_name"],
                "file_content": self.params["file_content"]
            })
        self.camera_task = camera.CameraTakePhotoAndVideo(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (markor_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorCreateNoteFromClipboard.generate_random_params()
        compound_params = {
            "file_name": markor_params["file_name"],
            "file_content": markor_params["file_content"],
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorMergeNotesAndCameraTakePhotoAndVideo(MarkorAndCamera):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "file1_name": {"type": "string"},
            "file2_name": {"type": "string"},
            "file3_name": {"type": "string"},
            "new_file_name": {"type": "string"},
            "file1_content": {"type": "string"},
            "file2_content": {"type": "string"},
            "file3_content": {"type": "string"},

        },
        "required": ["file1_name",
                     "file2_name",
                     "file3_name",
                     "new_file_name",
                     "file1_content",
                     "file2_content",
                     "file3_content", ],
    }
    template = (
        "Merge the contents of Markor notes {file1_name}, {file2_name} and"
        " {file3_name} (in the same order) into a new Markor note named"
        " {new_file_name} and save it. Add a new line between the content of each"
        " note."
        "then Take one Photo and one VIdeo"
    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.markor_task = markor.MarkorMergeNotes(
            params={
                "new_file_name": self.params["new_file_name"],
                "file1_name": self.params["file1_name"],
                "file2_name": self.params["file2_name"],
                "file3_name": self.params["file3_name"],
                "file1_content": self.params["file1_content"],
                "file2_content": self.params["file2_content"],
                "file3_content": self.params["file3_content"],

            })
        self.camera_task = camera.CameraTakePhotoAndVideo(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (markor_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorMergeNotes.generate_random_params()
        compound_params = {
            "new_file_name": markor_params["new_file_name"],
            "file1_name": markor_params["file1_name"],
            "file2_name": markor_params["file2_name"],
            "file3_name": markor_params["file3_name"],
            "file1_content": markor_params["file1_content"],
            "file2_content": markor_params["file2_content"],
            "file3_content": markor_params["file3_content"],
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorChangeNoteContentAndCameraTakePhotoAndVideo(MarkorAndCamera):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "original_name": {"type": "string"},
            "new_name": {"type": "string"},
            "updated_content": {"type": "string"},

        },
        "required": ["original_name", "new_name", "updated_content"],
    }
    template = (
        'Update the content of {original_name} to "{updated_content}" in Markor'
        " and change its name to {new_name}."
        "then Take one Photo and one VIdeo"
    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.markor_task = markor.MarkorChangeNoteContent(
            params={
                "original_name": self.params["original_name"],
                "new_name": self.params["new_name"],
                "updated_content": self.params["updated_content"],

            })
        self.camera_task = camera.CameraTakePhotoAndVideo(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (markor_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorChangeNoteContent.generate_random_params()
        compound_params = {
            "original_name": markor_params["original_name"],
            "new_name": markor_params["new_name"],
            "updated_content": markor_params["updated_content"],

        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorAddNoteHeaderAndCameraTakePhotoAndVideo(MarkorAndCamera):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "original_name": {"type": "string"},
            "new_name": {"type": "string"},
            "header": {"type": "string"},
            "original_content": {"type": "string"},

        },
        "required": ["original_name", "new_name", "header", "original_content"],
    }
    template = (
        "Update the Markor note {original_name} by adding the following text,"
        ' along with a new blank line before the existing content: "{header}",'
        " and rename it to {new_name}."
        "then Take one Photo and one VIdeo"
    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.markor_task = markor.MarkorAddNoteHeader(
            params={
                "original_name": self.params["original_name"],
                "new_name": self.params["new_name"],
                "header": self.params["header"],
                "original_content": self.params["original_content"],

            })
        self.camera_task = camera.CameraTakePhotoAndVideo(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (markor_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorAddNoteHeader.generate_random_params()
        compound_params = {
            "original_name": markor_params["original_name"],
            "new_name": markor_params["new_name"],
            "header": markor_params["header"],
            "original_content": markor_params["original_content"],

        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorEditNoteAndCameraTakePhotoAndVideo(MarkorAndCamera):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "file_name": {"type": "string"},
            "header": {"type": "string"},
            "footer": {"type": "string"},
            "replace_text": {"type": "string"},
            "edit_type": {
                "type": "string",
                "enum": ["header", "footer", "replace"],
            },

        },
        "required": ["file_name", "edit_type"],
    }

    @property
    def template(self) -> str:
        templates = {
            "header": (
                "Edit {file_name} in Markor. Add to the top of the note {header}"
                "then Take one Photo and one VIdeo"
            ),
            "footer": (
                "Edit {file_name} in Markor. Add to the bottom of the note {footer}"
                "then Take one Photo and one VIdeo"
            ),
            "replace": (
                "Edit {file_name} in Markor. Replace the text with {replace_text}"
                "then Take one Photo and one VIdeo"
            ),
        }

        if "edit_type" not in self.params and "edit_type" not in templates:
            return templates.get(
                self.params.get("edit_type"),
                "Invalid edit_type for {file_name} in Markor.",
            )
        return templates[self.params.get("edit_type")]

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        markor_params = {
            "file_name": self.params["file_name"],
            "edit_type": self.params["edit_type"],
        }
        if self.params["edit_type"] == "header":
            markor_params["header"] = self.params["header"]
        elif self.params["edit_type"] == "footer":
            markor_params["footer"] = self.params["footer"]
        elif self.params["edit_type"] == "replace":
            markor_params["replace_text"] = self.params["replace_text"]
        self.markor_task = markor.MarkorEditNote(markor_params)
        self.camera_task = camera.CameraTakePhotoAndVideo(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (markor_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorEditNote.generate_random_params()
        compound_params = {
            "file_name": markor_params["file_name"],
            "edit_type": markor_params["edit_type"],

        }
        if markor_params["edit_type"] == "header":
            compound_params["header"] = markor_params["header"]
        elif markor_params["edit_type"] == "footer":
            compound_params["footer"] = markor_params["footer"]
        elif markor_params["edit_type"] == "replace":
            compound_params["replace_text"] = markor_params["replace_text"]

        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorMoveNoteandCreateFolderAndCameraTakePhotosAndVideos(MarkorAndCamera):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "file_name": {"type": "string"},
            "source_folder": {"type": "string"},
            "destination_folder": {"type": "string"},
            "folder_name": {"type": "string"},
        },
        "required": ["file_name", "source_folder", "destination_folder", "folder_name"],
    }
    template = (
        "In Markor, move the note {file_name} from {source_folder} to"
        " {destination_folder}. Also, create a new folder named {folder_name} in Markor."
        " then Take five photos and two videos"
    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.move_file_task = markor.MarkorMoveNoteandCreateFolder(
            params={"file_name": self.params["file_name"],
                    "source_folder": self.params["source_folder"],
                    "destination_folder": self.params["destination_folder"],
                    "folder_name": self.params["folder_name"],
                    "noise_candidates": self.params["noise_candidates"]

                    })
        self.camera_task = camera.CameraTakePhotosAndVideos(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.move_file_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.move_file_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (markor_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorMoveNoteandCreateFolder.generate_random_params()
        compound_params = {
            "file_name": markor_params["file_name"],
            "source_folder": markor_params["source_folder"],
            "destination_folder": markor_params["destination_folder"],
            "noise_candidates": _NOTE_TITLES,
            "folder_name": markor_params["folder_name"],
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.move_file_task.tear_down(env)


class MarkorCreateFolderthenCreateNoteAndCameraTakePhotosAndVideos(MarkorAndCamera):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "file_name": {"type": "string"},
            "folder_name": {"type": "string"},
        },
        "required": ["folder_name", "file_name", ],
    }
    template = (
        "Create a new folder in Markor named {folder_name} and then create a new note named {file_name} in this folder with the following text:"
        " {text}"
        " then Take five photos and two videos"

    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.markor_task = markor.MarkorCreateFolderthenCreateNote(
            params={"file_name": self.params["file_name"],
                    "folder_name": self.params["folder_name"],
                    "text": self.params["text"],

                    })
        self.camera_task = camera.CameraTakePhotosAndVideos(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (markor_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorCreateFolderthenCreateNote.generate_random_params()
        compound_params = {
            "file_name": markor_params["file_name"],
            "folder_name": markor_params["folder_name"],
            "text": markor_params["text"],
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorMoveNoteAndCameraTakePhotosAndVideos(MarkorAndCamera):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "file_name": {"type": "string"},
            "source_folder": {"type": "string"},
            "destination_folder": {"type": "string"},
        },
        "required": ["file_name", "source_folder", "destination_folder"],
    }
    template = (
        "In Markor, move the note {file_name} from {source_folder} to"
        " {destination_folder}."
        "then Take five photos and two videos"
    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.move_file_task = markor.MarkorMoveNote(
            params={"file_name": self.params["file_name"],
                    "source_folder": self.params["source_folder"],
                    "destination_folder": self.params["destination_folder"],
                    "noise_candidates": self.params["noise_candidates"]

                    })
        self.camera_task = camera.CameraTakePhotosAndVideos(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.move_file_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.move_file_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (markor_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorMoveNote.generate_random_params()
        compound_params = {
            "file_name": markor_params["file_name"],
            "source_folder": markor_params["source_folder"],
            "destination_folder": markor_params["destination_folder"],
            "noise_candidates": _NOTE_TITLES,
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.move_file_task.tear_down(env)


class MarkorCreateFolderAndCameraTakePhotosAndVideos(MarkorAndCamera):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "folder_name": {"type": "string"},
        },
        "required": ["folder_name"],
    }
    template = (
        "Create a new folder in Markor named {folder_name}."
        "then Take five photos and two videos"
    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.markor_task = markor.MarkorCreateFolder(
            params={
                "folder_name": self.params["folder_name"],
            })
        self.camera_task = camera.CameraTakePhotosAndVideos(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (markor_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorCreateFolder.generate_random_params()
        compound_params = {
            "folder_name": markor_params["folder_name"],
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorCreateNoteAndCameraTakePhotosAndVideos(MarkorAndCamera):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "file_name": {"type": "string"},
            "text": {"type": "string"},
        },
        "required": ["file_name", "text"],
    }
    template = (
        "Create a new note in Markor named {file_name} with the following text:"
        " {text}"
        "then Take five photos and two videos"
    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.markor_task = markor.MarkorCreateNote(
            params={
                "file_name": self.params["file_name"],
                "text": self.params["text"]
            })
        self.camera_task = camera.CameraTakePhotosAndVideos(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (markor_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorCreateNote.generate_random_params()
        compound_params = {
            "file_name": markor_params["file_name"],
            "text": markor_params["text"],
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorCreateNoteFromClipboardAndCameraTakePhotosAndVideos(MarkorAndCamera):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "file_name": {"type": "string"},
            "file_content": {"type": "string"},
        },
        "required": ["file_name", "file_content"],
    }
    template = (
        "Create a note in Markor named {file_name}. Perform a paste operation in"
        " the note and save the note."
        "then Take five photos and two videos"
    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.markor_task = markor.MarkorCreateNoteFromClipboard(
            params={
                "file_name": self.params["file_name"],
                "file_content": self.params["file_content"]
            })
        self.camera_task = camera.CameraTakePhotosAndVideos(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (markor_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorCreateNoteFromClipboard.generate_random_params()
        compound_params = {
            "file_name": markor_params["file_name"],
            "file_content": markor_params["file_content"],
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorMergeNotesAndCameraTakePhotosAndVideos(MarkorAndCamera):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "file1_name": {"type": "string"},
            "file2_name": {"type": "string"},
            "file3_name": {"type": "string"},
            "new_file_name": {"type": "string"},
            "file1_content": {"type": "string"},
            "file2_content": {"type": "string"},
            "file3_content": {"type": "string"},

        },
        "required": ["file1_name",
                     "file2_name",
                     "file3_name",
                     "new_file_name",
                     "file1_content",
                     "file2_content",
                     "file3_content", ],
    }
    template = (
        "Merge the contents of Markor notes {file1_name}, {file2_name} and"
        " {file3_name} (in the same order) into a new Markor note named"
        " {new_file_name} and save it. Add a new line between the content of each"
        " note."
        "then Take five photos and two videos"
    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.markor_task = markor.MarkorMergeNotes(
            params={
                "new_file_name": self.params["new_file_name"],
                "file1_name": self.params["file1_name"],
                "file2_name": self.params["file2_name"],
                "file3_name": self.params["file3_name"],
                "file1_content": self.params["file1_content"],
                "file2_content": self.params["file2_content"],
                "file3_content": self.params["file3_content"],

            })
        self.camera_task = camera.CameraTakePhotosAndVideos(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (markor_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorMergeNotes.generate_random_params()
        compound_params = {
            "new_file_name": markor_params["new_file_name"],
            "file1_name": markor_params["file1_name"],
            "file2_name": markor_params["file2_name"],
            "file3_name": markor_params["file3_name"],
            "file1_content": markor_params["file1_content"],
            "file2_content": markor_params["file2_content"],
            "file3_content": markor_params["file3_content"],
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorChangeNoteContentAndCameraTakePhotosAndVideos(MarkorAndCamera):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "original_name": {"type": "string"},
            "new_name": {"type": "string"},
            "updated_content": {"type": "string"},

        },
        "required": ["original_name", "new_name", "updated_content"],
    }
    template = (
        'Update the content of {original_name} to "{updated_content}" in Markor'
        " and change its name to {new_name}."
        "then Take five photos and two videos"
    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.markor_task = markor.MarkorChangeNoteContent(
            params={
                "original_name": self.params["original_name"],
                "new_name": self.params["new_name"],
                "updated_content": self.params["updated_content"],

            })
        self.camera_task = camera.CameraTakePhotosAndVideos(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (markor_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorChangeNoteContent.generate_random_params()
        compound_params = {
            "original_name": markor_params["original_name"],
            "new_name": markor_params["new_name"],
            "updated_content": markor_params["updated_content"],

        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorAddNoteHeaderAndCameraTakePhotosAndVideos(MarkorAndCamera):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "original_name": {"type": "string"},
            "new_name": {"type": "string"},
            "header": {"type": "string"},
            "original_content": {"type": "string"},

        },
        "required": ["original_name", "new_name", "header", "original_content"],
    }
    template = (
        "Update the Markor note {original_name} by adding the following text,"
        ' along with a new blank line before the existing content: "{header}",'
        " and rename it to {new_name}."
        "then Take five photos and two videos"
    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.markor_task = markor.MarkorAddNoteHeader(
            params={
                "original_name": self.params["original_name"],
                "new_name": self.params["new_name"],
                "header": self.params["header"],
                "original_content": self.params["original_content"],

            })
        self.camera_task = camera.CameraTakePhotosAndVideos(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (markor_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorAddNoteHeader.generate_random_params()
        compound_params = {
            "original_name": markor_params["original_name"],
            "new_name": markor_params["new_name"],
            "header": markor_params["header"],
            "original_content": markor_params["original_content"],

        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorEditNoteAndCameraTakePhotosAndVideos(MarkorAndCamera):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "file_name": {"type": "string"},
            "header": {"type": "string"},
            "footer": {"type": "string"},
            "replace_text": {"type": "string"},
            "edit_type": {
                "type": "string",
                "enum": ["header", "footer", "replace"],
            },

        },
        "required": ["file_name", "edit_type"],
    }

    @property
    def template(self) -> str:
        templates = {
            "header": (
                "Edit {file_name} in Markor. Add to the top of the note {header}"
                "then Take five photos and two videos"
            ),
            "footer": (
                "Edit {file_name} in Markor. Add to the bottom of the note {footer}"
                "then Take five photos and two videos"
            ),
            "replace": (
                "Edit {file_name} in Markor. Replace the text with {replace_text}"
                "then Take five photos and two videos"
            ),
        }

        if "edit_type" not in self.params and "edit_type" not in templates:
            return templates.get(
                self.params.get("edit_type"),
                "Invalid edit_type for {file_name} in Markor.",
            )
        return templates[self.params.get("edit_type")]

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        markor_params = {
            "file_name": self.params["file_name"],
            "edit_type": self.params["edit_type"],
        }
        if self.params["edit_type"] == "header":
            markor_params["header"] = self.params["header"]
        elif self.params["edit_type"] == "footer":
            markor_params["footer"] = self.params["footer"]
        elif self.params["edit_type"] == "replace":
            markor_params["replace_text"] = self.params["replace_text"]
        self.markor_task = markor.MarkorEditNote(markor_params)
        self.camera_task = camera.CameraTakePhotosAndVideos(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (markor_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorEditNote.generate_random_params()
        compound_params = {
            "file_name": markor_params["file_name"],
            "edit_type": markor_params["edit_type"],

        }
        if markor_params["edit_type"] == "header":
            compound_params["header"] = markor_params["header"]
        elif markor_params["edit_type"] == "footer":
            compound_params["footer"] = markor_params["footer"]
        elif markor_params["edit_type"] == "replace":
            compound_params["replace_text"] = markor_params["replace_text"]

        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)

_NOTE_TITLES = [
    "grocery_list_weekly.md",
    "meeting_notes_project_team.md",
    "personal_goals_2024.md",
    "reading_list_2024.md",
    "research_paper_summary.md",
    "summer_vacation_plans.md",
    "budget_home_renovation.md",
    "april_workout_routine.md",
    "birthday_gift_ideas_mom.md",
    "recipe_homemade_pizza.md",
    "weekend_todo_list.md",
    "insurance_plan_comparison.md",
    "art_project_sketches.md",
    "python_learning_goals.md",
    "trip_reflections_recent.md",
    "startup_ideas_launch.md",
    "client_meetings_schedule.md",
    "favorite_book_quotes.md",
    "garden_layout_plan.md",
    "upcoming_presentation_outline.md",
]