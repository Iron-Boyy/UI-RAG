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
from android_world.task_evals.single import audio_recorder
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


class MarkorAndAudioAndDraw(task_eval.TaskEval):
  app_names = ("markor","audio recorder","simple draw pro")

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    file_utils.clear_directory(device_constants.MARKOR_DATA, env.base_env)

  def tear_down(self, env: interface.AsyncEnv) -> None:
    super().tear_down(env)
    file_utils.clear_directory(device_constants.MARKOR_DATA, env.base_env)


class MarkorMoveNoteandCreateFolderAndAudioRecorderRecordAudio(MarkorAndAudioAndDraw):
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
       "then Record an audio clip using Audio Recorder app and save it."
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
        self.audio_task = audio_recorder.AudioRecorderRecordAudio(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.move_file_task.initialize_task(env)
        self.audio_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.move_file_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        audio_success = self.audio_task.is_successful(env)
        logging.info("camera success: %s", audio_success)

        return (markor_success + audio_success) / 2.0

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


class MarkorCreateFolderthenCreateNoteAndAudioRecorderRecordAudio(MarkorAndAudioAndDraw):
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
        "then Record an audio clip using Audio Recorder app and save it. ."

    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.markor_task = markor.MarkorCreateFolderthenCreateNote(
            params={"file_name": self.params["file_name"],
                    "folder_name": self.params["folder_name"],
                    "text": self.params["text"],

                    })
        self.audio_task = audio_recorder.AudioRecorderRecordAudio(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.audio_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        audio_success = self.audio_task.is_successful(env)
        logging.info("camera success: %s", audio_success)

        return (markor_success + audio_success) / 2.0

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


class MarkorMoveNoteAndAudioRecorderRecordAudio(MarkorAndAudioAndDraw):
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
        "then Record an audio clip using Audio Recorder app and save it.."
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
        self.audio_task = audio_recorder.AudioRecorderRecordAudio(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.move_file_task.initialize_task(env)
        self.audio_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.move_file_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        audio_success = self.audio_task.is_successful(env)
        logging.info("camera success: %s", audio_success)

        return (markor_success + audio_success) / 2.0

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


class MarkorCreateFolderAndAudioRecorderRecordAudio(MarkorAndAudioAndDraw):
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
        "then Record an audio clip using Audio Recorder app and save it.."
    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.markor_task = markor.MarkorCreateFolder(
            params={
                "folder_name": self.params["folder_name"],
            })
        self.audio_task = audio_recorder.AudioRecorderRecordAudio(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.audio_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        audio_success = self.audio_task.is_successful(env)
        logging.info("camera success: %s", audio_success)

        return (markor_success + audio_success) / 2.0

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


class MarkorCreateNoteAndAudioRecorderRecordAudio(MarkorAndAudioAndDraw):
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
        "then Record an audio clip using Audio Recorder app and save it.."
    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.markor_task = markor.MarkorCreateNote(
            params={
                "file_name": self.params["file_name"],
                "text": self.params["text"]
            })
        self.audio_task = audio_recorder.AudioRecorderRecordAudio(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.audio_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        audio_success = self.audio_task.is_successful(env)
        logging.info("camera success: %s", audio_success)

        return (markor_success + audio_success) / 2.0

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


class MarkorCreateNoteFromClipboardAndAudioRecorderRecordAudio(MarkorAndAudioAndDraw):
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
        "then Record an audio clip using Audio Recorder app and save it.."
    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.markor_task = markor.MarkorCreateNoteFromClipboard(
            params={
                "file_name": self.params["file_name"],
                "file_content": self.params["file_content"]
            })
        self.audio_task = audio_recorder.AudioRecorderRecordAudio(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.audio_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        audio_success = self.audio_task.is_successful(env)
        logging.info("camera success: %s", audio_success)

        return (markor_success + audio_success) / 2.0

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


class MarkorMergeNotesAndAudioRecorderRecordAudio(MarkorAndAudioAndDraw):
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
        "then Record an audio clip using Audio Recorder app and save it.."
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
        self.audio_task = audio_recorder.AudioRecorderRecordAudio(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.audio_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        audio_success = self.audio_task.is_successful(env)
        logging.info("camera success: %s", audio_success)

        return (markor_success + audio_success) / 2.0

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


class MarkorChangeNoteContentAndAudioRecorderRecordAudio(MarkorAndAudioAndDraw):
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
        "then Record an audio clip using Audio Recorder app and save it.."
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
        self.audio_task = audio_recorder.AudioRecorderRecordAudio(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.audio_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        audio_success = self.audio_task.is_successful(env)
        logging.info("camera success: %s", audio_success)

        return (markor_success + audio_success) / 2.0

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


class MarkorAddNoteHeaderAndAudioRecorderRecordAudio(MarkorAndAudioAndDraw):
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
        "then Record an audio clip using Audio Recorder app and save it.."
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
        self.audio_task = audio_recorder.AudioRecorderRecordAudio(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.audio_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        audio_success = self.audio_task.is_successful(env)
        logging.info("camera success: %s", audio_success)

        return (markor_success + audio_success) / 2.0

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


class MarkorEditNoteAndAudioRecorderRecordAudio(MarkorAndAudioAndDraw):
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
                "then Record an audio clip using Audio Recorder app and save it.."
            ),
            "footer": (
                "Edit {file_name} in Markor. Add to the bottom of the note {footer}"
                "then Record an audio clip using Audio Recorder app and save it.."
            ),
            "replace": (
                "Edit {file_name} in Markor. Replace the text with {replace_text}"
                "then Record an audio clip using Audio Recorder app and save it.."
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
        self.audio_task = audio_recorder.AudioRecorderRecordAudio(params={})

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.audio_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        audio_success = self.audio_task.is_successful(env)
        logging.info("camera success: %s", audio_success)

        return (markor_success + audio_success) / 2.0

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



class MarkorMoveNoteandCreateFolderAndAudioRecorderRecordAudioWithSettings(MarkorAndAudioAndDraw):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "file_name": {"type": "string"},
            "source_folder": {"type": "string"},
            "destination_folder": {"type": "string"},
            "folder_name": {"type": "string"},
            "sample_rate": {"type": "string"},
            "bit_rate": {"type": "string"},
        },
        "required": ["file_name", "source_folder", "destination_folder", "folder_name"],
    }
    template = (
        "In Markor, move the note {file_name} from {source_folder} to"
        " {destination_folder}. Also, create a new folder named {folder_name} in Markor."
          'Record an audio clip with Sample rate "{sample_rate}" '
          'and Bitrate "{bit_rate}" using Audio Recorder app and save it.'
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
        self.audio_task = audio_recorder.AudioRecorderRecordAudioWithSettings(params={
            "sample_rate": self.params["sample_rate"],
            "bit_rate": self.params["bit_rate"]
        })

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.move_file_task.initialize_task(env)
        self.audio_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.move_file_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        audio_success = self.audio_task.is_successful(env)
        logging.info("camera success: %s", audio_success)

        return (markor_success + audio_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorMoveNoteandCreateFolder.generate_random_params()
        audio_params = audio_recorder.AudioRecorderRecordAudioWithSettings.generate_random_params()
        compound_params = {
            "file_name": markor_params["file_name"],
            "source_folder": markor_params["source_folder"],
            "destination_folder": markor_params["destination_folder"],
            "noise_candidates": _NOTE_TITLES,
            "folder_name": markor_params["folder_name"],
            "sample_rate":audio_params["sample_rate"],
            "bit_rate": audio_params["bit_rate"]
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.move_file_task.tear_down(env)


class MarkorCreateFolderthenCreateNoteAndAudioRecorderRecordAudioWithSettings(MarkorAndAudioAndDraw):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "file_name": {"type": "string"},
            "folder_name": {"type": "string"},
            "sample_rate": {"type": "string"},
            "bit_rate": {"type": "string"},

        },
        "required": ["folder_name", "file_name", ],
    }
    template = (
        "Create a new folder in Markor named {folder_name} and then create a new note named {file_name} in this folder with the following text:"
        " {text}"
'Record an audio clip with Sample rate "{sample_rate}" '
'and Bitrate "{bit_rate}" using Audio Recorder app and save it.'

    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.markor_task = markor.MarkorCreateFolderthenCreateNote(
            params={"file_name": self.params["file_name"],
                    "folder_name": self.params["folder_name"],
                    "text": self.params["text"],

                    })
        self.audio_task = audio_recorder.AudioRecorderRecordAudioWithSettings(params={
            "sample_rate": self.params["sample_rate"],
            "bit_rate": self.params["bit_rate"]
        })

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.audio_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        audio_success = self.audio_task.is_successful(env)
        logging.info("camera success: %s", audio_success)

        return (markor_success + audio_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorCreateFolderthenCreateNote.generate_random_params()
        audio_params = audio_recorder.AudioRecorderRecordAudioWithSettings.generate_random_params()
        compound_params = {
            "file_name": markor_params["file_name"],
            "folder_name": markor_params["folder_name"],
            "text": markor_params["text"],
            "sample_rate": audio_params["sample_rate"],
            "bit_rate": audio_params["bit_rate"]
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorMoveNoteAndAudioRecorderRecordAudioWithSettings(MarkorAndAudioAndDraw):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "file_name": {"type": "string"},
            "source_folder": {"type": "string"},
            "destination_folder": {"type": "string"},
            "sample_rate": {"type": "string"},
            "bit_rate": {"type": "string"},

        },
        "required": ["file_name", "source_folder", "destination_folder"],
    }
    template = (
        "In Markor, move the note {file_name} from {source_folder} to"
        " {destination_folder}."
        'Record an audio clip with Sample rate "{sample_rate}" '
        'and Bitrate "{bit_rate}" using Audio Recorder app and save it.'
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
        self.audio_task = audio_recorder.AudioRecorderRecordAudioWithSettings(params={
            "sample_rate": self.params["sample_rate"],
            "bit_rate": self.params["bit_rate"]
        })

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.move_file_task.initialize_task(env)
        self.audio_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.move_file_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        audio_success = self.audio_task.is_successful(env)
        logging.info("camera success: %s", audio_success)

        return (markor_success + audio_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorMoveNote.generate_random_params()
        audio_params = audio_recorder.AudioRecorderRecordAudioWithSettings.generate_random_params()
        compound_params = {
            "file_name": markor_params["file_name"],
            "source_folder": markor_params["source_folder"],
            "destination_folder": markor_params["destination_folder"],
            "noise_candidates": _NOTE_TITLES,
            "sample_rate": audio_params["sample_rate"],
            "bit_rate": audio_params["bit_rate"]
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.move_file_task.tear_down(env)


class MarkorCreateFolderAndAudioRecorderRecordAudioWithSettings(MarkorAndAudioAndDraw):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "folder_name": {"type": "string"},
            "sample_rate": {"type": "string"},
            "bit_rate": {"type": "string"},
        },
        "required": ["folder_name"],
    }
    template = (
        "Create a new folder in Markor named {folder_name}."
        'Record an audio clip with Sample rate "{sample_rate}" '
        'and Bitrate "{bit_rate}" using Audio Recorder app and save it.'
    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.markor_task = markor.MarkorCreateFolder(
            params={
                "folder_name": self.params["folder_name"],
            })
        self.audio_task = audio_recorder.AudioRecorderRecordAudioWithSettings(params={
            "sample_rate": self.params["sample_rate"],
            "bit_rate": self.params["bit_rate"]
        })

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.audio_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        audio_success = self.audio_task.is_successful(env)
        logging.info("camera success: %s", audio_success)

        return (markor_success + audio_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorCreateFolder.generate_random_params()
        audio_params = audio_recorder.AudioRecorderRecordAudioWithSettings.generate_random_params()
        compound_params = {
            "folder_name": markor_params["folder_name"],
            "sample_rate": audio_params["sample_rate"],
            "bit_rate": audio_params["bit_rate"]
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorCreateNoteAndAudioRecorderRecordAudioWithSettings(MarkorAndAudioAndDraw):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "file_name": {"type": "string"},
            "text": {"type": "string"},
            "sample_rate": {"type": "string"},
            "bit_rate": {"type": "string"},
        },
        "required": ["file_name", "text"],
    }
    template = (
        "Create a new note in Markor named {file_name} with the following text:"
        " {text}"
        'Then Record an audio clip with Sample rate "{sample_rate}" '
        'and Bitrate "{bit_rate}" using Audio Recorder app and save it.'
    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.markor_task = markor.MarkorCreateNote(
            params={
                "file_name": self.params["file_name"],
                "text": self.params["text"]
            })
        self.audio_task = audio_recorder.AudioRecorderRecordAudioWithSettings(params={
            "sample_rate": self.params["sample_rate"],
            "bit_rate": self.params["bit_rate"]
        })

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.audio_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        audio_success = self.audio_task.is_successful(env)
        logging.info("camera success: %s", audio_success)

        return (markor_success + audio_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorCreateNote.generate_random_params()
        audio_params = audio_recorder.AudioRecorderRecordAudioWithSettings.generate_random_params()
        compound_params = {
            "file_name": markor_params["file_name"],
            "text": markor_params["text"],
            "sample_rate": audio_params["sample_rate"],
            "bit_rate": audio_params["bit_rate"]
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorCreateNoteFromClipboardAndAudioRecorderRecordAudioWithSettings(MarkorAndAudioAndDraw):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "file_name": {"type": "string"},
            "file_content": {"type": "string"},
            "sample_rate": {"type": "string"},
            "bit_rate": {"type": "string"},
        },
        "required": ["file_name", "file_content"],
    }
    template = (
        "Create a note in Markor named {file_name}. Perform a paste operation in"
        " the note and save the note."
        'then Record an audio clip with Sample rate "{sample_rate}" '
        'and Bitrate "{bit_rate}" using Audio Recorder app and save it.'
    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.markor_task = markor.MarkorCreateNoteFromClipboard(
            params={
                "file_name": self.params["file_name"],
                "file_content": self.params["file_content"]
            })
        self.audio_task = audio_recorder.AudioRecorderRecordAudioWithSettings(params={
            "sample_rate": self.params["sample_rate"],
            "bit_rate": self.params["bit_rate"]
        })

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.audio_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        audio_success = self.audio_task.is_successful(env)
        logging.info("camera success: %s", audio_success)

        return (markor_success + audio_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorCreateNoteFromClipboard.generate_random_params()
        audio_params = audio_recorder.AudioRecorderRecordAudioWithSettings.generate_random_params()
        compound_params = {
            "file_name": markor_params["file_name"],
            "file_content": markor_params["file_content"],
            "sample_rate": audio_params["sample_rate"],
            "bit_rate": audio_params["bit_rate"]
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorMergeNotesAndAudioRecorderRecordAudioWithSettings(MarkorAndAudioAndDraw):
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
            "sample_rate": {"type": "string"},
            "bit_rate": {"type": "string"},

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
        'then Record an audio clip with Sample rate "{sample_rate}" '
        'and Bitrate "{bit_rate}" using Audio Recorder app and save it.'
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
        self.audio_task = audio_recorder.AudioRecorderRecordAudioWithSettings(params={
            "sample_rate": self.params["sample_rate"],
            "bit_rate": self.params["bit_rate"]
        })

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.audio_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        audio_success = self.audio_task.is_successful(env)
        logging.info("camera success: %s", audio_success)

        return (markor_success + audio_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorMergeNotes.generate_random_params()
        audio_params = audio_recorder.AudioRecorderRecordAudioWithSettings.generate_random_params()
        compound_params = {
            "new_file_name": markor_params["new_file_name"],
            "file1_name": markor_params["file1_name"],
            "file2_name": markor_params["file2_name"],
            "file3_name": markor_params["file3_name"],
            "file1_content": markor_params["file1_content"],
            "file2_content": markor_params["file2_content"],
            "file3_content": markor_params["file3_content"],
            "sample_rate": audio_params["sample_rate"],
            "bit_rate": audio_params["bit_rate"]
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorChangeNoteContentAndAudioRecorderRecordAudioWithSettings(MarkorAndAudioAndDraw):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "original_name": {"type": "string"},
            "new_name": {"type": "string"},
            "updated_content": {"type": "string"},
            "sample_rate": {"type": "string"},
            "bit_rate": {"type": "string"},

        },
        "required": ["original_name", "new_name", "updated_content"],
    }
    template = (
        'Update the content of {original_name} to "{updated_content}" in Markor'
        " and change its name to {new_name}."
        'then Record an audio clip with Sample rate "{sample_rate}" '
        'and Bitrate "{bit_rate}" using Audio Recorder app and save it.'
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
        self.audio_task = audio_recorder.AudioRecorderRecordAudioWithSettings(params={
            "sample_rate": self.params["sample_rate"],
            "bit_rate": self.params["bit_rate"]
        })

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.audio_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        audio_success = self.audio_task.is_successful(env)
        logging.info("camera success: %s", audio_success)

        return (markor_success + audio_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorChangeNoteContent.generate_random_params()
        audio_params = audio_recorder.AudioRecorderRecordAudioWithSettings.generate_random_params()
        compound_params = {
            "original_name": markor_params["original_name"],
            "new_name": markor_params["new_name"],
            "updated_content": markor_params["updated_content"],
            "sample_rate": audio_params["sample_rate"],
            "bit_rate": audio_params["bit_rate"]

        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorAddNoteHeaderAndAudioRecorderRecordAudioWithSettings(MarkorAndAudioAndDraw):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "original_name": {"type": "string"},
            "new_name": {"type": "string"},
            "header": {"type": "string"},
            "original_content": {"type": "string"},
            "sample_rate": {"type": "string"},
            "bit_rate": {"type": "string"},

        },
        "required": ["original_name", "new_name", "header", "original_content"],
    }
    template = (
        "Update the Markor note {original_name} by adding the following text,"
        ' along with a new blank line before the existing content: "{header}",'
        " and rename it to {new_name}."
        'then Record an audio clip with Sample rate "{sample_rate}" '
        'and Bitrate "{bit_rate}" using Audio Recorder app and save it.'
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
        self.audio_task = audio_recorder.AudioRecorderRecordAudioWithSettings(params={
            "sample_rate": self.params["sample_rate"],
            "bit_rate": self.params["bit_rate"]
        })

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.audio_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        audio_success = self.audio_task.is_successful(env)
        logging.info("camera success: %s", audio_success)

        return (markor_success + audio_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorAddNoteHeader.generate_random_params()
        audio_params = audio_recorder.AudioRecorderRecordAudioWithSettings.generate_random_params()
        compound_params = {
            "original_name": markor_params["original_name"],
            "new_name": markor_params["new_name"],
            "header": markor_params["header"],
            "original_content": markor_params["original_content"],
            "sample_rate": audio_params["sample_rate"],
            "bit_rate": audio_params["bit_rate"]

        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorEditNoteAndAudioRecorderRecordAudioWithSettings(MarkorAndAudioAndDraw):
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
            "sample_rate": {"type": "string"},
            "bit_rate": {"type": "string"},

        },
        "required": ["file_name", "edit_type"],
    }

    @property
    def template(self) -> str:
        templates = {
            "header": (
                "Edit {file_name} in Markor. Add to the top of the note {header}"
                'then Record an audio clip with Sample rate "{sample_rate}" '
                'and Bitrate "{bit_rate}" using Audio Recorder app and save it.'
            ),
            "footer": (
                "Edit {file_name} in Markor. Add to the bottom of the note {footer}"
                'then Record an audio clip with Sample rate "{sample_rate}" '
                'and Bitrate "{bit_rate}" using Audio Recorder app and save it.'
            ),
            "replace": (
                "Edit {file_name} in Markor. Replace the text with {replace_text}"
                'then Record an audio clip with Sample rate "{sample_rate}" '
                'and Bitrate "{bit_rate}" using Audio Recorder app and save it.'
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
        self.audio_task = audio_recorder.AudioRecorderRecordAudioWithSettings(params={
            "sample_rate": self.params["sample_rate"],
            "bit_rate": self.params["bit_rate"]
        })

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.audio_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        audio_success = self.audio_task.is_successful(env)
        logging.info("camera success: %s", audio_success)

        return (markor_success + audio_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorEditNote.generate_random_params()
        audio_params = audio_recorder.AudioRecorderRecordAudioWithSettings.generate_random_params()
        compound_params = {
            "file_name": markor_params["file_name"],
            "edit_type": markor_params["edit_type"],
            "sample_rate": audio_params["sample_rate"],
            "bit_rate": audio_params["bit_rate"]

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





class MarkorMoveNoteandCreateFolderAndAudioRecorderRecordAudioWithFileName(MarkorAndAudioAndDraw):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "file_name": {"type": "string"},
            "source_folder": {"type": "string"},
            "destination_folder": {"type": "string"},
            "folder_name": {"type": "string"},
          "file_name_audio": {"type": "string"},
          "text_audio": {"type": "string"},
        },
        "required": ["file_name", "source_folder", "destination_folder", "folder_name"],
    }
    template = (
        "In Markor, move the note {file_name} from {source_folder} to"
        " {destination_folder}. Also, create a new folder named {folder_name} in Markor."
        'then Record an audio clip and save it with name "{file_name}" using Audio'
      " Recorder app."
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
        self.audio_task = audio_recorder.AudioRecorderRecordAudioWithFileName(params={
                        "file_name": self.params["file_name_audio"],
                        "text": self.params["text_audio"]
        })

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.move_file_task.initialize_task(env)
        self.audio_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.move_file_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        audio_success = self.audio_task.is_successful(env)
        logging.info("camera success: %s", audio_success)

        return (markor_success + audio_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorMoveNoteandCreateFolder.generate_random_params()
        audio_params = audio_recorder.AudioRecorderRecordAudioWithFileName.generate_random_params()
        compound_params = {
            "file_name": markor_params["file_name"],
            "source_folder": markor_params["source_folder"],
            "destination_folder": markor_params["destination_folder"],
            "noise_candidates": _NOTE_TITLES,
            "folder_name": markor_params["folder_name"],
            "file_name_audio": audio_params["file_name"],
            "text_audio": "",
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.move_file_task.tear_down(env)


class MarkorCreateFolderthenCreateNoteAndAudioRecorderRecordAudioWithFileName(MarkorAndAudioAndDraw):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "file_name": {"type": "string"},
            "folder_name": {"type": "string"},
          "file_name_audio": {"type": "string"},
          "text_audio": {"type": "string"},

        },
        "required": ["folder_name", "file_name", ],
    }
    template = (
        "Create a new folder in Markor named {folder_name} and then create a new note named {file_name} in this folder with the following text:"
        " {text}"
              'then Record an audio clip and save it with name "{file_name}" using Audio'
      " Recorder app."

    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.markor_task = markor.MarkorCreateFolderthenCreateNote(
            params={"file_name": self.params["file_name"],
                    "folder_name": self.params["folder_name"],
                    "text": self.params["text"],

                    })
        self.audio_task = audio_recorder.AudioRecorderRecordAudioWithFileName(params={
"file_name": self.params["file_name_audio"],
                                                                        "text": self.params["text_audio"]
        })

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.audio_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        audio_success = self.audio_task.is_successful(env)
        logging.info("camera success: %s", audio_success)

        return (markor_success + audio_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorCreateFolderthenCreateNote.generate_random_params()
        audio_params = audio_recorder.AudioRecorderRecordAudioWithFileName.generate_random_params()
        compound_params = {
            "file_name": markor_params["file_name"],
            "folder_name": markor_params["folder_name"],
            "text": markor_params["text"],
        "file_name_audio": audio_params["file_name"],
        "text_audio": "",
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorMoveNoteAndAudioRecorderRecordAudioWithFileName(MarkorAndAudioAndDraw):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "file_name": {"type": "string"},
            "source_folder": {"type": "string"},
            "destination_folder": {"type": "string"},
          "file_name_audio": {"type": "string"},
          "text_audio": {"type": "string"},

        },
        "required": ["file_name", "source_folder", "destination_folder"],
    }
    template = (
        "In Markor, move the note {file_name} from {source_folder} to"
        " {destination_folder}."
                  'then Record an audio clip and save it with name "{file_name}" using Audio'
      " Recorder app."
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
        self.audio_task = audio_recorder.AudioRecorderRecordAudioWithFileName(params={
"file_name": self.params["file_name_audio"],
                                                                        "text": self.params["text_audio"]
        })

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.move_file_task.initialize_task(env)
        self.audio_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.move_file_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        audio_success = self.audio_task.is_successful(env)
        logging.info("camera success: %s", audio_success)

        return (markor_success + audio_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorMoveNote.generate_random_params()
        audio_params = audio_recorder.AudioRecorderRecordAudioWithFileName.generate_random_params()
        compound_params = {
            "file_name": markor_params["file_name"],
            "source_folder": markor_params["source_folder"],
            "destination_folder": markor_params["destination_folder"],
            "noise_candidates": _NOTE_TITLES,
            "file_name_audio": audio_params["file_name"],
            "text_audio": "",
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.move_file_task.tear_down(env)


class MarkorCreateFolderAndAudioRecorderRecordAudioWithFileName(MarkorAndAudioAndDraw):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "folder_name": {"type": "string"},
          "file_name_audio": {"type": "string"},
          "text_audio": {"type": "string"},
        },
        "required": ["folder_name"],
    }
    template = (
        "Create a new folder in Markor named {folder_name}."
              'then Record an audio clip and save it with name "{file_name}" using Audio'
      " Recorder app."
    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.markor_task = markor.MarkorCreateFolder(
            params={
                "folder_name": self.params["folder_name"],
            })
        self.audio_task = audio_recorder.AudioRecorderRecordAudioWithFileName(params={
"file_name": self.params["file_name_audio"],
                                                                        "text": self.params["text_audio"]
        })

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.audio_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        audio_success = self.audio_task.is_successful(env)
        logging.info("camera success: %s", audio_success)

        return (markor_success + audio_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorCreateFolder.generate_random_params()
        audio_params = audio_recorder.AudioRecorderRecordAudioWithFileName.generate_random_params()
        compound_params = {
            "folder_name": markor_params["folder_name"],
        "file_name_audio": audio_params["file_name"],
        "text_audio": "",
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorCreateNoteAndAudioRecorderRecordAudioWithFileName(MarkorAndAudioAndDraw):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "file_name": {"type": "string"},
            "text": {"type": "string"},
          "file_name_audio": {"type": "string"},
          "text_audio": {"type": "string"},
        },
        "required": ["file_name", "text"],
    }
    template = (
        "Create a new note in Markor named {file_name} with the following text:"
        " {text}"
              'then Record an audio clip and save it with name "{file_name}" using Audio'
      " Recorder app."
    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.markor_task = markor.MarkorCreateNote(
            params={
                "file_name": self.params["file_name"],
                "text": self.params["text"]
            })
        self.audio_task = audio_recorder.AudioRecorderRecordAudioWithFileName(params={
"file_name": self.params["file_name_audio"],
                                                                        "text": self.params["text_audio"]
        })

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.audio_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        audio_success = self.audio_task.is_successful(env)
        logging.info("camera success: %s", audio_success)

        return (markor_success + audio_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorCreateNote.generate_random_params()
        audio_params = audio_recorder.AudioRecorderRecordAudioWithFileName.generate_random_params()
        compound_params = {
            "file_name": markor_params["file_name"],
            "text": markor_params["text"],
        "file_name_audio": audio_params["file_name"],
        "text_audio": "",
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorCreateNoteFromClipboardAndAudioRecorderRecordAudioWithFileName(MarkorAndAudioAndDraw):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "file_name": {"type": "string"},
            "file_content": {"type": "string"},
          "file_name_audio": {"type": "string"},
          "text_audio": {"type": "string"},
        },
        "required": ["file_name", "file_content"],
    }
    template = (
        "Create a note in Markor named {file_name}. Perform a paste operation in"
        " the note and save the note."
              'then Record an audio clip and save it with name "{file_name}" using Audio'
      " Recorder app."
    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.markor_task = markor.MarkorCreateNoteFromClipboard(
            params={
                "file_name": self.params["file_name"],
                "file_content": self.params["file_content"]
            })
        self.audio_task = audio_recorder.AudioRecorderRecordAudioWithFileName(params={
"file_name": self.params["file_name_audio"],
                                                                        "text": self.params["text_audio"]
        })

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.audio_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        audio_success = self.audio_task.is_successful(env)
        logging.info("camera success: %s", audio_success)

        return (markor_success + audio_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorCreateNoteFromClipboard.generate_random_params()
        audio_params = audio_recorder.AudioRecorderRecordAudioWithFileName.generate_random_params()
        compound_params = {
            "file_name": markor_params["file_name"],
            "file_content": markor_params["file_content"],
        "file_name_audio": audio_params["file_name"],
        "text_audio": "",
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorMergeNotesAndAudioRecorderRecordAudioWithFileName(MarkorAndAudioAndDraw):
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
          "file_name_audio": {"type": "string"},
          "text_audio": {"type": "string"},

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
              'then Record an audio clip and save it with name "{file_name}" using Audio'
      " Recorder app."
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
        self.audio_task = audio_recorder.AudioRecorderRecordAudioWithFileName(params={
"file_name": self.params["file_name_audio"],
                                                                        "text": self.params["text_audio"]
        })

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.audio_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        audio_success = self.audio_task.is_successful(env)
        logging.info("camera success: %s", audio_success)

        return (markor_success + audio_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorMergeNotes.generate_random_params()
        audio_params = audio_recorder.AudioRecorderRecordAudioWithFileName.generate_random_params()
        compound_params = {
            "new_file_name": markor_params["new_file_name"],
            "file1_name": markor_params["file1_name"],
            "file2_name": markor_params["file2_name"],
            "file3_name": markor_params["file3_name"],
            "file1_content": markor_params["file1_content"],
            "file2_content": markor_params["file2_content"],
            "file3_content": markor_params["file3_content"],
        "file_name_audio": audio_params["file_name"],
        "text_audio": "",
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorChangeNoteContentAndAudioRecorderRecordAudioWithFileName(MarkorAndAudioAndDraw):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "original_name": {"type": "string"},
            "new_name": {"type": "string"},
            "updated_content": {"type": "string"},
          "file_name_audio": {"type": "string"},
          "text_audio": {"type": "string"},

        },
        "required": ["original_name", "new_name", "updated_content"],
    }
    template = (
        'Update the content of {original_name} to "{updated_content}" in Markor'
        " and change its name to {new_name}."
              'then Record an audio clip and save it with name "{file_name}" using Audio'
      " Recorder app."
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
        self.audio_task = audio_recorder.AudioRecorderRecordAudioWithFileName(params={
"file_name": self.params["file_name_audio"],
                                                                        "text": self.params["text_audio"]
        })

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.audio_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        audio_success = self.audio_task.is_successful(env)
        logging.info("camera success: %s", audio_success)

        return (markor_success + audio_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorChangeNoteContent.generate_random_params()
        audio_params = audio_recorder.AudioRecorderRecordAudioWithFileName.generate_random_params()
        compound_params = {
            "original_name": markor_params["original_name"],
            "new_name": markor_params["new_name"],
            "updated_content": markor_params["updated_content"],
        "file_name_audio": audio_params["file_name"],
        "text_audio": "",

        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorAddNoteHeaderAndAudioRecorderRecordAudioWithFileName(MarkorAndAudioAndDraw):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "original_name": {"type": "string"},
            "new_name": {"type": "string"},
            "header": {"type": "string"},
            "original_content": {"type": "string"},
          "file_name_audio": {"type": "string"},
          "text_audio": {"type": "string"},

        },
        "required": ["original_name", "new_name", "header", "original_content"],
    }
    template = (
        "Update the Markor note {original_name} by adding the following text,"
        ' along with a new blank line before the existing content: "{header}",'
        " and rename it to {new_name}."
              'then Record an audio clip and save it with name "{file_name}" using Audio'
      " Recorder app."
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
        self.audio_task = audio_recorder.AudioRecorderRecordAudioWithFileName(params={
"file_name": self.params["file_name_audio"],
                                                                        "text": self.params["text_audio"]
        })

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.audio_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        audio_success = self.audio_task.is_successful(env)
        logging.info("camera success: %s", audio_success)

        return (markor_success + audio_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorAddNoteHeader.generate_random_params()
        audio_params = audio_recorder.AudioRecorderRecordAudioWithFileName.generate_random_params()
        compound_params = {
            "original_name": markor_params["original_name"],
            "new_name": markor_params["new_name"],
            "header": markor_params["header"],
            "original_content": markor_params["original_content"],
        "file_name_audio": audio_params["file_name"],
        "text_audio": "",

        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorEditNoteAndAudioRecorderRecordAudioWithFileName(MarkorAndAudioAndDraw):
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
            "file_name_audio": {"type": "string"},
            "text_audio": {"type": "string"},

        },
        "required": ["file_name", "edit_type"],
    }

    @property
    def template(self) -> str:
        templates = {
            "header": (
                "Edit {file_name} in Markor. Add to the top of the note {header}"
                      'then Record an audio clip and save it with name "{file_name}" using Audio'
      " Recorder app."
            ),
            "footer": (
                "Edit {file_name} in Markor. Add to the bottom of the note {footer}"
                      'then Record an audio clip and save it with name "{file_name}" using Audio'
      " Recorder app."
            ),
            "replace": (
                "Edit {file_name} in Markor. Replace the text with {replace_text}"
       'then Record an audio clip and save it with name "{file_name}" using Audio'
      " Recorder app."
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
        self.audio_task = audio_recorder.AudioRecorderRecordAudioWithFileName(params={
                            "file_name": self.params["file_name_audio"],
                            "text": self.params["text_audio"]
        })

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.audio_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        audio_success = self.audio_task.is_successful(env)
        logging.info("camera success: %s", audio_success)

        return (markor_success + audio_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorEditNote.generate_random_params()
        audio_params = audio_recorder.AudioRecorderRecordAudioWithFileName.generate_random_params()
        compound_params = {
            "file_name": markor_params["file_name"],
            "edit_type": markor_params["edit_type"],
            "file_name_audio": audio_params["file_name"],
            "text_audio": "",

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




class MarkorMoveNoteandCreateFolderAndAudioRecorderRecordAudioWithSettingsAndFileName(MarkorAndAudioAndDraw):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "file_name": {"type": "string"},
            "source_folder": {"type": "string"},
            "destination_folder": {"type": "string"},
            "folder_name": {"type": "string"},
            "sample_rate": {"type": "string"},
            "bit_rate": {"type": "string"},
            "file_name_audio": {"type": "string"},
            "text_audio": {"type": "string"},
        },
        "required": ["file_name", "source_folder", "destination_folder", "folder_name"],
    }
    template = (
        "In Markor, move the note {file_name} from {source_folder} to"
        " {destination_folder}. Also, create a new folder named {folder_name} in Markor."
        'then Record an audio clip and save it with name "{file_name}" '
        'and Sample rate "{sample_rate}" and Bitrate "{bit_rate}" using Audio'
        " Recorder app."
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
        self.audio_task = audio_recorder.AudioRecorderRecordAudioWithSettingsAndFileName(params={
            "sample_rate": self.params["sample_rate"],
            "bit_rate": self.params["bit_rate"],
            "file_name": self.params["file_name_audio"],
            "text": self.params["text_audio"]
        })

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.move_file_task.initialize_task(env)
        self.audio_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.move_file_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        audio_success = self.audio_task.is_successful(env)
        logging.info("camera success: %s", audio_success)

        return (markor_success + audio_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorMoveNoteandCreateFolder.generate_random_params()
        audio_params = audio_recorder.AudioRecorderRecordAudioWithSettingsAndFileName.generate_random_params()
        compound_params = {
            "file_name": markor_params["file_name"],
            "source_folder": markor_params["source_folder"],
            "destination_folder": markor_params["destination_folder"],
            "noise_candidates": _NOTE_TITLES,
            "folder_name": markor_params["folder_name"],
            "sample_rate":audio_params["sample_rate"],
            "bit_rate": audio_params["bit_rate"],
            "file_name_audio": audio_params["file_name"],
            "text_audio": "",
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.move_file_task.tear_down(env)


class MarkorCreateFolderthenCreateNoteAndAudioRecorderRecordAudioWithSettingsAndFileName(MarkorAndAudioAndDraw):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "file_name": {"type": "string"},
            "folder_name": {"type": "string"},
            "sample_rate": {"type": "string"},
            "bit_rate": {"type": "string"},
            "file_name_audio": {"type": "string"},
            "text_audio": {"type": "string"},

        },
        "required": ["folder_name", "file_name", ],
    }
    template = (
        "Create a new folder in Markor named {folder_name} and then create a new note named {file_name} in this folder with the following text:"
        " {text}"
        'then Record an audio clip and save it with name "{file_name}" '
        'and Sample rate "{sample_rate}" and Bitrate "{bit_rate}" using Audio'
        " Recorder app."

    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.markor_task = markor.MarkorCreateFolderthenCreateNote(
            params={"file_name": self.params["file_name"],
                    "folder_name": self.params["folder_name"],
                    "text": self.params["text"],

                    })
        self.audio_task = audio_recorder.AudioRecorderRecordAudioWithSettingsAndFileName(params={
            "sample_rate": self.params["sample_rate"],
            "bit_rate": self.params["bit_rate"],
            "file_name": self.params["file_name_audio"],
            "text": self.params["text_audio"]
        })

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.audio_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        audio_success = self.audio_task.is_successful(env)
        logging.info("camera success: %s", audio_success)

        return (markor_success + audio_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorCreateFolderthenCreateNote.generate_random_params()
        audio_params = audio_recorder.AudioRecorderRecordAudioWithSettingsAndFileName.generate_random_params()
        compound_params = {
            "file_name": markor_params["file_name"],
            "folder_name": markor_params["folder_name"],
            "text": markor_params["text"],
            "sample_rate": audio_params["sample_rate"],
            "bit_rate": audio_params["bit_rate"],
            "file_name_audio": audio_params["file_name"],
            "text_audio": "",
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorMoveNoteAndAudioRecorderRecordAudioWithSettingsAndFileName(MarkorAndAudioAndDraw):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "file_name": {"type": "string"},
            "source_folder": {"type": "string"},
            "destination_folder": {"type": "string"},
            "sample_rate": {"type": "string"},
            "bit_rate": {"type": "string"},
            "file_name_audio": {"type": "string"},
            "text_audio": {"type": "string"},

        },
        "required": ["file_name", "source_folder", "destination_folder"],
    }
    template = (
        "In Markor, move the note {file_name} from {source_folder} to"
        " {destination_folder}."
        'then Record an audio clip and save it with name "{file_name}" '
        'and Sample rate "{sample_rate}" and Bitrate "{bit_rate}" using Audio'
        " Recorder app."
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
        self.audio_task = audio_recorder.AudioRecorderRecordAudioWithSettingsAndFileName(params={
            "sample_rate": self.params["sample_rate"],
            "bit_rate": self.params["bit_rate"],
            "file_name": self.params["file_name_audio"],
            "text": self.params["text_audio"]
        })

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.move_file_task.initialize_task(env)
        self.audio_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.move_file_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        audio_success = self.audio_task.is_successful(env)
        logging.info("camera success: %s", audio_success)

        return (markor_success + audio_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorMoveNote.generate_random_params()
        audio_params = audio_recorder.AudioRecorderRecordAudioWithSettingsAndFileName.generate_random_params()
        compound_params = {
            "file_name": markor_params["file_name"],
            "source_folder": markor_params["source_folder"],
            "destination_folder": markor_params["destination_folder"],
            "noise_candidates": _NOTE_TITLES,
            "sample_rate": audio_params["sample_rate"],
            "bit_rate": audio_params["bit_rate"],
            "file_name_audio": audio_params["file_name"],
            "text_audio": "",
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.move_file_task.tear_down(env)


class MarkorCreateFolderAndAudioRecorderRecordAudioWithSettingsAndFileName(MarkorAndAudioAndDraw):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "folder_name": {"type": "string"},
            "sample_rate": {"type": "string"},
            "bit_rate": {"type": "string"},
            "file_name_audio": {"type": "string"},
            "text_audio": {"type": "string"},
        },
        "required": ["folder_name"],
    }
    template = (
        "Create a new folder in Markor named {folder_name}."
		'then Record an audio clip and save it with name "{file_name}" '
		'and Sample rate "{sample_rate}" and Bitrate "{bit_rate}" using Audio'
		" Recorder app."
    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.markor_task = markor.MarkorCreateFolder(
            params={
                "folder_name": self.params["folder_name"],
            })
        self.audio_task = audio_recorder.AudioRecorderRecordAudioWithSettingsAndFileName(params={
            "sample_rate": self.params["sample_rate"],
            "bit_rate": self.params["bit_rate"],
            "file_name": self.params["file_name_audio"],
            "text": self.params["text_audio"]
        })

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.audio_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        audio_success = self.audio_task.is_successful(env)
        logging.info("camera success: %s", audio_success)

        return (markor_success + audio_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorCreateFolder.generate_random_params()
        audio_params = audio_recorder.AudioRecorderRecordAudioWithSettingsAndFileName.generate_random_params()
        compound_params = {
            "folder_name": markor_params["folder_name"],
            "sample_rate": audio_params["sample_rate"],
            "bit_rate": audio_params["bit_rate"],
            "file_name_audio": audio_params["file_name"],
            "text_audio": "",
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorCreateNoteAndAudioRecorderRecordAudioWithSettingsAndFileName(MarkorAndAudioAndDraw):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "file_name": {"type": "string"},
            "text": {"type": "string"},
            "sample_rate": {"type": "string"},
            "bit_rate": {"type": "string"},
            "file_name_audio": {"type": "string"},
            "text_audio": {"type": "string"},
        },
        "required": ["file_name", "text"],
    }
    template = (
        "Create a new note in Markor named {file_name} with the following text:"
        " {text}"
		'then Record an audio clip and save it with name "{file_name}" '
		'and Sample rate "{sample_rate}" and Bitrate "{bit_rate}" using Audio'
		" Recorder app."
    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.markor_task = markor.MarkorCreateNote(
            params={
                "file_name": self.params["file_name"],
                "text": self.params["text"]
            })
        self.audio_task = audio_recorder.AudioRecorderRecordAudioWithSettingsAndFileName(params={
            "sample_rate": self.params["sample_rate"],
            "bit_rate": self.params["bit_rate"],
            "file_name": self.params["file_name_audio"],
            "text": self.params["text_audio"]
        })

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.audio_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        audio_success = self.audio_task.is_successful(env)
        logging.info("camera success: %s", audio_success)

        return (markor_success + audio_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorCreateNote.generate_random_params()
        audio_params = audio_recorder.AudioRecorderRecordAudioWithSettingsAndFileName.generate_random_params()
        compound_params = {
            "file_name": markor_params["file_name"],
            "text": markor_params["text"],
            "sample_rate": audio_params["sample_rate"],
            "bit_rate": audio_params["bit_rate"],
            "file_name_audio": audio_params["file_name"],
            "text_audio": "",
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorCreateNoteFromClipboardAndAudioRecorderRecordAudioWithSettingsAndFileName(MarkorAndAudioAndDraw):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "file_name": {"type": "string"},
            "file_content": {"type": "string"},
            "sample_rate": {"type": "string"},
            "bit_rate": {"type": "string"},
            "file_name_audio": {"type": "string"},
            "text_audio": {"type": "string"},
        },
        "required": ["file_name", "file_content"],
    }
    template = (
        "Create a note in Markor named {file_name}. Perform a paste operation in"
        " the note and save the note."
		'then Record an audio clip and save it with name "{file_name}" '
		'and Sample rate "{sample_rate}" and Bitrate "{bit_rate}" using Audio'
		" Recorder app."
    )

    def __init__(self, params: dict[str, Any]):
        """Initialize the task."""
        super().__init__(params)
        self.markor_task = markor.MarkorCreateNoteFromClipboard(
            params={
                "file_name": self.params["file_name"],
                "file_content": self.params["file_content"]
            })
        self.audio_task = audio_recorder.AudioRecorderRecordAudioWithSettingsAndFileName(params={
            "sample_rate": self.params["sample_rate"],
            "bit_rate": self.params["bit_rate"],
            "file_name": self.params["file_name_audio"],
            "text": self.params["text_audio"]
        })

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.audio_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        audio_success = self.audio_task.is_successful(env)
        logging.info("camera success: %s", audio_success)

        return (markor_success + audio_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorCreateNoteFromClipboard.generate_random_params()
        audio_params = audio_recorder.AudioRecorderRecordAudioWithSettingsAndFileName.generate_random_params()
        compound_params = {
            "file_name": markor_params["file_name"],
            "file_content": markor_params["file_content"],
            "sample_rate": audio_params["sample_rate"],
            "bit_rate": audio_params["bit_rate"],
            "file_name_audio": audio_params["file_name"],
            "text_audio": "",
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorMergeNotesAndAudioRecorderRecordAudioWithSettingsAndFileName(MarkorAndAudioAndDraw):
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
            "sample_rate": {"type": "string"},
            "bit_rate": {"type": "string"},
            "file_name_audio": {"type": "string"},
            "text_audio": {"type": "string"},

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
		'then Record an audio clip and save it with name "{file_name}" '
		'and Sample rate "{sample_rate}" and Bitrate "{bit_rate}" using Audio'
		" Recorder app."
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
        self.audio_task = audio_recorder.AudioRecorderRecordAudioWithSettingsAndFileName(params={
            "sample_rate": self.params["sample_rate"],
            "bit_rate": self.params["bit_rate"],
            "file_name": self.params["file_name_audio"],
            "text": self.params["text_audio"]
        })

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.audio_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        audio_success = self.audio_task.is_successful(env)
        logging.info("camera success: %s", audio_success)

        return (markor_success + audio_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorMergeNotes.generate_random_params()
        audio_params = audio_recorder.AudioRecorderRecordAudioWithSettingsAndFileName.generate_random_params()
        compound_params = {
            "new_file_name": markor_params["new_file_name"],
            "file1_name": markor_params["file1_name"],
            "file2_name": markor_params["file2_name"],
            "file3_name": markor_params["file3_name"],
            "file1_content": markor_params["file1_content"],
            "file2_content": markor_params["file2_content"],
            "file3_content": markor_params["file3_content"],
            "sample_rate": audio_params["sample_rate"],
            "bit_rate": audio_params["bit_rate"],
            "file_name_audio": audio_params["file_name"],
            "text_audio": "",
        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorChangeNoteContentAndAudioRecorderRecordAudioWithSettingsAndFileName(MarkorAndAudioAndDraw):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "original_name": {"type": "string"},
            "new_name": {"type": "string"},
            "updated_content": {"type": "string"},
            "sample_rate": {"type": "string"},
            "bit_rate": {"type": "string"},
            "file_name_audio": {"type": "string"},
            "text_audio": {"type": "string"},

        },
        "required": ["original_name", "new_name", "updated_content"],
    }
    template = (
        'Update the content of {original_name} to "{updated_content}" in Markor'
        " and change its name to {new_name}."
        'then Record an audio clip with Sample rate "{sample_rate}" '
        'and Bitrate "{bit_rate}" using Audio Recorder app and save it.'
        'then Record an audio clip and save it with name "{file_name}" '
        'and Sample rate "{sample_rate}" and Bitrate "{bit_rate}" using Audio'
        " Recorder app."
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
        self.audio_task = audio_recorder.AudioRecorderRecordAudioWithSettingsAndFileName(params={
            "sample_rate": self.params["sample_rate"],
            "bit_rate": self.params["bit_rate"],
            "file_name": self.params["file_name_audio"],
            "text": self.params["text_audio"]
        })

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.audio_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        audio_success = self.audio_task.is_successful(env)
        logging.info("camera success: %s", audio_success)

        return (markor_success + audio_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorChangeNoteContent.generate_random_params()
        audio_params = audio_recorder.AudioRecorderRecordAudioWithSettingsAndFileName.generate_random_params()
        compound_params = {
            "original_name": markor_params["original_name"],
            "new_name": markor_params["new_name"],
            "updated_content": markor_params["updated_content"],
            "sample_rate": audio_params["sample_rate"],
            "bit_rate": audio_params["bit_rate"],
            "file_name_audio": audio_params["file_name"],
            "text_audio": "",

        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorAddNoteHeaderAndAudioRecorderRecordAudioWithSettingsAndFileName(MarkorAndAudioAndDraw):
    """Task for checking that a file has been moved in Markor and checking that a new folder in Markor has been created with a specific name."""

    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "original_name": {"type": "string"},
            "new_name": {"type": "string"},
            "header": {"type": "string"},
            "original_content": {"type": "string"},
            "sample_rate": {"type": "string"},
            "bit_rate": {"type": "string"},
            "file_name_audio": {"type": "string"},
            "text_audio": {"type": "string"},

        },
        "required": ["original_name", "new_name", "header", "original_content"],
    }
    template = (
        "Update the Markor note {original_name} by adding the following text,"
        ' along with a new blank line before the existing content: "{header}",'
        " and rename it to {new_name}."
		'then Record an audio clip and save it with name "{file_name}" '
		'and Sample rate "{sample_rate}" and Bitrate "{bit_rate}" using Audio'
		" Recorder app."
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
        self.audio_task = audio_recorder.AudioRecorderRecordAudioWithSettingsAndFileName(params={
            "sample_rate": self.params["sample_rate"],
            "bit_rate": self.params["bit_rate"],
            "file_name": self.params["file_name_audio"],
            "text": self.params["text_audio"]
        })

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.audio_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        audio_success = self.audio_task.is_successful(env)
        logging.info("camera success: %s", audio_success)

        return (markor_success + audio_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorAddNoteHeader.generate_random_params()
        audio_params = audio_recorder.AudioRecorderRecordAudioWithSettingsAndFileName.generate_random_params()
        compound_params = {
            "original_name": markor_params["original_name"],
            "new_name": markor_params["new_name"],
            "header": markor_params["header"],
            "original_content": markor_params["original_content"],
            "sample_rate": audio_params["sample_rate"],
            "bit_rate": audio_params["bit_rate"],
            "file_name_audio": audio_params["file_name"],
            "text_audio": "",

        }
        return compound_params

    def tear_down(self, env: interface.AsyncEnv) -> None:
        super().tear_down(env)
        self.markor_task.tear_down(env)


class MarkorEditNoteAndAudioRecorderRecordAudioWithSettingsAndFileName(MarkorAndAudioAndDraw):
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
            "sample_rate": {"type": "string"},
            "bit_rate": {"type": "string"},
            "file_name_audio": {"type": "string"},
            "text_audio": {"type": "string"},

        },
        "required": ["file_name", "edit_type"],
    }

    @property
    def template(self) -> str:
        templates = {
            "header": (
                "Edit {file_name} in Markor. Add to the top of the note {header}"
		'then Record an audio clip and save it with name "{file_name}" '
		'and Sample rate "{sample_rate}" and Bitrate "{bit_rate}" using Audio'
		" Recorder app."
            ),
            "footer": (
                "Edit {file_name} in Markor. Add to the bottom of the note {footer}"
		'then Record an audio clip and save it with name "{file_name}" '
		'and Sample rate "{sample_rate}" and Bitrate "{bit_rate}" using Audio'
		" Recorder app."
            ),
            "replace": (
                "Edit {file_name} in Markor. Replace the text with {replace_text}"
		'then Record an audio clip and save it with name "{file_name}" '
		'and Sample rate "{sample_rate}" and Bitrate "{bit_rate}" using Audio'
		" Recorder app."
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
        self.audio_task = audio_recorder.AudioRecorderRecordAudioWithSettingsAndFileName(params={
            "sample_rate": self.params["sample_rate"],
            "bit_rate": self.params["bit_rate"],
            "file_name": self.params["file_name_audio"],
            "text": self.params["text_audio"]
        })
    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.markor_task.initialize_task(env)
        self.audio_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        markor_success = self.markor_task.is_successful(env)
        logging.info("Markor success: %s", markor_success)

        audio_success = self.audio_task.is_successful(env)
        logging.info("camera success: %s", audio_success)

        return (markor_success + audio_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        markor_params = markor.MarkorEditNote.generate_random_params()
        audio_params = audio_recorder.AudioRecorderRecordAudioWithSettingsAndFileName.generate_random_params()
        compound_params = {
            "file_name": markor_params["file_name"],
            "edit_type": markor_params["edit_type"],
            "sample_rate": audio_params["sample_rate"],
            "bit_rate": audio_params["bit_rate"],
            "file_name_audio": audio_params["file_name"],
            "text_audio": "",

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