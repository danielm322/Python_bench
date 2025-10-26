# Development Prompt for Sonnet

## Introduction

Your task is to develop a web application capable of downloading videos from youtube either in video or audio mp3 format to a local computer. 

## Requirements

- Create the application in a new foler called "YT-web-application". All code must be generated in this folder
- Use the most convenient framework for frontend and backend.
- Produce a modern UI style, with professional style
- Provide a text field for the user to paste the video URL.
- The user can specify if he wants to download in video format or audio (mp3) format
- The user can select the audio quality or video quality.
- The download button should open a download window where the user chooses the location and the name of the downloaded file.
- The web application follows current industry best practices
- The web application uses high quality code, is modular, and is a baseline for further improvement.
- Avoid the error: Failed to download HTTP Error 403: Forbidden. For this use appropriate headers anbd configurations for yt-dlp to successfully download


## Functionality

1. The user provides the link to desired youtube video
2. The program pulls the video from Youtube and copies them to the selected save path in the selected format (audio or video)
3. A progress indicator shows the processing progress.
4. A message is shown when the process is complete
5. The web application has an 'about' section, where more information on the creators of the application can be found.

