# BlendMindAI

**AI Chat assistant addon for Blender using Groq and Gemini APIs**

BlendMindAI brings AI assistance directly into Blender, so you can ask questions about modeling, animation, rigging, textures and more without leaving the software.

---

## Features

- Groq and Gemini API support
- Conversation history (the AI remembers the context of your conversation)
- Responds in the same language you write in (English, Portuguese, Spanish, etc.)
- Multiple models available for both Groq and Gemini
- Clear history button with message counter

---

## Requirements

- Blender 4.0 or higher
- A free Groq API key **and/or** a free Gemini API key

---

## How to get your API Keys

### Groq (free)
1. Go to [console.groq.com](https://console.groq.com)
2. Create an account
3. Go to **API Keys** and click **Create API Key**
4. Copy your key (it starts with `gsk_`)

### Gemini (free)
1. Go to [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click **Create API Key**
4. Copy your key

---

## Installation

1. Download **BlendMindAI.py** from the [Releases](../../releases) page
2. Open Blender
3. Go to **Edit → Preferences → Add-ons**
4. Click **Install** and select the downloaded file
5. Enable the addon by checking the box next to **BlendMindAI**

---

## How to use

1. In the **3D Viewport**, press **N** to open the side panel
2. Click on the **BlendMindAI** tab
3. Select your API provider (**Groq** or **Gemini**)
4. Paste your API Key in the **API Key** field
5. Choose your preferred model
6. Type your question and click **Send**

---

## Recommended Models

> **Tip:** Gemini models are recommended for Blender-related questions as they tend to give more detailed and accurate responses.

| Provider | Model | Notes |
|----------|-------|-------|
| Gemini | Gemini 2.5 Flash Lite | ⭐ Best option overall, detailed responses |
| Gemini | Gemini 2.5 Flash | Good alternative, slightly faster |
| Groq | Groq Compound Mini | Fast responses, good for quick questions |

---

## Notes

- The conversation history is saved per Blender session and resets when you close Blender
- If you switch between APIs mid-conversation, it is recommended to clear the history first

---

## License

This project is licensed under the **GNU General Public License v3.0**. See the [LICENSE](LICENSE) file for details.

---

Made by [partunax](https://github.com/partunax755)

Built with the help of [Claude](https://claude.ai) (Anthropic's AI assistant)
