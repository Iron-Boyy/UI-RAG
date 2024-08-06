import argparse
import datetime

from collections.abc import Sequence
import cv2
import os
import shutil
import sys
import time

from absl import app
from absl import flags
from and_controller import list_all_devices, AndroidController, traverse_tree
from app_config import load_config
from app_utils import print_with_color, draw_bbox_multi
from env import env_launcher
from env import adb_utils
from env import representation_utils
from env import json_action
import agent_utils
import m3a_utils


def _find_adb_directory() -> str:
  """Returns the directory where adb is located."""
  potential_paths = [
      os.path.expanduser('~/Library/Android/sdk/platform-tools/adb'),
      os.path.expanduser('~/Android/Sdk/platform-tools/adb'),
  ]
  for path in potential_paths:
    if os.path.isfile(path):
      return path
  raise EnvironmentError(
      'adb not found in the common Android SDK paths. Please install Android'
      " SDK and ensure adb is in one of the expected directories. If it's"
      ' already installed, point to the installed location.'
  )

_ADB_PATH = flags.DEFINE_string(
    'adb_path',
    _find_adb_directory(),
    'Path to adb. Set if not installed through SDK.',
)
_EMULATOR_SETUP = flags.DEFINE_boolean(
    'perform_emulator_setup',
    False,
    'Whether to perform emulator setup. This must be done once and only once'
    ' before running Android World. After an emulator is setup, this flag'
    ' should always be False.',
)
_DEVICE_CONSOLE_PORT = flags.DEFINE_integer(
    'console_port',
    5554,
    'The console port of the running Android device. This can usually be'
    ' retrieved by looking at the output of `adb devices`. In general, the'
    ' first connected device is port 5554, the second is 5556, and'
    ' so on.',
)

_APP  = flags.DEFINE_string(
    'app',
    'None',
    'None',
)
_DEMO  = flags.DEFINE_string(
    'demo',
    'None',
    'None',
)
_ROOTDIR  = flags.DEFINE_string(
    'root_dir',
    './',
    'None',
)


def _generate_ui_element_description(
    ui_element: representation_utils.UIElement, index: int
) -> str:
  """Generate a description for a given UI element with important information.

  Args:
    ui_element: UI elements for the current screen.
    index: The numeric index for the UI element.

  Returns:
    The description for the UI element.
  """
  if ui_element.resource_name:
    if ui_element.text:
        element_id = ui_element.resource_name+"."+ui_element.class_name+"."+ui_element.text
    else:
        element_id = ui_element.resource_name+"."+ui_element.class_name
  else:
    if ui_element.text:
        element_id = ui_element.package_name+"."+ui_element.class_name+"."+ui_element.text
    else:
        if ui_element.content_description:
            element_id = ui_element.package_name+"."+ui_element.class_name+"."+ui_element.content_description
        else:
            element_id = ui_element.package_name+"."+ui_element.class_name
  element_description = f'UI element {element_id}: {{"index": {index}, '
  if ui_element.text:
    element_description += f'"text": "{ui_element.text}", '
  if ui_element.content_description:
    element_description += (
        f'"content_description": "{ui_element.content_description}", '
    )
  if ui_element.hint_text:
    element_description += f'"hint_text": "{ui_element.hint_text}", '
  if ui_element.tooltip:
    element_description += f'"tooltip": "{ui_element.tooltip}", '
  element_description += (
      f'"is_clickable": {"True" if ui_element.is_clickable else "False"}, '
  )
  element_description += (
      '"is_long_clickable":'
      f' {"True" if ui_element.is_long_clickable else "False"}, '
  )
  element_description += (
      f'"is_editable": {"True" if ui_element.is_editable else "False"}, '
  )
  if ui_element.is_scrollable:
    element_description += '"is_scrollable": True, '
  if ui_element.is_focusable:
    element_description += '"is_focusable": True, '
  element_description += (
      f'"is_selected": {"True" if ui_element.is_selected else "False"}, '
  )
  element_description += (
      f'"is_checked": {"True" if ui_element.is_checked else "False"}, '
  )
  return element_description[:-2] + '}'


def _generate_ui_elements_description_list(
    ui_elements: list[representation_utils.UIElement],
    screen_width_height_px: tuple[int, int],
) -> str:
  """Generate concise information for a list of UIElement.

  Args:
    ui_elements: UI elements for the current screen.
    screen_width_height_px: The height and width of the screen in pixels.

  Returns:
    Concise information for each UIElement.
  """
  tree_info = ''
  for index, ui_element in enumerate(ui_elements):
    if m3a_utils.validate_ui_element(ui_element, screen_width_height_px):
      tree_info += _generate_ui_element_description(ui_element, index) + '\n'
  return tree_info

def main(argv: Sequence[str]) -> None:
    del argv
    # arg_desc = "AppAgent - Human Demonstration"
    # parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=arg_desc)
    # parser.add_argument("--app")
    # parser.add_argument("--demo")
    # parser.add_argument("--root_dir", default="./")
    # args = vars(parser.parse_args())

    app = _APP.value
    demo_name = _DEMO.value
    root_dir = _ROOTDIR.value

    configs = load_config()

    if not app:
        print_with_color("What is the name of the app you are going to demo?", "blue")
        app = input()
        # app = app.replace(" ", "")
    if not demo_name:
        demo_timestamp = int(time.time())
        demo_name = datetime.datetime.fromtimestamp(demo_timestamp).strftime(f"demo_{app}_%Y-%m-%d_%H-%M-%S")

    work_dir = os.path.join(root_dir, "apps")
    if not os.path.exists(work_dir):
        os.mkdir(work_dir)
    work_dir = os.path.join(work_dir, app)
    if not os.path.exists(work_dir):
        os.mkdir(work_dir)
    demo_dir = os.path.join(work_dir, "demos")
    if not os.path.exists(demo_dir):
        os.mkdir(demo_dir)
    task_dir = os.path.join(demo_dir, demo_name)
    if os.path.exists(task_dir):
        shutil.rmtree(task_dir)
    os.mkdir(task_dir)
    raw_ss_dir = os.path.join(task_dir, "raw_screenshots")
    print(raw_ss_dir)
    os.mkdir(raw_ss_dir)
    xml_dir = os.path.join(task_dir, "xml")
    os.mkdir(xml_dir)
    labeled_ss_dir = os.path.join(task_dir, "labeled_screenshots")
    os.mkdir(labeled_ss_dir)
    element_ss_dir = os.path.join(task_dir, "ui_element")
    os.mkdir(element_ss_dir)
    record_path = os.path.join(task_dir, "record.txt")
    record_file = open(record_path, "w")
    task_desc_path = os.path.join(task_dir, "task_desc.txt")



    device_list = list_all_devices()
    if not device_list:
        print_with_color("ERROR: No device found!", "red")
        sys.exit()
    print_with_color("List of devices attached:\n" + str(device_list), "yellow")
    if len(device_list) == 1:
        device = device_list[0]
        print_with_color(f"Device selected: {device}", "yellow")
    else:
        print_with_color("Please choose the Android device to start demo by entering its ID:", "blue")
        device = input()
    controller = AndroidController(device)


    # print_with_color("Please state the goal of your following demo actions clearly, e.g. send a message to John", "blue")
    # task_desc = input()
    task_desc = "None"
    with open(task_desc_path, "w") as f:
        f.write(task_desc)


    env = env_launcher.load_and_setup_env(
        console_port=_DEVICE_CONSOLE_PORT.value,
        emulator_setup=_EMULATOR_SETUP.value,
        adb_path=_ADB_PATH.value,
    )
    env_launcher.verify_api_level(env)

    step = 0
    while True:
        step+=1
        step_data = {
            'raw_screenshot': None,
            'before_screenshot_with_som': None,
            'after_screenshot_with_som': None,
            'action_prompt': None,
            'action_output': None,
            'action_raw_response': None,
            'summary_prompt': None,
            'summary': None,
            'summary_raw_response': None,
        }
        state = env.get_state(wait_to_stabilize=True)
        orientation = adb_utils.get_orientation(env.base_env)
        logical_screen_size = env.logical_screen_size
        physical_frame_boundary = adb_utils.get_physical_frame_boundary(
            env.base_env
        )

        before_ui_elements = state.ui_elements
        print(before_ui_elements)
        before_ui_elements_list = _generate_ui_elements_description_list(
            before_ui_elements, logical_screen_size
        )
        step_data['raw_screenshot'] = state.pixels.copy()
        before_screenshot = state.pixels.copy()
        for index, ui_element in enumerate(before_ui_elements):
            if m3a_utils.validate_ui_element(ui_element, logical_screen_size):
                m3a_utils.add_ui_element_mark(
                    before_screenshot,
                    ui_element,
                    index,
                    logical_screen_size,
                    physical_frame_boundary,
                    orientation,
                )
        step_data['before_screenshot_with_som'] = before_screenshot.copy()
        screenshot_path = controller.get_screenshot(f"{demo_name}_{step}", raw_ss_dir)
        # xml_path = controller.get_xml(f"{demo_name}_{step}", xml_dir)
        user_input = "xxx"
        print_with_color("Choose one of the following actions you want to perform on the current screen:\nclick, double_tap, long_press "
                        "input_text, keyboard_enter, navigate_home, navigate_back, scroll, open_app, wait, stop", "blue")
        print(before_ui_elements_list)
        while user_input.lower() != "click" and user_input.lower() != "double_tap" and user_input.lower() != "long_press" \
                    and user_input.lower() != "input_text" and user_input.lower() != "keyboard_enter"\
                    and user_input.lower() != "navigate_home" and user_input.lower() != "navigate_back"\
                    and user_input.lower() != "scroll" and user_input.lower() != "stop"\
                    and user_input.lower() != "open_app" and user_input.lower() != "wait":
            user_input = input()
        action = {}
        
        element_list = screenshot_path.split("/")[-1][:-4]+".txt"
        element_list_path = os.path.join(element_ss_dir, element_list)
        element_list_file = open(element_list_path, "w")
        element_list_file.write(before_ui_elements_list)
        element_list_file.close()
        before_ui_elements_list = before_ui_elements_list.split('\nUI ')

        if user_input.lower() == "click":
            print("input element index:")
            action["index"] = int(input())
            action["action_type"] = user_input.lower()
            uid = before_ui_elements_list[action["index"]].split(": ")[0].split("element ")[1].replace("/","-").replace("\n","")
            record_file.write(f"click({uid}):::{element_list_path}\n")
        elif user_input.lower() == "double_tap":
            print("input element index:")
            action["index"] = int(input())
            action["action_type"] = user_input.lower()
            uid = before_ui_elements_list[action["index"]].split(": ")[0].split("element ")[1].replace("/","-").replace("\n","")
            record_file.write(f"double_tap({uid}):::{element_list_path}\n")
        elif user_input.lower() == "long_press":
            print("input element index:")
            action["index"] = int(input())
            action["action_type"] = user_input.lower()
            uid = before_ui_elements_list[action["index"]].split(": ")[0].split("element ")[1].replace("/","-").replace("\n","")
            record_file.write(f"long_press({uid}):::{element_list_path}\n")
        elif user_input.lower() == "input_text":
            print("input element index:")
            action["index"] = int(input())
            print("input text:")
            action["text"] = input()
            action["action_type"] = user_input.lower()
            uid = before_ui_elements_list[action["index"]].split(": ")[0].split("element ")[1].replace("/","-").replace("\n","")
            text = action["text"]
            record_file.write(f"input_text({uid}:sep:\"{text}\"):::{element_list_path}\n")
        elif user_input.lower() == "keyboard_enter":
            action["action_type"] = user_input.lower()
            record_file.write(f"keyboard_enter():::{element_list_path}\n")
        elif user_input.lower() == "navigate_home":
            action["action_type"] = user_input.lower()
            record_file.write(f"navigate_home():::{element_list_path}\n")
        elif user_input.lower() == "navigate_back":
            action["action_type"] = user_input.lower()
            record_file.write(f"navigate_back():::{element_list_path}\n")
        elif user_input.lower() == "scroll":
            print("input element index:")
            action["index"] = int(input())
            print("input the direction (<up, down, left, right>):")
            action["direction"] = input()
            action["action_type"] = user_input.lower()
            uid = before_ui_elements_list[action["index"]].split(": ")[0].split("element ")[1].replace("/","-").replace("\n","")
            direction = action["direction"]
            record_file.write(f"scroll({uid}:sep:\"{direction}\"):::{element_list_path}\n")
        elif user_input.lower() == "open_app":
            print("input app name:")
            action["app_name"] = input()
            action["action_type"] = user_input.lower()
            app_name = action["app_name"]
            record_file.write(f"open_app({app_name}):::{element_list_path}\n")
        elif user_input.lower() == "wait":
            action["action_type"] = user_input.lower()
            record_file.write(f"wait():::{element_list_path}\n")
        elif user_input.lower() == "stop":
            record_file.write("stop\n")
            record_file.close()
            break

        converted_action = json_action.JSONAction(
            **agent_utils.extract_json(str(action)),
        )

        env.execute_action(converted_action)
        time.sleep(3)
    print_with_color(f"Demonstration phase completed. {step} steps were recorded.", "yellow")


if __name__ == '__main__':
  app.run(main)