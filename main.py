from fasthtml.common import (Button, Div, Input, Link, Script, Span, fast_app,
                             serve, HTMLResponse)

app, rt = fast_app()

API_BASE_URL = "http://localhost:8000/api"


@app.get('/')
def homepage():
    return Div(
        # Importando Tailwind CSS
        Link(rel="stylesheet",
             href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css"),

        # Estrutura principal
        Div(
            # Header
            Div(
                "Chat Telegram",
                _class="bg-blue-500 text-white py-4 px-6 text-xl font-bold shadow-md"
            ),

            # Container de mensagens
            Div(
                id="chat-messages",
                _class="flex-1 p-4 overflow-y-auto"
            ),

            # Container de input
            Div(
                Input(
                    id="message-input",
                    placeholder="Digite uma mensagem...",
                    _class="w-full px-4 py-2 rounded-full border-2 border-gray-300 focus:outline-none focus:border-blue-500"
                ),
                Button(
                    Span("➤", _class="transform rotate-90 inline-block"),
                    id="send-button",
                    _class="ml-2 bg-blue-500 text-white rounded-full w-10 h-10 flex items-center justify-center hover:bg-blue-600 focus:outline-none"
                ),
                _class="bg-gray-100 p-4 flex items-center"
            ),
            _class="flex flex-col h-screen bg-gray-100"
        ),

        Script(f"""
            const chatMessages = document.getElementById('chat-messages');
            const messageInput = document.getElementById('message-input');
            const sendButton = document.getElementById('send-button');
            const apiBaseUrl = "{API_BASE_URL}";

            function addMessage(content, isUser = true) {{
                const messageDiv = document.createElement('div');
                messageDiv.className = `max-w-[70%] rounded-lg p-3 mb-2 ${{isUser ? 'ml-auto bg-green-200 text-right' : 'mr-auto bg-white'}}`;
                messageDiv.textContent = content;
                chatMessages.appendChild(messageDiv);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }}

            async function sendMessage() {{
                const message = messageInput.value.trim();
                if (message) {{
                    addMessage(message, true);
                    messageInput.value = '';

                    try {{
                        const response = await fetch(`${{apiBaseUrl}}/messages/`, {{
                            method: 'POST',
                            headers: {{
                                'Content-Type': 'application/json',
                                // Adicione cabeçalhos de autenticação se necessário
                            }},
                            body: JSON.stringify({{ content: message }})
                        }});

                        if (response.ok) {{
                            const data = await response.json();
                            console.log('Message sent:', data);
                        }} else {{
                            console.error('Failed to send message');
                        }}
                    }} catch (error) {{
                        console.error('Error:', error);
                    }}
                }}
            }}

            async function loadMessages() {{
                try {{
                    const response = await fetch(`${{apiBaseUrl}}/messages/`);
                    if (response.ok) {{
                        const messages = await response.json();
                        messages.forEach(msg => {{
                            addMessage(msg.content, msg.sender === 'Your Username');  // Ajuste conforme necessário
                        }});
                    }} else {{
                        console.error('Failed to load messages');
                    }}
                }} catch (error) {{
                    console.error('Error:', error);
                }}
            }}

            sendButton.addEventListener('click', sendMessage);
            messageInput.addEventListener('keypress', (e) => {{
                if (e.key === 'Enter') {{
                    sendMessage();
                }}
            }});

            // Carregar mensagens ao iniciar
            loadMessages();
        """)
    )

@app.get('/login')
async def login_page():
  return Div(
      # Login form with username and password fields
      Input(type="text", name="username", placeholder="Username"),
      Input(type="password", name="password", placeholder="Password"),
      Button("Login"),
  )

@app.post('/login')
async def login(request):
  form_data = await request.form()
  username = form_data.get('username')
  password = form_data.get('password')

  # Replace with your actual authentication logic
  if username == "admin" and password == "secret":
      # Successful login, create a session (placeholder)
      session_token = "your_generated_session_token"
      # Redirect to homepage with session token (optional)
      return HTMLResponse(headers={"Set-Cookie": f"session_token={session_token}"})
  else:
      # Login failed
      return Div("Invalid username or password")


serve()
