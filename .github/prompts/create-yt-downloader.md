# Development Prompt for Sonnet

## Introduction

Your task is to develop a basic GUI for the Linux desktop using PyQt5 or PyQt6. The purpose of this GUI is to enable the download of a youtube video to the local computer.

## Requirements

- Use PyQt5 or PyQt6 for the GUI.
- Provide a text field for the user to paste the video URL.
- Provide a path selection field for the user to choose where the video should be saved.
- Use the pytube library: https://github.com/pytube/pytube

## Functionality

1. The user provides the link to desired youtube video
2. The user selects the path where the video should be saved
3. The program pulls the video from Youtube and copies them to the selected save path.
4. A progress indicator shows the copy progress.
5. A success message is displayed when the video has been saved.