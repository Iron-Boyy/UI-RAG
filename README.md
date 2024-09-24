# UI-RAG

code is coming soon

## Using virtual device

1. Set up the Android Emulator
   1. Download Android Studio [here](https://developer.android.com/studio?gad_source=1&gclid=Cj0KCQjw3ZayBhDRARIsAPWzx8oLcadBD0vAq8xmUutaunLGSzhgEtLz4xVZ_SpV4G0xJazS7LxQkDsaAuveEALw_wcB&gclsrc=aw.ds)
   2. Create an Android Virtual Device (AVD) by following these instructions. For hardware select **Pixel 6**, for System Image select **Tiramisu, API Level 33**, and choose AVD name as **AndroidWorldAvd**. [Watch the setup video.](https://github.com/google-research/android_world/assets/162379927/efc33980-8b36-44be-bb2b-a92d4c334a50)

1. Launch the Android Emulator from the command line

    Launch the emulator from the command line, not using the Android Studio UI, with the `-grpc 8554` flag which is needed communication with accessibility forwarding app.

    ```bash
    # Typically it's located in ~/Android/Sdk/emulator/emulator or
    # ~/Library/Android/sdk/emulator/emulator
    EMULATOR_NAME=AndroidWorldAvd # From previous step
    ~/Library/Android/sdk/emulator/emulator -avd $EMULATOR_NAME -no-snapshot -grpc 8554
    ```


## Running tasks

**In Simple Calendar Pro, create a calendar event on 2023-10-29 at 13h with the title 'Call with the Team' and the description 'We will understand upcoming project milestones.'. The event should last for one hour.**

<video width="320" height="240" controls>
    <source src="https://github.com/Iron-Boyy/Android_world_dmcv/blob/main/asserts/github_rili.mov" type="video/mp4">
</video>

**How many attendees were present in the meeting titled 'Employee Performance Evaluation' in the Joplin app? Express your answer as just a single number.**

<video width="320" height="240" controls>
    <source src="https://github.com/Iron-Boyy/Android_world_dmcv/blob/main/asserts/github_jiansuo.mov" type="video/mp4">
</video>

**Send a text message using Simple SMS Messenger to +16597910719 with message: Beauty is in the eye of the beholder.**

<video width="320" height="240" controls>
    <source src="https://github.com/Iron-Boyy/Android_world_dmcv/blob/main/asserts/github_message.mov" type="video/mp4">
</video>

**Turn wifi off.**

<video width="320" height="240" controls>
    <source src="https://github.com/Iron-Boyy/Android_world_dmcv/blob/main/asserts/github_wifi.mov" type="video/mp4">
</video>



