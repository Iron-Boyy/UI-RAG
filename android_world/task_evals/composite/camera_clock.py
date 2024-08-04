from typing import Any
import subprocess
import random
from absl import logging
from android_world.env import interface
from android_world.env import representation_utils
from android_world.task_evals import task_eval
from android_world.task_evals.single import  clock
from android_world.task_evals.single import  camera

class CameraOpenAndClockOpen(camera._Camera, clock._ClockEval):
    complexity = 1
    schema = {}
    template = (
        "Open Clock App,then open camera app"
    )
    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.camera_task = camera.CameraOpen(
        params={}
    )
        self.clock_task = clock.ClockOpen(
        params={}
    )
        self.camera_task.initialize_task(env)
        self.clock_task.initialize_task(env)
    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        return self.camera_task.is_successful()

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class CameraTakeVideoAndClockOpen(camera._Camera, clock._ClockEval):
    complexity = 2
    schema = {}
    template = (
        "Take one video ,then open clock app"
    )
    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.camera_task = camera.CameraTakeVideo(
        params={}
    )
        self.clock_task = clock.ClockOpen(
        params={}
    )
        self.camera_task.initialize_task(env)
        self.clock_task.initialize_task(env)
    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        clock_success = self.clock_task.is_successful(env)
        logging.info("clock success: %s", clock_success)

        return (camera_success+ clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class CameraTakeVideosAndClockOpen(camera._Camera, clock._ClockEval):
    complexity = 2
    schema = {}
    template = (
        "Take two videos ,then open clock app"
    )
    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.camera_task = camera.CameraTakeVideos(
        params={}
    )
        self.clock_task = clock.ClockOpen(
        params={}
    )
        self.camera_task.initialize_task(env)
        self.clock_task.initialize_task(env)
    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        clock_success = self.clock_task.is_successful(env)
        logging.info("clock success: %s", clock_success)

        return (camera_success+ clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class CameraTakePhotoAndClockOpen(camera._Camera, clock._ClockEval):
    complexity = 2
    schema = {}
    template = (
        "Take one photo ,then open clock app"
    )
    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.camera_task = camera.CameraTakePhoto(
        params={}
    )
        self.clock_task = clock.ClockOpen(
        params={}
    )
        self.camera_task.initialize_task(env)
        self.clock_task.initialize_task(env)
    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        clock_success = self.clock_task.is_successful(env)
        logging.info("clock success: %s", clock_success)

        return (camera_success+ clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class CameraTakePhotosAndClockOpen(camera._Camera, clock._ClockEval):
    complexity = 2
    schema = {}
    template = (
        "Take three photos ,then open clock app"
    )
    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.camera_task = camera.CameraTakePhotos(
        params={}
    )
        self.clock_task = clock.ClockOpen(
        params={}
    )
        self.camera_task.initialize_task(env)
        self.clock_task.initialize_task(env)
    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        clock_success = self.clock_task.is_successful(env)
        logging.info("clock success: %s", clock_success)

        return (camera_success+ clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class CameraTakePhotoAndVideoAndClockOpen(camera._Camera, clock._ClockEval):
    complexity = 2
    schema = {}
    template = (
        "Take one photo and one video ,then open clock app"
    )
    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.camera_task = camera.CameraTakePhotoAndVideo(
        params={}
    )
        self.clock_task = clock.ClockOpen(
        params={}
    )
        self.camera_task.initialize_task(env)
        self.clock_task.initialize_task(env)
    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        clock_success = self.clock_task.is_successful(env)
        logging.info("clock success: %s", clock_success)

        return (camera_success+ clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class CameraTakePhotosAndVideosAndClockOpen(camera._Camera, clock._ClockEval):
    complexity = 3
    schema = {}
    template = (
        "Take five photos and two videos ,then open clock app"
    )
    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.camera_task = camera.CameraTakePhotosAndVideos(
        params={}
    )
        self.clock_task = clock.ClockOpen(
        params={}
    )
        self.camera_task.initialize_task(env)
        self.clock_task.initialize_task(env)
    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        clock_success = self.clock_task.is_successful(env)
        logging.info("clock success: %s", clock_success)

        return (camera_success+ clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class CameraTakeVideoAndClockStopWatchPaused(camera._Camera,clock._ClockEval):
    complexity = 2
    schema = {
        "type": "object",
        "properties": {},
        "required": [],
    }
    template = "Take one video, then Pause the stopwatch in clock app"

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.camera_task=camera.CameraTakeVideo(
            params={}
        )
        self.clock_task=clock.ClockStopWatchPausedVerify(
            params={}
        )
        self.camera_task.initialize_task(env)
        self.clock_task.initialize_task(env)
    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        clock_success = self.clock_task.is_successful(env)
        logging.info("clock success: %s", clock_success)

        return (camera_success+ clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        return {}
class CameraTakeVideoAndClockStopWatchRunning(camera._Camera, clock._ClockEval):
    complexity = 2
    schema = {
        "type": "object",
        "properties": {},
        "required": [],
    }
    template = "Take one video, then run the stopwatch in clock app"

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.camera_task = camera.CameraTakeVideo(
            params={}
        )
        self.clock_task = clock.ClockStopWatchRunning(
            params={}
        )
        self.camera_task.initialize_task(env)
        self.clock_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        clock_success = self.clock_task.is_successful(env)
        logging.info("clock success: %s", clock_success)

        return (camera_success + clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class CameraTakeVideoAndClockStopWatchRunningAndPaused(camera._Camera, clock._ClockEval):
    complexity = 2
    schema = {
        "type": "object",
        "properties": {},
        "required": [],
    }
    template = "Take one video, then Run the stopwatch and then Pause it in clock app"

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.camera_task = camera.CameraTakeVideo(
            params={}
        )
        self.clock_task = clock.ClockStopWatchRunningAndPaused(
            params={}
        )
        self.camera_task.initialize_task(env)
        self.clock_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        clock_success = self.clock_task.is_successful(env)
        logging.info("clock success: %s", clock_success)

        return (camera_success + clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class CameraOpenAndClockWatchRunningAndReset(camera._Camera, clock._ClockEval):
    complexity = 2
    schema = {
        "type": "object",
        "properties": {},
        "required": [],
    }
    template = "Run the stopwatch and reset the stopwatch in clock app,then open camera app"

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.camera_task = camera.CameraOpen(
            params={}
        )
        self.clock_task = clock.ClockWatchRunningAndReset(
            params={}
        )
        self.camera_task.initialize_task(env)
        self.clock_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        clock_success = self.clock_task.is_successful(env)
        logging.info("clock success: %s", clock_success)

        return (camera_success + clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        return {}
class CameraOpenAndClockStopWatchPaused(camera._Camera,clock._ClockEval):
    complexity = 2
    schema = {
        "type": "object",
        "properties": {},
        "required": [],
    }
    template = "Pause the stopwatch in clock app,then open camera app"

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.camera_task=camera.CameraOpen(
            params={}
        )
        self.clock_task=clock.ClockStopWatchPausedVerify(
            params={}
        )
        self.camera_task.initialize_task(env)
        self.clock_task.initialize_task(env)
    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        clock_success = self.clock_task.is_successful(env)
        logging.info("clock success: %s", clock_success)

        return (camera_success+ clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        return {}
class CameraOpenAndClockStopWatchRunning(camera._Camera, clock._ClockEval):
    complexity = 2
    schema = {
        "type": "object",
        "properties": {},
        "required": [],
    }
    template = "run the stopwatch in clock app,then open camera app"

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.camera_task = camera.CameraOpen(
            params={}
        )
        self.clock_task = clock.ClockStopWatchRunning(
            params={}
        )
        self.camera_task.initialize_task(env)
        self.clock_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        clock_success = self.clock_task.is_successful(env)
        logging.info("clock success: %s", clock_success)

        return (camera_success + clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class CameraOpenAndClockStopWatchRunningAndPaused(camera._Camera, clock._ClockEval):
    complexity = 2
    schema = {
        "type": "object",
        "properties": {},
        "required": [],
    }
    template = "Run the stopwatch and then Pause it in clock app,then open camera app"

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.camera_task = camera.CameraOpen(
            params={}
        )
        self.clock_task = clock.ClockStopWatchRunningAndPaused(
            params={}
        )
        self.camera_task.initialize_task(env)
        self.clock_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        clock_success = self.clock_task.is_successful(env)
        logging.info("clock success: %s", clock_success)

        return (camera_success + clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class CameraTakeVideoAndClockWatchRunningAndReset(camera._Camera, clock._ClockEval):
    complexity = 2
    schema = {
        "type": "object",
        "properties": {},
        "required": [],
    }
    template = "Take one video, then Run the stopwatch and reset the stopwatch in clock app"

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.camera_task = camera.CameraTakeVideo(
            params={}
        )
        self.clock_task = clock.ClockWatchRunningAndReset(
            params={}
        )
        self.camera_task.initialize_task(env)
        self.clock_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        clock_success = self.clock_task.is_successful(env)
        logging.info("clock success: %s", clock_success)

        return (camera_success + clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        return {}


class CameraTakeVideosAndClockStopWatchPaused(camera._Camera, clock._ClockEval):
    complexity = 3
    schema = {
        "type": "object",
        "properties": {},
        "required": [],
    }
    template = "Take two videos, then Pause the stopwatch in clock app"

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.camera_task = camera.CameraTakeVideos(
            params={}
        )
        self.clock_task = clock.ClockStopWatchPausedVerify(
            params={}
        )
        self.camera_task.initialize_task(env)
        self.clock_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        clock_success = self.clock_task.is_successful(env)
        logging.info("clock success: %s", clock_success)

        return (camera_success + clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        return {}


class CameraTakeVideosAndClockStopWatchRunning(camera._Camera, clock._ClockEval):
    complexity = 3
    schema = {
        "type": "object",
        "properties": {},
        "required": [],
    }
    template = "Take two videos, then run the stopwatch in clock app"

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.camera_task = camera.CameraTakeVideos(
            params={}
        )
        self.clock_task = clock.ClockStopWatchRunning(
            params={}
        )
        self.camera_task.initialize_task(env)
        self.clock_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        clock_success = self.clock_task.is_successful(env)
        logging.info("clock success: %s", clock_success)

        return (camera_success + clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        return {}


class CameraTakeVideosAndClockStopWatchRunningAndPaused(camera._Camera, clock._ClockEval):
    complexity = 3
    schema = {
        "type": "object",
        "properties": {},
        "required": [],
    }
    template = "Take two videos, then Run the stopwatch and then Pause it in clock app"

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.camera_task = camera.CameraTakeVideos(
            params={}
        )
        self.clock_task = clock.ClockStopWatchRunningAndPaused(
            params={}
        )
        self.camera_task.initialize_task(env)
        self.clock_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        clock_success = self.clock_task.is_successful(env)
        logging.info("clock success: %s", clock_success)

        return (camera_success + clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        return {}


class CameraTakeVideosAndClockWatchRunningAndReset(camera._Camera, clock._ClockEval):
    complexity = 3
    schema = {
        "type": "object",
        "properties": {},
        "required": [],
    }
    template = "Take two videos, then Run the stopwatch and reset the stopwatch in clock app"

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.camera_task = camera.CameraTakeVideos(
            params={}
        )
        self.clock_task = clock.ClockWatchRunningAndReset(
            params={}
        )
        self.camera_task.initialize_task(env)
        self.clock_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        clock_success = self.clock_task.is_successful(env)
        logging.info("clock success: %s", clock_success)

        return (camera_success + clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class CameraTakePhotoAndClockStopWatchPaused(camera._Camera,clock._ClockEval):
    complexity = 2
    schema = {
        "type": "object",
        "properties": {},
        "required": [],
    }
    template = "Take one photo, then Pause the stopwatch in clock app"

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.camera_task=camera.CameraTakePhoto(
            params={}
        )
        self.clock_task=clock.ClockStopWatchPausedVerify(
            params={}
        )
        self.camera_task.initialize_task(env)
        self.clock_task.initialize_task(env)
    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        clock_success = self.clock_task.is_successful(env)
        logging.info("clock success: %s", clock_success)

        return (camera_success+ clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class CameraTakePhotoAndClockStopWatchRunning(camera._Camera, clock._ClockEval):
    complexity = 2
    schema = {
        "type": "object",
        "properties": {},
        "required": [],
    }
    template = "Take one photo, then run the stopwatch in clock app"

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.camera_task = camera.CameraTakePhoto(
            params={}
        )
        self.clock_task = clock.ClockStopWatchRunning(
            params={}
        )
        self.camera_task.initialize_task(env)
        self.clock_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        clock_success = self.clock_task.is_successful(env)
        logging.info("clock success: %s", clock_success)

        return (camera_success + clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class CameraTakePhotoAndClockStopWatchRunningAndPaused(camera._Camera, clock._ClockEval):
    complexity = 2
    schema = {
        "type": "object",
        "properties": {},
        "required": [],
    }
    template = "Take one photo, then Run the stopwatch and then Pause it in clock app"

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.camera_task = camera.CameraTakePhoto(
            params={}
        )
        self.clock_task = clock.ClockStopWatchRunningAndPaused(
            params={}
        )
        self.camera_task.initialize_task(env)
        self.clock_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        clock_success = self.clock_task.is_successful(env)
        logging.info("clock success: %s", clock_success)

        return (camera_success + clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class CameraTakePhotoAndClockWatchRunningAndReset(camera._Camera, clock._ClockEval):
    complexity = 2
    schema = {
        "type": "object",
        "properties": {},
        "required": [],
    }
    template = "Take one photo, then Run the stopwatch and reset the stopwatch in clock app"

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.camera_task = camera.CameraTakePhoto(
            params={}
        )
        self.clock_task = clock.ClockWatchRunningAndReset(
            params={}
        )
        self.camera_task.initialize_task(env)
        self.clock_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        clock_success = self.clock_task.is_successful(env)
        logging.info("clock success: %s", clock_success)

        return (camera_success + clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class CameraTakePhotosAndClockStopWatchPaused(camera._Camera, clock._ClockEval):
    complexity = 3
    schema = {
        "type": "object",
        "properties": {},
        "required": [],
    }
    template = "Take three photos, then Pause the stopwatch in clock app"

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.camera_task = camera.CameraTakePhotos(
            params={}
        )
        self.clock_task = clock.ClockStopWatchPausedVerify(
            params={}
        )
        self.camera_task.initialize_task(env)
        self.clock_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        clock_success = self.clock_task.is_successful(env)
        logging.info("clock success: %s", clock_success)

        return (camera_success + clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class CameraTakePhotosAndClockStopWatchRunning(camera._Camera, clock._ClockEval):
    complexity = 3
    schema = {
        "type": "object",
        "properties": {},
        "required": [],
    }
    template = "Take three photos, then run the stopwatch in clock app"

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.camera_task = camera.CameraTakePhotos(
            params={}
        )
        self.clock_task = clock.ClockStopWatchRunning(
            params={}
        )
        self.camera_task.initialize_task(env)
        self.clock_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        clock_success = self.clock_task.is_successful(env)
        logging.info("clock success: %s", clock_success)

        return (camera_success + clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        return {}


class CameraTakePhotosAndClockStopWatchRunningAndPaused(camera._Camera, clock._ClockEval):
    complexity = 3
    schema = {
        "type": "object",
        "properties": {},
        "required": [],
    }
    template = "Take three photos, then Run the stopwatch and then Pause it in clock app"

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.camera_task = camera.CameraTakePhotos(
            params={}
        )
        self.clock_task = clock.ClockStopWatchRunningAndPaused(
            params={}
        )
        self.camera_task.initialize_task(env)
        self.clock_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        clock_success = self.clock_task.is_successful(env)
        logging.info("clock success: %s", clock_success)

        return (camera_success + clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class CameraTakePhotosAndClockWatchRunningAndReset(camera._Camera, clock._ClockEval):
    complexity = 3
    schema = {
        "type": "object",
        "properties": {},
        "required": [],
    }
    template = "Take three photos, then Run the stopwatch and reset the stopwatch in clock app"

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.camera_task = camera.CameraTakePhotos(
            params={}
        )
        self.clock_task = clock.ClockWatchRunningAndReset(
            params={}
        )
        self.camera_task.initialize_task(env)
        self.clock_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        clock_success = self.clock_task.is_successful(env)
        logging.info("clock success: %s", clock_success)

        return (camera_success + clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class CameraTakePhotoAndVideoAndClockStopWatchPaused(camera._Camera,clock._ClockEval):
    complexity = 3
    schema = {
        "type": "object",
        "properties": {},
        "required": [],
    }
    template = "Take one photo and one video, then Pause the stopwatch in clock app"

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.camera_task=camera.CameraTakePhotoAndVideo(
            params={}
        )
        self.clock_task=clock.ClockStopWatchPausedVerify(
            params={}
        )
        self.camera_task.initialize_task(env)
        self.clock_task.initialize_task(env)
    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        clock_success = self.clock_task.is_successful(env)
        logging.info("clock success: %s", clock_success)

        return (camera_success+ clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class CameraTakePhotoAndVideoAndClockStopWatchRunning(camera._Camera, clock._ClockEval):
    complexity = 3
    schema = {
        "type": "object",
        "properties": {},
        "required": [],
    }
    template = "Take one photo and one video, then run the stopwatch in clock app"

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.camera_task = camera.CameraTakePhotoAndVideo(
            params={}
        )
        self.clock_task = clock.ClockStopWatchRunning(
            params={}
        )
        self.camera_task.initialize_task(env)
        self.clock_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        clock_success = self.clock_task.is_successful(env)
        logging.info("clock success: %s", clock_success)

        return (camera_success + clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class CameraTakePhotoAndVideoAndClockStopWatchRunningAndPaused(camera._Camera, clock._ClockEval):
    complexity = 3
    schema = {
        "type": "object",
        "properties": {},
        "required": [],
    }
    template = "Take one photo and one video, then Run the stopwatch and then Pause it in clock app"

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.camera_task = camera.CameraTakePhotoAndVideo(
            params={}
        )
        self.clock_task = clock.ClockStopWatchRunningAndPaused(
            params={}
        )
        self.camera_task.initialize_task(env)
        self.clock_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        clock_success = self.clock_task.is_successful(env)
        logging.info("clock success: %s", clock_success)

        return (camera_success + clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class CameraTakePhotoAndAndClockWatchRunningAndReset(camera._Camera, clock._ClockEval):
    complexity = 2
    schema = {
        "type": "object",
        "properties": {},
        "required": [],
    }
    template = "Take one photo and one video, then Run the stopwatch and reset the stopwatch in clock app"

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.camera_task = camera.CameraTakePhotoAndVideo(
            params={}
        )
        self.clock_task = clock.ClockWatchRunningAndReset(
            params={}
        )
        self.camera_task.initialize_task(env)
        self.clock_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        clock_success = self.clock_task.is_successful(env)
        logging.info("clock success: %s", clock_success)

        return (camera_success + clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class CameraTakePhotosAndVideosAndClockStopWatchPaused(camera._Camera, clock._ClockEval):
    complexity = 3
    schema = {
        "type": "object",
        "properties": {},
        "required": [],
    }
    template = "Take five photos and two videos, then Pause the stopwatch in clock app"

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.camera_task = camera.CameraTakePhotosAndVideos(
            params={}
        )
        self.clock_task = clock.ClockStopWatchPausedVerify(
            params={}
        )
        self.camera_task.initialize_task(env)
        self.clock_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        clock_success = self.clock_task.is_successful(env)
        logging.info("clock success: %s", clock_success)

        return (camera_success + clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class CameraTakePhotosAndVideosAndClockStopWatchRunning(camera._Camera, clock._ClockEval):
    complexity = 3
    schema = {
        "type": "object",
        "properties": {},
        "required": [],
    }
    template = "Take five photos and two videos, then run the stopwatch in clock app"

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.camera_task = camera.CameraTakePhotosAndVideos(
            params={}
        )
        self.clock_task = clock.ClockStopWatchRunning(
            params={}
        )
        self.camera_task.initialize_task(env)
        self.clock_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        clock_success = self.clock_task.is_successful(env)
        logging.info("clock success: %s", clock_success)

        return (camera_success + clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class CameraTakePhotosAndVideosAndClockStopWatchRunningAndPaused(camera._Camera, clock._ClockEval):
    complexity = 3
    schema = {
        "type": "object",
        "properties": {},
        "required": [],
    }
    template = "TTake five photos and two videos., then Run the stopwatch and then Pause it in clock app"

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.camera_task = camera.CameraTakePhotosAndVideos(
            params={}
        )
        self.clock_task = clock.ClockStopWatchRunningAndPaused(
            params={}
        )
        self.camera_task.initialize_task(env)
        self.clock_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        clock_success = self.clock_task.is_successful(env)
        logging.info("clock success: %s", clock_success)

        return (camera_success + clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class CameraTakePhotosAndVideosAndClockWatchRunningAndReset(camera._Camera, clock._ClockEval):
    complexity = 3
    schema = {
        "type": "object",
        "properties": {},
        "required": [],
    }
    template = "Take five photos and two videos. , then Run the stopwatch and reset the stopwatch in clock app"

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.camera_task = camera.CameraTakePhotosAndVideos(
            params={}
        )
        self.clock_task = clock.ClockWatchRunningAndReset(
            params={}
        )
        self.camera_task.initialize_task(env)
        self.clock_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        clock_success = self.clock_task.is_successful(env)
        logging.info("clock success: %s", clock_success)

        return (camera_success + clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        return {}

class CameraTakeVideoAndClockEntry(camera._Camera, clock._ClockEval):
    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "hours": {"type": "integer"},
            "minutes": {"type": "integer"},
            "seconds": {"type": "integer"},
        },
        "required": ["hours", "minutes", "seconds"],
    }
    template = ("Take one video ,then"
            "Create a timer with {hours} hours, {minutes} minutes, and {seconds}"
            " seconds in clock app. Do not start the timer .")

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.camera_task = camera.CameraTakeVideo(
            params={}
        )
        self.clock_task = clock.ClockWatchRunningAndReset(
            params={"hours": self.params["hours"],
                    "minutes": self.params["minutes"],
                    "seconds": self.params["seconds"]
                    }
        )
        self.camera_task.initialize_task(env)
        self.clock_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        clock_success = self.clock_task.is_successful(env)
        logging.info("clock success: %s", clock_success)

        return (camera_success + clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        clock_params = clock.ClockTimerEntry.generate_random_params()
        return clock_params

class CameraTakeVideosAndClockEntry(camera._Camera, clock._ClockEval):
    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "hours": {"type": "integer"},
            "minutes": {"type": "integer"},
            "seconds": {"type": "integer"},
        },
        "required": ["hours", "minutes", "seconds"],
    }
    template = ("Take two videos ,then"
            "Create a timer with {hours} hours, {minutes} minutes, and {seconds}"
            " seconds in clock app. Do not start the timer .")

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.camera_task = camera.CameraTakeVideos(
            params={}
        )
        self.clock_task = clock.ClockWatchRunningAndReset(
            params={"hours": self.params["hours"],
                    "minutes": self.params["minutes"],
                    "seconds": self.params["seconds"]
                    }
        )
        self.camera_task.initialize_task(env)
        self.clock_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        clock_success = self.clock_task.is_successful(env)
        logging.info("clock success: %s", clock_success)

        return (camera_success + clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        clock_params = clock.ClockTimerEntry.generate_random_params()
        return clock_params

class CameraTakePhotoAndClockEntry(camera._Camera, clock._ClockEval):
    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "hours": {"type": "integer"},
            "minutes": {"type": "integer"},
            "seconds": {"type": "integer"},
        },
        "required": ["hours", "minutes", "seconds"],
    }
    template = ("Take one photo  ,then"
            "Create a timer with {hours} hours, {minutes} minutes, and {seconds}"
            " seconds in clock app. Do not start the timer .")

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.camera_task = camera.CameraTakePhoto(
            params={}
        )
        self.clock_task = clock.ClockWatchRunningAndReset(
            params={"hours": self.params["hours"],
                    "minutes": self.params["minutes"],
                    "seconds": self.params["seconds"]
                    }
        )
        self.camera_task.initialize_task(env)
        self.clock_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        clock_success = self.clock_task.is_successful(env)
        logging.info("clock success: %s", clock_success)

        return (camera_success + clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        clock_params = clock.ClockTimerEntry.generate_random_params()
        return clock_params

class CameraTakePhotosAndClockEntry(camera._Camera, clock._ClockEval):
    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "hours": {"type": "integer"},
            "minutes": {"type": "integer"},
            "seconds": {"type": "integer"},
        },
        "required": ["hours", "minutes", "seconds"],
    }
    template = ("Take three photos  ,then"
            "Create a timer with {hours} hours, {minutes} minutes, and {seconds}"
            " seconds in clock app. Do not start the timer .")

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.camera_task = camera.CameraTakePhotos(
            params={}
        )
        self.clock_task = clock.ClockWatchRunningAndReset(
            params={"hours": self.params["hours"],
                    "minutes": self.params["minutes"],
                    "seconds": self.params["seconds"]
                    }
        )
        self.camera_task.initialize_task(env)
        self.clock_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        clock_success = self.clock_task.is_successful(env)
        logging.info("clock success: %s", clock_success)

        return (camera_success + clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        clock_params = clock.ClockTimerEntry.generate_random_params()
        return clock_params


class CameraTakeVideoAndPhotoAndClockEntry(camera._Camera, clock._ClockEval):
    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "hours": {"type": "integer"},
            "minutes": {"type": "integer"},
            "seconds": {"type": "integer"},
        },
        "required": ["hours", "minutes", "seconds"],
    }
    template = ("Take one video and one photo ,then"
                "Create a timer with {hours} hours, {minutes} minutes, and {seconds}"
                " seconds in clock app. Do not start the timer .")

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.camera_task = camera.CameraTakePhotoAndVideo(
            params={}
        )
        self.clock_task = clock.ClockWatchRunningAndReset(
            params={"hours": self.params["hours"],
                    "minutes": self.params["minutes"],
                    "seconds": self.params["seconds"]
                    }
        )
        self.camera_task.initialize_task(env)
        self.clock_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        clock_success = self.clock_task.is_successful(env)
        logging.info("clock success: %s", clock_success)

        return (camera_success + clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        clock_params = clock.ClockTimerEntry.generate_random_params()
        return clock_params

class CameraTakeVideosAndPhotosAndClockEntry(camera._Camera, clock._ClockEval):
    complexity = 3
    schema = {
        "type": "object",
        "properties": {
            "hours": {"type": "integer"},
            "minutes": {"type": "integer"},
            "seconds": {"type": "integer"},
        },
        "required": ["hours", "minutes", "seconds"],
    }
    template = ("Take two videos and five photos ,then"
                "Create a timer with {hours} hours, {minutes} minutes, and {seconds}"
                " seconds in clock app. Do not start the timer .")

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.camera_task = camera.CameraTakePhotosAndVideos(
            params={}
        )
        self.clock_task = clock.ClockWatchRunningAndReset(
            params={"hours": self.params["hours"],
                    "minutes": self.params["minutes"],
                    "seconds": self.params["seconds"]
                    }
        )
        self.camera_task.initialize_task(env)
        self.clock_task.initialize_task(env)

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        camera_success = self.camera_task.is_successful(env)
        logging.info("camera success: %s", camera_success)

        clock_success = self.clock_task.is_successful(env)
        logging.info("clock success: %s", clock_success)

        return (camera_success + clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, str | int]:
        clock_params = clock.ClockTimerEntry.generate_random_params()
        return clock_params