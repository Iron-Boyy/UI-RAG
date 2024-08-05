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

"""A Multimodal Autonomous Agent for Android (M3A)."""

import time, os
from android_world.agents import agent_utils
from android_world.agents import base_agent
from android_world.agents import infer
from android_world.agents import m3a_utils
from android_world.env import adb_utils
from android_world.env import interface
from android_world.env import json_action
from android_world.env import representation_utils

from android_world.database import FileDatabase, DocumentDatabase, generate_md5_string, IndexDatabase
from android_world.embedding import get_embedding, BgeEmbedding
import tqdm

PROMPT_PREFIX = (
    'You are an agent who can operate an Android phone on behalf of a user.'
    " Based on user's goal/request, you may\n"
    '- Answer back if the request/goal is a question (or a chat message),'
    ' like user asks "What is my schedule for today?".\n'
    '- Complete some tasks described in the requests/goals by'
    ' performing actions (step by step) on the phone.\n\n'
    'When given a user request, you will try to complete it step by step.'
    ' At each step, you will be given the current screenshot (including the'
    ' original screenshot and the same screenshot with bounding'
    ' boxes and numeric indexes added to some UI elements) and a history of'
    ' what you have done (in text).'
    ' Also, the function of each element in the screen shot will also be provided.'#my addition
    ' Based on these pieces of information and'
    ' the goal, you must choose to perform one of the'
    ' action in the following list (action description followed by the JSON'
    ' format) by outputing the action in the correct JSON format.\n'
    '- If you think the task has been completed, finish the task by using the'
    ' status action with complete as goal_status:'
    ' `{{"action_type": "status", "goal_status": "complete"}}`\n'
    '- If you think the task is not feasible (including cases like you don\'t'
    ' have enough information or can not perform some necessary actions),'
    ' finish by using the `status` action with infeasible as goal_status:'
    ' `{{"action_type": "status", "goal_status": "infeasible"}}`\n'
    "- Answer user's question:"
    ' `{{"action_type": "answer", "text": "<answer_text>"}}`\n'
    '- Click/tap on an element on the screen. We have added marks (bounding'
    ' boxes with numeric indexes on their TOP LEFT corner) to most of the UI'
    ' elements in the screenshot, use the numeric index to indicate which'
    ' element you want to click:'
    ' `{{"action_type": "click", "index": <target_index>}}`.\n'
    '- Long press on an element on the screen, similar with the click action'
    ' above, use the numeric label on the bounding box to indicate which'
    ' element you want to long press:'
    ' `{{"action_type": "long_press", "index": <target_index>}}`.\n'
    '- Type text into a text field (this action contains clicking the text'
    ' field, typing in the text and pressing the enter, so no need to click on'
    ' the target field to start), use the numeric label'
    ' on the bounding box to indicate the target text field:'
    ' `{{"action_type": "input_text", "text": <text_input>,'
    ' "index": <target_index>}}`\n'
    '- Press the Enter key: `{{"action_type": "keyboard_enter"}}`\n'
    '- Navigate to the home screen: `{{"action_type": "navigate_home"}}`\n'
    '- Navigate back: `{{"action_type": "navigate_back"}}`\n'
    '- Scroll the screen or a scrollable UI element in one of the four'
    ' directions, use the same numeric index as above if you want to scroll a'
    ' specific UI element, leave it empty when scroll the whole screen:'
    ' `{{"action_type": "scroll", "direction": <up, down, left, right>,'
    ' "index": <optional_target_index>}}`\n'
    '- Open an app (nothing will happen if the app is not'
    ' installed): `{{"action_type": "open_app", "app_name": <name>}}`\n'
    '- Wait for the screen to update: `{{"action_type": "wait"}}`\n'
)


GUIDANCE = (
    'Here are some useful guidelines you need to follow:\n'
    'General:\n'
    '- Usually there will be multiple ways to complete a task, pick the'
    ' easiest one. Also when something does not work as expected (due'
    ' to various reasons), sometimes a simple retry can solve the problem,'
    " but if it doesn't (you can see that from the history),"
    ' SWITCH to other solutions.\n'
    '- Sometimes you may need to navigate the phone to gather information'
    ' needed to complete the task, for example if user asks'
    ' "what is my schedule tomorrow", then you may want to open the calendar'
    ' app (using the `open_app` action), look up information there, answer'
    " user's question (using the `answer` action) and finish (using"
    ' the `status` action with complete as goal_status).\n'
    '- For requests that are questions (or chat messages), remember to use'
    ' the `answer` action to reply to user explicitly before finish!'
    ' Merely displaying the answer on the screen is NOT sufficient (unless'
    ' the goal is something like "show me ...").\n'
    '- If the desired state is already achieved (e.g., enabling Wi-Fi when'
    " it's already on), you can just complete the task.\n"
    'Action Related:\n'
    '- Use the `open_app` action whenever you want to open an app'
    ' (nothing will happen if the app is not installed).\n'
    '- Use the `input_text` action whenever you want to type'
    ' something (including password) instead of clicking characters on the'
    ' keyboard one by one. Sometimes there is some default text in the text'
    ' field you want to type in, remember to delete them before typing.\n'
    '- For `click`, `long_press` and `input_text`, the index parameter you'
    ' pick must be VISIBLE in the screenshot and also in the UI element'
    ' list given to you (some elements in the list may NOT be visible on'
    ' the screen so you can not interact with them).\n'
    '- Consider exploring the screen by using the `scroll`'
    ' action with different directions to reveal additional content.\n'
    '- The direction parameter for the `scroll` action can be confusing'
    " sometimes as it's opposite to swipe, for example, to view content at the"
    ' bottom, the `scroll` direction should be set to "down". It has been'
    ' observed that you have difficulties in choosing the correct direction, so'
    ' if one does not work, try the opposite as well.\n'
    'Text Related Operations:\n'
    '- Normally to select certain text on the screen: <i> Enter text selection'
    ' mode by long pressing the area where the text is, then some of the words'
    ' near the long press point will be selected (highlighted with two pointers'
    ' indicating the range) and usually a text selection bar will also appear'
    ' with options like `copy`, `paste`, `select all`, etc.'
    ' <ii> Select the exact text you need. Usually the text selected from the'
    ' previous step is NOT the one you want, you need to adjust the'
    ' range by dragging the two pointers. If you want to select all text in'
    ' the text field, simply click the `select all` button in the bar.\n'
    "- At this point, you don't have the ability to drag something around the"
    ' screen, so in general you can not select arbitrary text.\n'
    '- To delete some text: the most traditional way is to place the cursor'
    ' at the right place and use the backspace button in the keyboard to'
    ' delete the characters one by one (can long press the backspace to'
    ' accelerate if there are many to delete). Another approach is to first'
    ' select the text you want to delete, then click the backspace button'
    ' in the keyboard.\n'
    '- To copy some text: first select the exact text you want to copy, which'
    ' usually also brings up the text selection bar, then click the `copy`'
    ' button in bar.\n'
    '- To paste text into a text box, first long press the'
    ' text box, then usually the text selection bar will appear with a'
    ' `paste` button in it.\n'
    '- When typing into a text field, sometimes an auto-complete dropdown'
    ' list will appear. This usually indicating this is a enum field and you'
    ' should try to select the best match by clicking the corresponding one'
    ' in the list.\n'
)


ACTION_SELECTION_PROMPT_TEMPLATE = (
    PROMPT_PREFIX
    + '\nThe current user goal/request is: {goal}\n\n'
    'Here is a history of what you have done so far:\n{history}\n\n'
    'The current screenshot and the same screenshot with bounding boxes'
    ' and labels added are also given to you.\n'
    'Here is a list of detailed'
    ' information for some of the UI elements (notice that some elements in'
    ' this list may not be visible in the current screen and so you can not'
    ' interact with it, can try to scroll the screen to reveal it first),'
    ' the numeric indexes are'
    ' consistent with the ones in the labeled screenshot:\n{ui_elements}\n'
    + GUIDANCE
    + '{additional_guidelines}'
    +' Here is the functions of all the UI elements in the app:\n{ui_function}\n'
    +' You should strictly decide your action basing on the function list above.'
    + '\nNow output an action from the above list in the correct JSON format,'
    ' following the reason why you do that. Your answer should look like:\n'
    'Reason: ...\nAction: {{"action_type":...}}\n\n'
    'Your Answer:\n'
)


SUMMARY_PROMPT_TEMPLATE = (
    PROMPT_PREFIX
    + '\nThe (overall) user goal/request is: {goal}\n'
    'Now I want you to summerize the latest step.\n'
    'You will be given the screenshot before you performed the action (which'
    ' has a text label "before" on the bottom right), the action you chose'
    ' (together with the reason) and the screenshot after the action was'
    ' performed (which has a text label "after" on the bottom right).\n'
    'Also here is the list of detailed information for some UI elements'
    ' in the before screenshot:\n{before_elements}\n'
    'Here is the list for the after screenshot:\n{after_elements}\n'
    'This is the action you picked: {action}\n'
    'Based on the reason: {reason}\n\n'
    'By comparing the two screenshots (plus the UI element lists) and the'
    ' action performed, give a brief summary of this step. This summary'
    ' will be added to action history and used in future action selection,'
    ' so try to include essential information you think that will be most'
    ' useful for future action selections like what you'
    ' intended to do, why, if it worked as expected, if not'
    ' what might be the reason (be critical, the action/reason might be'
    ' wrong), what should/should not be done next and so on. Some more'
    ' rules/tips you should follow:\n'
    # '- Keep it short (better less than 50 words) and in a single line\n'
    '- Keep it detail (around 200 words)\n'
    "- Some actions (like `answer`, `wait`) don't involve screen change,"
    ' you can just assume they work as expected.\n'
    '- Given this summary will be added into action history, it can be used as'
    ' memory to include information that needs to be remembered, or shared'
    ' between different apps.\n\n'
    'Summary of this step: '
)

OBSERVER_PROMPT = (
  'Imagine that you are a user who has an android phone and you can use all kinds of apps skillfullly.'
  ' Now you are given the current screenshot (including the original screenshot and the same screenshot with bounding boxes and numeric indexes added to some UI elements),'
  ' Your task is introducing the function of each UI element, as if someone was asking you to help with using an app in your phone.'
  ' You should detail an element\'s purpose, list all the possible result for each operation of an UI element.'
  ' Outputing all the (function:xxx,UI element:related UI element\'s index) pair in the correct JSON format.'
  # 'Here is the screenshot:\n{screenshot}\n'
  # 'Here is the labeled screenshot:\n{labeled_screenshot}\n'
  'Now your task begin:'
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
        if ui_element.content_description:
            element_id = ui_element.resource_name+"."+ui_element.class_name+"."+ui_element.content_description
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


def _action_selection_prompt(
    goal: str,
    history: list[str],
    ui_elements: str,
    ui_function: str,
    additional_guidelines: list[str] | None = None,
) -> str:
  """Generate the prompt for the action selection.

  Args:
    goal: The current goal.
    history: Summaries for previous steps.
    ui_elements: A list of descriptions for the UI elements.
    additional_guidelines: Task specific guidelines.

  Returns:
    The text prompt for action selection that will be sent to gpt4v.
  """
  if history:
    history = '\n'.join(history)
  else:
    history = 'You just started, no action has been performed yet.'

  extra_guidelines = ''
  if additional_guidelines:
    extra_guidelines = 'For The Current Task:\n'
    for guideline in additional_guidelines:
      extra_guidelines += f'- {guideline}\n'

  return ACTION_SELECTION_PROMPT_TEMPLATE.format(
      goal=goal,
      history=history,
      ui_elements=ui_elements if ui_elements else 'Not available',
      ui_function=ui_function,
      additional_guidelines=extra_guidelines,
  )


def _summarize_prompt(
    action: str,
    reason: str,
    goal: str,
    before_elements: str,
    after_elements: str,
) -> str:
  """Generate the prompt for the summarization step.

  Args:
    action: Action picked.
    reason: The reason to pick the action.
    goal: The overall goal.
    before_elements: Information for UI elements on the before screenshot.
    after_elements: Information for UI elements on the after screenshot.

  Returns:
    The text prompt for summarization that will be sent to gpt4v.
  """
  return SUMMARY_PROMPT_TEMPLATE.format(
      goal=goal,
      before_elements=before_elements,
      after_elements=after_elements,
      action=action,
      reason=reason,
  )



class DocumentRetrieval():
    def __init__(self, dim, cache_dir = "./", emd_path="", override_db=False) -> None:
        self.dim = dim
        self.cache_dir = cache_dir
        self.mkdir_if_not_exist(cache_dir)
        self.override_db = override_db

        self.doc_db = None
        self.file_db = None
        self.index_db = None

        self.file_db = FileDatabase(db_path=os.path.join(self.cache_dir,"file_database.db"))

        if emd_path != "":
            self.emd_model = BgeEmbedding(emd_path)
            self.get_embedding = self.emd_model.encode
        else:
            self.get_embedding = get_embedding

    def mkdir_if_not_exist(self, path):
        try:
            os.makedirs(path)
        except FileExistsError:
            print("Directory already exists")

    def init_database(self, db_name):
        if os.path.exists(os.path.join(self.cache_dir,f"{db_name}_text.db")):
            os.remove(os.path.join(self.cache_dir,f"{db_name}_text.db"))
            os.remove(os.path.join(self.cache_dir,f"{db_name}_index.db"))
        self.doc_db = DocumentDatabase(db_path=os.path.join(self.cache_dir,f"{db_name}_text.db"))
        self.index_db = IndexDatabase(db_path=os.path.join(self.cache_dir,f"{db_name}_index.db"), dim=self.dim)

    def _upload_document(self, file_path):
        loader = PDFLoader()
        ret = loader.load_document(doc_path=file_path)
        if ret != 'Success':
            raise Exception('Error loading document')
        document_loaded = loader.extract_doc_content()       
        loader.unload_document()

        return document_loaded

    def _split_document(self, document, chunk_size):
        
        chunk_list_all = []
        total_content = ""
        for page in document['doc_content']:
            page_num = page['page_num']
            page_content = page['page_content']
            total_content += page_content
            chunk_list = split_text_internal(page_content, chunk_size)

            chunk_list_all.append((page_num,chunk_list))
        
        filesize = self.cal_filesize(total_content)

        return chunk_list_all,filesize
    
    # def json2chunk(self, document):


    

    def cal_filesize(self, text):
        return len(text.encode('utf-8'))


    def add_document(self, file_dir, databasename,chunk_size = 2000):
        self.init_database(databasename)
        chunk_list_all = []
        for i in range(len(file_dir)):
            chunk_list = []
            chunk_list.append(file_dir[i])
            chunk_list_all.append((i,chunk_list))
        
        index = 0
        for (page_num, chunks) in tqdm.tqdm(chunk_list_all):
            for chunk in chunks:
                embedding = self.get_embedding(chunk)
                self.index_db.add(embedding,[index])
                self.doc_db.add(index,chunk,"",page_num,commit=False)
                index += 1
        
        self.index_db.save()
        self.doc_db.commit()
    

    def del_document(self, file_path):
        
        filename = os.path.basename(file_path)
        md5_name = generate_md5_string(filename)
        
        if self.file_db is None:
            self.file_db = FileDatabase(db_path=os.path.join(self.cache_dir,"file_database.db"))

        result = self.file_db.search_with_name(filename, return_info=['kbname'])

        if result is None:
            print("Document not found, return")
        else:
            _, kbname = result
            kbname = [x[0] for x in kbname]
            for _kbname in kbname:

                if os.path.exists(os.path.join(self.cache_dir, f"{_kbname}_text.db")):
                    os.remove(os.path.join(self.cache_dir, f"{_kbname}_text.db"))
                if os.path.exists(os.path.join(self.cache_dir, f"{_kbname}_index.db")):
                    os.remove(os.path.join(self.cache_dir, f"{_kbname}_index.db"))
            self.file_db.delete_with_name(filename)

    def search_document(self, query, top_k = 2, threshold=None):
        base_embedding = self.get_embedding(query)

        query_len = base_embedding.shape[0]
        result = self.index_db.search(base_embedding, top_k)
        
        distances = result[0][0]
        indexes = result[1][0]
        result = [(x,y) for (x,y) in zip(distances, indexes)]
        if threshold is not None:
            result = [(x,y) for (x,y) in result if x >= threshold]

        
        retrieval_content_list = []
        retrieval_page_list = []
        retrieval_score_list = []
        
        for (distance, index) in result:
            _, chunk_info = self.doc_db.search_with_vec_index(index, return_info=['chunk_content','page'])
            if chunk_info.__len__() == 1:
                chunk_info = [x for x in chunk_info[0]]

                retrieval_content_list.append(chunk_info[0])
                retrieval_page_list.append(chunk_info[1])
                retrieval_score_list.append(distance)


        return {
            "content": retrieval_content_list,
            "page": retrieval_page_list,
            "score": retrieval_score_list
        }
    
    

    def template_with_qa(self, query, content_dict):

        content_len = content_dict['content'].__len__()
        content_list = "[no_ref]{}\n" * content_len
        content_list_completed = content_list.format(*content_dict['content'])
        max_score = max(content_dict['score'])

        prompt = '''请参考以下知识回复用户最新的问题，参考程度为：{}，在生成时注明所引用的知识的角标，前缀为[no_ref]的知识无需注明。
{}
问题：{}
'''
        return prompt.format(max_score, content_list_completed, query)
    

    def search_related(self, query, top_k):

        content_dict = self.search_document(query, top_k)
        print(content_dict)

        return content_dict['content']


class M3A(base_agent.EnvironmentInteractingAgent):
  """M3A which stands for Multimodal Autonomous Agent for Android."""

  # Wait a few seconds for the screen to stablize after executing an action.
  WAIT_AFTER_ACTION_SECONDS = 2.0

  def __init__(
      self,
      env: interface.AsyncEnv,
      llm: infer.MultimodalLlmWrapper,
      name: str = 'M3A',
  ):
    """Initializes a RandomAgent.

    Args:
      env: The environment.
      llm: The multimodal LLM wrapper.
      name: The agent name.
    """
    super().__init__(env, name)
    self.llm = llm
    self.history = []
    self.additional_guidelines = None
    self.observation_output = ""

  def set_task_guidelines(self, task_guidelines: list[str]) -> None:
    self.additional_guidelines = task_guidelines

  def reset(self, go_home_on_reset: bool = False):
    super().reset(go_home_on_reset)
    # Hide the coordinates on screen which might affect the vision model.
    self.env.hide_automation_ui()
    self.history = []

  def step(self, goal: str) -> base_agent.AgentInteractionResult:
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
    print('----------step ' + str(len(self.history) + 1))

    state = self.get_post_transition_state()
    orientation = adb_utils.get_orientation(self.env.base_env)
    logical_screen_size = self.env.logical_screen_size
    physical_frame_boundary = adb_utils.get_physical_frame_boundary(
        self.env.base_env
    )

    before_ui_elements = state.ui_elements
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

    if len(self.history) == 0:

      databasename = "appdatabase"
      db_sys = DocumentRetrieval(384, emd_path="/home/SENSETIME/luozhihao/code/android_world/bge-small-en-v1.5", override_db=True)
      app_introduction_path = "/home/SENSETIME/luozhihao/code/AppAgent/apps/introduction"
      app_introduction_dir = os.listdir(app_introduction_path)
      introduction = []
      for file in app_introduction_dir:
        with open(os.path.join(app_introduction_path, file), "r") as w:
          introduction_content = w.read()
        introduction.append(file.split("_")[0]+":"+introduction_content)
      db_sys.add_document(introduction, databasename, chunk_size=200)

      documention= db_sys.search_related(goal, 2)

      ui_doc = ""
      for i in range(len(documention)):
        app_name = documention[i].split(":")[0]
        app_folder_path = os.path.join("/home/SENSETIME/luozhihao/code/AppAgent/apps",app_name.replace(" ","*"))
        app_ui_path = os.path.join(app_folder_path,app_name+".txt")
        with open(app_ui_path, "r") as w:
          doc_content = w.read()
        ui_doc+=app_name+":\n"+doc_content+"\n\n"

      print(ui_doc)
      


      self.observation_output=ui_doc
      # self.observation_output="None"
    # if len(self.history)!=0:
    #   observation_prompt = OBSERVER_PROMPT
    #   # .format(
    #   #   screenshot=before_screenshot,
    #   #   labeled_screenshot=before_ui_elements_list
    #   # )
    #   observation_output, raw_response = self.llm.predict_mm(
    #       observation_prompt,
    #       [
    #           step_data['raw_screenshot'],
    #           before_screenshot,
    #       ],
    #   )
      # print(observation_prompt)
      # print(observation_output)


    action_prompt = _action_selection_prompt(
        goal,
        [
            'Step ' + str(i + 1) + '- ' + step_info['summary']
            for i, step_info in enumerate(self.history)
        ],
        before_ui_elements_list,
        self.observation_output,
        self.additional_guidelines,
    )
    step_data['action_prompt'] = action_prompt
    # print(action_prompt)
    action_output, raw_response = self.llm.predict_mm(
        action_prompt,
        [
            step_data['raw_screenshot'],
            before_screenshot,
        ],
    )

    if not raw_response:
      raise RuntimeError('Error calling LLM in action selection phase.')
    step_data['action_output'] = action_output
    step_data['action_raw_response'] = raw_response

    reason, action = m3a_utils.parse_reason_action_output(action_output)

    # If the output is not in the right format, add it to step summary which
    # will be passed to next step and return.
    if (not reason) or (not action):
      print('Action prompt output is not in the correct format.')
      step_data['summary'] = (
          'Output for action selection is not in the correct format, so no'
          ' action is performed.'
      )
      self.history.append(step_data)

      return base_agent.AgentInteractionResult(
          False,
          step_data,
      )

    print('Action: ' + action)
    print('Reason: ' + reason)

    try:
      converted_action = json_action.JSONAction(
          **agent_utils.extract_json(action),
      )
    except Exception as e:  # pylint: disable=broad-exception-caught
      print('Failed to convert the output to a valid action.')
      print(str(e))
      step_data['summary'] = (
          'Can not parse the output to a valid action. Please make sure to pick'
          ' the action from the list with required parameters (if any) in the'
          ' correct JSON format!'
      )
      self.history.append(step_data)
      return base_agent.AgentInteractionResult(
          False,
          step_data,
      )

    if (
        converted_action.action_type
        in ['click', 'long_press', 'input_text', 'scroll']
        and converted_action.index is not None
    ):
      if converted_action.index >= len(before_ui_elements):
        print('Index out of range.')
        step_data['summary'] = (
            'The parameter index is out of range. Remember the index must be in'
            ' the UI element list!'
        )
        self.history.append(step_data)
        return base_agent.AgentInteractionResult(False, step_data)

      # Add mark to the target element.
      m3a_utils.add_ui_element_mark(
          step_data['raw_screenshot'],
          before_ui_elements[converted_action.index],
          converted_action.index,
          logical_screen_size,
          physical_frame_boundary,
          orientation,
      )

    if converted_action.action_type == 'status':
      if converted_action.goal_status == 'infeasible':
        print('Agent stopped since it thinks mission impossible.')
      step_data['summary'] = 'Agent thinks the request has been completed.'
      self.history.append(step_data)
      return base_agent.AgentInteractionResult(
          True,
          step_data,
      )

    if converted_action.action_type == 'answer':
      print('Agent answered with: ' + converted_action.text)

    try:
      self.env.execute_action(converted_action)
    except Exception as e:  # pylint: disable=broad-exception-caught
      print('Failed to execute action.')
      print(str(e))
      step_data['summary'] = (
          'Can not execute the action, make sure to select the action with'
          ' the required parameters (if any) in the correct JSON format!'
      )
      return base_agent.AgentInteractionResult(
          False,
          step_data,
      )

    time.sleep(self.WAIT_AFTER_ACTION_SECONDS)

    state = self.env.get_state(wait_to_stabilize=False)
    orientation = adb_utils.get_orientation(self.env.base_env)
    logical_screen_size = self.env.logical_screen_size
    physical_frame_boundary = adb_utils.get_physical_frame_boundary(
        self.env.base_env
    )

    after_ui_elements = state.ui_elements
    after_ui_elements_list = _generate_ui_elements_description_list(
        after_ui_elements, logical_screen_size
    )
    after_screenshot = state.pixels.copy()
    for index, ui_element in enumerate(after_ui_elements):
      if m3a_utils.validate_ui_element(ui_element, logical_screen_size):
        m3a_utils.add_ui_element_mark(
            after_screenshot,
            ui_element,
            index,
            logical_screen_size,
            physical_frame_boundary,
            orientation,
        )

    m3a_utils.add_screenshot_label(
        step_data['before_screenshot_with_som'], 'before'
    )
    m3a_utils.add_screenshot_label(after_screenshot, 'after')
    step_data['after_screenshot_with_som'] = after_screenshot.copy()

    summary_prompt = _summarize_prompt(
        action,
        reason,
        goal,
        before_ui_elements_list,
        after_ui_elements_list,
    )
    summary, raw_response = self.llm.predict_mm(
        summary_prompt,
        [
            before_screenshot,
            after_screenshot,
        ],
    )

    if not raw_response:
      step_data['summary'] = (
          'Some error occurred calling LLM during summarization phase.'
      )
      self.history.append(step_data)
      return base_agent.AgentInteractionResult(
          False,
          step_data,
      )

    step_data['summary_prompt'] = summary_prompt
    step_data['summary'] = f'Action selected: {action}. {summary}'
    print('Summary: ' + summary)
    step_data['summary_raw_response'] = raw_response

    self.history.append(step_data)
    return base_agent.AgentInteractionResult(
        False,
        step_data,
    )
