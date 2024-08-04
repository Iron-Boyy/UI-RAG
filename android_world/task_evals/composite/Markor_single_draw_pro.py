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
from android_world.task_evals.single import simple_draw_pro
from android_world.task_evals.single import markor
from absl import logging
from android_world.env import adb_utils
from android_world.task_evals.single import vlc
from android_world.task_evals.utils import receipt_generator
from android_world.utils import datetime_utils
from android_world.utils import fuzzy_match_lib
import subprocess

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


class MarkorAndDraw(task_eval.TaskEval):
  app_names = ("markor","simple draw pro")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    file_utils.clear_directory(device_constants.MARKOR_DATA, env.base_env)

  def tear_down(self, env: interface.AsyncEnv) -> None:
    super().tear_down(env)
    file_utils.clear_directory(device_constants.MARKOR_DATA, env.base_env)

class MarkorMoveNoteandCreateFolderAndSimpleDrawProCreateDrawing(MarkorAndDraw):
  """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

  complexity = 3
  schema = {
      "type": "object",
      "properties": {
          "file_name": {"type": "string"},
          "file_name_draw": {"type": "string"},
          "source_folder": {"type": "string"},
          "destination_folder": {"type": "string"},
          "folder_name": {"type": "string"},
          "text": {"type": "string"},
      },
      "required": ["file_name", "source_folder", "destination_folder", "folder_name", "file_name_draw","text"],
  }
  template = (
      "In Markor, move the note {file_name} from {source_folder} to"
      " {destination_folder}. Also, create a new folder named {folder_name} in Markor."
      "then Create a new drawing in Simple Draw Pro. Name it {file_name_draw}. Save it in"
      " the Pictures folder within the sdk_gphone_x86_64 storage area."
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
    self.draw_task = simple_draw_pro.SimpleDrawProCreateDrawing(params={"file_name": self.params["file_name_draw"],
                                                                        "text": self.params["text"]})



  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    self.move_file_task.initialize_task(env)
    self.draw_task.initialize_task(env)


  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    markor_success = self.move_file_task.is_successful(env)
    logging.info("Markor success: %s", markor_success)

    draw_success = self.draw_task.is_successful(env)
    logging.info("Draw success: %s", draw_success)

    return (markor_success + draw_success) / 2.0

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    markor_params = markor.MarkorMoveNoteandCreateFolder.generate_random_params()
    draw_params = simple_draw_pro.SimpleDrawProCreateDrawing.generate_random_params()
    compound_params ={
        "file_name": markor_params["file_name"],
        "source_folder": markor_params["source_folder"],
        "destination_folder": markor_params["destination_folder"],
        "noise_candidates": _NOTE_TITLES,
        "folder_name": markor_params["folder_name"],
        "file_name_draw": draw_params["file_name"],
        "text": "",  # Unused.
    }
    return compound_params

  def tear_down(self, env: interface.AsyncEnv) -> None:
    super().tear_down(env)
    self.move_file_task.tear_down(env)

class MarkorCreateFolderthenCreateNoteAndSimpleDrawProCreateDrawing(MarkorAndDraw):
  """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

  complexity = 3
  schema = {
      "type": "object",
      "properties": {
          "file_name": {"type": "string"},
          "file_name_draw": {"type": "string"},
          "folder_name": {"type": "string"},
          "text": {"type": "string"},
      },
      "required": ["folder_name", "file_name", "text","file_name_draw"],
  }
  template = (
      "Create a new folder in Markor named {folder_name} and then create a new note named {file_name} in this folder with the following text:"
      " {text}"
      "then Create a new drawing in Simple Draw Pro. Name it {file_name_draw}. Save it in"
      " the Pictures folder within the sdk_gphone_x86_64 storage area."
  )

  def __init__(self, params: dict[str, Any]):
    """Initialize the task."""
    super().__init__(params)
    self.markor_task = markor.MarkorCreateFolderthenCreateNote(
        params={ "file_name": self.params["file_name"],
                 "folder_name" : self.params["folder_name"],
                 "text": self.params["text"],

        })
    self.draw_task = simple_draw_pro.SimpleDrawProCreateDrawing(params={"file_name": self.params["file_name_draw"],
                                                                        "text": self.params["text_none"]})



  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    self.markor_task.initialize_task(env)
    self.draw_task.initialize_task(env)


  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    markor_success = self.markor_task.is_successful(env)
    logging.info("Markor success: %s", markor_success)

    draw_success = self.draw_task.is_successful(env)
    logging.info("Draw success: %s", draw_success)

    return (markor_success + draw_success) / 2.0

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    markor_params = markor.MarkorCreateFolderthenCreateNote.generate_random_params()
    draw_params = simple_draw_pro.SimpleDrawProCreateDrawing.generate_random_params()
    compound_params ={
        "file_name": markor_params["file_name"],
        "folder_name": markor_params["folder_name"],
        "text": markor_params["text"],
        "text_none": "",  # Unused.
        "file_name_draw": draw_params["file_name"],
    }
    return compound_params

  def tear_down(self, env: interface.AsyncEnv) -> None:
    super().tear_down(env)
    self.markor_task.tear_down(env)


class MarkorMoveNoteAndSimpleDrawProCreateDrawing(MarkorAndDraw):
  """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

  complexity = 3
  schema = {
      "type": "object",
      "properties": {
          "file_name": {"type": "string"},
          "file_name_draw": {"type": "string"},
          "source_folder": {"type": "string"},
          "destination_folder": {"type": "string"},
          "text": {"type": "string"},
      },
      "required": ["file_name", "source_folder", "destination_folder" ,"file_name_draw","text"],
  }
  template = (
      "In Markor, move the note {file_name} from {source_folder} to"
      " {destination_folder}."
      "then Create a new drawing in Simple Draw Pro. Name it {file_name_draw}. Save it in"
      " the Pictures folder within the sdk_gphone_x86_64 storage area."
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
    self.draw_task = simple_draw_pro.SimpleDrawProCreateDrawing(params={"file_name": self.params["file_name_draw"],
                                                                        "text": self.params["text"]})



  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    self.move_file_task.initialize_task(env)
    self.draw_task.initialize_task(env)


  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    markor_success = self.move_file_task.is_successful(env)
    logging.info("Markor success: %s", markor_success)

    draw_success = self.draw_task.is_successful(env)
    logging.info("Draw success: %s", draw_success)

    return (markor_success + draw_success) / 2.0

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    markor_params = markor.MarkorMoveNote.generate_random_params()
    draw_params = simple_draw_pro.SimpleDrawProCreateDrawing.generate_random_params()
    compound_params ={
        "file_name": markor_params["file_name"],
        "source_folder": markor_params["source_folder"],
        "destination_folder": markor_params["destination_folder"],
        "noise_candidates": _NOTE_TITLES,
        "file_name_draw": draw_params["file_name"],
        "text": "",  # Unused.
    }
    return compound_params

  def tear_down(self, env: interface.AsyncEnv) -> None:
    super().tear_down(env)
    self.move_file_task.tear_down(env)


class MarkorCreateFolderAndSimpleDrawProCreateDrawing(MarkorAndDraw):
  """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

  complexity = 3
  schema = {
      "type": "object",
      "properties": {
          "file_name_draw": {"type": "string"},
          "folder_name": {"type": "string"},
          "text": {"type": "string"},
      },
      "required": ["folder_name", "file_name_draw","text"],
  }
  template = (
      "Create a new folder in Markor named {folder_name}."
      "then Create a new drawing in Simple Draw Pro. Name it {file_name_draw}. Save it in"
      " the Pictures folder within the sdk_gphone_x86_64 storage area."
  )

  def __init__(self, params: dict[str, Any]):
    """Initialize the task."""
    super().__init__(params)
    self.markor_task = markor.MarkorCreateFolder(
        params={
                 "folder_name" : self.params["folder_name"],
        })
    self.draw_task = simple_draw_pro.SimpleDrawProCreateDrawing(params={"file_name": self.params["file_name_draw"],
                                                                        "text": self.params["text"]})



  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    self.markor_task.initialize_task(env)
    self.draw_task.initialize_task(env)


  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    markor_success = self.markor_task.is_successful(env)
    logging.info("Markor success: %s", markor_success)

    draw_success = self.draw_task.is_successful(env)
    logging.info("Draw success: %s", draw_success)

    return (markor_success + draw_success) / 2.0

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    markor_params = markor.MarkorCreateFolder.generate_random_params()
    draw_params = simple_draw_pro.SimpleDrawProCreateDrawing.generate_random_params()
    compound_params ={
        "folder_name": markor_params["folder_name"],
        "file_name_draw": draw_params["file_name"],
        "text": "",  # Unused.
    }
    return compound_params

  def tear_down(self, env: interface.AsyncEnv) -> None:
    super().tear_down(env)
    self.markor_task.tear_down(env)

class MarkorCreateNoteAndSimpleDrawProCreateDrawing(MarkorAndDraw):
  """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

  complexity = 3
  schema = {
      "type": "object",
      "properties": {
          "file_name": {"type": "string"},
          "file_name_draw": {"type": "string"},
          "text_draw": {"type": "string"},
          "text": {"type": "string"},
      },
      "required": ["file_name_draw","text","text_draw"],
  }
  template = (
      "Create a new note in Markor named {file_name} with the following text:"
      " {text}"
      "then Create a new drawing in Simple Draw Pro. Name it {file_name_draw}. Save it in"
      " the Pictures folder within the sdk_gphone_x86_64 storage area."
  )

  def __init__(self, params: dict[str, Any]):
    """Initialize the task."""
    super().__init__(params)
    self.markor_task = markor.MarkorCreateNote(
        params={
                 "file_name" : self.params["file_name"],
                 "text": self.params["text"]
        })
    self.draw_task = simple_draw_pro.SimpleDrawProCreateDrawing(params={"file_name": self.params["file_name_draw"],
                                                                        "text": self.params["text_draw"]})



  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    self.markor_task.initialize_task(env)
    self.draw_task.initialize_task(env)


  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    markor_success = self.markor_task.is_successful(env)
    logging.info("Markor success: %s", markor_success)

    draw_success = self.draw_task.is_successful(env)
    logging.info("Draw success: %s", draw_success)

    return (markor_success + draw_success) / 2.0

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    markor_params = markor.MarkorCreateNote.generate_random_params()
    draw_params = simple_draw_pro.SimpleDrawProCreateDrawing.generate_random_params()
    compound_params ={
        "file_name": markor_params["file_name"],
        "file_name_draw": draw_params["file_name"],
        "text_draw": "",
        "text":  markor_params["text"],
    }
    return compound_params

  def tear_down(self, env: interface.AsyncEnv) -> None:
    super().tear_down(env)
    self.markor_task.tear_down(env)


class MarkorCreateNoteFromClipboardAndSimpleDrawProCreateDrawing(MarkorAndDraw):
  """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

  complexity = 3
  schema = {
      "type": "object",
      "properties": {
          "file_name": {"type": "string"},
          "file_name_draw": {"type": "string"},
          "text_draw": {"type": "string"},
          "file_content": {"type": "string"},
      },
      "required": ["file_name","file_name_draw","file_content","text_draw"],
  }
  template = (
      "Create a note in Markor named {file_name}. Perform a paste operation in"
      " the note and save the note."
      "then Create a new drawing in Simple Draw Pro. Name it {file_name_draw}. Save it in"
      " the Pictures folder within the sdk_gphone_x86_64 storage area."
  )

  def __init__(self, params: dict[str, Any]):
    """Initialize the task."""
    super().__init__(params)
    self.markor_task = markor.MarkorCreateNoteFromClipboard(
        params={
                 "file_name" : self.params["file_name"],
                 "file_content": self.params["file_content"]
        })
    self.draw_task = simple_draw_pro.SimpleDrawProCreateDrawing(params={"file_name": self.params["file_name_draw"],
                                                                        "text": self.params["text_draw"]})



  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    self.markor_task.initialize_task(env)
    self.draw_task.initialize_task(env)


  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    markor_success = self.markor_task.is_successful(env)
    logging.info("Markor success: %s", markor_success)

    draw_success = self.draw_task.is_successful(env)
    logging.info("Draw success: %s", draw_success)

    return (markor_success + draw_success) / 2.0

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    markor_params = markor.MarkorCreateNoteFromClipboard.generate_random_params()
    draw_params = simple_draw_pro.SimpleDrawProCreateDrawing.generate_random_params()
    compound_params ={
        "file_name": markor_params["file_name"],
        "file_name_draw": draw_params["file_name"],
        "text_draw": "",
        "file_content": markor_params["file_content"],
    }
    return compound_params

  def tear_down(self, env: interface.AsyncEnv) -> None:
    super().tear_down(env)
    self.markor_task.tear_down(env)


class MarkorMergeNotesAndSimpleDrawProCreateDrawing(MarkorAndDraw):
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
          "file_name_draw": {"type": "string"},
          "text_draw": {"type": "string"},

      },
      "required": [   "file1_name",
          "file2_name",
          "file3_name",
          "new_file_name",
          "file1_content",
          "file2_content",
          "file3_content","file_name_draw","text_draw"],
  }
  template = (
      "Merge the contents of Markor notes {file1_name}, {file2_name} and"
      " {file3_name} (in the same order) into a new Markor note named"
      " {new_file_name} and save it. Add a new line between the content of each"
      " note."
      "then Create a new drawing in Simple Draw Pro. Name it {file_name_draw}. Save it in"
      " the Pictures folder within the sdk_gphone_x86_64 storage area."
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
    self.draw_task = simple_draw_pro.SimpleDrawProCreateDrawing(params={"file_name": self.params["file_name_draw"],
                                                                        "text": self.params["text_draw"]})



  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    self.markor_task.initialize_task(env)
    self.draw_task.initialize_task(env)


  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    markor_success = self.markor_task.is_successful(env)
    logging.info("Markor success: %s", markor_success)

    draw_success = self.draw_task.is_successful(env)
    logging.info("Draw success: %s", draw_success)

    return (markor_success + draw_success) / 2.0

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    markor_params = markor.MarkorMergeNotes.generate_random_params()
    draw_params = simple_draw_pro.SimpleDrawProCreateDrawing.generate_random_params()
    compound_params ={
        "new_file_name": markor_params["new_file_name"],
        "file1_name": markor_params["file1_name"],
        "file2_name": markor_params["file2_name"],
        "file3_name": markor_params["file3_name"],
        "file1_content": markor_params["file1_content"],
        "file2_content": markor_params["file2_content"],
        "file3_content": markor_params["file3_content"],
        "file_name_draw": draw_params["file_name"],
        "text_draw": "",

    }
    return compound_params

  def tear_down(self, env: interface.AsyncEnv) -> None:
    super().tear_down(env)
    self.markor_task.tear_down(env)


class MarkorsAndSimpleDrawProCreateDrawing(MarkorAndDraw):
  """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

  complexity = 3
  schema = {
      "type": "object",
      "properties": {
          "file_name_draw": {"type": "string"},
          "text_draw": {"type": "string"},

      },
      "required": ["file_name_draw",
                   "text_draw"],
  }
  template = (
      "then Create a new drawing in Simple Draw Pro. Name it {file_name_draw}. Save it in"
      " the Pictures folder within the sdk_gphone_x86_64 storage area."
  )

  def __init__(self, params: dict[str, Any]):
    """Initialize the task."""
    super().__init__(params)
    self.markor_task = markor.MarkorMergeNotes(
        params={
                 "new_file_name" : self.params["new_file_name"],

        })
    self.draw_task = simple_draw_pro.SimpleDrawProCreateDrawing(params={"file_name": self.params["file_name_draw"],
                                                                        "text": self.params["text_draw"]})



  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    self.markor_task.initialize_task(env)
    self.draw_task.initialize_task(env)


  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    markor_success = self.markor_task.is_successful(env)
    logging.info("Markor success: %s", markor_success)

    draw_success = self.draw_task.is_successful(env)
    logging.info("Draw success: %s", draw_success)

    return (markor_success + draw_success) / 2.0

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    markor_params = markor.M.generate_random_params()
    draw_params = simple_draw_pro.SimpleDrawProCreateDrawing.generate_random_params()
    compound_params ={
        "file_name_draw": draw_params["file_name"],
        "text_draw": "",

    }
    return compound_params

  def tear_down(self, env: interface.AsyncEnv) -> None:
    super().tear_down(env)
    self.markor_task.tear_down(env)


class MarkorChangeNoteContentAndSimpleDrawProCreateDrawing(MarkorAndDraw):
  """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

  complexity = 3
  schema = {
      "type": "object",
      "properties": {
          "original_name": {"type": "string"},
          "new_name": {"type": "string"},
          "updated_content": {"type": "string"},
          "file_name_draw": {"type": "string"},
          "text_draw": {"type": "string"},

      },
      "required": ["original_name", "new_name", "updated_content","file_name_draw",
                   "text_draw"],
  }
  template = (
      'Update the content of {original_name} to "{updated_content}" in Markor'
      " and change its name to {new_name}."
      "then Create a new drawing in Simple Draw Pro. Name it {file_name_draw}. Save it in"
      " the Pictures folder within the sdk_gphone_x86_64 storage area."
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
    self.draw_task = simple_draw_pro.SimpleDrawProCreateDrawing(params={"file_name": self.params["file_name_draw"],
                                                                        "text": self.params["text_draw"]})



  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    self.markor_task.initialize_task(env)
    self.draw_task.initialize_task(env)


  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    markor_success = self.markor_task.is_successful(env)
    logging.info("Markor success: %s", markor_success)

    draw_success = self.draw_task.is_successful(env)
    logging.info("Draw success: %s", draw_success)

    return (markor_success + draw_success) / 2.0

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    markor_params = markor.MarkorChangeNoteContent.generate_random_params()
    draw_params = simple_draw_pro.SimpleDrawProCreateDrawing.generate_random_params()
    compound_params ={
        "original_name": markor_params["original_name"],
        "new_name": markor_params["new_name"],
        "updated_content": markor_params["updated_content"],
        "file_name_draw": draw_params["file_name"],
        "text_draw": "",

    }
    return compound_params

  def tear_down(self, env: interface.AsyncEnv) -> None:
    super().tear_down(env)
    self.markor_task.tear_down(env)


class MarkorAddNoteHeaderAndSimpleDrawProCreateDrawing(MarkorAndDraw):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "original_name": {"type": "string"},
            "new_name": {"type": "string"},
            "header": {"type": "string"},
            "original_content": {"type": "string"},
            "file_name_draw": {"type": "string"},
            "text_draw": {"type": "string"},

        },
        "required": ["original_name", "new_name", "header", "original_content","file_name_draw",
                     "text_draw"],
    }
    template = (
        "Update the Markor note {original_name} by adding the following text,"
        ' along with a new blank line before the existing content: "{header}",'
        " and rename it to {new_name}."
        "then Create a new drawing in Simple Draw Pro. Name it {file_name_draw}. Save it in"
        " the Pictures folder within the sdk_gphone_x86_64 storage area."
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
        self.draw_task = simple_draw_pro.SimpleDrawProCreateDrawing(params={"file_name": self.params["file_name_draw"],
                                                                            "text": self.params["text_draw"]})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.draw_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        draw_success = self.draw_task.is_successful(env)
        logging.info("Draw success: %s", draw_success)

        return (markor_success + draw_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorAddNoteHeader.generate_random_params()
        draw_params = simple_draw_pro.SimpleDrawProCreateDrawing.generate_random_params()
        compound_params = {
            "original_name": markor_params["original_name"],
            "new_name": markor_params["new_name"],
            "header": markor_params["header"],
            "original_content": markor_params["original_content"],
            "file_name_draw": draw_params["file_name"],
            "text_draw": "",

        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)

class MarkorEditNoteAndSimpleDrawProCreateDrawing(MarkorAndDraw):
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
          "file_name_draw": {"type": "string"},
          "text_draw": {"type": "string"},

      },
      "required": ["file_name", "edit_type","file_name_draw",
                   "text_draw"],
  }
  @property
  def template(self) -> str:
    templates = {
        "header": (
            "Edit {file_name} in Markor. Add to the top of the note {header}"
            "then Create a new drawing in Simple Draw Pro. Name it {file_name_draw}. Save it in"
            " the Pictures folder within the sdk_gphone_x86_64 storage area."
        ),
        "footer": (
            "Edit {file_name} in Markor. Add to the bottom of the note {footer}"
            "then Create a new drawing in Simple Draw Pro. Name it {file_name_draw}. Save it in"
            " the Pictures folder within the sdk_gphone_x86_64 storage area."
        ),
        "replace": (
            "Edit {file_name} in Markor. Replace the text with {replace_text}"
            "then Create a new drawing in Simple Draw Pro. Name it {file_name_draw}. Save it in"
            " the Pictures folder within the sdk_gphone_x86_64 storage area."
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
    self.draw_task = simple_draw_pro.SimpleDrawProCreateDrawing(params={"file_name": self.params["file_name_draw"],
                                                                        "text": self.params["text_draw"]})



  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    self.markor_task.initialize_task(env)
    self.draw_task.initialize_task(env)


  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    markor_success = self.markor_task.is_successful(env)
    logging.info("Markor success: %s", markor_success)

    draw_success = self.draw_task.is_successful(env)
    logging.info("Draw success: %s", draw_success)

    return (markor_success + draw_success) / 2.0

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    markor_params = markor.MarkorEditNote.generate_random_params()
    draw_params = simple_draw_pro.SimpleDrawProCreateDrawing.generate_random_params()
    compound_params ={
        "file_name": markor_params["file_name"],
        "edit_type": markor_params["edit_type"],
        "file_name_draw": draw_params["file_name"],
        "text_draw": "",
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

class MarkorMoveNoteandCreateFolderAndSimpleDrawProCreateDrawing2(MarkorAndDraw):
  """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

  complexity = 3
  schema = {
      "type": "object",
      "properties": {
          "file_name": {"type": "string"},
          "file_name_draw": {"type": "string"},
          "source_folder": {"type": "string"},
          "destination_folder": {"type": "string"},
          "folder_name": {"type": "string"},
          "text": {"type": "string"},
      },
      "required": ["file_name", "source_folder", "destination_folder", "folder_name", "file_name_draw","text"],
  }
  template = (
      "In Markor, move the note {file_name} from {source_folder} to"
      " {destination_folder}. Also, create a new folder named {folder_name} in Markor."
      "then Create a new drawing in Simple Draw Pro. Name it {file_name_draw}. Save it in"
      " the Pictures folder within the sdk_gphone_x86_64 storage area."
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
    self.draw_task = simple_draw_pro.SimpleDrawProCreateDrawing(params={"file_name": self.params["file_name_draw"],
                                                                        "text": self.params["text"]})



  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    self.move_file_task.initialize_task(env)
    self.draw_task.initialize_task(env)


  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    markor_success = self.move_file_task.is_successful(env)
    logging.info("Markor success: %s", markor_success)

    draw_success = self.draw_task.is_successful(env)
    logging.info("Draw success: %s", draw_success)

    return (markor_success + draw_success) / 2.0

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    markor_params = markor.MarkorMoveNoteandCreateFolder.generate_random_params()
    draw_params = simple_draw_pro.SimpleDrawProCreateDrawing.generate_random_params()
    compound_params ={
        "file_name": markor_params["file_name"],
        "source_folder": markor_params["source_folder"],
        "destination_folder": markor_params["destination_folder"],
        "noise_candidates": _NOTE_TITLES,
        "folder_name": markor_params["folder_name"],
        "file_name_draw": draw_params["file_name"],
        "text": "",  # Unused.
    }
    return compound_params

  def tear_down(self, env: interface.AsyncEnv) -> None:
    super().tear_down(env)
    self.move_file_task.tear_down(env)

class MarkorCreateFolderthenCreateNoteAndSimpleDrawProCreateDrawing2(MarkorAndDraw):
  """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

  complexity = 3
  schema = {
      "type": "object",
      "properties": {
          "file_name": {"type": "string"},
          "file_name_draw": {"type": "string"},
          "folder_name": {"type": "string"},
          "text": {"type": "string"},
      },
      "required": ["folder_name", "file_name", "text","file_name_draw"],
  }
  template = (
      "Create a new folder in Markor named {folder_name} and then create a new note named {file_name} in this folder with the following text:"
      " {text}"
      "then Create a new drawing in Simple Draw Pro. Name it {file_name_draw}. Save it in"
      " the Pictures folder within the sdk_gphone_x86_64 storage area."
  )

  def __init__(self, params: dict[str, Any]):
    """Initialize the task."""
    super().__init__(params)
    self.markor_task = markor.MarkorCreateFolderthenCreateNote(
        params={ "file_name": self.params["file_name"],
                 "folder_name" : self.params["folder_name"],
                 "text": self.params["text"],

        })
    self.draw_task = simple_draw_pro.SimpleDrawProCreateDrawing(params={"file_name": self.params["file_name_draw"],
                                                                        "text": self.params["text_none"]})



  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    self.markor_task.initialize_task(env)
    self.draw_task.initialize_task(env)


  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    markor_success = self.markor_task.is_successful(env)
    logging.info("Markor success: %s", markor_success)

    draw_success = self.draw_task.is_successful(env)
    logging.info("Draw success: %s", draw_success)

    return (markor_success + draw_success) / 2.0

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    markor_params = markor.MarkorCreateFolderthenCreateNote.generate_random_params()
    draw_params = simple_draw_pro.SimpleDrawProCreateDrawing.generate_random_params()
    compound_params ={
        "file_name": markor_params["file_name"],
        "folder_name": markor_params["folder_name"],
        "text": markor_params["text"],
        "text_none": "",  # Unused.
        "file_name_draw": draw_params["file_name"],
    }
    return compound_params

  def tear_down(self, env: interface.AsyncEnv) -> None:
    super().tear_down(env)
    self.markor_task.tear_down(env)

class MarkorMoveNoteAndSimpleDrawProCreateDrawing2(MarkorAndDraw):
  """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

  complexity = 3
  schema = {
      "type": "object",
      "properties": {
          "file_name": {"type": "string"},
          "file_name_draw": {"type": "string"},
          "source_folder": {"type": "string"},
          "destination_folder": {"type": "string"},
          "text": {"type": "string"},
      },
      "required": ["file_name", "source_folder", "destination_folder" ,"file_name_draw","text"],
  }
  template = (
      "In Markor, move the note {file_name} from {source_folder} to"
      " {destination_folder}."
      "then Create a new drawing in Simple Draw Pro. Name it {file_name_draw}. Save it in"
      " the Pictures folder within the sdk_gphone_x86_64 storage area."
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
    self.draw_task = simple_draw_pro.SimpleDrawProCreateDrawing(params={"file_name": self.params["file_name_draw"],
                                                                        "text": self.params["text"]})



  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    self.move_file_task.initialize_task(env)
    self.draw_task.initialize_task(env)


  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    markor_success = self.move_file_task.is_successful(env)
    logging.info("Markor success: %s", markor_success)

    draw_success = self.draw_task.is_successful(env)
    logging.info("Draw success: %s", draw_success)

    return (markor_success + draw_success) / 2.0

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    markor_params = markor.MarkorMoveNote.generate_random_params()
    draw_params = simple_draw_pro.SimpleDrawProCreateDrawing.generate_random_params()
    compound_params ={
        "file_name": markor_params["file_name"],
        "source_folder": markor_params["source_folder"],
        "destination_folder": markor_params["destination_folder"],
        "noise_candidates": _NOTE_TITLES,
        "file_name_draw": draw_params["file_name"],
        "text": "",  # Unused.
    }
    return compound_params

  def tear_down(self, env: interface.AsyncEnv) -> None:
    super().tear_down(env)
    self.move_file_task.tear_down(env)


class MarkorCreateFolderAndSimpleDrawProCreateDrawing2(MarkorAndDraw):
  """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

  complexity = 3
  schema = {
      "type": "object",
      "properties": {
          "file_name_draw": {"type": "string"},
          "folder_name": {"type": "string"},
          "text": {"type": "string"},
      },
      "required": ["folder_name", "file_name_draw","text"],
  }
  template = (
      "Create a new folder in Markor named {folder_name}."
      "then Create a new drawing in Simple Draw Pro. Name it {file_name_draw}. Save it in"
      " the Pictures folder within the sdk_gphone_x86_64 storage area."
  )

  def __init__(self, params: dict[str, Any]):
    """Initialize the task."""
    super().__init__(params)
    self.markor_task = markor.MarkorCreateFolder(
        params={
                 "folder_name" : self.params["folder_name"],
        })
    self.draw_task = simple_draw_pro.SimpleDrawProCreateDrawing(params={"file_name": self.params["file_name_draw"],
                                                                        "text": self.params["text"]})



  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    self.markor_task.initialize_task(env)
    self.draw_task.initialize_task(env)


  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    markor_success = self.markor_task.is_successful(env)
    logging.info("Markor success: %s", markor_success)

    draw_success = self.draw_task.is_successful(env)
    logging.info("Draw success: %s", draw_success)

    return (markor_success + draw_success) / 2.0

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    markor_params = markor.MarkorCreateFolder.generate_random_params()
    draw_params = simple_draw_pro.SimpleDrawProCreateDrawing.generate_random_params()
    compound_params ={
        "folder_name": markor_params["folder_name"],
        "file_name_draw": draw_params["file_name"],
        "text": "",  # Unused.
    }
    return compound_params

  def tear_down(self, env: interface.AsyncEnv) -> None:
    super().tear_down(env)
    self.markor_task.tear_down(env)

class MarkorCreateNoteAndSimpleDrawProCreateDrawing2(MarkorAndDraw):
  """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

  complexity = 3
  schema = {
      "type": "object",
      "properties": {
          "file_name": {"type": "string"},
          "file_name_draw": {"type": "string"},
          "text_draw": {"type": "string"},
          "text": {"type": "string"},
      },
      "required": ["file_name_draw","text","text_draw"],
  }
  template = (
      "Create a new note in Markor named {file_name} with the following text:"
      " {text}"
      "then Create a new drawing in Simple Draw Pro. Name it {file_name_draw}. Save it in"
      " the Pictures folder within the sdk_gphone_x86_64 storage area."
  )

  def __init__(self, params: dict[str, Any]):
    """Initialize the task."""
    super().__init__(params)
    self.markor_task = markor.MarkorCreateNote(
        params={
                 "file_name" : self.params["file_name"],
                 "text": self.params["text"]
        })
    self.draw_task = simple_draw_pro.SimpleDrawProCreateDrawing(params={"file_name": self.params["file_name_draw"],
                                                                        "text": self.params["text_draw"]})



  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    self.markor_task.initialize_task(env)
    self.draw_task.initialize_task(env)


  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    markor_success = self.markor_task.is_successful(env)
    logging.info("Markor success: %s", markor_success)

    draw_success = self.draw_task.is_successful(env)
    logging.info("Draw success: %s", draw_success)

    return (markor_success + draw_success) / 2.0

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    markor_params = markor.MarkorCreateNote.generate_random_params()
    draw_params = simple_draw_pro.SimpleDrawProCreateDrawing.generate_random_params()
    compound_params ={
        "file_name": markor_params["file_name"],
        "file_name_draw": draw_params["file_name"],
        "text_draw": "",
        "text":  markor_params["text"],
    }
    return compound_params

  def tear_down(self, env: interface.AsyncEnv) -> None:
    super().tear_down(env)
    self.markor_task.tear_down(env)


class MarkorCreateNoteFromClipboardAndSimpleDrawProCreateDrawing2(MarkorAndDraw):
  """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

  complexity = 3
  schema = {
      "type": "object",
      "properties": {
          "file_name": {"type": "string"},
          "file_name_draw": {"type": "string"},
          "text_draw": {"type": "string"},
          "file_content": {"type": "string"},
      },
      "required": ["file_name","file_name_draw","file_content","text_draw"],
  }
  template = (
      "Create a note in Markor named {file_name}. Perform a paste operation in"
      " the note and save the note."
      "then Create a new drawing in Simple Draw Pro. Name it {file_name_draw}. Save it in"
      " the Pictures folder within the sdk_gphone_x86_64 storage area."
  )

  def __init__(self, params: dict[str, Any]):
    """Initialize the task."""
    super().__init__(params)
    self.markor_task = markor.MarkorCreateNoteFromClipboard(
        params={
                 "file_name" : self.params["file_name"],
                 "file_content": self.params["file_content"]
        })
    self.draw_task = simple_draw_pro.SimpleDrawProCreateDrawing(params={"file_name": self.params["file_name_draw"],
                                                                        "text": self.params["text_draw"]})



  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    self.markor_task.initialize_task(env)
    self.draw_task.initialize_task(env)


  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    markor_success = self.markor_task.is_successful(env)
    logging.info("Markor success: %s", markor_success)

    draw_success = self.draw_task.is_successful(env)
    logging.info("Draw success: %s", draw_success)

    return (markor_success + draw_success) / 2.0

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    markor_params = markor.MarkorCreateNoteFromClipboard.generate_random_params()
    draw_params = simple_draw_pro.SimpleDrawProCreateDrawing.generate_random_params()
    compound_params ={
        "file_name": markor_params["file_name"],
        "file_name_draw": draw_params["file_name"],
        "text_draw": "",
        "file_content": markor_params["file_content"],
    }
    return compound_params

  def tear_down(self, env: interface.AsyncEnv) -> None:
    super().tear_down(env)
    self.markor_task.tear_down(env)


class MarkorMergeNotesAndSimpleDrawProCreateDrawing2(MarkorAndDraw):
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
          "file_name_draw": {"type": "string"},
          "text_draw": {"type": "string"},

      },
      "required": [   "file1_name",
          "file2_name",
          "file3_name",
          "new_file_name",
          "file1_content",
          "file2_content",
          "file3_content","file_name_draw","text_draw"],
  }
  template = (
      "Merge the contents of Markor notes {file1_name}, {file2_name} and"
      " {file3_name} (in the same order) into a new Markor note named"
      " {new_file_name} and save it. Add a new line between the content of each"
      " note."
      "then Create a new drawing in Simple Draw Pro. Name it {file_name_draw}. Save it in"
      " the Pictures folder within the sdk_gphone_x86_64 storage area."
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
    self.draw_task = simple_draw_pro.SimpleDrawProCreateDrawing(params={"file_name": self.params["file_name_draw"],
                                                                        "text": self.params["text_draw"]})



  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    self.markor_task.initialize_task(env)
    self.draw_task.initialize_task(env)


  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    markor_success = self.markor_task.is_successful(env)
    logging.info("Markor success: %s", markor_success)

    draw_success = self.draw_task.is_successful(env)
    logging.info("Draw success: %s", draw_success)

    return (markor_success + draw_success) / 2.0

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    markor_params = markor.MarkorMergeNotes.generate_random_params()
    draw_params = simple_draw_pro.SimpleDrawProCreateDrawing.generate_random_params()
    compound_params ={
        "new_file_name": markor_params["new_file_name"],
        "file1_name": markor_params["file1_name"],
        "file2_name": markor_params["file2_name"],
        "file3_name": markor_params["file3_name"],
        "file1_content": markor_params["file1_content"],
        "file2_content": markor_params["file2_content"],
        "file3_content": markor_params["file3_content"],
        "file_name_draw": draw_params["file_name"],
        "text_draw": "",

    }
    return compound_params

  def tear_down(self, env: interface.AsyncEnv) -> None:
    super().tear_down(env)
    self.markor_task.tear_down(env)


class MarkorsAndSimpleDrawProCreateDrawing2(MarkorAndDraw):
  """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

  complexity = 3
  schema = {
      "type": "object",
      "properties": {
          "file_name_draw": {"type": "string"},
          "text_draw": {"type": "string"},

      },
      "required": ["file_name_draw",
                   "text_draw"],
  }
  template = (
      "then Create a new drawing in Simple Draw Pro. Name it {file_name_draw}. Save it in"
      " the Pictures folder within the sdk_gphone_x86_64 storage area."
  )

  def __init__(self, params: dict[str, Any]):
    """Initialize the task."""
    super().__init__(params)
    self.markor_task = markor.MarkorMergeNotes(
        params={
                 "new_file_name" : self.params["new_file_name"],

        })
    self.draw_task = simple_draw_pro.SimpleDrawProCreateDrawing(params={"file_name": self.params["file_name_draw"],
                                                                        "text": self.params["text_draw"]})



  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    self.markor_task.initialize_task(env)
    self.draw_task.initialize_task(env)


  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    markor_success = self.markor_task.is_successful(env)
    logging.info("Markor success: %s", markor_success)

    draw_success = self.draw_task.is_successful(env)
    logging.info("Draw success: %s", draw_success)

    return (markor_success + draw_success) / 2.0

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    markor_params = markor.M.generate_random_params()
    draw_params = simple_draw_pro.SimpleDrawProCreateDrawing.generate_random_params()
    compound_params ={
        "file_name_draw": draw_params["file_name"],
        "text_draw": "",

    }
    return compound_params

  def tear_down(self, env: interface.AsyncEnv) -> None:
    super().tear_down(env)
    self.markor_task.tear_down(env)


class MarkorChangeNoteContentAndSimpleDrawProCreateDrawing2(MarkorAndDraw):
  """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

  complexity = 3
  schema = {
      "type": "object",
      "properties": {
          "original_name": {"type": "string"},
          "new_name": {"type": "string"},
          "updated_content": {"type": "string"},
          "file_name_draw": {"type": "string"},
          "text_draw": {"type": "string"},

      },
      "required": ["original_name", "new_name", "updated_content","file_name_draw",
                   "text_draw"],
  }
  template = (
      'Update the content of {original_name} to "{updated_content}" in Markor'
      " and change its name to {new_name}."
      "then Create a new drawing in Simple Draw Pro. Name it {file_name_draw}. Save it in"
      " the Pictures folder within the sdk_gphone_x86_64 storage area."
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
    self.draw_task = simple_draw_pro.SimpleDrawProCreateDrawing(params={"file_name": self.params["file_name_draw"],
                                                                        "text": self.params["text_draw"]})



  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    self.markor_task.initialize_task(env)
    self.draw_task.initialize_task(env)


  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    markor_success = self.markor_task.is_successful(env)
    logging.info("Markor success: %s", markor_success)

    draw_success = self.draw_task.is_successful(env)
    logging.info("Draw success: %s", draw_success)

    return (markor_success + draw_success) / 2.0

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    markor_params = markor.MarkorChangeNoteContent.generate_random_params()
    draw_params = simple_draw_pro.SimpleDrawProCreateDrawing.generate_random_params()
    compound_params ={
        "original_name": markor_params["original_name"],
        "new_name": markor_params["new_name"],
        "updated_content": markor_params["updated_content"],
        "file_name_draw": draw_params["file_name"],
        "text_draw": "",

    }
    return compound_params

  def tear_down(self, env: interface.AsyncEnv) -> None:
    super().tear_down(env)
    self.markor_task.tear_down(env)


class MarkorAddNoteHeaderAndSimpleDrawProCreateDrawing2(MarkorAndDraw):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "original_name": {"type": "string"},
            "new_name": {"type": "string"},
            "header": {"type": "string"},
            "original_content": {"type": "string"},
            "file_name_draw": {"type": "string"},
            "text_draw": {"type": "string"},

        },
        "required": ["original_name", "new_name", "header", "original_content","file_name_draw",
                     "text_draw"],
    }
    template = (
        "Update the Markor note {original_name} by adding the following text,"
        ' along with a new blank line before the existing content: "{header}",'
        " and rename it to {new_name}."
        "then Create a new drawing in Simple Draw Pro. Name it {file_name_draw}. Save it in"
        " the Pictures folder within the sdk_gphone_x86_64 storage area."
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
        self.draw_task = simple_draw_pro.SimpleDrawProCreateDrawing(params={"file_name": self.params["file_name_draw"],
                                                                            "text": self.params["text_draw"]})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.draw_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        draw_success = self.draw_task.is_successful(env)
        logging.info("Draw success: %s", draw_success)

        return (markor_success + draw_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorAddNoteHeader.generate_random_params()
        draw_params = simple_draw_pro.SimpleDrawProCreateDrawing.generate_random_params()
        compound_params = {
            "original_name": markor_params["original_name"],
            "new_name": markor_params["new_name"],
            "header": markor_params["header"],
            "original_content": markor_params["original_content"],
            "file_name_draw": draw_params["file_name"],
            "text_draw": "",

        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)

class MarkorEditNoteAndSimpleDrawProCreateDrawing2(MarkorAndDraw):
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
          "file_name_draw": {"type": "string"},
          "text_draw": {"type": "string"},

      },
      "required": ["file_name", "edit_type","file_name_draw",
                   "text_draw"],
  }
  @property
  def template(self) -> str:
    templates = {
        "header": (
            "Edit {file_name} in Markor. Add to the top of the note {header}"
            "then Create a new drawing in Simple Draw Pro. Name it {file_name_draw}. Save it in"
            " the Pictures folder within the sdk_gphone_x86_64 storage area."
        ),
        "footer": (
            "Edit {file_name} in Markor. Add to the bottom of the note {footer}"
            "then Create a new drawing in Simple Draw Pro. Name it {file_name_draw}. Save it in"
            " the Pictures folder within the sdk_gphone_x86_64 storage area."
        ),
        "replace": (
            "Edit {file_name} in Markor. Replace the text with {replace_text}"
            "then Create a new drawing in Simple Draw Pro. Name it {file_name_draw}. Save it in"
            " the Pictures folder within the sdk_gphone_x86_64 storage area."
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
    self.draw_task = simple_draw_pro.SimpleDrawProCreateDrawing(params={"file_name": self.params["file_name_draw"],
                                                                        "text": self.params["text_draw"]})



  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    self.markor_task.initialize_task(env)
    self.draw_task.initialize_task(env)


  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    markor_success = self.markor_task.is_successful(env)
    logging.info("Markor success: %s", markor_success)

    draw_success = self.draw_task.is_successful(env)
    logging.info("Draw success: %s", draw_success)

    return (markor_success + draw_success) / 2.0

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    markor_params = markor.MarkorEditNote.generate_random_params()
    draw_params = simple_draw_pro.SimpleDrawProCreateDrawing.generate_random_params()
    compound_params ={
        "file_name": markor_params["file_name"],
        "edit_type": markor_params["edit_type"],
        "file_name_draw": draw_params["file_name"],
        "text_draw": "",
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
