/**
 * Admin Panel JavaScript





























SELECT 'Users table and chat_logs updates completed successfully!' AS Status;-- Display success messageCREATE INDEX IF NOT EXISTS idx_user_id ON chat_logs(user_id);-- Add index for user_idFOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL;ADD CONSTRAINT fk_chat_logs_user ALTER TABLE chat_logs -- Add foreign key constraintALTER TABLE chat_logs ADD COLUMN IF NOT EXISTS user_id INT NULL AFTER id;-- Add user_id column to chat_logs if it doesn't exist) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;    is_active BOOLEAN DEFAULT TRUE    last_login TIMESTAMP NULL,    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,    email VARCHAR(100),    full_name VARCHAR(100),    password_hash VARCHAR(255) NOT NULL,    username VARCHAR(50) NOT NULL UNIQUE,    id INT AUTO_INCREMENT PRIMARY KEY,CREATE TABLE IF NOT EXISTS users (-- Create users table if it doesn't exist-- ============================================-- Run this script to add user authentication support * Handles intent management, response management, and model retraining
 */

let intents = [];
let currentIntentId = null;

// Show section
function showSection(section) {
    // Hide all sections
    document.getElementById('intentsSection').classList.add('hidden');
    document.getElementById('responsesSection').classList.add('hidden');
    document.getElementById('logsSection').classList.add('hidden');
    
    // Show selected section
    if (section === 'intents') {
        document.getElementById('intentsSection').classList.remove('hidden');
        loadIntents();
    } else if (section === 'responses') {
        document.getElementById('responsesSection').classList.remove('hidden');
        loadIntents(); // Load intents for dropdown
    } else if (section === 'logs') {
        document.getElementById('logsSection').classList.remove('hidden');
        loadChatLogs();
    }
}

// ==================== INTENTS ====================

async function loadIntents() {
    try {
        const response = await fetch('/api/intents');
        intents = await response.json();
        
        // Update intents list
        const intentsList = document.getElementById('intentsList');
        if (intentsList) {
            intentsList.innerHTML = '';
            
            intents.forEach(intent => {
                const intentCard = document.createElement('div');
                intentCard.className = 'bg-gray-50 p-4 rounded-lg border border-gray-200 flex items-center justify-between';
                intentCard.innerHTML = `
                    <div>
                        <h3 class="font-semibold text-gray-800">${intent.intent_name}</h3>
                        <p class="text-sm text-gray-600">${intent.description || 'No description'}</p>
                    </div>
                    <div class="flex gap-2">
                        <button onclick="viewResponses(${intent.id})" class="text-blue-500 hover:text-blue-700">
                            <i class="fas fa-eye"></i>
                        </button>
                        <button onclick="deleteIntent(${intent.id})" class="text-red-500 hover:text-red-700">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                `;
                intentsList.appendChild(intentCard);
            });
        }
        
        // Update dropdowns
        updateIntentDropdowns();
        
    } catch (error) {
        console.error('Error loading intents:', error);
        showNotification('Error loading intents', 'error');
    }
}

function updateIntentDropdowns() {
    const intentSelect = document.getElementById('intentSelect');
    const responseIntentSelect = document.getElementById('responseIntentSelect');
    
    if (intentSelect) {
        intentSelect.innerHTML = '<option value="">-- Select an Intent --</option>';
        intents.forEach(intent => {
            const option = document.createElement('option');
            option.value = intent.id;
            option.textContent = intent.intent_name;
            intentSelect.appendChild(option);
        });
    }
    
    if (responseIntentSelect) {
        responseIntentSelect.innerHTML = '<option value="">-- Select Intent --</option>';
        intents.forEach(intent => {
            const option = document.createElement('option');
            option.value = intent.id;
            option.textContent = intent.intent_name;
            responseIntentSelect.appendChild(option);
        });
    }
}

function showAddIntentModal() {
    document.getElementById('addIntentModal').classList.remove('hidden');
    document.getElementById('addIntentModal').classList.add('flex');
}

async function addIntent() {
    const name = document.getElementById('newIntentName').value.trim();
    const description = document.getElementById('newIntentDesc').value.trim();
    
    if (!name) {
        alert('Please enter an intent name');
        return;
    }
    
    try {
        const response = await fetch('/api/intents', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                intent_name: name,
                description: description
            })
        });
        
        if (response.ok) {
            showNotification('Intent added successfully', 'success');
            closeModal('addIntentModal');
            loadIntents();
            
            // Clear form
            document.getElementById('newIntentName').value = '';
            document.getElementById('newIntentDesc').value = '';
        } else {
            showNotification('Error adding intent', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Error adding intent', 'error');
    }
}

async function deleteIntent(intentId) {
    if (!confirm('Are you sure you want to delete this intent and all its responses?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/intents/${intentId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            showNotification('Intent deleted successfully', 'success');
            loadIntents();
        } else {
            showNotification('Error deleting intent', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Error deleting intent', 'error');
    }
}

function viewResponses(intentId) {
    currentIntentId = intentId;
    document.getElementById('intentSelect').value = intentId;
    showSection('responses');
    loadResponses();
}

// ==================== RESPONSES ====================

async function loadResponses() {
    const intentId = document.getElementById('intentSelect').value;
    
    if (!intentId) {
        document.getElementById('responsesList').innerHTML = '<p class="text-gray-500">Please select an intent</p>';
        return;
    }
    
    try {
        const response = await fetch(`/api/responses/${intentId}`);
        const responses = await response.json();
        
        const responsesList = document.getElementById('responsesList');
        responsesList.innerHTML = '';
        
        if (responses.length === 0) {
            responsesList.innerHTML = '<p class="text-gray-500">No responses found for this intent</p>';
            return;
        }
        
        responses.forEach(resp => {
            const responseCard = document.createElement('div');
            responseCard.className = 'bg-gray-50 p-4 rounded-lg border border-gray-200';
            responseCard.innerHTML = `
                <div class="mb-2">
                    <span class="text-xs font-semibold text-blue-600 bg-blue-100 px-2 py-1 rounded">PATTERN</span>
                    <p class="text-sm text-gray-700 mt-1">${resp.pattern}</p>
                </div>
                <div class="mb-2">
                    <span class="text-xs font-semibold text-green-600 bg-green-100 px-2 py-1 rounded">RESPONSE</span>
                    <p class="text-sm text-gray-700 mt-1">${resp.response}</p>
                </div>
                <div class="flex justify-end">
                    <button onclick="deleteResponse(${resp.id})" class="text-red-500 hover:text-red-700 text-sm">
                        <i class="fas fa-trash mr-1"></i>Delete
                    </button>
                </div>
            `;
            responsesList.appendChild(responseCard);
        });
        
    } catch (error) {
        console.error('Error loading responses:', error);
        showNotification('Error loading responses', 'error');
    }
}

function showAddResponseModal() {
    document.getElementById('addResponseModal').classList.remove('hidden');
    document.getElementById('addResponseModal').classList.add('flex');
}

async function addResponse() {
    const intentId = document.getElementById('responseIntentSelect').value;
    const pattern = document.getElementById('newPattern').value.trim();
    const response = document.getElementById('newResponse').value.trim();
    
    if (!intentId || !pattern || !response) {
        alert('Please fill all fields');
        return;
    }
    
    try {
        const res = await fetch('/api/responses', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                intent_id: parseInt(intentId),
                pattern: pattern,
                response: response,
                priority: 0
            })
        });
        
        if (res.ok) {
            showNotification('Response added successfully', 'success');
            closeModal('addResponseModal');
            
            // Clear form
            document.getElementById('newPattern').value = '';
            document.getElementById('newResponse').value = '';
            
            // Reload if viewing same intent
            if (document.getElementById('intentSelect').value == intentId) {
                loadResponses();
            }
        } else {
            showNotification('Error adding response', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Error adding response', 'error');
    }
}

async function deleteResponse(responseId) {
    if (!confirm('Are you sure you want to delete this response?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/responses/${responseId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            showNotification('Response deleted successfully', 'success');
            loadResponses();
        } else {
            showNotification('Error deleting response', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Error deleting response', 'error');
    }
}

// ==================== MODEL RETRAINING ====================

async function retrainModel() {
    if (!confirm('This will retrain the AI model with updated data. This may take a few minutes. Continue?')) {
        return;
    }
    
    showNotification('Retraining model... Please wait', 'info');
    
    try {
        const response = await fetch('/api/retrain', {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showNotification('Model retrained successfully! Changes are now active.', 'success');
            // Show model status after retraining
            setTimeout(() => checkModelStatus(), 1000);
        } else {
            showNotification('Error: ' + (data.error || 'Retraining failed'), 'error');
            console.error('Retrain error details:', data);
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Error retraining model', 'error');
    }
}

async function checkModelStatus() {
    try {
        const response = await fetch('/api/debug/model-status');
        const status = await response.json();
        
        console.log('=== MODEL STATUS ===');
        console.log('Model Loaded:', status.model_loaded);
        console.log('NLP Processor:', status.nlp_processor_available);
        console.log('Intents in Memory:', status.intents_loaded);
        console.log('Intents in File:', status.intents_json_file_count);
        console.log('Intent Tags:', status.intents_list);
        console.log('Intent Labels:', status.intent_labels);
        console.log('==================');
        
        // Show a summary notification
        if (status.model_loaded && status.intents_loaded > 0) {
            showNotification(`✓ Model is healthy: ${status.intents_loaded} intents loaded`, 'success');
        } else {
            showNotification('⚠ Model may have issues - check console', 'error');
        }
        
        return status;
    } catch (error) {
        console.error('Error checking model status:', error);
        showNotification('Error checking model status', 'error');
    }
}

// ==================== CHAT LOGS ====================

async function loadChatLogs() {
    try {
        const response = await fetch('/api/chat-logs?limit=50');
        const logs = await response.json();
        
        const logsTable = document.getElementById('logsTable');
        logsTable.innerHTML = '';
        
        if (logs.length === 0) {
            logsTable.innerHTML = '<tr><td colspan="6" class="text-center py-4 text-gray-500">No logs found</td></tr>';
            return;
        }
        
        logs.forEach(log => {
            const row = document.createElement('tr');
            row.className = 'border-b hover:bg-gray-50';
            
            const time = new Date(log.created_at).toLocaleString();
            const confidence = (log.confidence_score * 100).toFixed(1) + '%';
            const confidenceColor = log.confidence_score > 0.6 ? 'text-green-600' : 'text-red-600';
            
            // Display user information
            const userDisplay = log.username 
                ? `<span class="text-blue-600 font-medium">${log.username}</span>${log.full_name ? `<br><span class="text-xs text-gray-500">${log.full_name}</span>` : ''}`
                : '<span class="text-gray-400 italic">Guest</span>';
            
            row.innerHTML = `
                <td class="px-4 py-2 text-gray-600">${time}</td>
                <td class="px-4 py-2">${userDisplay}</td>
                <td class="px-4 py-2">${truncate(log.user_message, 50)}</td>
                <td class="px-4 py-2">${truncate(log.bot_response, 50)}</td>
                <td class="px-4 py-2">
                    <span class="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded">${log.predicted_intent || 'unknown'}</span>
                </td>
                <td class="px-4 py-2 ${confidenceColor} font-semibold">${confidence}</td>
            `;
            
            logsTable.appendChild(row);
        });
        
    } catch (error) {
        console.error('Error loading logs:', error);
        showNotification('Error loading chat logs', 'error');
    }
}

// ==================== UTILITY FUNCTIONS ====================

function closeModal(modalId) {
    document.getElementById(modalId).classList.add('hidden');
    document.getElementById(modalId).classList.remove('flex');
}

function showNotification(message, type = 'info') {
    const colors = {
        success: 'bg-green-500',
        error: 'bg-red-500',
        info: 'bg-blue-500'
    };
    
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 ${colors[type]} text-white px-6 py-3 rounded-lg shadow-lg z-50`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

function truncate(text, length) {
    return text.length > length ? text.substring(0, length) + '...' : text;
}

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    showSection('intents');
});
