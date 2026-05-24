BlendMindAI
AI Chat assistant addon for Blender using Groq and Gemini APIs
BlendMindAI brings AI assistance directly into Blender, so you can ask questions about modeling, animation, rigging, textures and more without leaving the software.

Features

Groq and Gemini API support
Conversation history (the AI remembers the context of your conversation)
Responds in the same language you write in (English, Portuguese, Spanish, etc.)
Multiple models available for both Groq and Gemini
Clear history button with message counter


Requirements

Blender 4.0 or higher
A free Groq API key and/or a free Gemini API key


How to get your API Keys
Groq (free)

Go to console.groq.com
Create an account
Go to API Keys and click Create API Key
Copy your key (it starts with gsk_)

Gemini (free)

Go to aistudio.google.com/apikey
Sign in with your Google account
Click Create API Key
Copy your key


Installation

Download BlendMindAI.py from the Releases page
Open Blender
Go to Edit → Preferences → Add-ons
Click Install and select the downloaded file
Enable the addon by checking the box next to BlendMindAI


How to use

In the 3D Viewport, press N to open the side panel
Click on the BlendMindAI tab
Select your API provider (Groq or Gemini)
Paste your API Key in the API Key field
Choose your preferred model
Type your question and click Send


Recommended Models
ProviderModelNotesGeminiGemini 2.5 Flash LiteBest free option, detailed responsesGroqGroq Compound MiniFast and capable

Notes

The conversation history is saved per Blender session and resets when you close Blender
If you switch between APIs mid-conversation, it is recommended to clear the history first
Models marked as "Pro" may require a paid plan


License
This project is licensed under the GNU General Public License v3.0. See the LICENSE file for details.

Made by partunax
Built with the help of Claude (Anthropic's AI assistant)
