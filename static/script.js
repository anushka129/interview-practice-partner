const chatEl = document.getElementById("chat");
const messageInput = document.getElementById("message");
const sendBtn = document.getElementById("send");
const roleSelect = document.getElementById("role");
const feedbackBtn = document.getElementById("feedback");
const micBtn = document.getElementById("mic");
const restartBtn = document.getElementById("restart");

let currentSessionId = null;
let isWaiting = false;

// Add message to chat
function appendMessage(who, text) {
    const div = document.createElement("div");
    div.className = `message ${who}`;
    
    const bubble = document.createElement("div");
    bubble.className = "bubble";
    
    // Simple formatting for feedback
    if (text.includes("**") || text.includes("-")) {
        const formattedText = text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\n/g, '<br>');
        bubble.innerHTML = formattedText;
    } else {
        bubble.textContent = text;
    }
    
    div.appendChild(bubble);
    chatEl.appendChild(div);
    chatEl.scrollTop = chatEl.scrollHeight;
}

// Show thinking indicator
function showThinking() {
    const div = document.createElement("div");
    div.className = "message bot";
    div.id = "thinking-indicator";
    div.innerHTML = '<div class="bubble">💭 Thinking...</div>';
    chatEl.appendChild(div);
    chatEl.scrollTop = chatEl.scrollHeight;
}

// Remove thinking indicator
function removeThinking() {
    const indicator = document.getElementById("thinking-indicator");
    if (indicator) {
        indicator.remove();
    }
}

// Send message to server
async function sendMessage(mode = "mock") {
    if (isWaiting) return;
    
    const text = messageInput.value.trim();
    
    // Add user message if provided
    if (text && mode === "mock") {
        appendMessage("user", text);
        messageInput.value = "";
    }
    
    isWaiting = true;
    sendBtn.disabled = true;
    feedbackBtn.disabled = true;
    
    showThinking();
    
    try {
        const response = await fetch("/api/interview", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                message: text,
                role: roleSelect.value,
                mode: mode,
                session_id: currentSessionId
            })
        });
        
        const data = await response.json();
        removeThinking();
        
        if (data.reply) {
            appendMessage("bot", data.reply);
            
            // Update session ID if provided
            if (data.session_id) {
                currentSessionId = data.session_id;
            }
            
            // Show source indicator for demo purposes
            if (data.source) {
                const sourceDiv = document.createElement("div");
                sourceDiv.style.textAlign = "center";
                sourceDiv.style.color = "#666";
                sourceDiv.style.fontSize = "0.8em";
                sourceDiv.style.margin = "5px 0";
                sourceDiv.textContent = `✨ Response generated offline`;
                chatEl.appendChild(sourceDiv);
                chatEl.scrollTop = chatEl.scrollHeight;
            }
        } else {
            appendMessage("bot", "Sorry, I didn't get a response. Please try again.");
        }
        
    } catch (error) {
        removeThinking();
        appendMessage("bot", "Network error. Please check your connection.");
        console.error("Error:", error);
    } finally {
        isWaiting = false;
        sendBtn.disabled = false;
        feedbackBtn.disabled = false;
    }
}

// Initialize speech recognition (optional)
function initSpeechRecognition() {
    if ('webkitSpeechRecognition' in window) {
        const recognition = new webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';
        
        recognition.onstart = function() {
            micBtn.classList.add('listening');
            appendMessage("bot", "🎤 Listening...");
        };
        
        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            messageInput.value = transcript;
            micBtn.classList.remove('listening');
        };
        
        recognition.onerror = function() {
            micBtn.classList.remove('listening');
        };
        
        recognition.onend = function() {
            micBtn.classList.remove('listening');
        };
        
        micBtn.onclick = function() {
            recognition.start();
        };
    } else {
        micBtn.disabled = true;
        micBtn.title = "Speech recognition not supported";
    }
}

// Event listeners
sendBtn.addEventListener('click', () => sendMessage("mock"));
feedbackBtn.addEventListener('click', () => sendMessage("feedback"));

restartBtn.addEventListener('click', () => {
    chatEl.innerHTML = '';
    currentSessionId = null;
    appendMessage("bot", "🔄 Interview restarted! Choose your role and type 'start' to begin.");
});

roleSelect.addEventListener('change', () => {
    appendMessage("bot", `Role changed to: ${roleSelect.value}. Type 'start' to begin.`);
});

// Keyboard support
messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !isWaiting) {
        sendMessage("mock");
    }
});

// Initialize the app
initSpeechRecognition();
appendMessage("bot", "👋 Welcome to Interview Practice Partner! \n\n💡 How to use:\n• Choose your desired role\n• Type 'start' to begin interview\n• Answer each question naturally\n• Click 'Get Feedback' when done\n• Use microphone for voice input\n\n🚀 This works completely offline!");