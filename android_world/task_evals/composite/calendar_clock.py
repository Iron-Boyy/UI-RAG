import dataclasses
import random
import subprocess
from typing import Any, Callable, Optional
from android_world.env import device_constants
from android_world.env import interface
from android_world.task_evals.common_validators import sqlite_validators
from android_world.task_evals.single.calendar import calendar_evaluators
from android_world.task_evals.single.calendar import calendar_utils
from android_world.task_evals.single.calendar import events_generator
from android_world.task_evals.single import clock
from android_world.task_evals.single.calendar import calendar
from android_world.task_evals.utils import sqlite_schema_utils
from android_world.utils import datetime_utils

_YEAR = "year"
_MONTH = "month"
_DAY = "day"
_DAY_OF_WEEK = "day_of_week"
_HOUR = "hour"
_EVENT_TITLE = "event_title"
_EVENT_DESCRIPTION = "event_description"
_DURATION_MINS = "duration_mins"
_REPEAT_INTERVAL = "repeat_rule"
_REPEAT_INTERVALS = {"daily": 60 * 60 * 24, "weekly": 60 * 60 * 24 * 7}


def _generate_noise_events(
    target_events: list[sqlite_schema_utils.CalendarEvent],
    n: int,
    filter_fn: Optional[
        Callable[[sqlite_schema_utils.CalendarEvent], bool]
    ] = None,
) -> list[sqlite_schema_utils.CalendarEvent]:
  if filter_fn is None:
    target_titles = set(event.title for event in target_events)
    filter_fn = lambda candidate: candidate.title not in target_titles

  return sqlite_schema_utils.get_random_items(
      n,
      lambda: events_generator.generate_event(
          datetime_utils.create_random_october_2023_unix_ts(start_day=1)
      ),
      filter_fn=filter_fn,
  )

class _SimpleCalendarAndClock(sqlite_validators.SQLiteApp):
  """Base class for calendar tasks and evaluation logic.

                  October 2023
              Su Mo Tu We Th Fr Sa
              1  2  3  4  5  6  7
              8  9 10 11 12 13 14
              [15]16 17 18 19 20 21
              22 23 24 25 26 27 28
              29 30 31

  The current date on the emulator will be set as October 15, 2023.
  """

  app_name_with_db = "simple calendar pro"
  app_names = ("simple calendar pro","clock")
  schema = {}

  db_key = "id"
  db_path = calendar_utils.DB_PATH
  table_name = calendar_utils.EVENTS_TABLE
  row_type = sqlite_schema_utils.CalendarEvent

class SimpleCalendarAddOneEventAndStopWatchPaused(_SimpleCalendarAndClock, sqlite_validators.AddMultipleRows):
    complexity = 2
    schema = {
    }
    template = (
      "in Simple Calendar Pro, create a calendar event on {year}-{month}-{day}"
        " at {hour}h with the title '{event_title}' and the description"
        " '{event_description}'. The event should last for {duration_mins} mins , then pause the stop watch in clock app"
    )

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.clock_task=clock.ClockStopWatchPausedVerify(params={})
        self.clock_task.initialize_task(env)

    @classmethod
    def _get_random_target_row(cls) -> sqlite_schema_utils.CalendarEvent:
        """Generates a random calendar event."""
        return events_generator.generate_event(
            datetime_utils.create_random_october_2023_unix_ts()
        )

    def validate_addition_integrity(
            self,
            before: list[sqlite_schema_utils.CalendarEvent],
            after: list[sqlite_schema_utils.CalendarEvent],
            reference_rows: list[sqlite_schema_utils.CalendarEvent],
    ) -> bool:
        """Validates the integrity of the event addition."""
        return calendar_evaluators.validate_event_addition_integrity(
            before,
            after,
            reference_rows,
            extras_compare=["repeat_rule", "repeat_interval"],
        )

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        after = self.list_rows(env.base_env)
        row_addition_successful = self.validate_addition_integrity(
            self.before, after, self.params["row_objects"]
        )
        if row_addition_successful: row_success=1
        else : row_success = 0

        clock_success = self.clock_task.is_successful(env)

        return (row_success + clock_success) / 2.0
    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        event = cls._get_random_target_row()
        n_noise_events = random.randint(0, 20)
        return {

            _YEAR: device_constants.DT.year,
            _MONTH: device_constants.DT.month,
            _DAY: event.start_datetime.day,
            _HOUR: event.start_datetime.hour,
            _DURATION_MINS: event.duration_mins,
            _EVENT_TITLE: event.title,
            _EVENT_DESCRIPTION: event.description,
            sqlite_validators.ROW_OBJECTS: [event],
            sqlite_validators.NOISE_ROW_OBJECTS: _generate_noise_events(
                [event], n_noise_events
            ),
        }

class SimpleCalendarAddOneEventAndClockStopWatchRunning(_SimpleCalendarAndClock, sqlite_validators.AddMultipleRows):
    complexity = 2
    schema = {
    }
    template = (
      "in Simple Calendar Pro, create a calendar event on {year}-{month}-{day}"
        " at {hour}h with the title '{event_title}' and the description"
        " '{event_description}'. The event should last for {duration_mins} mins , then run the stop watch in clock app"
    )

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.clock_task=clock.ClockStopWatchRunning(params={})
        self.clock_task.initialize_task(env)
    @classmethod
    def _get_random_target_row(cls) -> sqlite_schema_utils.CalendarEvent:
        """Generates a random calendar event."""
        return events_generator.generate_event(
            datetime_utils.create_random_october_2023_unix_ts()
        )

    def validate_addition_integrity(
            self,
            before: list[sqlite_schema_utils.CalendarEvent],
            after: list[sqlite_schema_utils.CalendarEvent],
            reference_rows: list[sqlite_schema_utils.CalendarEvent],
    ) -> bool:
        """Validates the integrity of the event addition."""
        return calendar_evaluators.validate_event_addition_integrity(
            before,
            after,
            reference_rows,
            extras_compare=["repeat_rule", "repeat_interval"],
        )

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        after = self.list_rows(env.base_env)
        row_addition_successful = self.validate_addition_integrity(
            self.before, after, self.params["row_objects"]
        )
        if row_addition_successful: row_success=1
        else : row_success = 0

        clock_success = self.clock_task.is_successful(env)

        return (row_success + clock_success) / 2.0
    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        event = cls._get_random_target_row()
        n_noise_events = random.randint(0, 20)
        return {

            _YEAR: device_constants.DT.year,
            _MONTH: device_constants.DT.month,
            _DAY: event.start_datetime.day,
            _HOUR: event.start_datetime.hour,
            _DURATION_MINS: event.duration_mins,
            _EVENT_TITLE: event.title,
            _EVENT_DESCRIPTION: event.description,
            sqlite_validators.ROW_OBJECTS: [event],
            sqlite_validators.NOISE_ROW_OBJECTS: _generate_noise_events(
                [event], n_noise_events
            ),
        }

class SimpleCalendarAddOneEventAndClockStopWatchRunningAndPaused(_SimpleCalendarAndClock, sqlite_validators.AddMultipleRows):
    complexity = 2
    schema = {
    }
    template = (
      "in Simple Calendar Pro, create a calendar event on {year}-{month}-{day}"
        " at {hour}h with the title '{event_title}' and the description"
        " '{event_description}'. The event should last for {duration_mins} mins "
      " then Run the stopwatch and then Pause it in clock app"
    )

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.clock_task=clock.ClockStopWatchRunningAndPaused(params={})
        self.clock_task.initialize_task(env)

    @classmethod
    def _get_random_target_row(cls) -> sqlite_schema_utils.CalendarEvent:
        """Generates a random calendar event."""
        return events_generator.generate_event(
            datetime_utils.create_random_october_2023_unix_ts()
        )

    def validate_addition_integrity(
            self,
            before: list[sqlite_schema_utils.CalendarEvent],
            after: list[sqlite_schema_utils.CalendarEvent],
            reference_rows: list[sqlite_schema_utils.CalendarEvent],
    ) -> bool:
        """Validates the integrity of the event addition."""
        return calendar_evaluators.validate_event_addition_integrity(
            before,
            after,
            reference_rows,
            extras_compare=["repeat_rule", "repeat_interval"],
        )

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        after = self.list_rows(env.base_env)
        row_addition_successful = self.validate_addition_integrity(
            self.before, after, self.params["row_objects"]
        )
        if row_addition_successful: row_success=1
        else : row_success = 0

        clock_success = self.clock_task.is_successful(env)

        return (row_success + clock_success) / 2.0
    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        event = cls._get_random_target_row()
        n_noise_events = random.randint(0, 20)
        return {

            _YEAR: device_constants.DT.year,
            _MONTH: device_constants.DT.month,
            _DAY: event.start_datetime.day,
            _HOUR: event.start_datetime.hour,
            _DURATION_MINS: event.duration_mins,
            _EVENT_TITLE: event.title,
            _EVENT_DESCRIPTION: event.description,
            sqlite_validators.ROW_OBJECTS: [event],
            sqlite_validators.NOISE_ROW_OBJECTS: _generate_noise_events(
                [event], n_noise_events
            ),
        }

class SimpleCalendarAddOneEventAndClockWatchRunningAndReset(_SimpleCalendarAndClock, sqlite_validators.AddMultipleRows):
    complexity = 2
    schema = {
    }
    template = (
      "in Simple Calendar Pro, create a calendar event on {year}-{month}-{day}"
        " at {hour}h with the title '{event_title}' and the description"
        " '{event_description}'. The event should last for {duration_mins} mins "
      " then Run the stopwatch and reset the stopwatch in clock app"
    )

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.clock_task=clock.ClockWatchRunningAndReset(params={})
        self.clock_task.initialize_task(env)

    @classmethod
    def _get_random_target_row(cls) -> sqlite_schema_utils.CalendarEvent:
        """Generates a random calendar event."""
        return events_generator.generate_event(
            datetime_utils.create_random_october_2023_unix_ts()
        )

    def validate_addition_integrity(
            self,
            before: list[sqlite_schema_utils.CalendarEvent],
            after: list[sqlite_schema_utils.CalendarEvent],
            reference_rows: list[sqlite_schema_utils.CalendarEvent],
    ) -> bool:
        """Validates the integrity of the event addition."""
        return calendar_evaluators.validate_event_addition_integrity(
            before,
            after,
            reference_rows,
            extras_compare=["repeat_rule", "repeat_interval"],
        )

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        after = self.list_rows(env.base_env)
        row_addition_successful = self.validate_addition_integrity(
            self.before, after, self.params["row_objects"]
        )
        if row_addition_successful: row_success=1
        else : row_success = 0

        clock_success = self.clock_task.is_successful(env)

        return (row_success + clock_success) / 2.0
    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        event = cls._get_random_target_row()
        n_noise_events = random.randint(0, 20)
        return {

            _YEAR: device_constants.DT.year,
            _MONTH: device_constants.DT.month,
            _DAY: event.start_datetime.day,
            _HOUR: event.start_datetime.hour,
            _DURATION_MINS: event.duration_mins,
            _EVENT_TITLE: event.title,
            _EVENT_DESCRIPTION: event.description,
            sqlite_validators.ROW_OBJECTS: [event],
            sqlite_validators.NOISE_ROW_OBJECTS: _generate_noise_events(
                [event], n_noise_events
            ),
        }

class SimpleCalendarAddOneEventTomorrowAndStopWatchPaused(_SimpleCalendarAndClock, sqlite_validators.AddMultipleRows):
    complexity = 2
    schema = {
    }
    template = (
      "in Simple Calendar Pro, create a calendar event for tomorrow"
        " at {hour}h with the title '{event_title}' and the description"
        " '{event_description}'. The event should last for {duration_mins} mins , then pause the stop watch in clock app"
    )

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.clock_task=clock.ClockStopWatchPausedVerify(params={})
        self.clock_task.initialize_task(env)

    @classmethod
    def _get_random_target_row(cls):
        # Generate an event for tomorrow.
        return events_generator.generate_event(
            datetime_utils.create_random_october_2023_unix_ts(
                device_constants.DT.day + 1, device_constants.DT.day + 1
            )
        )
    def validate_addition_integrity(
            self,
            before: list[sqlite_schema_utils.CalendarEvent],
            after: list[sqlite_schema_utils.CalendarEvent],
            reference_rows: list[sqlite_schema_utils.CalendarEvent],
    ) -> bool:
        """Validates the integrity of the event addition."""
        return calendar_evaluators.validate_event_addition_integrity(
            before,
            after,
            reference_rows,
            extras_compare=["repeat_rule", "repeat_interval"],
        )

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        after = self.list_rows(env.base_env)
        row_addition_successful = self.validate_addition_integrity(
            self.before, after, self.params["row_objects"]
        )
        if row_addition_successful: row_success=1
        else : row_success = 0

        clock_success = self.clock_task.is_successful(env)

        return (row_success + clock_success) / 2.0
    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        event = cls._get_random_target_row()
        n_noise_events = random.randint(0, 20)
        return {

            _YEAR: device_constants.DT.year,
            _MONTH: device_constants.DT.month,
            _DAY: event.start_datetime.day,
            _HOUR: event.start_datetime.hour,
            _DURATION_MINS: event.duration_mins,
            _EVENT_TITLE: event.title,
            _EVENT_DESCRIPTION: event.description,
            sqlite_validators.ROW_OBJECTS: [event],
            sqlite_validators.NOISE_ROW_OBJECTS: _generate_noise_events(
                [event], n_noise_events
            ),
        }

class SimpleCalendarAddOneEventTomorrowAndClockStopWatchRunning(_SimpleCalendarAndClock, sqlite_validators.AddMultipleRows):
    complexity = 2
    schema = {
    }
    template = (
      "in Simple Calendar Pro, create a calendar event for tomorrow"
        " at {hour}h with the title '{event_title}' and the description"
        " '{event_description}'. The event should last for {duration_mins} mins , then run the stop watch in clock app"
    )

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.clock_task=clock.ClockStopWatchRunning(params={})
        self.clock_task.initialize_task(env)
    @classmethod
    def _get_random_target_row(cls):
        # Generate an event for tomorrow.
        return events_generator.generate_event(
            datetime_utils.create_random_october_2023_unix_ts(
                device_constants.DT.day + 1, device_constants.DT.day + 1
            )
        )

    def validate_addition_integrity(
            self,
            before: list[sqlite_schema_utils.CalendarEvent],
            after: list[sqlite_schema_utils.CalendarEvent],
            reference_rows: list[sqlite_schema_utils.CalendarEvent],
    ) -> bool:
        """Validates the integrity of the event addition."""
        return calendar_evaluators.validate_event_addition_integrity(
            before,
            after,
            reference_rows,
            extras_compare=["repeat_rule", "repeat_interval"],
        )

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        after = self.list_rows(env.base_env)
        row_addition_successful = self.validate_addition_integrity(
            self.before, after, self.params["row_objects"]
        )
        if row_addition_successful: row_success=1
        else : row_success = 0

        clock_success = self.clock_task.is_successful(env)

        return (row_success + clock_success) / 2.0
    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        event = cls._get_random_target_row()
        n_noise_events = random.randint(0, 20)
        return {

            _YEAR: device_constants.DT.year,
            _MONTH: device_constants.DT.month,
            _DAY: event.start_datetime.day,
            _HOUR: event.start_datetime.hour,
            _DURATION_MINS: event.duration_mins,
            _EVENT_TITLE: event.title,
            _EVENT_DESCRIPTION: event.description,
            sqlite_validators.ROW_OBJECTS: [event],
            sqlite_validators.NOISE_ROW_OBJECTS: _generate_noise_events(
                [event], n_noise_events
            ),
        }

class SimpleCalendarAddOneEventTomorrowAndClockStopWatchRunningAndPaused(_SimpleCalendarAndClock, sqlite_validators.AddMultipleRows):
    complexity = 2
    schema = {
    }
    template = (
      "in Simple Calendar Pro, create a calendar event for tomorrow"
        " at {hour}h with the title '{event_title}' and the description"
        " '{event_description}'. The event should last for {duration_mins} mins "
      " then Run the stopwatch and then Pause it in clock app"
    )

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.clock_task=clock.ClockStopWatchRunningAndPaused(params={})
        self.clock_task.initialize_task(env)

    @classmethod
    def _get_random_target_row(cls):
        # Generate an event for tomorrow.
        return events_generator.generate_event(
            datetime_utils.create_random_october_2023_unix_ts(
                device_constants.DT.day + 1, device_constants.DT.day + 1
            )
        )

    def validate_addition_integrity(
            self,
            before: list[sqlite_schema_utils.CalendarEvent],
            after: list[sqlite_schema_utils.CalendarEvent],
            reference_rows: list[sqlite_schema_utils.CalendarEvent],
    ) -> bool:
        """Validates the integrity of the event addition."""
        return calendar_evaluators.validate_event_addition_integrity(
            before,
            after,
            reference_rows,
            extras_compare=["repeat_rule", "repeat_interval"],
        )

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        after = self.list_rows(env.base_env)
        row_addition_successful = self.validate_addition_integrity(
            self.before, after, self.params["row_objects"]
        )
        if row_addition_successful: row_success=1
        else : row_success = 0

        clock_success = self.clock_task.is_successful(env)

        return (row_success + clock_success) / 2.0
    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        event = cls._get_random_target_row()
        n_noise_events = random.randint(0, 20)
        return {

            _YEAR: device_constants.DT.year,
            _MONTH: device_constants.DT.month,
            _DAY: event.start_datetime.day,
            _HOUR: event.start_datetime.hour,
            _DURATION_MINS: event.duration_mins,
            _EVENT_TITLE: event.title,
            _EVENT_DESCRIPTION: event.description,
            sqlite_validators.ROW_OBJECTS: [event],
            sqlite_validators.NOISE_ROW_OBJECTS: _generate_noise_events(
                [event], n_noise_events
            ),
        }

class SimpleCalendarAddOneEventTomorrowAndClockWatchRunningAndReset(_SimpleCalendarAndClock, sqlite_validators.AddMultipleRows):
    complexity = 2
    schema = {
    }
    template = (
      "in Simple Calendar Pro, create a calendar event for tomorrow"
        " at {hour}h with the title '{event_title}' and the description"
        " '{event_description}'. The event should last for {duration_mins} mins "
      " then Run the stopwatch and reset the stopwatch in clock app"
    )

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.clock_task=clock.ClockWatchRunningAndReset(params={})
        self.clock_task.initialize_task(env)

    @classmethod
    def _get_random_target_row(cls):
        # Generate an event for tomorrow.
        return events_generator.generate_event(
            datetime_utils.create_random_october_2023_unix_ts(
                device_constants.DT.day + 1, device_constants.DT.day + 1
            )
        )

    def validate_addition_integrity(
            self,
            before: list[sqlite_schema_utils.CalendarEvent],
            after: list[sqlite_schema_utils.CalendarEvent],
            reference_rows: list[sqlite_schema_utils.CalendarEvent],
    ) -> bool:
        """Validates the integrity of the event addition."""
        return calendar_evaluators.validate_event_addition_integrity(
            before,
            after,
            reference_rows,
            extras_compare=["repeat_rule", "repeat_interval"],
        )

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        after = self.list_rows(env.base_env)
        row_addition_successful = self.validate_addition_integrity(
            self.before, after, self.params["row_objects"]
        )
        if row_addition_successful: row_success=1
        else : row_success = 0

        clock_success = self.clock_task.is_successful(env)

        return (row_success + clock_success) / 2.0
    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        event = cls._get_random_target_row()
        n_noise_events = random.randint(0, 20)
        return {

            _YEAR: device_constants.DT.year,
            _MONTH: device_constants.DT.month,
            _DAY: event.start_datetime.day,
            _HOUR: event.start_datetime.hour,
            _DURATION_MINS: event.duration_mins,
            _EVENT_TITLE: event.title,
            _EVENT_DESCRIPTION: event.description,
            sqlite_validators.ROW_OBJECTS: [event],
            sqlite_validators.NOISE_ROW_OBJECTS: _generate_noise_events(
                [event], n_noise_events
            ),
        }

class SimpleCalendarAddOneEventInOneWeekAndStopWatchPaused(_SimpleCalendarAndClock, sqlite_validators.AddMultipleRows):
    complexity = 2
    schema = {
    }
    template = (
      "in Simple Calendar Pro, create a calendar event in one week from today"
        " at {hour}h with the title '{event_title}' and the description"
        " '{event_description}'. The event should last for {duration_mins} mins , then pause the stop watch in clock app"
    )

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.clock_task=clock.ClockStopWatchPausedVerify(params={})
        self.clock_task.initialize_task(env)

    @classmethod
    def _get_random_target_row(cls):
        # Generate an event for InOneWeek.
        return events_generator.generate_event(
            datetime_utils.create_random_october_2023_unix_ts(
                device_constants.DT.day + 7, device_constants.DT.day + 7
            )
        )
    def validate_addition_integrity(
            self,
            before: list[sqlite_schema_utils.CalendarEvent],
            after: list[sqlite_schema_utils.CalendarEvent],
            reference_rows: list[sqlite_schema_utils.CalendarEvent],
    ) -> bool:
        """Validates the integrity of the event addition."""
        return calendar_evaluators.validate_event_addition_integrity(
            before,
            after,
            reference_rows,
            extras_compare=["repeat_rule", "repeat_interval"],
        )

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        after = self.list_rows(env.base_env)
        row_addition_successful = self.validate_addition_integrity(
            self.before, after, self.params["row_objects"]
        )
        if row_addition_successful: row_success=1
        else : row_success = 0

        clock_success = self.clock_task.is_successful(env)

        return (row_success + clock_success) / 2.0
    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        event = cls._get_random_target_row()
        n_noise_events = random.randint(0, 20)
        return {

            _YEAR: device_constants.DT.year,
            _MONTH: device_constants.DT.month,
            _DAY: event.start_datetime.day,
            _HOUR: event.start_datetime.hour,
            _DURATION_MINS: event.duration_mins,
            _EVENT_TITLE: event.title,
            _EVENT_DESCRIPTION: event.description,
            sqlite_validators.ROW_OBJECTS: [event],
            sqlite_validators.NOISE_ROW_OBJECTS: _generate_noise_events(
                [event], n_noise_events
            ),
        }

class SimpleCalendarAddOneEventInOneWeekAndClockStopWatchRunning(_SimpleCalendarAndClock, sqlite_validators.AddMultipleRows):
    complexity = 2
    schema = {
    }
    template = (
      "in Simple Calendar Pro, create a calendar event in one week from today"
        " at {hour}h with the title '{event_title}' and the description"
        " '{event_description}'. The event should last for {duration_mins} mins , then run the stop watch in clock app"
    )

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.clock_task=clock.ClockStopWatchRunning(params={})
        self.clock_task.initialize_task(env)
    @classmethod
    def _get_random_target_row(cls):
        # Generate an event for InOneWeek.
        return events_generator.generate_event(
            datetime_utils.create_random_october_2023_unix_ts(
                device_constants.DT.day + 7, device_constants.DT.day + 7
            )
        )

    def validate_addition_integrity(
            self,
            before: list[sqlite_schema_utils.CalendarEvent],
            after: list[sqlite_schema_utils.CalendarEvent],
            reference_rows: list[sqlite_schema_utils.CalendarEvent],
    ) -> bool:
        """Validates the integrity of the event addition."""
        return calendar_evaluators.validate_event_addition_integrity(
            before,
            after,
            reference_rows,
            extras_compare=["repeat_rule", "repeat_interval"],
        )

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        after = self.list_rows(env.base_env)
        row_addition_successful = self.validate_addition_integrity(
            self.before, after, self.params["row_objects"]
        )
        if row_addition_successful: row_success=1
        else : row_success = 0

        clock_success = self.clock_task.is_successful(env)

        return (row_success + clock_success) / 2.0
    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        event = cls._get_random_target_row()
        n_noise_events = random.randint(0, 20)
        return {

            _YEAR: device_constants.DT.year,
            _MONTH: device_constants.DT.month,
            _DAY: event.start_datetime.day,
            _HOUR: event.start_datetime.hour,
            _DURATION_MINS: event.duration_mins,
            _EVENT_TITLE: event.title,
            _EVENT_DESCRIPTION: event.description,
            sqlite_validators.ROW_OBJECTS: [event],
            sqlite_validators.NOISE_ROW_OBJECTS: _generate_noise_events(
                [event], n_noise_events
            ),
        }

class SimpleCalendarAddOneEventInOneWeekAndClockStopWatchRunningAndPaused(_SimpleCalendarAndClock, sqlite_validators.AddMultipleRows):
    complexity = 2
    schema = {
    }
    template = (
      "in Simple Calendar Pro, create a calendar event in one week from today"
        " at {hour}h with the title '{event_title}' and the description"
        " '{event_description}'. The event should last for {duration_mins} mins "
      " then Run the stopwatch and then Pause it in clock app"
    )

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.clock_task=clock.ClockStopWatchRunningAndPaused(params={})
        self.clock_task.initialize_task(env)

    @classmethod
    def _get_random_target_row(cls):
        # Generate an event for InOneWeek.
        return events_generator.generate_event(
            datetime_utils.create_random_october_2023_unix_ts(
                device_constants.DT.day + 7, device_constants.DT.day + 7
            )
        )

    def validate_addition_integrity(
            self,
            before: list[sqlite_schema_utils.CalendarEvent],
            after: list[sqlite_schema_utils.CalendarEvent],
            reference_rows: list[sqlite_schema_utils.CalendarEvent],
    ) -> bool:
        """Validates the integrity of the event addition."""
        return calendar_evaluators.validate_event_addition_integrity(
            before,
            after,
            reference_rows,
            extras_compare=["repeat_rule", "repeat_interval"],
        )

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        after = self.list_rows(env.base_env)
        row_addition_successful = self.validate_addition_integrity(
            self.before, after, self.params["row_objects"]
        )
        if row_addition_successful: row_success=1
        else : row_success = 0

        clock_success = self.clock_task.is_successful(env)

        return (row_success + clock_success) / 2.0
    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        event = cls._get_random_target_row()
        n_noise_events = random.randint(0, 20)
        return {

            _YEAR: device_constants.DT.year,
            _MONTH: device_constants.DT.month,
            _DAY: event.start_datetime.day,
            _HOUR: event.start_datetime.hour,
            _DURATION_MINS: event.duration_mins,
            _EVENT_TITLE: event.title,
            _EVENT_DESCRIPTION: event.description,
            sqlite_validators.ROW_OBJECTS: [event],
            sqlite_validators.NOISE_ROW_OBJECTS: _generate_noise_events(
                [event], n_noise_events
            ),
        }

class SimpleCalendarAddOneEventInOneWeekAndClockWatchRunningAndReset(_SimpleCalendarAndClock, sqlite_validators.AddMultipleRows):
    complexity = 2
    schema = {
    }
    template = (
      "in Simple Calendar Pro, create a calendar event in one week from today"
        " at {hour}h with the title '{event_title}' and the description"
        " '{event_description}'. The event should last for {duration_mins} mins "
      " then Run the stopwatch and reset the stopwatch in clock app"
    )

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.clock_task=clock.ClockWatchRunningAndReset(params={})
        self.clock_task.initialize_task(env)

    @classmethod
    def _get_random_target_row(cls):
        # Generate an event for InOneWeek.
        return events_generator.generate_event(
            datetime_utils.create_random_october_2023_unix_ts(
                device_constants.DT.day + 7, device_constants.DT.day + 7
            )
        )

    def validate_addition_integrity(
            self,
            before: list[sqlite_schema_utils.CalendarEvent],
            after: list[sqlite_schema_utils.CalendarEvent],
            reference_rows: list[sqlite_schema_utils.CalendarEvent],
    ) -> bool:
        """Validates the integrity of the event addition."""
        return calendar_evaluators.validate_event_addition_integrity(
            before,
            after,
            reference_rows,
            extras_compare=["repeat_rule", "repeat_interval"],
        )

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        after = self.list_rows(env.base_env)
        row_addition_successful = self.validate_addition_integrity(
            self.before, after, self.params["row_objects"]
        )
        if row_addition_successful: row_success=1
        else : row_success = 0

        clock_success = self.clock_task.is_successful(env)

        return (row_success + clock_success) / 2.0
    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        event = cls._get_random_target_row()
        n_noise_events = random.randint(0, 20)
        return {

            _YEAR: device_constants.DT.year,
            _MONTH: device_constants.DT.month,
            _DAY: event.start_datetime.day,
            _HOUR: event.start_datetime.hour,
            _DURATION_MINS: event.duration_mins,
            _EVENT_TITLE: event.title,
            _EVENT_DESCRIPTION: event.description,
            sqlite_validators.ROW_OBJECTS: [event],
            sqlite_validators.NOISE_ROW_OBJECTS: _generate_noise_events(
                [event], n_noise_events
            ),
        }


class SimpleCalendarAddOneEventInTwoWeeksAndStopWatchPaused(_SimpleCalendarAndClock, sqlite_validators.AddMultipleRows):
    complexity = 2
    schema = {
    }
    template = (
      "in Simple Calendar Pro, create a calendar event in two weeks from today"
        " at {hour}h with the title '{event_title}' and the description"
        " '{event_description}'. The event should last for {duration_mins} mins , then pause the stop watch in clock app"
    )

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.clock_task=clock.ClockStopWatchPausedVerify(params={})
        self.clock_task.initialize_task(env)

    @classmethod
    def _get_random_target_row(cls):
        # Generate an event for InTwoWeeks.
        return events_generator.generate_event(
            datetime_utils.create_random_october_2023_unix_ts(
                device_constants.DT.day + 14, device_constants.DT.day + 14
            )
        )
    def validate_addition_integrity(
            self,
            before: list[sqlite_schema_utils.CalendarEvent],
            after: list[sqlite_schema_utils.CalendarEvent],
            reference_rows: list[sqlite_schema_utils.CalendarEvent],
    ) -> bool:
        """Validates the integrity of the event addition."""
        return calendar_evaluators.validate_event_addition_integrity(
            before,
            after,
            reference_rows,
            extras_compare=["repeat_rule", "repeat_interval"],
        )

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        after = self.list_rows(env.base_env)
        row_addition_successful = self.validate_addition_integrity(
            self.before, after, self.params["row_objects"]
        )
        if row_addition_successful: row_success=1
        else : row_success = 0

        clock_success = self.clock_task.is_successful(env)

        return (row_success + clock_success) / 2.0
    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        event = cls._get_random_target_row()
        n_noise_events = random.randint(0, 20)
        return {

            _YEAR: device_constants.DT.year,
            _MONTH: device_constants.DT.month,
            _DAY: event.start_datetime.day,
            _HOUR: event.start_datetime.hour,
            _DURATION_MINS: event.duration_mins,
            _EVENT_TITLE: event.title,
            _EVENT_DESCRIPTION: event.description,
            sqlite_validators.ROW_OBJECTS: [event],
            sqlite_validators.NOISE_ROW_OBJECTS: _generate_noise_events(
                [event], n_noise_events
            ),
        }

class SimpleCalendarAddOneEventInTwoWeeksAndClockStopWatchRunning(_SimpleCalendarAndClock, sqlite_validators.AddMultipleRows):
    complexity = 2
    schema = {
    }
    template = (
      "in Simple Calendar Pro, create a calendar event in two weeks from today"
        " at {hour}h with the title '{event_title}' and the description"
        " '{event_description}'. The event should last for {duration_mins} mins , then run the stop watch in clock app"
    )

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.clock_task=clock.ClockStopWatchRunning(params={})
        self.clock_task.initialize_task(env)
    @classmethod
    def _get_random_target_row(cls):
        # Generate an event for InTwoWeeks.
        return events_generator.generate_event(
            datetime_utils.create_random_october_2023_unix_ts(
                device_constants.DT.day + 14, device_constants.DT.day + 14
            )
        )

    def validate_addition_integrity(
            self,
            before: list[sqlite_schema_utils.CalendarEvent],
            after: list[sqlite_schema_utils.CalendarEvent],
            reference_rows: list[sqlite_schema_utils.CalendarEvent],
    ) -> bool:
        """Validates the integrity of the event addition."""
        return calendar_evaluators.validate_event_addition_integrity(
            before,
            after,
            reference_rows,
            extras_compare=["repeat_rule", "repeat_interval"],
        )

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        after = self.list_rows(env.base_env)
        row_addition_successful = self.validate_addition_integrity(
            self.before, after, self.params["row_objects"]
        )
        if row_addition_successful: row_success=1
        else : row_success = 0

        clock_success = self.clock_task.is_successful(env)

        return (row_success + clock_success) / 2.0
    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        event = cls._get_random_target_row()
        n_noise_events = random.randint(0, 20)
        return {

            _YEAR: device_constants.DT.year,
            _MONTH: device_constants.DT.month,
            _DAY: event.start_datetime.day,
            _HOUR: event.start_datetime.hour,
            _DURATION_MINS: event.duration_mins,
            _EVENT_TITLE: event.title,
            _EVENT_DESCRIPTION: event.description,
            sqlite_validators.ROW_OBJECTS: [event],
            sqlite_validators.NOISE_ROW_OBJECTS: _generate_noise_events(
                [event], n_noise_events
            ),
        }

class SimpleCalendarAddOneEventInTwoWeeksAndClockStopWatchRunningAndPaused(_SimpleCalendarAndClock, sqlite_validators.AddMultipleRows):
    complexity = 2
    schema = {
    }
    template = (
      "in Simple Calendar Pro, create a calendar event in two weeks from today"
        " at {hour}h with the title '{event_title}' and the description"
        " '{event_description}'. The event should last for {duration_mins} mins "
      " then Run the stopwatch and then Pause it in clock app"
    )

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.clock_task=clock.ClockStopWatchRunningAndPaused(params={})
        self.clock_task.initialize_task(env)

    @classmethod
    def _get_random_target_row(cls):
        # Generate an event for InTwoWeeks.
        return events_generator.generate_event(
            datetime_utils.create_random_october_2023_unix_ts(
                device_constants.DT.day + 14, device_constants.DT.day + 14
            )
        )

    def validate_addition_integrity(
            self,
            before: list[sqlite_schema_utils.CalendarEvent],
            after: list[sqlite_schema_utils.CalendarEvent],
            reference_rows: list[sqlite_schema_utils.CalendarEvent],
    ) -> bool:
        """Validates the integrity of the event addition."""
        return calendar_evaluators.validate_event_addition_integrity(
            before,
            after,
            reference_rows,
            extras_compare=["repeat_rule", "repeat_interval"],
        )

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        after = self.list_rows(env.base_env)
        row_addition_successful = self.validate_addition_integrity(
            self.before, after, self.params["row_objects"]
        )
        if row_addition_successful: row_success=1
        else : row_success = 0

        clock_success = self.clock_task.is_successful(env)

        return (row_success + clock_success) / 2.0
    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        event = cls._get_random_target_row()
        n_noise_events = random.randint(0, 20)
        return {

            _YEAR: device_constants.DT.year,
            _MONTH: device_constants.DT.month,
            _DAY: event.start_datetime.day,
            _HOUR: event.start_datetime.hour,
            _DURATION_MINS: event.duration_mins,
            _EVENT_TITLE: event.title,
            _EVENT_DESCRIPTION: event.description,
            sqlite_validators.ROW_OBJECTS: [event],
            sqlite_validators.NOISE_ROW_OBJECTS: _generate_noise_events(
                [event], n_noise_events
            ),
        }

class SimpleCalendarAddOneEventInTwoWeeksAndClockWatchRunningAndReset(_SimpleCalendarAndClock, sqlite_validators.AddMultipleRows):
    complexity = 2
    schema = {
    }
    template = (
      "in Simple Calendar Pro, create a calendar event in two weeks from today"
        " at {hour}h with the title '{event_title}' and the description"
        " '{event_description}'. The event should last for {duration_mins} mins "
      " then Run the stopwatch and reset the stopwatch in clock app"
    )

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.clock_task=clock.ClockWatchRunningAndReset(params={})
        self.clock_task.initialize_task(env)

    @classmethod
    def _get_random_target_row(cls):
        # Generate an event for InTwoWeeks.
        return events_generator.generate_event(
            datetime_utils.create_random_october_2023_unix_ts(
                device_constants.DT.day + 14, device_constants.DT.day + 14
            )
        )

    def validate_addition_integrity(
            self,
            before: list[sqlite_schema_utils.CalendarEvent],
            after: list[sqlite_schema_utils.CalendarEvent],
            reference_rows: list[sqlite_schema_utils.CalendarEvent],
    ) -> bool:
        """Validates the integrity of the event addition."""
        return calendar_evaluators.validate_event_addition_integrity(
            before,
            after,
            reference_rows,
            extras_compare=["repeat_rule", "repeat_interval"],
        )

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        after = self.list_rows(env.base_env)
        row_addition_successful = self.validate_addition_integrity(
            self.before, after, self.params["row_objects"]
        )
        if row_addition_successful: row_success=1
        else : row_success = 0

        clock_success = self.clock_task.is_successful(env)

        return (row_success + clock_success) / 2.0
    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        event = cls._get_random_target_row()
        n_noise_events = random.randint(0, 20)
        return {

            _YEAR: device_constants.DT.year,
            _MONTH: device_constants.DT.month,
            _DAY: event.start_datetime.day,
            _HOUR: event.start_datetime.hour,
            _DURATION_MINS: event.duration_mins,
            _EVENT_TITLE: event.title,
            _EVENT_DESCRIPTION: event.description,
            sqlite_validators.ROW_OBJECTS: [event],
            sqlite_validators.NOISE_ROW_OBJECTS: _generate_noise_events(
                [event], n_noise_events
            ),
        }
    

class SimpleCalendarAddOneEventInOneMonthAndStopWatchPaused(_SimpleCalendarAndClock, sqlite_validators.AddMultipleRows):
    complexity = 2
    schema = {
    }
    template = (
      "in Simple Calendar Pro, create a calendar event in one month from today"
        " at {hour}h with the title '{event_title}' and the description"
        " '{event_description}'. The event should last for {duration_mins} mins , then pause the stop watch in clock app"
    )

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.clock_task=clock.ClockStopWatchPausedVerify(params={})
        self.clock_task.initialize_task(env)

    @classmethod
    def _get_random_target_row(cls):
        # Generate an event for InOneMonth.
        return events_generator.generate_event(
            datetime_utils.create_random_october_2023_unix_ts(
                device_constants.DT.month + 1, device_constants.DT.month + 1
            )
        )
    def validate_addition_integrity(
            self,
            before: list[sqlite_schema_utils.CalendarEvent],
            after: list[sqlite_schema_utils.CalendarEvent],
            reference_rows: list[sqlite_schema_utils.CalendarEvent],
    ) -> bool:
        """Validates the integrity of the event addition."""
        return calendar_evaluators.validate_event_addition_integrity(
            before,
            after,
            reference_rows,
            extras_compare=["repeat_rule", "repeat_interval"],
        )

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        after = self.list_rows(env.base_env)
        row_addition_successful = self.validate_addition_integrity(
            self.before, after, self.params["row_objects"]
        )
        if row_addition_successful: row_success=1
        else : row_success = 0

        clock_success = self.clock_task.is_successful(env)

        return (row_success + clock_success) / 2.0
    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        event = cls._get_random_target_row()
        n_noise_events = random.randint(0, 20)
        return {

            _YEAR: device_constants.DT.year,
            _MONTH: device_constants.DT.month,
            _DAY: event.start_datetime.day,
            _HOUR: event.start_datetime.hour,
            _DURATION_MINS: event.duration_mins,
            _EVENT_TITLE: event.title,
            _EVENT_DESCRIPTION: event.description,
            sqlite_validators.ROW_OBJECTS: [event],
            sqlite_validators.NOISE_ROW_OBJECTS: _generate_noise_events(
                [event], n_noise_events
            ),
        }

class SimpleCalendarAddOneEventInOneMonthAndClockStopWatchRunning(_SimpleCalendarAndClock, sqlite_validators.AddMultipleRows):
    complexity = 2
    schema = {
    }
    template = (
      "in Simple Calendar Pro, create a calendar event in one month from today"
        " at {hour}h with the title '{event_title}' and the description"
        " '{event_description}'. The event should last for {duration_mins} mins , then run the stop watch in clock app"
    )

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.clock_task=clock.ClockStopWatchRunning(params={})
        self.clock_task.initialize_task(env)
    @classmethod
    def _get_random_target_row(cls):
        # Generate an event for InOneMonth.
        return events_generator.generate_event(
            datetime_utils.create_random_october_2023_unix_ts(
                device_constants.DT.month + 1, device_constants.DT.month + 1
            )
        )

    def validate_addition_integrity(
            self,
            before: list[sqlite_schema_utils.CalendarEvent],
            after: list[sqlite_schema_utils.CalendarEvent],
            reference_rows: list[sqlite_schema_utils.CalendarEvent],
    ) -> bool:
        """Validates the integrity of the event addition."""
        return calendar_evaluators.validate_event_addition_integrity(
            before,
            after,
            reference_rows,
            extras_compare=["repeat_rule", "repeat_interval"],
        )

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        after = self.list_rows(env.base_env)
        row_addition_successful = self.validate_addition_integrity(
            self.before, after, self.params["row_objects"]
        )
        if row_addition_successful: row_success=1
        else : row_success = 0

        clock_success = self.clock_task.is_successful(env)

        return (row_success + clock_success) / 2.0
    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        event = cls._get_random_target_row()
        n_noise_events = random.randint(0, 20)
        return {

            _YEAR: device_constants.DT.year,
            _MONTH: device_constants.DT.month,
            _DAY: event.start_datetime.day,
            _HOUR: event.start_datetime.hour,
            _DURATION_MINS: event.duration_mins,
            _EVENT_TITLE: event.title,
            _EVENT_DESCRIPTION: event.description,
            sqlite_validators.ROW_OBJECTS: [event],
            sqlite_validators.NOISE_ROW_OBJECTS: _generate_noise_events(
                [event], n_noise_events
            ),
        }

class SimpleCalendarAddOneEventInOneMonthAndClockStopWatchRunningAndPaused(_SimpleCalendarAndClock, sqlite_validators.AddMultipleRows):
    complexity = 2
    schema = {
    }
    template = (
      "in Simple Calendar Pro, create a calendar event in one month from today"
        " at {hour}h with the title '{event_title}' and the description"
        " '{event_description}'. The event should last for {duration_mins} mins "
      " then Run the stopwatch and then Pause it in clock app"
    )

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.clock_task=clock.ClockStopWatchRunningAndPaused(params={})
        self.clock_task.initialize_task(env)

    @classmethod
    def _get_random_target_row(cls):
        # Generate an event for InOneMonth.
        return events_generator.generate_event(
            datetime_utils.create_random_october_2023_unix_ts(
                device_constants.DT.month + 1, device_constants.DT.month + 1
            )
        )

    def validate_addition_integrity(
            self,
            before: list[sqlite_schema_utils.CalendarEvent],
            after: list[sqlite_schema_utils.CalendarEvent],
            reference_rows: list[sqlite_schema_utils.CalendarEvent],
    ) -> bool:
        """Validates the integrity of the event addition."""
        return calendar_evaluators.validate_event_addition_integrity(
            before,
            after,
            reference_rows,
            extras_compare=["repeat_rule", "repeat_interval"],
        )

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        after = self.list_rows(env.base_env)
        row_addition_successful = self.validate_addition_integrity(
            self.before, after, self.params["row_objects"]
        )
        if row_addition_successful: row_success=1
        else : row_success = 0

        clock_success = self.clock_task.is_successful(env)

        return (row_success + clock_success) / 2.0
    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        event = cls._get_random_target_row()
        n_noise_events = random.randint(0, 20)
        return {

            _YEAR: device_constants.DT.year,
            _MONTH: device_constants.DT.month,
            _DAY: event.start_datetime.day,
            _HOUR: event.start_datetime.hour,
            _DURATION_MINS: event.duration_mins,
            _EVENT_TITLE: event.title,
            _EVENT_DESCRIPTION: event.description,
            sqlite_validators.ROW_OBJECTS: [event],
            sqlite_validators.NOISE_ROW_OBJECTS: _generate_noise_events(
                [event], n_noise_events
            ),
        }

class SimpleCalendarAddOneEventInOneMonthAndClockWatchRunningAndReset(_SimpleCalendarAndClock, sqlite_validators.AddMultipleRows):
    complexity = 2
    schema = {
    }
    template = (
      "in Simple Calendar Pro, create a calendar event in one month from today"
        " at {hour}h with the title '{event_title}' and the description"
        " '{event_description}'. The event should last for {duration_mins} mins "
      " then Run the stopwatch and reset the stopwatch in clock app"
    )

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.clock_task=clock.ClockWatchRunningAndReset(params={})
        self.clock_task.initialize_task(env)

    @classmethod
    def _get_random_target_row(cls):
        # Generate an event for InOneMonth.
        return events_generator.generate_event(
            datetime_utils.create_random_october_2023_unix_ts(
                device_constants.DT.month + 1, device_constants.DT.month + 1
            )
        )

    def validate_addition_integrity(
            self,
            before: list[sqlite_schema_utils.CalendarEvent],
            after: list[sqlite_schema_utils.CalendarEvent],
            reference_rows: list[sqlite_schema_utils.CalendarEvent],
    ) -> bool:
        """Validates the integrity of the event addition."""
        return calendar_evaluators.validate_event_addition_integrity(
            before,
            after,
            reference_rows,
            extras_compare=["repeat_rule", "repeat_interval"],
        )

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        after = self.list_rows(env.base_env)
        row_addition_successful = self.validate_addition_integrity(
            self.before, after, self.params["row_objects"]
        )
        if row_addition_successful: row_success=1
        else : row_success = 0

        clock_success = self.clock_task.is_successful(env)

        return (row_success + clock_success) / 2.0
    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        event = cls._get_random_target_row()
        n_noise_events = random.randint(0, 20)
        return {

            _YEAR: device_constants.DT.year,
            _MONTH: device_constants.DT.month,
            _DAY: event.start_datetime.day,
            _HOUR: event.start_datetime.hour,
            _DURATION_MINS: event.duration_mins,
            _EVENT_TITLE: event.title,
            _EVENT_DESCRIPTION: event.description,
            sqlite_validators.ROW_OBJECTS: [event],
            sqlite_validators.NOISE_ROW_OBJECTS: _generate_noise_events(
                [event], n_noise_events
            ),
        }


class SimpleCalendarAddOneEventInTwoMonthAndStopWatchPaused(_SimpleCalendarAndClock, sqlite_validators.AddMultipleRows):
    complexity = 2
    schema = {
    }
    template = (
      "in Simple Calendar Pro, create a calendar event in two months from today"
        " at {hour}h with the title '{event_title}' and the description"
        " '{event_description}'. The event should last for {duration_mins} mins , then pause the stop watch in clock app"
    )

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.clock_task=clock.ClockStopWatchPausedVerify(params={})
        self.clock_task.initialize_task(env)

    @classmethod
    def _get_random_target_row(cls):
        # Generate an event for InTwoMonth.
        return events_generator.generate_event(
            datetime_utils.create_random_october_2023_unix_ts(
                device_constants.DT.month + 2, device_constants.DT.month + 2
            )
        )
    def validate_addition_integrity(
            self,
            before: list[sqlite_schema_utils.CalendarEvent],
            after: list[sqlite_schema_utils.CalendarEvent],
            reference_rows: list[sqlite_schema_utils.CalendarEvent],
    ) -> bool:
        """Validates the integrity of the event addition."""
        return calendar_evaluators.validate_event_addition_integrity(
            before,
            after,
            reference_rows,
            extras_compare=["repeat_rule", "repeat_interval"],
        )

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        after = self.list_rows(env.base_env)
        row_addition_successful = self.validate_addition_integrity(
            self.before, after, self.params["row_objects"]
        )
        if row_addition_successful: row_success=1
        else : row_success = 0

        clock_success = self.clock_task.is_successful(env)

        return (row_success + clock_success) / 2.0
    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        event = cls._get_random_target_row()
        n_noise_events = random.randint(0, 20)
        return {

            _YEAR: device_constants.DT.year,
            _MONTH: device_constants.DT.month,
            _DAY: event.start_datetime.day,
            _HOUR: event.start_datetime.hour,
            _DURATION_MINS: event.duration_mins,
            _EVENT_TITLE: event.title,
            _EVENT_DESCRIPTION: event.description,
            sqlite_validators.ROW_OBJECTS: [event],
            sqlite_validators.NOISE_ROW_OBJECTS: _generate_noise_events(
                [event], n_noise_events
            ),
        }

class SimpleCalendarAddOneEventInTwoMonthAndClockStopWatchRunning(_SimpleCalendarAndClock, sqlite_validators.AddMultipleRows):
    complexity = 2
    schema = {
    }
    template = (
      "in Simple Calendar Pro, create a calendar event in two months from today"
        " at {hour}h with the title '{event_title}' and the description"
        " '{event_description}'. The event should last for {duration_mins} mins , then run the stop watch in clock app"
    )

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.clock_task=clock.ClockStopWatchRunning(params={})
        self.clock_task.initialize_task(env)
    @classmethod
    def _get_random_target_row(cls):
        # Generate an event for InTwoMonth.
        return events_generator.generate_event(
            datetime_utils.create_random_october_2023_unix_ts(
                device_constants.DT.month + 2, device_constants.DT.month + 2
            )
        )

    def validate_addition_integrity(
            self,
            before: list[sqlite_schema_utils.CalendarEvent],
            after: list[sqlite_schema_utils.CalendarEvent],
            reference_rows: list[sqlite_schema_utils.CalendarEvent],
    ) -> bool:
        """Validates the integrity of the event addition."""
        return calendar_evaluators.validate_event_addition_integrity(
            before,
            after,
            reference_rows,
            extras_compare=["repeat_rule", "repeat_interval"],
        )

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        after = self.list_rows(env.base_env)
        row_addition_successful = self.validate_addition_integrity(
            self.before, after, self.params["row_objects"]
        )
        if row_addition_successful: row_success=1
        else : row_success = 0

        clock_success = self.clock_task.is_successful(env)

        return (row_success + clock_success) / 2.0
    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        event = cls._get_random_target_row()
        n_noise_events = random.randint(0, 20)
        return {

            _YEAR: device_constants.DT.year,
            _MONTH: device_constants.DT.month,
            _DAY: event.start_datetime.day,
            _HOUR: event.start_datetime.hour,
            _DURATION_MINS: event.duration_mins,
            _EVENT_TITLE: event.title,
            _EVENT_DESCRIPTION: event.description,
            sqlite_validators.ROW_OBJECTS: [event],
            sqlite_validators.NOISE_ROW_OBJECTS: _generate_noise_events(
                [event], n_noise_events
            ),
        }

class SimpleCalendarAddOneEventInTwoMonthAndClockStopWatchRunningAndPaused(_SimpleCalendarAndClock, sqlite_validators.AddMultipleRows):
    complexity = 2
    schema = {
    }
    template = (
      "in Simple Calendar Pro, create a calendar event in two months from today"
        " at {hour}h with the title '{event_title}' and the description"
        " '{event_description}'. The event should last for {duration_mins} mins "
      " then Run the stopwatch and then Pause it in clock app"
    )

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.clock_task=clock.ClockStopWatchRunningAndPaused(params={})
        self.clock_task.initialize_task(env)

    @classmethod
    def _get_random_target_row(cls):
        # Generate an event for InTwoMonth.
        return events_generator.generate_event(
            datetime_utils.create_random_october_2023_unix_ts(
                device_constants.DT.month + 2, device_constants.DT.month + 2
            )
        )

    def validate_addition_integrity(
            self,
            before: list[sqlite_schema_utils.CalendarEvent],
            after: list[sqlite_schema_utils.CalendarEvent],
            reference_rows: list[sqlite_schema_utils.CalendarEvent],
    ) -> bool:
        """Validates the integrity of the event addition."""
        return calendar_evaluators.validate_event_addition_integrity(
            before,
            after,
            reference_rows,
            extras_compare=["repeat_rule", "repeat_interval"],
        )

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        after = self.list_rows(env.base_env)
        row_addition_successful = self.validate_addition_integrity(
            self.before, after, self.params["row_objects"]
        )
        if row_addition_successful: row_success=1
        else : row_success = 0

        clock_success = self.clock_task.is_successful(env)

        return (row_success + clock_success) / 2.0
    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        event = cls._get_random_target_row()
        n_noise_events = random.randint(0, 20)
        return {

            _YEAR: device_constants.DT.year,
            _MONTH: device_constants.DT.month,
            _DAY: event.start_datetime.day,
            _HOUR: event.start_datetime.hour,
            _DURATION_MINS: event.duration_mins,
            _EVENT_TITLE: event.title,
            _EVENT_DESCRIPTION: event.description,
            sqlite_validators.ROW_OBJECTS: [event],
            sqlite_validators.NOISE_ROW_OBJECTS: _generate_noise_events(
                [event], n_noise_events
            ),
        }

class SimpleCalendarAddOneEventInTwoMonthAndClockWatchRunningAndReset(_SimpleCalendarAndClock, sqlite_validators.AddMultipleRows):
    complexity = 2
    schema = {
    }
    template = (
      "in Simple Calendar Pro, create a calendar event in two months from today"
        " at {hour}h with the title '{event_title}' and the description"
        " '{event_description}'. The event should last for {duration_mins} mins "
      " then Run the stopwatch and reset the stopwatch in clock app"
    )

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.clock_task=clock.ClockWatchRunningAndReset(params={})
        self.clock_task.initialize_task(env)

    @classmethod
    def _get_random_target_row(cls):
        # Generate an event for InTwoMonth.
        return events_generator.generate_event(
            datetime_utils.create_random_october_2023_unix_ts(
                device_constants.DT.month + 2, device_constants.DT.month + 2
            )
        )

    def validate_addition_integrity(
            self,
            before: list[sqlite_schema_utils.CalendarEvent],
            after: list[sqlite_schema_utils.CalendarEvent],
            reference_rows: list[sqlite_schema_utils.CalendarEvent],
    ) -> bool:
        """Validates the integrity of the event addition."""
        return calendar_evaluators.validate_event_addition_integrity(
            before,
            after,
            reference_rows,
            extras_compare=["repeat_rule", "repeat_interval"],
        )

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        after = self.list_rows(env.base_env)
        row_addition_successful = self.validate_addition_integrity(
            self.before, after, self.params["row_objects"]
        )
        if row_addition_successful: row_success=1
        else : row_success = 0

        clock_success = self.clock_task.is_successful(env)

        return (row_success + clock_success) / 2.0
    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        event = cls._get_random_target_row()
        n_noise_events = random.randint(0, 20)
        return {

            _YEAR: device_constants.DT.year,
            _MONTH: device_constants.DT.month,
            _DAY: event.start_datetime.day,
            _HOUR: event.start_datetime.hour,
            _DURATION_MINS: event.duration_mins,
            _EVENT_TITLE: event.title,
            _EVENT_DESCRIPTION: event.description,
            sqlite_validators.ROW_OBJECTS: [event],
            sqlite_validators.NOISE_ROW_OBJECTS: _generate_noise_events(
                [event], n_noise_events
            ),
        }


class SimpleCalendarAddRepeatingEventAndStopWatchPaused(_SimpleCalendarAndClock, sqlite_validators.AddMultipleRows):
    complexity = 3
    schema = {
    }
    template = (
      "In Simple Calendar Pro, create a recurring calendar event titled"
      " '{event_title}' starting on {year}-{month}-{day} at"
      " {hour}h. The event recurs {repeat_rule}, forever, and lasts for"
      " {duration_mins} minutes each occurrence. The event description should"
      " be '{event_description}'"
      " then pause the stop watch in clock app"
    )

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.clock_task=clock.ClockStopWatchPausedVerify(params={})
        self.clock_task.initialize_task(env)

    @classmethod
    def _get_random_target_row(cls) -> sqlite_schema_utils.CalendarEvent:
        """Generates a random calendar event."""
        return events_generator.generate_event(
            datetime_utils.create_random_october_2023_unix_ts()
        )

    def validate_addition_integrity(
            self,
            before: list[sqlite_schema_utils.CalendarEvent],
            after: list[sqlite_schema_utils.CalendarEvent],
            reference_rows: list[sqlite_schema_utils.CalendarEvent],
    ) -> bool:
        """Validates the integrity of the event addition."""
        return calendar_evaluators.validate_event_addition_integrity(
            before,
            after,
            reference_rows,
            extras_compare=["repeat_rule", "repeat_interval"],
        )

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        after = self.list_rows(env.base_env)
        row_addition_successful = self.validate_addition_integrity(
            self.before, after, self.params["row_objects"]
        )
        if row_addition_successful: row_success=1
        else : row_success = 0

        clock_success = self.clock_task.is_successful(env)

        return (row_success + clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        """Generate random parameters for a new calendar event task."""
        template = cls._get_random_target_row()
        repeat_interval = random.choice(list(_REPEAT_INTERVALS))
        if repeat_interval == "weekly":
            repeat_rule = calendar_utils.generate_simple_calendar_weekly_repeat_rule(
                template.start_datetime.isoweekday()
            )
        else:
            repeat_rule = 0
        event = dataclasses.replace(
            template,
            repeat_interval=_REPEAT_INTERVALS[repeat_interval],
            repeat_rule=repeat_rule,
        )
        noise_events = _generate_noise_events([event], random.randint(0, 20))
        return {
            _YEAR: device_constants.DT.year,
            _MONTH: device_constants.DT.month,
            _DAY: event.start_datetime.day,
            _HOUR: event.start_datetime.hour,
            _DURATION_MINS: event.duration_mins,
            _EVENT_TITLE: event.title,
            _EVENT_DESCRIPTION: event.description,
            sqlite_validators.ROW_OBJECTS: [event],
            sqlite_validators.NOISE_ROW_OBJECTS: noise_events,
            _REPEAT_INTERVAL: repeat_interval,
        }

class SimpleCalendarAddRepeatingEventAndClockStopWatchRunning(_SimpleCalendarAndClock, sqlite_validators.AddMultipleRows):
    complexity = 2
    schema = {
    }
    template = (
      "In Simple Calendar Pro, create a recurring calendar event titled"
      " '{event_title}' starting on {year}-{month}-{day} at"
      " {hour}h. The event recurs {repeat_rule}, forever, and lasts for"
      " {duration_mins} minutes each occurrence. The event description should"
      " be '{event_description}'"
      "then run the stop watch in clock app"
    )

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.clock_task=clock.ClockStopWatchRunning(params={})
        self.clock_task.initialize_task(env)
    @classmethod
    def _get_random_target_row(cls) -> sqlite_schema_utils.CalendarEvent:
        """Generates a random calendar event."""
        return events_generator.generate_event(
            datetime_utils.create_random_october_2023_unix_ts()
        )

    def validate_addition_integrity(
            self,
            before: list[sqlite_schema_utils.CalendarEvent],
            after: list[sqlite_schema_utils.CalendarEvent],
            reference_rows: list[sqlite_schema_utils.CalendarEvent],
    ) -> bool:
        """Validates the integrity of the event addition."""
        return calendar_evaluators.validate_event_addition_integrity(
            before,
            after,
            reference_rows,
            extras_compare=["repeat_rule", "repeat_interval"],
        )

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        after = self.list_rows(env.base_env)
        row_addition_successful = self.validate_addition_integrity(
            self.before, after, self.params["row_objects"]
        )
        if row_addition_successful: row_success=1
        else : row_success = 0

        clock_success = self.clock_task.is_successful(env)

        return (row_success + clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        """Generate random parameters for a new calendar event task."""
        template = cls._get_random_target_row()
        repeat_interval = random.choice(list(_REPEAT_INTERVALS))
        if repeat_interval == "weekly":
            repeat_rule = calendar_utils.generate_simple_calendar_weekly_repeat_rule(
                template.start_datetime.isoweekday()
            )
        else:
            repeat_rule = 0
        event = dataclasses.replace(
            template,
            repeat_interval=_REPEAT_INTERVALS[repeat_interval],
            repeat_rule=repeat_rule,
        )
        noise_events = _generate_noise_events([event], random.randint(0, 20))
        return {
            _YEAR: device_constants.DT.year,
            _MONTH: device_constants.DT.month,
            _DAY: event.start_datetime.day,
            _HOUR: event.start_datetime.hour,
            _DURATION_MINS: event.duration_mins,
            _EVENT_TITLE: event.title,
            _EVENT_DESCRIPTION: event.description,
            sqlite_validators.ROW_OBJECTS: [event],
            sqlite_validators.NOISE_ROW_OBJECTS: noise_events,
            _REPEAT_INTERVAL: repeat_interval,
        }

class SimpleCalendarAddRepeatingEventAndClockStopWatchRunningAndPaused(_SimpleCalendarAndClock, sqlite_validators.AddMultipleRows):
    complexity = 2
    schema = {
    }
    template = (
      "In Simple Calendar Pro, create a recurring calendar event titled"
      " '{event_title}' starting on {year}-{month}-{day} at"
      " {hour}h. The event recurs {repeat_rule}, forever, and lasts for"
      " {duration_mins} minutes each occurrence. The event description should"
      " be '{event_description}'"
      " then Run the stopwatch and then Pause it in clock app"
    )

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.clock_task=clock.ClockStopWatchRunningAndPaused(params={})
        self.clock_task.initialize_task(env)

    @classmethod
    def _get_random_target_row(cls) -> sqlite_schema_utils.CalendarEvent:
        """Generates a random calendar event."""
        return events_generator.generate_event(
            datetime_utils.create_random_october_2023_unix_ts()
        )

    def validate_addition_integrity(
            self,
            before: list[sqlite_schema_utils.CalendarEvent],
            after: list[sqlite_schema_utils.CalendarEvent],
            reference_rows: list[sqlite_schema_utils.CalendarEvent],
    ) -> bool:
        """Validates the integrity of the event addition."""
        return calendar_evaluators.validate_event_addition_integrity(
            before,
            after,
            reference_rows,
            extras_compare=["repeat_rule", "repeat_interval"],
        )

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        after = self.list_rows(env.base_env)
        row_addition_successful = self.validate_addition_integrity(
            self.before, after, self.params["row_objects"]
        )
        if row_addition_successful: row_success=1
        else : row_success = 0

        clock_success = self.clock_task.is_successful(env)

        return (row_success + clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        """Generate random parameters for a new calendar event task."""
        template = cls._get_random_target_row()
        repeat_interval = random.choice(list(_REPEAT_INTERVALS))
        if repeat_interval == "weekly":
            repeat_rule = calendar_utils.generate_simple_calendar_weekly_repeat_rule(
                template.start_datetime.isoweekday()
            )
        else:
            repeat_rule = 0
        event = dataclasses.replace(
            template,
            repeat_interval=_REPEAT_INTERVALS[repeat_interval],
            repeat_rule=repeat_rule,
        )
        noise_events = _generate_noise_events([event], random.randint(0, 20))
        return {
            _YEAR: device_constants.DT.year,
            _MONTH: device_constants.DT.month,
            _DAY: event.start_datetime.day,
            _HOUR: event.start_datetime.hour,
            _DURATION_MINS: event.duration_mins,
            _EVENT_TITLE: event.title,
            _EVENT_DESCRIPTION: event.description,
            sqlite_validators.ROW_OBJECTS: [event],
            sqlite_validators.NOISE_ROW_OBJECTS: noise_events,
            _REPEAT_INTERVAL: repeat_interval,
        }

class SimpleCalendarAddRepeatingEventAndClockWatchRunningAndReset(_SimpleCalendarAndClock, sqlite_validators.AddMultipleRows):
    complexity = 2
    schema = {
    }
    template = (
      "In Simple Calendar Pro, create a recurring calendar event titled"
      " '{event_title}' starting on {year}-{month}-{day} at"
      " {hour}h. The event recurs {repeat_rule}, forever, and lasts for"
      " {duration_mins} minutes each occurrence. The event description should"
      " be '{event_description}'"
      " then Run the stopwatch and reset the stopwatch in clock app"
    )

    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.clock_task=clock.ClockWatchRunningAndReset(params={})
        self.clock_task.initialize_task(env)

    @classmethod
    def _get_random_target_row(cls) -> sqlite_schema_utils.CalendarEvent:
        """Generates a random calendar event."""
        return events_generator.generate_event(
            datetime_utils.create_random_october_2023_unix_ts()
        )

    def validate_addition_integrity(
            self,
            before: list[sqlite_schema_utils.CalendarEvent],
            after: list[sqlite_schema_utils.CalendarEvent],
            reference_rows: list[sqlite_schema_utils.CalendarEvent],
    ) -> bool:
        """Validates the integrity of the event addition."""
        return calendar_evaluators.validate_event_addition_integrity(
            before,
            after,
            reference_rows,
            extras_compare=["repeat_rule", "repeat_interval"],
        )

    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        after = self.list_rows(env.base_env)
        row_addition_successful = self.validate_addition_integrity(
            self.before, after, self.params["row_objects"]
        )
        if row_addition_successful: row_success=1
        else : row_success = 0

        clock_success = self.clock_task.is_successful(env)

        return (row_success + clock_success) / 2.0

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        """Generate random parameters for a new calendar event task."""
        template = cls._get_random_target_row()
        repeat_interval = random.choice(list(_REPEAT_INTERVALS))
        if repeat_interval == "weekly":
            repeat_rule = calendar_utils.generate_simple_calendar_weekly_repeat_rule(
                template.start_datetime.isoweekday()
            )
        else:
            repeat_rule = 0
        event = dataclasses.replace(
            template,
            repeat_interval=_REPEAT_INTERVALS[repeat_interval],
            repeat_rule=repeat_rule,
        )
        noise_events = _generate_noise_events([event], random.randint(0, 20))
        return {
            _YEAR: device_constants.DT.year,
            _MONTH: device_constants.DT.month,
            _DAY: event.start_datetime.day,
            _HOUR: event.start_datetime.hour,
            _DURATION_MINS: event.duration_mins,
            _EVENT_TITLE: event.title,
            _EVENT_DESCRIPTION: event.description,
            sqlite_validators.ROW_OBJECTS: [event],
            sqlite_validators.NOISE_ROW_OBJECTS: noise_events,
            _REPEAT_INTERVAL: repeat_interval,
        }

class SimpleCalendarDeleteEventsAndStopWatchPaused(_SimpleCalendarAndClock,sqlite_validators.DeleteMultipleRows):
    n_rows = 3
    n_rows_noise = 20
    complexity = 3
    template = (
        "In Simple Calendar Pro, delete all the calendar events on"
        " {year}-{month}-{day}"
        " then pause the stop watch in clock app"
    )
    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.clock_task=clock.ClockStopWatchPausedVerify(params={})
        self.clock_task.initialize_task(env)
    def validate_deletion_integrity(
            self,
            before: list[sqlite_schema_utils.CalendarEvent],
            after: list[sqlite_schema_utils.CalendarEvent],
    ) -> bool:
        """Validates the integrity of the event deletion."""
        return calendar_evaluators.validate_event_removal_integrity(
            before, after, [r.id for r in self.rows_to_delete]
        )

    @classmethod
    def _get_random_target_row(cls, day: int):
        return events_generator.generate_event(
            datetime_utils.create_random_october_2023_unix_ts(
                start_day=day, end_day=day
            )
        )

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        """Generate random parameters for a remove calendar event task."""
        template = events_generator.generate_event(
            datetime_utils.create_random_october_2023_unix_ts()
        )
        events = [
            cls._get_random_target_row(template.start_datetime.day)
            for _ in range(cls.n_rows)
        ]
        noise_events = _generate_noise_events(
            events,
            cls.n_rows_noise,
            filter_fn=lambda candidate: candidate.start_datetime.day
                                        not in (target.start_datetime.day for target in events),
        )
        return {
            _YEAR: device_constants.DT.year,
            _MONTH: device_constants.DT.month,
            _DAY: template.start_datetime.day,
            sqlite_validators.ROW_OBJECTS: events,
            sqlite_validators.NOISE_ROW_OBJECTS: noise_events,
        }
    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        after = self.list_rows(env.base_env)
        deletion_successful = self.validate_deletion_integrity(self.before, after)
        if deletion_successful: del_success=1
        else : del_success = 0

        clock_success = self.clock_task.is_successful(env)

        return (del_success + clock_success) / 2.0

class SimpleCalendarDeleteEventsAndClockStopWatchRunning(_SimpleCalendarAndClock,sqlite_validators.DeleteMultipleRows):
    n_rows = 3
    n_rows_noise = 20
    complexity = 3
    template = (
        "In Simple Calendar Pro, delete all the calendar events on"
        " {year}-{month}-{day}"
      "then run the stop watch in clock app"
    )
    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.clock_task=clock.ClockStopWatchRunning(params={})
        self.clock_task.initialize_task(env)
    def validate_deletion_integrity(
            self,
            before: list[sqlite_schema_utils.CalendarEvent],
            after: list[sqlite_schema_utils.CalendarEvent],
    ) -> bool:
        """Validates the integrity of the event deletion."""
        return calendar_evaluators.validate_event_removal_integrity(
            before, after, [r.id for r in self.rows_to_delete]
        )

    @classmethod
    def _get_random_target_row(cls, day: int):
        return events_generator.generate_event(
            datetime_utils.create_random_october_2023_unix_ts(
                start_day=day, end_day=day
            )
        )

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        """Generate random parameters for a remove calendar event task."""
        template = events_generator.generate_event(
            datetime_utils.create_random_october_2023_unix_ts()
        )
        events = [
            cls._get_random_target_row(template.start_datetime.day)
            for _ in range(cls.n_rows)
        ]
        noise_events = _generate_noise_events(
            events,
            cls.n_rows_noise,
            filter_fn=lambda candidate: candidate.start_datetime.day
                                        not in (target.start_datetime.day for target in events),
        )
        return {
            _YEAR: device_constants.DT.year,
            _MONTH: device_constants.DT.month,
            _DAY: template.start_datetime.day,
            sqlite_validators.ROW_OBJECTS: events,
            sqlite_validators.NOISE_ROW_OBJECTS: noise_events,
        }
    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        after = self.list_rows(env.base_env)
        deletion_successful = self.validate_deletion_integrity(self.before, after)
        if deletion_successful: del_success=1
        else : del_success = 0

        clock_success = self.clock_task.is_successful(env)

        return (del_success + clock_success) / 2.0

class SimpleCalendarDeleteEventsAndClockWatchRunningAndReset(_SimpleCalendarAndClock,sqlite_validators.DeleteMultipleRows):
    n_rows = 3
    n_rows_noise = 20
    complexity = 3
    template = (
        "In Simple Calendar Pro, delete all the calendar events on"
        " {year}-{month}-{day}"
      " then Run the stopwatch and reset the stopwatch in clock app"
    )
    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.clock_task=clock.ClockWatchRunningAndReset(params={})
        self.clock_task.initialize_task(env)
    def validate_deletion_integrity(
            self,
            before: list[sqlite_schema_utils.CalendarEvent],
            after: list[sqlite_schema_utils.CalendarEvent],
    ) -> bool:
        """Validates the integrity of the event deletion."""
        return calendar_evaluators.validate_event_removal_integrity(
            before, after, [r.id for r in self.rows_to_delete]
        )

    @classmethod
    def _get_random_target_row(cls, day: int):
        return events_generator.generate_event(
            datetime_utils.create_random_october_2023_unix_ts(
                start_day=day, end_day=day
            )
        )

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        """Generate random parameters for a remove calendar event task."""
        template = events_generator.generate_event(
            datetime_utils.create_random_october_2023_unix_ts()
        )
        events = [
            cls._get_random_target_row(template.start_datetime.day)
            for _ in range(cls.n_rows)
        ]
        noise_events = _generate_noise_events(
            events,
            cls.n_rows_noise,
            filter_fn=lambda candidate: candidate.start_datetime.day
                                        not in (target.start_datetime.day for target in events),
        )
        return {
            _YEAR: device_constants.DT.year,
            _MONTH: device_constants.DT.month,
            _DAY: template.start_datetime.day,
            sqlite_validators.ROW_OBJECTS: events,
            sqlite_validators.NOISE_ROW_OBJECTS: noise_events,
        }
    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        after = self.list_rows(env.base_env)
        deletion_successful = self.validate_deletion_integrity(self.before, after)
        if deletion_successful: del_success=1
        else : del_success = 0

        clock_success = self.clock_task.is_successful(env)

        return (del_success + clock_success) / 2.0

class SimpleCalendarDeleteEventsAndClockStopWatchRunningAndPaused(_SimpleCalendarAndClock,sqlite_validators.DeleteMultipleRows):
    n_rows = 3
    n_rows_noise = 20
    complexity = 3
    template = (
        "In Simple Calendar Pro, delete all the calendar events on"
        " {year}-{month}-{day}"
      " then Run the stopwatch and then Pause it in clock app"
    )
    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.clock_task=clock.ClockStopWatchRunningAndPaused(params={})
        self.clock_task.initialize_task(env)
    def validate_deletion_integrity(
            self,
            before: list[sqlite_schema_utils.CalendarEvent],
            after: list[sqlite_schema_utils.CalendarEvent],
    ) -> bool:
        """Validates the integrity of the event deletion."""
        return calendar_evaluators.validate_event_removal_integrity(
            before, after, [r.id for r in self.rows_to_delete]
        )

    @classmethod
    def _get_random_target_row(cls, day: int):
        return events_generator.generate_event(
            datetime_utils.create_random_october_2023_unix_ts(
                start_day=day, end_day=day
            )
        )

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        """Generate random parameters for a remove calendar event task."""
        template = events_generator.generate_event(
            datetime_utils.create_random_october_2023_unix_ts()
        )
        events = [
            cls._get_random_target_row(template.start_datetime.day)
            for _ in range(cls.n_rows)
        ]
        noise_events = _generate_noise_events(
            events,
            cls.n_rows_noise,
            filter_fn=lambda candidate: candidate.start_datetime.day
                                        not in (target.start_datetime.day for target in events),
        )
        return {
            _YEAR: device_constants.DT.year,
            _MONTH: device_constants.DT.month,
            _DAY: template.start_datetime.day,
            sqlite_validators.ROW_OBJECTS: events,
            sqlite_validators.NOISE_ROW_OBJECTS: noise_events,
        }
    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        after = self.list_rows(env.base_env)
        deletion_successful = self.validate_deletion_integrity(self.before, after)
        if deletion_successful: del_success=1
        else : del_success = 0

        clock_success = self.clock_task.is_successful(env)

        return (del_success + clock_success) / 2.0


class SimpleCalendarDeleteEventsA2ndStopWatchPaused(_SimpleCalendarAndClock,sqlite_validators.DeleteMultipleRows):
    n_rows = 3
    n_rows_noise = 25
    complexity = 3
    template = (
        "In Simple Calendar Pro, delete all the calendar events on"
        " {year}-{month}-{day}"
        " then pause the stop watch in clock app"
    )
    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.clock_task=clock.ClockStopWatchPausedVerify(params={})
        self.clock_task.initialize_task(env)
    def validate_deletion_integrity(
            self,
            before: list[sqlite_schema_utils.CalendarEvent],
            after: list[sqlite_schema_utils.CalendarEvent],
    ) -> bool:
        """Validates the integrity of the event deletion."""
        return calendar_evaluators.validate_event_removal_integrity(
            before, after, [r.id for r in self.rows_to_delete]
        )

    @classmethod
    def _get_random_target_row(cls, day: int):
        return events_generator.generate_event(
            datetime_utils.create_random_october_2023_unix_ts(
                start_day=day, end_day=day
            )
        )

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        """Generate random parameters for a remove calendar event task."""
        template = events_generator.generate_event(
            datetime_utils.create_random_october_2023_unix_ts()
        )
        events = [
            cls._get_random_target_row(template.start_datetime.day)
            for _ in range(cls.n_rows)
        ]
        noise_events = _generate_noise_events(
            events,
            cls.n_rows_noise,
            filter_fn=lambda candidate: candidate.start_datetime.day
                                        not in (target.start_datetime.day for target in events),
        )
        return {
            _YEAR: device_constants.DT.year,
            _MONTH: device_constants.DT.month,
            _DAY: template.start_datetime.day,
            sqlite_validators.ROW_OBJECTS: events,
            sqlite_validators.NOISE_ROW_OBJECTS: noise_events,
        }
    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        after = self.list_rows(env.base_env)
        deletion_successful = self.validate_deletion_integrity(self.before, after)
        if deletion_successful: del_success=1
        else : del_success = 0

        clock_success = self.clock_task.is_successful(env)

        return (del_success + clock_success) / 2.0

class SimpleCalendarDeleteEvents2AndClockStopWatchRunning(_SimpleCalendarAndClock,sqlite_validators.DeleteMultipleRows):
    n_rows = 3
    n_rows_noise = 25
    complexity = 3
    template = (
        "In Simple Calendar Pro, delete all the calendar events on"
        " {year}-{month}-{day}"
      "then run the stop watch in clock app"
    )
    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.clock_task=clock.ClockStopWatchRunning(params={})
        self.clock_task.initialize_task(env)
    def validate_deletion_integrity(
            self,
            before: list[sqlite_schema_utils.CalendarEvent],
            after: list[sqlite_schema_utils.CalendarEvent],
    ) -> bool:
        """Validates the integrity of the event deletion."""
        return calendar_evaluators.validate_event_removal_integrity(
            before, after, [r.id for r in self.rows_to_delete]
        )

    @classmethod
    def _get_random_target_row(cls, day: int):
        return events_generator.generate_event(
            datetime_utils.create_random_october_2023_unix_ts(
                start_day=day, end_day=day
            )
        )

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        """Generate random parameters for a remove calendar event task."""
        template = events_generator.generate_event(
            datetime_utils.create_random_october_2023_unix_ts()
        )
        events = [
            cls._get_random_target_row(template.start_datetime.day)
            for _ in range(cls.n_rows)
        ]
        noise_events = _generate_noise_events(
            events,
            cls.n_rows_noise,
            filter_fn=lambda candidate: candidate.start_datetime.day
                                        not in (target.start_datetime.day for target in events),
        )
        return {
            _YEAR: device_constants.DT.year,
            _MONTH: device_constants.DT.month,
            _DAY: template.start_datetime.day,
            sqlite_validators.ROW_OBJECTS: events,
            sqlite_validators.NOISE_ROW_OBJECTS: noise_events,
        }
    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        after = self.list_rows(env.base_env)
        deletion_successful = self.validate_deletion_integrity(self.before, after)
        if deletion_successful: del_success=1
        else : del_success = 0

        clock_success = self.clock_task.is_successful(env)

        return (del_success + clock_success) / 2.0

class SimpleCalendarDeleteEvents2AndClockWatchRunningAndReset(_SimpleCalendarAndClock,sqlite_validators.DeleteMultipleRows):
    n_rows = 3
    n_rows_noise = 25
    complexity = 3
    template = (
        "In Simple Calendar Pro, delete all the calendar events on"
        " {year}-{month}-{day}"
      " then Run the stopwatch and reset the stopwatch in clock app"
    )
    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.clock_task=clock.ClockWatchRunningAndReset(params={})
        self.clock_task.initialize_task(env)
    def validate_deletion_integrity(
            self,
            before: list[sqlite_schema_utils.CalendarEvent],
            after: list[sqlite_schema_utils.CalendarEvent],
    ) -> bool:
        """Validates the integrity of the event deletion."""
        return calendar_evaluators.validate_event_removal_integrity(
            before, after, [r.id for r in self.rows_to_delete]
        )

    @classmethod
    def _get_random_target_row(cls, day: int):
        return events_generator.generate_event(
            datetime_utils.create_random_october_2023_unix_ts(
                start_day=day, end_day=day
            )
        )

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        """Generate random parameters for a remove calendar event task."""
        template = events_generator.generate_event(
            datetime_utils.create_random_october_2023_unix_ts()
        )
        events = [
            cls._get_random_target_row(template.start_datetime.day)
            for _ in range(cls.n_rows)
        ]
        noise_events = _generate_noise_events(
            events,
            cls.n_rows_noise,
            filter_fn=lambda candidate: candidate.start_datetime.day
                                        not in (target.start_datetime.day for target in events),
        )
        return {
            _YEAR: device_constants.DT.year,
            _MONTH: device_constants.DT.month,
            _DAY: template.start_datetime.day,
            sqlite_validators.ROW_OBJECTS: events,
            sqlite_validators.NOISE_ROW_OBJECTS: noise_events,
        }
    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        after = self.list_rows(env.base_env)
        deletion_successful = self.validate_deletion_integrity(self.before, after)
        if deletion_successful: del_success=1
        else : del_success = 0

        clock_success = self.clock_task.is_successful(env)

        return (del_success + clock_success) / 2.0

class SimpleCalendarDeleteEvents2AndClockStopWatchRunningAndPaused(_SimpleCalendarAndClock,sqlite_validators.DeleteMultipleRows):
    n_rows = 3
    n_rows_noise = 25
    complexity = 3
    template = (
        "In Simple Calendar Pro, delete all the calendar events on"
        " {year}-{month}-{day}"
      " then Run the stopwatch and then Pause it in clock app"
    )
    def initialize_task(self, env: interface.AsyncEnv) -> None:
        super().initialize_task(env)
        self.clock_task=clock.ClockStopWatchRunningAndPaused(params={})
        self.clock_task.initialize_task(env)
    def validate_deletion_integrity(
            self,
            before: list[sqlite_schema_utils.CalendarEvent],
            after: list[sqlite_schema_utils.CalendarEvent],
    ) -> bool:
        """Validates the integrity of the event deletion."""
        return calendar_evaluators.validate_event_removal_integrity(
            before, after, [r.id for r in self.rows_to_delete]
        )

    @classmethod
    def _get_random_target_row(cls, day: int):
        return events_generator.generate_event(
            datetime_utils.create_random_october_2023_unix_ts(
                start_day=day, end_day=day
            )
        )

    @classmethod
    def generate_random_params(cls) -> dict[str, Any]:
        """Generate random parameters for a remove calendar event task."""
        template = events_generator.generate_event(
            datetime_utils.create_random_october_2023_unix_ts()
        )
        events = [
            cls._get_random_target_row(template.start_datetime.day)
            for _ in range(cls.n_rows)
        ]
        noise_events = _generate_noise_events(
            events,
            cls.n_rows_noise,
            filter_fn=lambda candidate: candidate.start_datetime.day
                                        not in (target.start_datetime.day for target in events),
        )
        return {
            _YEAR: device_constants.DT.year,
            _MONTH: device_constants.DT.month,
            _DAY: template.start_datetime.day,
            sqlite_validators.ROW_OBJECTS: events,
            sqlite_validators.NOISE_ROW_OBJECTS: noise_events,
        }
    def is_successful(self, env: interface.AsyncEnv) -> float:
        super().is_successful(env)
        after = self.list_rows(env.base_env)
        deletion_successful = self.validate_deletion_integrity(self.before, after)
        if deletion_successful: del_success=1
        else : del_success = 0

        clock_success = self.clock_task.is_successful(env)

        return (del_success + clock_success) / 2.0