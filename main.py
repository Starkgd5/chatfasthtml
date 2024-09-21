from fasthtml.common import *

app, rt = fast_app()


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

        Script("""
            const chatMessages = document.getElementById('chat-messages');
            const messageInput = document.getElementById('message-input');
            const sendButton = document.getElementById('send-button');

            function addMessage(content, isUser = true) {
                const messageDiv = document.createElement('div');
                messageDiv.className = `max-w-[70%] rounded-lg p-3 mb-2 ${isUser ? 'ml-auto bg-green-200 text-right' : 'mr-auto bg-white'}`;
                messageDiv.textContent = content;
                chatMessages.appendChild(messageDiv);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }

            function sendMessage() {
                const message = messageInput.value.trim();
                if (message) {
                    addMessage(message, true);
                    messageInput.value = '';
                    
                    // Simular resposta do assistente
                    setTimeout(() => {
                        addMessage('Obrigado pela sua mensagem! Como posso ajudar?', false);
                    }, 1000);
                }
            }

            sendButton.addEventListener('click', sendMessage);
            messageInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });

            // Adicionar mensagem inicial
            addMessage('Bem-vindo ao chat! Este é um sistema de mensagens estilo Telegram usando Tailwind CSS.', false);
        """)
    )


serve()
