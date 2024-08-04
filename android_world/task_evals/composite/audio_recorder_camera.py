import subprocess
import random
from absl import logging
from typing import Any
from android_world.env import interface
from android_world.task_evals.single import audio_recorder
from android_world.task_evals.single import camera
from android_world.task_evals import task_eval
from android_world.utils import file_utils
from android_world.env import device_constants
from android_world.task_evals.common_validators import file_validators
from android_world.task_evals.utils import user_data_generation
class AudioRecorderOpenAndCameraOpen(audio_recorder._AudioRecorder, camera._Camera):
    complexity = 1
    schema = {}
    template = (
        "Open Camera App,then open audio recorder app"
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
                if result[i].split(" ")[2] == "com.dimowner.audiorecorder/.app.main.MainActivity}":
                    return 1
                else:
                    return 0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class AudioRecorderRecordAudioAndCameraOpen(audio_recorder._AudioRecorder,camera._Camera):
    complexity = 3
    schema = {
        "type": "object",
        "properties": {},
        "required": [],
    }
    template = "Record an audio clip using Audio Recorder app and save it, then ,open camera app"

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.audiotask = audio_recorder.AudioRecorderRecordAudio(
        params={}
    )
        self.camera = camera.CameraOpen(
        params={}
    )
        self.audiotask.initialize_task(env)
        self.camera.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        audio_success = self.audiotask.is_successful(env)
        logging.info("audio success: %s", audio_success)

        camera_success = self.camera.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (audio_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class AudioRecorderRecordAudioWithSettingsAndCameraOpen(audio_recorder._AudioRecorder,camera._Camera):
  """Task for checking that one audio recording has been completed."""

  complexity = 3
  schema = {
      "type": "object",
      "properties": {"sample_rate": {"type": "string"},
          "bit_rate": {"type": "string"},},
      "required": [],
  }
  template = 'Record an audio clip with Sample rate "{sample_rate}" and Bitrate "{bit_rate}" using Audio Recorder app and save it,then open camera app'

  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    self.audiotask = audio_recorder.AudioRecorderRecordAudio(
        params={"sample_rate": self.params["sample_rate"],
            "bit_rate": self.params["bit_rate"],
                }
    )
    self.camera = camera.CameraOpen(
        params={}
    )
    self.audiotask.initialize_task(env)
    self.camera.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    audio_success = self.audiotask.is_successful(env)
    logging.info("audio success: %s", audio_success)

    camera_success = self.camera.is_successful(env)
    logging.info("camera success: %s", camera_success)

    return (audio_success + camera_success) / 2.0

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:

    sample_rate = [
        "8kHz",
        "16kHz",
        "22kHz",
        "32kHz",
        "44.1kHz",
        "48kHz",
    ]
    bit_rate =[
        "48 kbps",
        "96 kbps",
        "128 kbps",
        "192 kbps",
        "256 kbps",
    ]
    samplerate=random.choice(sample_rate)
    bitrate=random.choice(bit_rate)
    return {
        "sample_rate": samplerate,
        "bit_rate": bitrate,
        "text": "",  # Unused.
    }

class AudioRecorderRecordAudioWithFileNameAndCameraOpen(audio_recorder._AudioRecorder,camera._Camera):
  """Task for checking that one audio recording with file_name has been completed."""

  complexity = 2
  schema = file_validators.CreateFile.schema
  template = (
      'Record an audio clip and save it with name "{file_name}" using Audio'
      " Recorder app. then open camera app"
  )

  def __init__(self, params: dict[str, Any]):
    """See base class."""
    super().__init__(params)
    self.initialized = False
    self.audiotask = audio_recorder.AudioRecorderRecordAudioWithFileName(
        params)
    self.camera = camera.CameraOpen(
        params={}
    )

  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    self.audiotask.initialize_task(env)
    self.camera.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    audio_success = self.audiotask.is_successful(env)
    logging.info("audio success: %s", audio_success)

    camera_success = self.camera.is_successful(env)
    logging.info("camera success: %s", camera_success)

    return (audio_success + camera_success) / 2.0

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
    name = [
        "interview",
        "meeting",
        "lecture",
        "session",
        "note",
        "conference",
        "webinar",
        "workshop",
        "seminar",
        "briefing",
        "discussion",
        "talk",
        "presentation",
        "training",
        "guidance",
        "memo",
        "narration",
        "storytelling",
        "journal",
        "diary",
        "debate",
        "symposium",
        "roundtable",
        "consultation",
        "review",
    ]
    return {
        "file_name": user_data_generation.generate_modified_file_name(
            random.choice(name) + ".m4a"
        ),
        "text": "",  # Unused.
    }

  def tear_down(self, env: interface.AsyncEnv) -> None:
    super().tear_down(env)
    self.audiotask.tear_down(env)

class AudioOpenAndCameraTakePhoto(audio_recorder._AudioRecorder,camera._Camera):
    complexity = 2
    schema = {
        "type": "object",
        "properties": {},
        "required": [],
    }
    template = "Take one photo ,then Open Audio Recorder app"

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.audio_task=audio_recorder.AudioRecoderOpen(params={})
        self.camera_task=camera.CameraTakePhoto(params={})
        self.audio_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        audio_success = self.audio_task.is_successful(env)
        logging.info("audio success: %s", audio_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (audio_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        return {}

class AudioOpenAndCameraTakeVideo(audio_recorder._AudioRecorder,camera._Camera):
    complexity = 2
    schema = {
        "type": "object",
        "properties": {},
        "required": [],
    }
    template = "Take one video ,then Open Audio Recorder app"

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.audio_task=audio_recorder.AudioRecoderOpen(params={})
        self.camera_task=camera.CameraTakeVideo(params={})
        self.audio_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        audio_success = self.audio_task.is_successful(env)
        logging.info("audio success: %s", audio_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (audio_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        return {}

class AudioOpenAndCameraTakePhotos(audio_recorder._AudioRecorder,camera._Camera):
    complexity = 2
    schema = {
        "type": "object",
        "properties": {},
        "required": [],
    }
    template = "Take three photos ,then Open Audio Recorder app"

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.audio_task=audio_recorder.AudioRecoderOpen(params={})
        self.camera_task=camera.CameraTakePhotos(params={})
        self.audio_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        audio_success = self.audio_task.is_successful(env)
        logging.info("audio success: %s", audio_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (audio_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        return {}
class AudioOpenAndCameraTakeVideos(audio_recorder._AudioRecorder,camera._Camera):
    complexity = 2
    schema = {
        "type": "object",
        "properties": {},
        "required": [],
    }
    template = "Take two videos ,then Open Audio Recorder app"

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.audio_task=audio_recorder.AudioRecoderOpen(params={})
        self.camera_task=camera.CameraTakeVideos(params={})
        self.audio_task.initialize_task(env)
        self.camera_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        audio_success = self.audio_task.is_successful(env)
        logging.info("audio success: %s", audio_success)

        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (audio_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        return {}

class AudioRecorderRecordAudioAndCameraTakePhoto(audio_recorder._AudioRecorder,camera._Camera):
    complexity = 3
    schema = {
        "type": "object",
        "properties": {},
        "required": [],
    }
    template = "Record an audio clip using Audio Recorder app and save it, then take a photo"

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.audiotask = audio_recorder.AudioRecorderRecordAudio(
        params={}
    )
        self.camera = camera.CameraTakePhoto(
        params={}
    )
        self.audiotask.initialize_task(env)
        self.camera.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        audio_success = self.audiotask.is_successful(env)
        logging.info("audio success: %s", audio_success)

        camera_success = self.camera.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (audio_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class AudioRecorderRecordAudioAndCameraTakePhotos(audio_recorder._AudioRecorder,camera._Camera):
    complexity = 3
    schema = {
        "type": "object",
        "properties": {},
        "required": [],
    }
    template = "Record an audio clip using Audio Recorder app and save it, then take three photos"

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.audiotask = audio_recorder.AudioRecorderRecordAudio(
        params={}
    )
        self.camera = camera.CameraTakePhoto(
        params={}
    )
        self.audiotask.initialize_task(env)
        self.camera.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        audio_success = self.audiotask.is_successful(env)
        logging.info("audio success: %s", audio_success)

        camera_success = self.camera.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (audio_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class AudioRecorderRecordAudioAndCameraTakeVideo(audio_recorder._AudioRecorder,camera._Camera):
    complexity = 3
    schema = {
        "type": "object",
        "properties": {},
        "required": [],
    }
    template = "Record an audio clip using Audio Recorder app and save it, then take a video"

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.audiotask = audio_recorder.AudioRecorderRecordAudio(
        params={}
    )
        self.camera = camera.CameraTakeVideo(
        params={}
    )
        self.audiotask.initialize_task(env)
        self.camera.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        audio_success = self.audiotask.is_successful(env)
        logging.info("audio success: %s", audio_success)

        camera_success = self.camera.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (audio_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class AudioRecorderRecordAudioAndCameraTakeVideos(audio_recorder._AudioRecorder,camera._Camera):
    complexity = 3
    schema = {
        "type": "object",
        "properties": {},
        "required": [],
    }
    template = "Record an audio clip using Audio Recorder app and save it, then take two videos"

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.audiotask = audio_recorder.AudioRecorderRecordAudio(
        params={}
    )
        self.camera = camera.CameraTakeVideos(
        params={}
    )
        self.audiotask.initialize_task(env)
        self.camera.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        audio_success = self.audiotask.is_successful(env)
        logging.info("audio success: %s", audio_success)

        camera_success = self.camera.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (audio_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class AudioRecorderRecordAudioWithFileNameAndCameraTakePhoto(audio_recorder._AudioRecorder,camera._Camera):
  """Task for checking that one audio recording with file_name has been completed."""

  complexity = 3
  schema = file_validators.CreateFile.schema
  template = (
      'Record an audio clip and save it with name "{file_name}" using Audio'
      " Recorder app. then take one photo"
  )

  def __init__(self, params: dict[str, Any]):
    """See base class."""
    super().__init__(params)
    self.initialized = False
    self.audiotask = audio_recorder.AudioRecorderRecordAudioWithFileName(
        params)
    self.camera = camera.CameraTakePhoto(
        params={}
    )

  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    self.audiotask.initialize_task(env)
    self.camera.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    audio_success = self.audiotask.is_successful(env)
    logging.info("audio success: %s", audio_success)

    camera_success = self.camera.is_successful(env)
    logging.info("camera success: %s", camera_success)

    return (audio_success + camera_success) / 2.0

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
    name = [
        "interview",
        "meeting",
        "lecture",
        "session",
        "note",
        "conference",
        "webinar",
        "workshop",
        "seminar",
        "briefing",
        "discussion",
        "talk",
        "presentation",
        "training",
        "guidance",
        "memo",
        "narration",
        "storytelling",
        "journal",
        "diary",
        "debate",
        "symposium",
        "roundtable",
        "consultation",
        "review",
    ]
    return {
        "file_name": user_data_generation.generate_modified_file_name(
            random.choice(name) + ".m4a"
        ),
        "text": "",  # Unused.
    }

  def tear_down(self, env: interface.AsyncEnv) -> None:
    super().tear_down(env)
    self.audiotask.tear_down(env)

class AudioRecorderRecordAudioWithFileNameAndCameraTakePhotos(audio_recorder._AudioRecorder,camera._Camera):
  """Task for checking that one audio recording with file_name has been completed."""

  complexity = 3
  schema = file_validators.CreateFile.schema
  template = (
      'Record an audio clip and save it with name "{file_name}" using Audio'
      " Recorder app. then take three photos"
  )

  def __init__(self, params: dict[str, Any]):
    """See base class."""
    super().__init__(params)
    self.initialized = False
    self.audiotask = audio_recorder.AudioRecorderRecordAudioWithFileName(
        params)
    self.camera = camera.CameraTakePhotos(
        params={}
    )

  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    self.audiotask.initialize_task(env)
    self.camera.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    audio_success = self.audiotask.is_successful(env)
    logging.info("audio success: %s", audio_success)

    camera_success = self.camera.is_successful(env)
    logging.info("camera success: %s", camera_success)

    return (audio_success + camera_success) / 2.0

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
    name = [
        "interview",
        "meeting",
        "lecture",
        "session",
        "note",
        "conference",
        "webinar",
        "workshop",
        "seminar",
        "briefing",
        "discussion",
        "talk",
        "presentation",
        "training",
        "guidance",
        "memo",
        "narration",
        "storytelling",
        "journal",
        "diary",
        "debate",
        "symposium",
        "roundtable",
        "consultation",
        "review",
    ]
    return {
        "file_name": user_data_generation.generate_modified_file_name(
            random.choice(name) + ".m4a"
        ),
        "text": "",  # Unused.
    }

  def tear_down(self, env: interface.AsyncEnv) -> None:
    super().tear_down(env)
    self.audiotask.tear_down(env)

class AudioRecorderRecordAudioWithFileNameAndCameraTakeVideo(audio_recorder._AudioRecorder,camera._Camera):
  """Task for checking that one audio recording with file_name has been completed."""

  complexity = 3
  schema = file_validators.CreateFile.schema
  template = (
      'Record an audio clip and save it with name "{file_name}" using Audio'
      " Recorder app. then take one video"
  )

  def __init__(self, params: dict[str, Any]):
    """See base class."""
    super().__init__(params)
    self.initialized = False
    self.audiotask = audio_recorder.AudioRecorderRecordAudioWithFileName(
        params)
    self.camera = camera.CameraTakeVideo(
        params={}
    )

  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    self.audiotask.initialize_task(env)
    self.camera.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    audio_success = self.audiotask.is_successful(env)
    logging.info("audio success: %s", audio_success)

    camera_success = self.camera.is_successful(env)
    logging.info("camera success: %s", camera_success)

    return (audio_success + camera_success) / 2.0

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
    name = [
        "interview",
        "meeting",
        "lecture",
        "session",
        "note",
        "conference",
        "webinar",
        "workshop",
        "seminar",
        "briefing",
        "discussion",
        "talk",
        "presentation",
        "training",
        "guidance",
        "memo",
        "narration",
        "storytelling",
        "journal",
        "diary",
        "debate",
        "symposium",
        "roundtable",
        "consultation",
        "review",
    ]
    return {
        "file_name": user_data_generation.generate_modified_file_name(
            random.choice(name) + ".m4a"
        ),
        "text": "",  # Unused.
    }

  def tear_down(self, env: interface.AsyncEnv) -> None:
    super().tear_down(env)
    self.audiotask.tear_down(env)

class AudioRecorderRecordAudioWithFileNameAndCameraTakePhotoAndVideo(audio_recorder._AudioRecorder,camera._Camera):
  """Task for checking that one audio recording with file_name has been completed."""

  complexity = 3
  schema = file_validators.CreateFile.schema
  template = (
      'Record an audio clip and save it with name "{file_name}" using Audio'
      " Recorder app. then take one photo and one video"
  )

  def __init__(self, params: dict[str, Any]):
    """See base class."""
    super().__init__(params)
    self.initialized = False
    self.audiotask = audio_recorder.AudioRecorderRecordAudioWithFileName(
        params)
    self.camera = camera.CameraTakePhotoAndVideo(
        params={}
    )

  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    self.audiotask.initialize_task(env)
    self.camera.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    audio_success = self.audiotask.is_successful(env)
    logging.info("audio success: %s", audio_success)

    camera_success = self.camera.is_successful(env)
    logging.info("camera success: %s", camera_success)

    return (audio_success + camera_success) / 2.0

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
    name = [
        "interview",
        "meeting",
        "lecture",
        "session",
        "note",
        "conference",
        "webinar",
        "workshop",
        "seminar",
        "briefing",
        "discussion",
        "talk",
        "presentation",
        "training",
        "guidance",
        "memo",
        "narration",
        "storytelling",
        "journal",
        "diary",
        "debate",
        "symposium",
        "roundtable",
        "consultation",
        "review",
    ]
    return {
        "file_name": user_data_generation.generate_modified_file_name(
            random.choice(name) + ".m4a"
        ),
        "text": "",  # Unused.
    }

  def tear_down(self, env: interface.AsyncEnv) -> None:
    super().tear_down(env)
    self.audiotask.tear_down(env)
class AudioRecorderRecordAudioWithFileNameAndCameraTakeVideos(audio_recorder._AudioRecorder,camera._Camera):
  """Task for checking that one audio recording with file_name has been completed."""

  complexity = 3
  schema = file_validators.CreateFile.schema
  template = (
      'Record an audio clip and save it with name "{file_name}" using Audio'
      " Recorder app. then take two videos"
  )

  def __init__(self, params: dict[str, Any]):
    """See base class."""
    super().__init__(params)
    self.initialized = False
    self.audiotask = audio_recorder.AudioRecorderRecordAudioWithFileName(
        params)
    self.camera = camera.CameraTakeVideos(
        params={}
    )

  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    self.audiotask.initialize_task(env)
    self.camera.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    audio_success = self.audiotask.is_successful(env)
    logging.info("audio success: %s", audio_success)

    camera_success = self.camera.is_successful(env)
    logging.info("camera success: %s", camera_success)

    return (audio_success + camera_success) / 2.0

  @classmethod
  def generate_random_params(cls) -> dict[str, str | int]:
    name = [
        "interview",
        "meeting",
        "lecture",
        "session",
        "note",
        "conference",
        "webinar",
        "workshop",
        "seminar",
        "briefing",
        "discussion",
        "talk",
        "presentation",
        "training",
        "guidance",
        "memo",
        "narration",
        "storytelling",
        "journal",
        "diary",
        "debate",
        "symposium",
        "roundtable",
        "consultation",
        "review",
    ]
    return {
        "file_name": user_data_generation.generate_modified_file_name(
            random.choice(name) + ".m4a"
        ),
        "text": "",  # Unused.
    }

  def tear_down(self, env: interface.AsyncEnv) -> None:
    super().tear_down(env)
    self.audiotask.tear_down(env)

class AudioRecorderRecordAudioWithSettingsAndCameraTakePhoto(audio_recorder._AudioRecorder,camera._Camera):
    complexity = 3
    schema = {
        "type": "object",
        "properties": {"sample_rate": {"type": "string"},
                       "bit_rate": {"type": "string"}, },
        "required": [],
    }
    template = 'Record an audio clip with Sample rate "{sample_rate}" and Bitrate "{bit_rate}" using Audio Recorder app and save it., then take a photo'

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.audiotask = audio_recorder.AudioRecorderRecordAudioWithSettings(
        params={  "sample_rate": self.params["sample_rate"],
            "bit_rate": self.params["bit_rate"],}
    )
        self.camera = camera.CameraTakePhoto(
        params={}
    )
        self.audiotask.initialize_task(env)
        self.camera.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        audio_success = self.audiotask.is_successful(env)
        logging.info("audio success: %s", audio_success)

        camera_success = self.camera.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (audio_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        sample_rate = [
            "8kHz",
            "16kHz",
            "22kHz",
            "32kHz",
            "44.1kHz",
            "48kHz",
        ]
        bit_rate = [
            "48 kbps",
            "96 kbps",
            "128 kbps",
            "192 kbps",
            "256 kbps",
        ]
        samplerate = random.choice(sample_rate)
        bitrate = random.choice(bit_rate)
        return {
            "sample_rate": samplerate,
            "bit_rate": bitrate,
            "text": "",  # Unused.
        }

class AudioRecorderRecordAudioWithSettingsAndCameraTakePhotos(audio_recorder._AudioRecorder,camera._Camera):
    complexity = 3
    schema = {
        "type": "object",
        "properties": {"sample_rate": {"type": "string"},
                       "bit_rate": {"type": "string"}, },
        "required": [],
    }
    template = 'Record an audio clip with Sample rate "{sample_rate}" and Bitrate "{bit_rate}" using Audio Recorder app and save it., then take three photos'

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.audiotask = audio_recorder.AudioRecorderRecordAudioWithSettings(
        params={  "sample_rate": self.params["sample_rate"],
            "bit_rate": self.params["bit_rate"],}
    )
        self.camera = camera.CameraTakePhotos(
        params={}
    )
        self.audiotask.initialize_task(env)
        self.camera.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        audio_success = self.audiotask.is_successful(env)
        logging.info("audio success: %s", audio_success)

        camera_success = self.camera.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (audio_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        sample_rate = [
            "8kHz",
            "16kHz",
            "22kHz",
            "32kHz",
            "44.1kHz",
            "48kHz",
        ]
        bit_rate = [
            "48 kbps",
            "96 kbps",
            "128 kbps",
            "192 kbps",
            "256 kbps",
        ]
        samplerate = random.choice(sample_rate)
        bitrate = random.choice(bit_rate)
        return {
            "sample_rate": samplerate,
            "bit_rate": bitrate,
            "text": "",  # Unused.
        }

class AudioRecorderRecordAudioWithSettingsAndCameraTakeVideo(audio_recorder._AudioRecorder,camera._Camera):
    complexity = 3
    schema = {
        "type": "object",
        "properties": {"sample_rate": {"type": "string"},
                       "bit_rate": {"type": "string"}, },
        "required": [],
    }
    template = 'Record an audio clip with Sample rate "{sample_rate}" and Bitrate "{bit_rate}" using Audio Recorder app and save it., then take one video'

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.audiotask = audio_recorder.AudioRecorderRecordAudioWithSettings(
        params={  "sample_rate": self.params["sample_rate"],
            "bit_rate": self.params["bit_rate"],}
    )
        self.camera = camera.CameraTakeVideo(
        params={}
    )
        self.audiotask.initialize_task(env)
        self.camera.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        audio_success = self.audiotask.is_successful(env)
        logging.info("audio success: %s", audio_success)

        camera_success = self.camera.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (audio_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        sample_rate = [
            "8kHz",
            "16kHz",
            "22kHz",
            "32kHz",
            "44.1kHz",
            "48kHz",
        ]
        bit_rate = [
            "48 kbps",
            "96 kbps",
            "128 kbps",
            "192 kbps",
            "256 kbps",
        ]
        samplerate = random.choice(sample_rate)
        bitrate = random.choice(bit_rate)
        return {
            "sample_rate": samplerate,
            "bit_rate": bitrate,
            "text": "",  # Unused.
        }

class AudioRecorderRecordAudioWithSettingsAndCameraTakeVideos(audio_recorder._AudioRecorder,camera._Camera):
    complexity = 3
    schema = {
        "type": "object",
        "properties": {"sample_rate": {"type": "string"},
                       "bit_rate": {"type": "string"}, },
        "required": [],
    }
    template = 'Record an audio clip with Sample rate "{sample_rate}" and Bitrate "{bit_rate}" using Audio Recorder app and save it., then take two videos'

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.audiotask = audio_recorder.AudioRecorderRecordAudioWithSettings(
        params={  "sample_rate": self.params["sample_rate"],
            "bit_rate": self.params["bit_rate"],}
    )
        self.camera = camera.CameraTakeVideos(
        params={}
    )
        self.audiotask.initialize_task(env)
        self.camera.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        audio_success = self.audiotask.is_successful(env)
        logging.info("audio success: %s", audio_success)

        camera_success = self.camera.is_successful(env)
        logging.info("camera success: %s", camera_success)

        return (audio_success + camera_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        sample_rate = [
            "8kHz",
            "16kHz",
            "22kHz",
            "32kHz",
            "44.1kHz",
            "48kHz",
        ]
        bit_rate = [
            "48 kbps",
            "96 kbps",
            "128 kbps",
            "192 kbps",
            "256 kbps",
        ]
        samplerate = random.choice(sample_rate)
        bitrate = random.choice(bit_rate)
        return {
            "sample_rate": samplerate,
            "bit_rate": bitrate,
            "text": "",  # Unused.
        }