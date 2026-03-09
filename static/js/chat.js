/**
 * Chat Interface JavaScript
 * Handles user interactions, message sending, authentication, and voice support
 */

const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');
const voiceBtn = document.getElementById('voiceBtn');

let isLoggedIn = false;
let currentUser = null;

// Check login status on page load
window.addEventListener('DOMContentLoaded', checkLoginStatus);

async function checkLoginStatus() {
    try {
        const response = await fetch('/api/check-login');
        const data = await response.json();
        
        if (data.logged_in) {
            isLoggedIn = true;
            currentUser = data.user;
            updateUIForLoggedIn(data.user.username);
        } else {
            updateUIForLoggedOut();
        }
    } catch (error) {
        console.error('Login check error:', error);
        updateUIForLoggedOut();
    }
}

function updateUIForLoggedIn(username) {
    document.getElementById('loginBtn').classList.add('hidden');
    document.getElementById('loggedInSection').classList.remove('hidden');
    document.getElementById('loggedInSection').classList.add('flex');
    document.getElementById('userName').textContent = username;
    messageInput.disabled = false;
    sendBtn.disabled = false;
    messageInput.placeholder = 'Type your message here...';
}

function updateUIForLoggedOut() {
    document.getElementById('loginBtn').classList.remove('hidden');
    document.getElementById('loggedInSection').classList.add('hidden');
    document.getElementById('loggedInSection').classList.remove('flex');
    messageInput.disabled = false;
    sendBtn.disabled = false;
    messageInput.placeholder = 'Type your message here...';
}

// Login Modal Functions
function openLoginModal() {
    document.getElementById('loginModal').classList.remove('hidden');
    document.getElementById('registerModal').classList.add('hidden');
}

function showLoginModal() {
    openLoginModal();
}

function closeLoginModal() {
    document.getElementById('loginModal').classList.add('hidden');
    document.getElementById('loginForm').reset();
    document.getElementById('loginError').classList.add('hidden');
}

function showRegisterModal() {
    document.getElementById('registerModal').classList.remove('hidden');
    document.getElementById('loginModal').classList.add('hidden');
}

function closeRegisterModal() {
    document.getElementById('registerModal').classList.add('hidden');
    document.getElementById('registerForm').reset();
    document.getElementById('registerError').classList.add('hidden');
    document.getElementById('registerSuccess').classList.add('hidden');
}

// Handle Login
async function handleLogin(event) {
    event.preventDefault();
    
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;
    const errorDiv = document.getElementById('loginError');
    
    try {
        const response = await fetch('/api/user-login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Check if user is admin
            if (data.isAdmin) {
                // Redirect to admin panel
                window.location.href = '/admin';
                return;
            }
            
            // Regular user login
            isLoggedIn = true;
            currentUser = data.user;
            updateUIForLoggedIn(username);
            closeLoginModal();
            addMessage('Welcome ' + username + '! How can I help you today?', false);
        } else {
            errorDiv.textContent = data.error || 'Login failed';
            errorDiv.classList.remove('hidden');
        }
    } catch (error) {
        errorDiv.textContent = 'Login error: ' + error.message;
        errorDiv.classList.remove('hidden');
    }
}

// Handle Register
async function handleRegister(event) {
    event.preventDefault();
    
    const fullName = document.getElementById('regFullName').value;
    const username = document.getElementById('regUsername').value;
    const email = document.getElementById('regEmail').value;
    const password = document.getElementById('regPassword').value;
    const errorDiv = document.getElementById('registerError');
    const successDiv = document.getElementById('registerSuccess');
    
    errorDiv.classList.add('hidden');
    successDiv.classList.add('hidden');
    
    try {
        const response = await fetch('/api/user-register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ full_name: fullName, username, email, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            successDiv.textContent = 'Registration successful! Please login.';
            successDiv.classList.remove('hidden');
            document.getElementById('registerForm').reset();
            setTimeout(() => showLoginModal(), 2000);
        } else {
            errorDiv.textContent = data.error || 'Registration failed';
            errorDiv.classList.remove('hidden');
        }
    } catch (error) {
        errorDiv.textContent = 'Registration error: ' + error.message;
        errorDiv.classList.remove('hidden');
    }
}

// Handle Logout
async function logout() {
    try {
        await fetch('/api/user-logout', { method: 'POST' });
        isLoggedIn = false;
        currentUser = null;
        updateUIForLoggedOut();
        // Keep the existing messages, don't clear
    } catch (error) {
        console.error('Logout error:', error);
    }
}

async function handleLogout() {
    logout();
}

// Add message to chat
function addMessage(text, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message flex gap-4 mb-6';
    
    if (isUser) {
        messageDiv.classList.add('justify-end');
        messageDiv.innerHTML = `
            <div class="user-message text-white rounded-3xl rounded-tr-md px-6 py-4" style="max-width: calc(100% - 70px);">
                <p class="font-medium break-words">${escapeHtml(text)}</p>
            </div>
            <div class="w-11 h-11 rounded-full bg-gradient-to-r from-gray-400 to-gray-600 flex items-center justify-center flex-shrink-0 shadow-lg">
                <i class="fas fa-user text-white text-lg"></i>
            </div>
        `;
    } else {
        messageDiv.innerHTML = `
            <div class="w-11 h-11 rounded-full bg-gradient-to-r from-cyan-500 to-blue-600 flex items-center justify-center flex-shrink-0 shadow-lg">
                <i class="fas fa-robot text-white text-lg"></i>
            </div>
            <div class="bot-message rounded-3xl rounded-tl-md px-6 py-4" style="max-width: calc(100% - 70px);">
                <p class="text-gray-800 break-words">${escapeHtml(text)}</p>
            </div>
        `;
    }
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

// Add typing indicator
function showTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message flex gap-4 mb-6';
    typingDiv.id = 'typingIndicator';
    typingDiv.innerHTML = `
        <div class="w-11 h-11 rounded-full bg-gradient-to-r from-purple-500 to-indigo-600 flex items-center justify-center flex-shrink-0 shadow-lg">
            <i class="fas fa-robot text-white text-lg"></i>
        </div>
        <div class="typing-indicator">
            <span></span>
            <span></span>
            <span></span>
        </div>
    `;
    
    chatMessages.appendChild(typingDiv);
    scrollToBottom();
}

// Remove typing indicator
function hideTypingIndicator() {
    const typingIndicator = document.getElementById('typingIndicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

// Send message
async function sendMessage() {
    const message = messageInput.value.trim();
    
    if (!message) {
        return;
    }
    
    if (!isLoggedIn) {
        addMessage('Please login to send messages.', false);
        showLoginModal();
        return;
    }
    
    // Disable input
    messageInput.disabled = true;
    sendBtn.disabled = true;
    
    // Add user message
    addMessage(message, true);
    
    // Clear input
    messageInput.value = '';
    
    // Show typing indicator
    showTypingIndicator();
    
    try {
        // Send to backend
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message })
        });
        
        const data = await response.json();
        
        // Hide typing indicator
        hideTypingIndicator();
        
        // Add bot response
        if (data.response) {
            addMessage(data.response, false);
            
            // Optional: Speak response (uncomment if you want TTS)
            // speakText(data.response);
        } else if (data.error) {
            addMessage('Sorry, I encountered an error. Please try again.', false);
        }
        
    } catch (error) {
        console.error('Error:', error);
        hideTypingIndicator();
        addMessage('Sorry, I couldn\'t connect to the server. Please check your connection.', false);
    } finally {
        // Re-enable input
        messageInput.disabled = false;
        sendBtn.disabled = false;
        messageInput.focus();
    }
}

// Handle Enter key
function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

// Send quick message
function sendQuickMessage(message) {
    messageInput.value = message;
    sendMessage();
}

// Clear chat
function clearChat() {
    if (confirm('Are you sure you want to clear the chat history?')) {
        const welcomeMessage = chatMessages.querySelector('.message');
        chatMessages.innerHTML = '';
        if (welcomeMessage) {
            chatMessages.appendChild(welcomeMessage.cloneNode(true));
        }
    }
}

// Voice input
async function startVoiceInput() {
    // Check browser support
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        alert('Voice recognition is not supported in your browser. Please use Chrome or Edge.');
        return;
    }
    
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    
    recognition.lang = 'en-US';
    recognition.continuous = false;
    recognition.interimResults = false;
    
    // Change button state
    voiceBtn.innerHTML = '<i class="fas fa-stop"></i>';
    voiceBtn.classList.add('bg-red-500');
    voiceBtn.disabled = true;
    
    recognition.onstart = function() {
        console.log('Voice recognition started');
    };
    
    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        messageInput.value = transcript;
        console.log('Recognized:', transcript);
    };
    
    recognition.onerror = function(event) {
        console.error('Voice recognition error:', event.error);
        alert('Voice recognition error: ' + event.error);
    };
    
    recognition.onend = function() {
        voiceBtn.innerHTML = '<i class="fas fa-microphone"></i>';
        voiceBtn.classList.remove('bg-red-500');
        voiceBtn.disabled = false;
    };
    
    recognition.start();
}

// Text-to-Speech (optional)
function speakText(text) {
    if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 1.0;
        utterance.pitch = 1.0;
        utterance.volume = 1.0;
        speechSynthesis.speak(utterance);
    }
}

// Scroll to bottom
function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    messageInput.focus();
    
    // Auto-scroll on new messages
    const observer = new MutationObserver(scrollToBottom);
    observer.observe(chatMessages, { childList: true });
});
