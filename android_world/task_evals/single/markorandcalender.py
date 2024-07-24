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

"""Tasks for Markor app."""

import dataclasses
import datetime
import os
import random
from typing import Any

from absl import logging
from android_world.env import adb_utils
from android_world.env import device_constants
from android_world.env import interface
from android_world.task_evals import task_eval
from android_world.task_evals.common_validators import file_validators
from android_world.task_evals.single import vlc
from android_world.task_evals.utils import receipt_generator
from android_world.task_evals.utils import user_data_generation
from android_world.utils import datetime_utils
from android_world.utils import file_utils
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


"""Tasks for Simple Calendar Pro app."""

import dataclasses
import random
from typing import Any, Callable, Optional
from android_world.env import device_constants
from android_world.task_evals.common_validators import sqlite_validators
from android_world.task_evals.single.calendar import calendar_evaluators
from android_world.task_evals.single.calendar import calendar_utils
from android_world.task_evals.single.calendar import events_generator
from android_world.task_evals.utils import sqlite_schema_utils
from android_world.utils import datetime_utils

# Keys in generated parameters and used to populate goal template.
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


# class _SimpleCalendar(sqlite_validators.SQLiteApp):
#   """Base class for calendar tasks and evaluation logic.

#                   October 2023
#               Su Mo Tu We Th Fr Sa
#               1  2  3  4  5  6  7
#               8  9 10 11 12 13 14
#               [15]16 17 18 19 20 21
#               22 23 24 25 26 27 28
#               29 30 31

#   The current date on the emulator will be set as October 15, 2023.
#   """

#   app_name_with_db = "simple calendar pro"
#   app_names = ("simple calendar pro",)
#   schema = {}

#   db_key = "id"
#   db_path = calendar_utils.DB_PATH
#   table_name = calendar_utils.EVENTS_TABLE
#   row_type = sqlite_schema_utils.CalendarEvent


class MarkorandCalender(sqlite_validators.SQLiteApp):
  app_name_with_db = "simple calendar pro"
  app_names = ("markor","simple calendar pro",)
  schema = {}

  db_key = "id"
  db_path = calendar_utils.DB_PATH
  table_name = calendar_utils.EVENTS_TABLE
  row_type = sqlite_schema_utils.CalendarEvent

  def initialize_task(self, env: interface.AsyncEnv):
    super().initialize_task(env)
    file_utils.clear_directory(device_constants.MARKOR_DATA, env.base_env)

  def tear_down(self, env: interface.AsyncEnv) -> None:
    super().tear_down(env)
    file_utils.clear_directory(device_constants.MARKOR_DATA, env.base_env)


class MarkorCreateFolderandSimpleCalendarAddOneEvent(MarkorandCalender, sqlite_validators.AddMultipleRows):
  """Task for checking that a new folder in Markor has been created with a specific name."""

  complexity = 2
  schema = {
      "type": "object",
      "properties": {
          "folder_name": {"type": "string"},
      },
      "required": ["folder_name"],
  }
  template = (
      "Create a new folder in Markor named {folder_name}."
      "Also, in Simple Calendar Pro, create a calendar event on {year}-{month}-{day}"
      " at {hour}h with the title '{event_title}' and the description"
      " '{event_description}'. The event should last for {duration_mins} mins."
  )

  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    self.before = self.list_rows(env.base_env)
    user_data_generation.generate_noise_files(
        "file",
        device_constants.MARKOR_DATA,
        env.base_env,
        _NOTE_TITLES,
    )

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
    if row_addition_successful:
        folder_name = self.params["folder_name"]

        exists = file_utils.check_file_or_folder_exists(
            folder_name, device_constants.MARKOR_DATA, env.base_env
        )

        if not exists:
            logging.info("%s not found", folder_name)
            return 0.0

        return 1.0
    return 0.0

  @classmethod
  def generate_random_params(cls) -> dict[str, Any]:
    random_folder_name = "folder_" + str(
        datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    )
    event = cls._get_random_target_row()
    n_noise_events = random.randint(0, 20)
    return {
        "folder_name": random_folder_name,
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


class MarkorCreateFolderwithCalender(MarkorandCalender, sqlite_validators.AddMultipleRows):
  """Task for checking that a new folder in Markor has been created with a specific name."""

  complexity = 2
  template = (
      "Create a new folder in Markor and name it using the first word of the title of the event in Oct 17."
  )

  def initialize_task(self, env: interface.AsyncEnv) -> None:
    super().initialize_task(env)
    self.before = self.list_rows(env.base_env)
    user_data_generation.generate_noise_files(
        "file",
        device_constants.MARKOR_DATA,
        env.base_env,
        _NOTE_TITLES,
    )

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
    if row_addition_successful:
        folder_name = "Call"

        exists = file_utils.check_file_or_folder_exists(
            folder_name, device_constants.MARKOR_DATA, env.base_env
        )

        if not exists:
            logging.info("%s not found", folder_name)
            return 0.0

        return 1.0
    return 0.0

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
    # return {"folder_name": random_folder_name}



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
