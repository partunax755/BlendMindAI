bl_info = {
    "name": "BlendMindAI",
    "author": "partunax",
    "version": (1, 3, 5),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > AI Assistant",
    "description": "BlendMindAI - AI Chat inside Blender using Groq or Gemini (Beta)",
    "category": "3D View",
}

import bpy
import threading
import urllib.request
import urllib.error
import json

class AIAddonProperties(bpy.types.PropertyGroup):
    provider: bpy.props.EnumProperty(
        name="Provider",
        items=[
            ("groq", "Groq", "Use Groq API"),
            ("gemini", "Gemini", "Use Google Gemini API"),
        ],
        default="groq"
    )
    groq_api_key: bpy.props.StringProperty(
        name="Groq API Key",
        default="",
        subtype='PASSWORD'
    )
    gemini_api_key: bpy.props.StringProperty(
        name="Gemini API Key",
        default="",
        subtype='PASSWORD'
    )
    user_input: bpy.props.StringProperty(
        name="Message",
        default=""
    )
    response_text: bpy.props.StringProperty(
        name="Response",
        default="The response will appear here...",
    )
    is_loading: bpy.props.BoolProperty(default=False)
    conversation_history: bpy.props.StringProperty(
        name="History",
        default="[]"
    )

    groq_model: bpy.props.EnumProperty(
        name="Groq Model",
        items=[
            ("groq/compound",                 "Groq Compound",         "Modelo composto da Groq"),
            ("groq/compound-mini",            "Groq Compound Mini",    "Versão menor do Groq Compound"),
            ("mixtral-8x7b-32768",            "Mixtral 8x7B",          "Mistral AI"),
            ("openai/gpt-oss-120b",           "GPT OSS 120B",          "OpenAI open source 120B"),
            ("openai/gpt-oss-20b",            "GPT OSS 20B",           "OpenAI open source 20B"),
            ("qwen/qwen3-32b",                "Qwen3 32B",             "Alibaba Cloud"),
            ("canopylabs/orpheus-v1-english", "Orpheus v1 English",    "Canopy Labs"),
            ("llama-3.1-8b-instant",          "Llama 3.1 8B",          "Meta - rápido"),
            ("llama-3.3-70b-versatile",       "Llama 3.3 70B",         "Meta - capaz"),
        ],
        default="groq/compound-mini"
    )

    gemini_model: bpy.props.EnumProperty(
        name="Gemini Model",
        items=[
            ("gemini-3.5-flash",        "Gemini 3.5 Flash",        "Mais recente - gratuito"),
            ("gemini-2.5-flash",        "Gemini 2.5 Flash",        "Melhor custo-benefício - gratuito"),
            ("gemini-2.5-flash-lite",   "Gemini 2.5 Flash Lite",   "Mais rápido e leve - gratuito"),
            ("gemini-3.1-flash-lite",   "Gemini 3.1 Flash Lite",   "Geração 3 leve - gratuito"),
            ("gemini-3-flash",          "Gemini 3 Flash",          "Geração 3 - gratuito"),
            ("gemma-4-26b",             "Gemma 4 26B",             "Modelo open source Google - gratuito"),
            ("gemma-4-31b",             "Gemma 4 31B",             "Modelo open source Google maior - gratuito"),
        ],
        default="gemini-2.5-flash-lite"
    )


class AI_OT_SendMessage(bpy.types.Operator):
    bl_idname = "ai_assistant.send_message"
    bl_label = "Enviar"

    def execute(self, context):
        props = context.scene.ai_props

        if props.provider == "groq" and not props.groq_api_key:
            self.report({'ERROR'}, "Please add your Groq API Key!")
            return {'CANCELLED'}
        if props.provider == "gemini" and not props.gemini_api_key:
            self.report({'ERROR'}, "Please add your Gemini API Key!")
            return {'CANCELLED'}
        if not props.user_input.strip():
            self.report({'ERROR'}, "Escreve alguma coisa!")
            return {'CANCELLED'}

        props.is_loading = True
        props.response_text = "Thinking..."

        user_message = props.user_input
        provider = props.provider
        groq_key = props.groq_api_key
        gemini_key = props.gemini_api_key
        groq_model = props.groq_model
        gemini_model = props.gemini_model

        system_prompt = "You are an expert Blender 3D assistant. Always respond in the same language the user is writing in. Keep your answers clear, well organized, with blank lines between paragraphs and numbered steps when needed. Be objective but complete. Focus on helping with modeling, animation, rigging, textures and everything related to Blender."

        def call_groq():
            history = json.loads(props.conversation_history)
            messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": user_message}]
            payload = json.dumps({
                "model": groq_model,
                "messages": messages,
                "max_tokens": 8192,
                "temperature": 0.7
            }).encode('utf-8')

            req = urllib.request.Request(
                "https://api.groq.com/openai/v1/chat/completions",
                data=payload,
                headers={
                    "Authorization": f"Bearer {groq_key}",
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0"
                },
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=30) as r:
                result = json.loads(r.read().decode('utf-8'))
                return result['choices'][0]['message']['content']

        def call_gemini():
            history = json.loads(props.conversation_history)
            contents = []
            # primeira mensagem sempre com o system prompt
            contents.append({"role": "user", "parts": [{"text": system_prompt}]})
            contents.append({"role": "model", "parts": [{"text": "Understood! I am ready to help with Blender 3D."}]})
            for msg in history:
                role = "user" if msg["role"] == "user" else "model"
                contents.append({"role": role, "parts": [{"text": msg["content"]}]})
            contents.append({"role": "user", "parts": [{"text": user_message}]})
            payload = json.dumps({
                "contents": contents,
                "generationConfig": {
                    "maxOutputTokens": 8192,
                    "temperature": 0.7
                }
            }).encode('utf-8')

            url = f"https://generativelanguage.googleapis.com/v1beta/models/{gemini_model}:generateContent?key={gemini_key}"
            req = urllib.request.Request(
                url,
                data=payload,
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0"
                },
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=30) as r:
                result = json.loads(r.read().decode('utf-8'))
                return result['candidates'][0]['content']['parts'][0]['text']

        def run():
            try:
                if provider == "groq":
                    answer = call_groq()
                else:
                    answer = call_gemini()

                def update_ui():
                    history = json.loads(props.conversation_history)
                    history.append({"role": "user", "content": user_message})
                    history.append({"role": "assistant", "content": answer})
                    if len(history) > 10:
                        history = history[-10:]
                    props.conversation_history = json.dumps(history)
                    props.response_text = answer
                    props.is_loading = False
                    props.user_input = ""
                    for area in bpy.context.screen.areas:
                        area.tag_redraw()
                    return None
                bpy.app.timers.register(update_ui, first_interval=0.1)

            except urllib.error.HTTPError as e:
                msg = f"Erro HTTP {e.code}: Verifica sua API Key!"
                def update_error():
                    props.response_text = msg
                    props.is_loading = False
                    for area in bpy.context.screen.areas:
                        area.tag_redraw()
                    return None
                bpy.app.timers.register(update_error, first_interval=0.1)

            except Exception as e:
                msg = f"Erro: {str(e)}"
                def update_error():
                    props.response_text = msg
                    props.is_loading = False
                    for area in bpy.context.screen.areas:
                        area.tag_redraw()
                    return None
                bpy.app.timers.register(update_error, first_interval=0.1)

        thread = threading.Thread(target=run)
        thread.daemon = True
        thread.start()
        return {'FINISHED'}


class AI_OT_ClearResponse(bpy.types.Operator):
    bl_idname = "ai_assistant.clear_response"
    bl_label = "Limpar"

    def execute(self, context):
        context.scene.ai_props.response_text = "The response will appear here..."
        return {'FINISHED'}


class AI_OT_ClearHistory(bpy.types.Operator):
    bl_idname = "ai_assistant.clear_history"
    bl_label = "Limpar Histórico"
    bl_description = "Apaga o histórico da conversa e começa do zero"

    def execute(self, context):
        context.scene.ai_props.conversation_history = "[]"
        context.scene.ai_props.response_text = "History cleared! New conversation started."
        return {'FINISHED'}


class AI_PT_Panel(bpy.types.Panel):
    bl_label = "BlendMindAI"
    bl_idname = "AI_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'BlendMindAI'

    def draw(self, context):
        layout = self.layout
        props = context.scene.ai_props
        import json

        box = layout.box()
        box.label(text="Settings:", icon='SETTINGS')
        box.prop(props, "provider", text="API")

        if props.provider == "groq":
            box.prop(props, "groq_api_key", text="API Key")
            box.prop(props, "groq_model", text="Model")
        else:
            box.prop(props, "gemini_api_key", text="API Key")
            box.prop(props, "gemini_model", text="Model")

        layout.separator()

        box = layout.box()
        box.label(text="Your question:", icon='QUESTION')
        box.prop(props, "user_input", text="")

        row = box.row()
        if props.is_loading:
            row.label(text="Thinking...", icon='SORTTIME')
        else:
            row.operator("ai_assistant.send_message", text="Send", icon='PLAY')
        
        # Mostra quantas mensagens tem no histórico
        history = json.loads(props.conversation_history)
        if len(history) > 0:
            row2 = layout.row()
            row2.operator("ai_assistant.clear_history", text=f"Clear history ({len(history)//2} msgs)", icon='TRASH')

        layout.separator()

        box = layout.box()
        row = box.row()
        row.label(text="Response:", icon='INFO')
        row.operator("ai_assistant.clear_response", text="", icon='X')

        import re
        response = props.response_text
        # Remove markdown
        response = re.sub(r"[*]{2}(.+?)[*]{2}", r"\1", response)
        response = re.sub(r"[*](.+?)[*]", r"\1", response)
        response = re.sub(r"[#]{1,6} *", "", response)
        response = re.sub(r"`(.+?)`", r"\1", response)


        wrap_width = 45
        paragraphs = response.split("\n")
        for paragraph in paragraphs:
            if paragraph.strip() == "":
                box.separator()
                continue
            words = paragraph.split()
            line = ""
            for word in words:
                if len(line) + len(word) + 1 <= wrap_width:
                    line += (" " if line else "") + word
                else:
                    if line:
                        box.label(text=line)
                    line = word
            if line:
                box.label(text=line)


classes = [
    AIAddonProperties,
    AI_OT_SendMessage,
    AI_OT_ClearResponse,
    AI_OT_ClearHistory,
    AI_PT_Panel,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.ai_props = bpy.props.PointerProperty(type=AIAddonProperties)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.ai_props

if __name__ == "__main__":
    register()
