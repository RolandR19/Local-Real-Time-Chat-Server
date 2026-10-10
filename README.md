Local Real-Time Chat Server

A lightweight, zero-configuration local chat server built with Python (aiohttp) and a modern HTML5/WebSockets web interface. Designed to let multiple devices (such as smartphones, tablets, and other computers) chat locally over a Wi-Fi network without requiring an internet connection or external hosting.

Features

Real-time Messaging: Instant message delivery across all connected clients using WebSockets.

Local Network Access: Automatically detects and displays local IP addresses so mobile devices (like iPhones via Safari or Android browsers) can easily connect.

Responsive Mobile UI: Clean, native-feeling chat interface inspired by modern messaging apps, optimized for small screens with safe-area support.

Single-File Simplicity: The entire backend server and frontend client are self-contained within a single Python script.

Requirements

Python 3.8 or higher

aiohttp library

Installation & Setup

Install dependencies:
Open your terminal and install the required aiohttp package:

pip install aiohttp


Run the server:
Execute the Python script:

python chat_server.py


Access the Chat:

On the host PC: Open your browser and go to http://localhost:8000

On other devices (phones/tablets): Connect to the same Wi-Fi network and open the URL displayed in your terminal (e.g., http://192.168.x.x:8000).

How to Use

Enter your preferred username when prompted upon opening the page.

Type your message in the text input box and press Enter or click Send.

Messages will update instantly for everyone connected to the local network session.
