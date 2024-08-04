import subprocess
import random
from absl import logging
from typing import Any
from android_world.env import interface
from android_world.task_evals.single import audio_recorder
from android_world.task_evals.single import  clock
from android_world.task_evals.common_validators import file_validators
from android_world.task_evals.utils import user_data_generation
from android_world.env import device_constants
class AudioRecoderOpenAndClockOpen(audio_recorder._AudioRecorder, clock._ClockEval):
    complexity = 1
    schema = {}
    template = (
        "Open Clock App,then open audiorecorder app"
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

class AudioRecorderRecordAudioAndClockOpen(audio_recorder._AudioRecorder, clock._ClockEval):
        complexity = 3
        schema = {
            "type": "object",
            "properties": {},
            "required": [],
        }
        template = "Record an audio clip using Audio Recorder app and save it, then ,open clock app"

        def initialize_task(self, env: interface.AsyncEnv) -> None:
            super().initialize_task(env)
            self.audiotask = audio_recorder.AudioRecorderRecordAudio(
                params={}
            )
            self.clock = clock.ClockOpen(
                params={}
            )
            self.audiotask.initialize_task(env)
            self.clock.initialize_task(env)

        def is_successful(self, env: interface.AsyncEnv) -> float:
            super().is_successful(env)
            audio_success = self.audiotask.is_successful(env)
            logging.info("audio success: %s", audio_success)

            clock_success = self.clock.is_successful(env)
            logging.info("clock success: %s", clock_success)

            return (audio_success + clock_success) / 2.0

        @classmethod
        def generate_random_params(cls) -> dict[str, str | int]:
            return {}

class AudioRecorderRecordAudioWithSettingsAndClockOpen(audio_recorder._AudioRecorder, clock._ClockEval):
    complexity = 3
    schema = {
        "type": "object",
        "properties": {"sample_rate": {"type": "string"},
                       "bit_rate": {"type": "string"}, },
        "required": [],
    }
    template = 'Record an audio clip with Sample rate "{sample_rate}" and Bitrate "{bit_rate}" using Audio Recorder appand save it, then ,open clock app'

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.audio_task = audio_recorder.AudioRecorderRecordAudioWithSettings(
            params={"sample_rate": self.params["sample_rate"],
                    "bit_rate": self.params["bit_rate"],
                    }
        )
        self.clock_task = clock.ClockOpen(
            params={}
        )
        self.audio_task.initialize_task(env)
        self.clock_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        audio_success = self.audio_task.is_successful(env)
        logging.info("audio success: %s", audio_success)

        clock_success = self.clock_task.is_successful(env)
        logging.info("clock success: %s", clock_success)

        return (audio_success + clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        audio_params = audio_recorder.AudioRecorderRecordAudioWithSettings.generate_random_params()
        return audio_params
class AudioRecorderRecordAudioWithFileNameAndClockOpen(audio_recorder._AudioRecorder, clock._ClockEval):
    complexity = 3
    schema = file_validators.CreateFile.schema
    template = (
        'Record an audio clip and save it with name "{file_name}" using Audio in clock app'
        " Recorder app then open clock app"
    )

    def __init__(self, params: dict[str, Any]):
        """See base class."""
        super().__init__(params)
        self.initialized = False
        self.audio_task = file_validators.CreateFile(
            params, device_constants.AUDIORECORDER_DATA
        )
    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.clock_task = clock.ClockOpen(
            params={}
        )
        self.audio_task.initialize_task(env)
        self.clock_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        audio_success = self.audio_task.is_successful(env)
        logging.info("audio success: %s", audio_success)

        clock_success = self.clock_task.is_successful(env)
        logging.info("clock success: %s", clock_success)

        return (audio_success + clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        audio_params = audio_recorder.AudioRecorderRecordAudioWithFileName.generate_random_params()
        return audio_params
class AudioRecorderRecordAudioAndClockStopWatchPaused(audio_recorder._AudioRecorder, clock._ClockEval):
    complexity = 3
    schema = {
        "type": "object",
        "properties": {},
        "required": [],
    }
    template = "Record an audio clip using Audio Recorder app and save it,then Pause the stopwatch in clock app"

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.audio_task=audio_recorder.AudioRecorderRecordAudio(
            params={}
        )
        self.clock_task=clock.ClockStopWatchPausedVerify(
            params={}
        )
        self.audio_task.initialize_task(env)
        self.clock_task.initialize_task(env)
    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        audio_success = self.audio_task.is_successful(env)
        logging.info("audio success: %s", audio_success)

        clock_success = self.clock_task.is_successful(env)
        logging.info("clock success: %s", clock_success)

        return (audio_success + clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        return {}
class AudioRecorderRecordAudioAndClockStopWatchRunningAndPaused(audio_recorder._AudioRecorder, clock._ClockEval):
    complexity = 3
    schema = {
        "type": "object",
        "properties": {},
        "required": [],
    }
    template = "Record an audio clip using Audio Recorder app and save it,then Run the stopwatch and then Pause it in clock app."

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.audio_task=audio_recorder.AudioRecorderRecordAudio(
            params={}
        )
        self.clock_task=clock.ClockStopWatchRunningAndPaused(
            params={}
        )
        self.audio_task.initialize_task(env)
        self.clock_task.initialize_task(env)
    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        audio_success = self.audio_task.is_successful(env)
        logging.info("audio success: %s", audio_success)

        clock_success = self.clock_task.is_successful(env)
        logging.info("clock success: %s", clock_success)

        return (audio_success + clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        return {}
class AudioRecorderRecordAudioAndStopWatchRunning(audio_recorder._AudioRecorder, clock._ClockEval):
    complexity = 3
    schema = {
        "type": "object",
        "properties": {},
        "required": [],
    }
    template = "Record an audio clip using Audio Recorder app and save it,then run the stopwatch in clock app"

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.audio_task=audio_recorder.AudioRecorderRecordAudio(
            params={}
        )
        self.clock_task=clock.ClockStopWatchRunning(
            params={}
        )
        self.audio_task.initialize_task(env)
        self.clock_task.initialize_task(env)
    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        audio_success = self.audio_task.is_successful(env)
        logging.info("audio success: %s", audio_success)

        clock_success = self.clock_task.is_successful(env)
        logging.info("clock success: %s", clock_success)

        return (audio_success + clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class AudioRecorderRecordAudioAndClockTimerEntry(audio_recorder._AudioRecorder, clock._ClockEval):
    complexity = 4
    schema = {
        "type": "object",
        "properties": {
            "hours": {"type": "integer"},
            "minutes": {"type": "integer"},
            "seconds": {"type": "integer"},
        },
        "required": ["hours", "minutes", "seconds"],
    }
    template = ("Record an audio clip using Audio Recorder app and save it,then Create a timer with {hours} hours, {minutes} minutes, and {seconds} in clock app"
                " seconds. Do not start the timer.")

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.audio_task=audio_recorder.AudioRecorderRecordAudio(
            params={}
        )
        self.clock_task = clock.ClockWatchRunningAndReset(
            params={"hours": self.params["hours"],
                    "minutes": self.params["minutes"],
                    "seconds": self.params["seconds"]
                    }
        )
        self.audio_task.initialize_task(env)
        self.clock_task.initialize_task(env)
    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        audio_success = self.audio_task.is_successful(env)
        logging.info("audio success: %s", audio_success)

        clock_success = self.clock_task.is_successful(env)
        logging.info("clock success: %s", clock_success)

        return (audio_success + clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        clock_params = clock.ClockTimerEntry.generate_random_params()
        return clock_params
class AudioRecorderRecordAudioAndStopWatchRunningAndReset(audio_recorder._AudioRecorder, clock._ClockEval):
    complexity = 3
    schema = {
        "type": "object",
        "properties": {},
        "required": [],
    }
    template = "Record an audio clip using Audio Recorder app and save it,then Run the stopwatch and reset the stopwatch in clock app."

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.audio_task=audio_recorder.AudioRecorderRecordAudio(
            params={}
        )
        self.clock_task=clock.ClockWatchRunningAndReset(
            params={}
        )
        self.audio_task.initialize_task(env)
        self.clock_task.initialize_task(env)
    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        audio_success = self.audio_task.is_successful(env)
        logging.info("audio success: %s", audio_success)

        clock_success = self.clock_task.is_successful(env)
        logging.info("clock success: %s", clock_success)

        return (audio_success + clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class AudioRecorderRecordAudioWithSettingsAndClockTimerEntry(audio_recorder._AudioRecorder, clock._ClockEval):
    complexity = 4
    schema = {
        "type": "object",
        "properties": {
            "hours": {"type": "integer"},
            "minutes": {"type": "integer"},
            "seconds": {"type": "integer"},
            "sample_rate": {"type": "string"},
            "bit_rate": {"type": "string"},
        },
        "required": ["hours", "minutes", "seconds","sample_rate","bit_rate"],
    }
    template =  ("Record an audio clip with Sample rate {sample_rate} "
                 "and Bitrate {bit_rate} using Audio Recorder app and save it."
                "Create a timer with {hours} hours, {minutes} minutes, and {seconds}"
                " seconds. Do not start the timer. in clock app" )


    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.audio_task = audio_recorder.AudioRecorderRecordAudioWithSettings(
            params={"sample_rate": self.params["sample_rate"],
                    "bit_rate": self.params["bit_rate"],
                    }
        )
        self.clock_task=clock.ClockWatchRunningAndReset(
            params={"hours":self.params["hours"],
                    "minutes":self.params["minutes"],
                    "seconds":self.params["seconds"]
            }
        )
        self.audio_task.initialize_task(env)
        self.clock_task.initialize_task(env)
    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        audio_success = self.audio_task.is_successful(env)
        logging.info("audio success: %s", audio_success)

        clock_success = self.clock_task.is_successful(env)
        logging.info("clock success: %s", clock_success)

        return (audio_success + clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
       audio_params=audio_recorder.AudioRecorderRecordAudioWithSettings.generate_random_params()
       clock_params=clock.ClockTimerEntry.generate_random_params()
       compound_params = {
           "sample_rate":audio_params["sample_rate"],
           "bit_rate": audio_params["bit_rate"],
           "hours":clock_params["hours"],
           "minutes":clock_params["minutes"],
           "seconds":clock_params["seconds"]
       }
       return  compound_params

class AudioRecorderRecordAudioWithSettingsAndClockStopWatchPaused(audio_recorder._AudioRecorder, clock._ClockEval):
    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "sample_rate": {"type": "string"},
            "bit_rate": {"type": "string"},
        },
        "required": ["sample_rate","bit_rate"],
    }
    template =  ("Record an audio clip with Sample rate {sample_rate} "
                 "and Bitrate {bit_rate} using Audio Recorder app and save it,then Pause the stopwatch in clock app."
                 )


    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.audio_task = audio_recorder.AudioRecorderRecordAudioWithSettings(
            params={"sample_rate": self.params["sample_rate"],
                    "bit_rate": self.params["bit_rate"],
                    }
        )
        self.clock_task=clock.ClockStopWatchPausedVerify(
            params={
            }
        )
        self.audio_task.initialize_task(env)
        self.clock_task.initialize_task(env)
    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        audio_success = self.audio_task.is_successful(env)
        logging.info("audio success: %s", audio_success)

        clock_success = self.clock_task.is_successful(env)
        logging.info("clock success: %s", clock_success)

        return (audio_success + clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
       audio_params=audio_recorder.AudioRecorderRecordAudioWithSettings.generate_random_params()
       compound_params = {
           "sample_rate":audio_params["sample_rate"],
           "bit_rate": audio_params["bit_rate"],
       }
       return  compound_params

class AudioRecorderRecordAudioWithSettingsAndClockStopWatchRunning(audio_recorder._AudioRecorder, clock._ClockEval):
    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "sample_rate": {"type": "string"},
            "bit_rate": {"type": "string"},
        },
        "required": ["sample_rate","bit_rate"],
    }
    template =  ("Record an audio clip with Sample rate {sample_rate} "
                 "and Bitrate {bit_rate} using Audio Recorder app and save it,then run the stopwatch in clock app."
                 )


    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.audio_task = audio_recorder.AudioRecorderRecordAudioWithSettings(
            params={"sample_rate": self.params["sample_rate"],
                    "bit_rate": self.params["bit_rate"],
                    }
        )
        self.clock_task=clock.ClockStopWatchRunning(
            params={
            }
        )
        self.audio_task.initialize_task(env)
        self.clock_task.initialize_task(env)
    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        audio_success = self.audio_task.is_successful(env)
        logging.info("audio success: %s", audio_success)

        clock_success = self.clock_task.is_successful(env)
        logging.info("clock success: %s", clock_success)

        return (audio_success + clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
       audio_params=audio_recorder.AudioRecorderRecordAudioWithSettings.generate_random_params()
       compound_params = {
           "sample_rate":audio_params["sample_rate"],
           "bit_rate": audio_params["bit_rate"],
       }
       return  compound_params

class AudioRecorderRecordAudioWithSettingsAndClockStopWatchRunningAndPaused(audio_recorder._AudioRecorder, clock._ClockEval):
    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "sample_rate": {"type": "string"},
            "bit_rate": {"type": "string"},
        },
        "required": ["sample_rate","bit_rate"],
    }
    template =  ("Record an audio clip with Sample rate {sample_rate} "
                 "and Bitrate {bit_rate} using Audio Recorder app and save it,then run the stopwatch,then pause it in clock app"
                 )


    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.audio_task = audio_recorder.AudioRecorderRecordAudioWithSettings(
            params={"sample_rate": self.params["sample_rate"],
                    "bit_rate": self.params["bit_rate"],
                    }
        )
        self.clock_task=clock.ClockStopWatchRunningAndPaused(
            params={
            }
        )
        self.audio_task.initialize_task(env)
        self.clock_task.initialize_task(env)
    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        audio_success = self.audio_task.is_successful(env)
        logging.info("audio success: %s", audio_success)

        clock_success = self.clock_task.is_successful(env)
        logging.info("clock success: %s", clock_success)

        return (audio_success + clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
       audio_params=audio_recorder.AudioRecorderRecordAudioWithSettings.generate_random_params()
       compound_params = {
           "sample_rate":audio_params["sample_rate"],
           "bit_rate": audio_params["bit_rate"],
       }
       return  compound_params

class AudioRecorderRecordAudioWithSettingsAndClockWatchRunningAndReset(audio_recorder._AudioRecorder, clock._ClockEval):
    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "sample_rate": {"type": "string"},
            "bit_rate": {"type": "string"},
        },
        "required": ["sample_rate","bit_rate"],
    }
    template =  ("Record an audio clip with Sample rate {sample_rate} "
                 "and Bitrate {bit_rate} using Audio Recorder app and save it,then Run the stopwatch and reset the stopwatch in clock app."
                 )


    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.audio_task = audio_recorder.AudioRecorderRecordAudioWithSettings(
            params={"sample_rate": self.params["sample_rate"],
                    "bit_rate": self.params["bit_rate"],
                    }
        )
        self.clock_task=clock.ClockWatchRunningAndReset(
            params={
            }
        )
        self.audio_task.initialize_task(env)
        self.clock_task.initialize_task(env)
    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        audio_success = self.audio_task.is_successful(env)
        logging.info("audio success: %s", audio_success)

        clock_success = self.clock_task.is_successful(env)
        logging.info("clock success: %s", clock_success)

        return (audio_success + clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
       audio_params=audio_recorder.AudioRecorderRecordAudioWithSettings.generate_random_params()
       compound_params = {
           "sample_rate":audio_params["sample_rate"],
           "bit_rate": audio_params["bit_rate"],
       }
       return  compound_params

class AudioRecorderRecordAudioWithFileNameAndClockStopWatchPaused(audio_recorder._AudioRecorder,clock._ClockEval):
  """Task for checking that one audio recording with file_name has been completed."""

  complexity = 3
  schema = file_validators.CreateFile.schema
  template = (
      'Record an audio clip and save it with name "{file_name}" using Audio'
      " Recorder app,then Pause the stopwatch in clock app."
  )

  def __init__(self, params: dict[str, Any]):
    """See base class."""
    super().__init__(params)
    self.initialized = False
    self.audio_task = audio_recorder.AudioRecorderRecordAudioWithFileName(
        params)
    self.clock_task = clock.ClockStopWatchPausedVerify(
        params={}
    )

  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    self.audio_task.initialize_task(env)
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    audio_success = self.audio_task.is_successful(env)
    logging.info("audio success: %s", audio_success)

    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)

    return (audio_success + clock_success) / 2.0

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
    self.audio_task.tear_down(env)

class AudioRecorderRecordAudioWithFileNameAndClockStopWatchRunning(audio_recorder._AudioRecorder,clock._ClockEval):
  """Task for checking that one audio recording with file_name has been completed."""

  complexity = 3
  schema = file_validators.CreateFile.schema
  template = (
      'Record an audio clip and save it with name "{file_name}" using Audio'
      " Recorder app,then Run the stopwatch in clock app."
  )

  def __init__(self, params: dict[str, Any]):
    """See base class."""
    super().__init__(params)
    self.initialized = False
    self.audio_task = audio_recorder.AudioRecorderRecordAudioWithFileName(
        params)
    self.clock_task = clock.ClockStopWatchRunning(
        params={}
    )

  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    self.audio_task.initialize_task(env)
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    audio_success = self.audio_task.is_successful(env)
    logging.info("audio success: %s", audio_success)

    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)

    return (audio_success + clock_success) / 2.0

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
    self.audio_task.tear_down(env)

class AudioRecorderRecordAudioWithFileNameAndClockStopWatchRunningAndPaused(audio_recorder._AudioRecorder,clock._ClockEval):
  """Task for checking that one audio recording with file_name has been completed."""

  complexity = 3
  schema = file_validators.CreateFile.schema
  template = (
      'Record an audio clip and save it with name "{file_name}" using Audio'
      " Recorder app,then Run the stopwatch and then Pause it in clock app."
  )

  def __init__(self, params: dict[str, Any]):
    """See base class."""
    super().__init__(params)
    self.initialized = False
    self.audio_task = audio_recorder.AudioRecorderRecordAudioWithFileName(
        params)
    self.clock_task = clock.ClockStopWatchRunningAndPaused(
        params={}
    )

  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    self.audio_task.initialize_task(env)
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    audio_success = self.audio_task.is_successful(env)
    logging.info("audio success: %s", audio_success)

    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)

    return (audio_success + clock_success) / 2.0

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
    self.audio_task.tear_down(env)

class AudioRecorderRecordAudioWithFileNameAndClockWatchRunningAndReset(audio_recorder._AudioRecorder,clock._ClockEval):
  """Task for checking that one audio recording with file_name has been completed."""

  complexity = 3
  schema = file_validators.CreateFile.schema
  template = (
      'Record an audio clip and save it with name "{file_name}" using Audio'
      " Recorder app,then Run the stopwatch and reset the stopwatch in clock app."
  )

  def __init__(self, params: dict[str, Any]):
    """See base class."""
    super().__init__(params)
    self.initialized = False
    self.audio_task = audio_recorder.AudioRecorderRecordAudioWithFileName(
        params)
    self.clock_task = clock.ClockWatchRunningAndReset(
        params={}
    )

  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    self.audio_task.initialize_task(env)
    self.clock_task.initialize_task(env)

  def is_successful(self, env: interface.AsyncEnv) -> float:
    super().is_successful(env)
    audio_success = self.audio_task.is_successful(env)
    logging.info("audio success: %s", audio_success)

    clock_success = self.clock_task.is_successful(env)
    logging.info("clock success: %s", clock_success)

    return (audio_success + clock_success) / 2.0

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
    self.audio_task.tear_down(env)

