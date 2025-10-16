// Global state
let currentTopic = null;
let currentQuizzes = [];
let currentQuizIndex = 0;
let userAnswers = [];
let userName = '';

// DOM elements
const welcomeSection = document.getElementById('welcome-section');
const topicsSection = document.getElementById('topics-section');
const quizSection = document.getElementById('quiz-section');
const resultsSection = document.getElementById('results-section');
const nameModal = document.getElementById('name-modal');

// Initialize the app
document.addEventListener('DOMContentLoaded', function() {
    loadTopics();
    setupEventListeners();
    loadTopicsForUpload();
});

// Event listeners
function setupEventListeners() {
    // Initialize sample data
    document.getElementById('init-data-btn').addEventListener('click', initializeSampleData);
    
    // Navigation
    document.getElementById('back-to-topics').addEventListener('click', showTopicsSection);
    document.getElementById('back-to-topics-final').addEventListener('click', showTopicsSection);
    document.getElementById('try-again-btn').addEventListener('click', restartCurrentQuiz);
    
    // Modal
    document.getElementById('start-quiz-btn').addEventListener('click', startQuizWithName);
    document.getElementById('user-name-input').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            startQuizWithName();
        }
    });
    
    // Excel upload functionality
    document.getElementById('download-template-btn').addEventListener('click', downloadTemplate);
    document.getElementById('upload-excel-btn').addEventListener('click', uploadExcelFile);
    document.getElementById('excel-file').addEventListener('change', handleFileSelection);
    document.getElementById('topic-select').addEventListener('change', handleTopicSelection);
}

// API functions
async function apiCall(endpoint, options = {}) {
    try {
        const response = await fetch(endpoint, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API call failed:', error);
        showMessage('An error occurred. Please try again.', 'error');
        throw error;
    }
}

// Initialize sample data
async function initializeSampleData() {
    const btn = document.getElementById('init-data-btn');
    const originalText = btn.textContent;
    btn.textContent = 'Initializing...';
    btn.disabled = true;
    
    try {
        const result = await apiCall('/api/init-data/', { method: 'POST' });
        showMessage(result.message, 'success');
        await loadTopics();
    } catch (error) {
        showMessage('Failed to initialize sample data', 'error');
    } finally {
        btn.textContent = originalText;
        btn.disabled = false;
    }
}

// Load topics from API
async function loadTopics() {
    try {
        const topics = await apiCall('/api/topics/');
        displayTopics(topics);
    } catch (error) {
        console.error('Failed to load topics:', error);
    }
}

// Display topics
function displayTopics(topics) {
    const container = document.getElementById('topics-container');
    
    if (topics.length === 0) {
        container.innerHTML = '<p class="loading">No topics available. Click "Initialize Sample Data" to get started!</p>';
        return;
    }
    
    container.innerHTML = topics.map(topic => `
        <button class="topic-card" onclick="selectTopic(${topic.id}, '${topic.title}')">
            <h3>${topic.title}</h3>
            <p>${topic.description || 'Practice your skills with this topic'}</p>
        </button>
    `).join('');
}

// Select a topic and show name modal
function selectTopic(topicId, topicTitle) {
    currentTopic = { id: topicId, title: topicTitle };
    showNameModal();
}

// Show name input modal
function showNameModal() {
    nameModal.classList.remove('hidden');
    document.getElementById('user-name-input').focus();
}

// Start quiz with user name
async function startQuizWithName() {
    const nameInput = document.getElementById('user-name-input');
    userName = nameInput.value.trim();
    
    if (!userName) {
        nameInput.focus();
        return;
    }
    
    nameModal.classList.add('hidden');
    nameInput.value = '';
    
    await loadQuizzes(currentTopic.id);
}

// Load quizzes for a topic
async function loadQuizzes(topicId) {
    try {
        currentQuizzes = await apiCall(`/api/quizzes/topic/${topicId}`);
        
        if (currentQuizzes.length === 0) {
            showMessage('No quizzes available for this topic yet.', 'error');
            return;
        }
        
        currentQuizIndex = 0;
        userAnswers = [];
        showQuizSection();
        displayCurrentQuiz();
    } catch (error) {
        showMessage('Failed to load quizzes', 'error');
    }
}

// Show quiz section
function showQuizSection() {
    hideAllSections();
    quizSection.classList.remove('hidden');
    document.getElementById('quiz-topic-title').textContent = currentTopic.title;
}

// Display current quiz
function displayCurrentQuiz() {
    const quiz = currentQuizzes[currentQuizIndex];
    const container = document.getElementById('quiz-container');
    
    container.innerHTML = `
        <div class="quiz-progress">
            Question ${currentQuizIndex + 1} of ${currentQuizzes.length}
        </div>
        
        <div class="quiz-card">
            <div class="quiz-question">${quiz.question}</div>
            <div class="quiz-choices">
                ${quiz.choices.map((choice, index) => `
                    <button class="choice-btn" onclick="selectAnswer('${choice}', ${index})">
                        ${choice}
                    </button>
                `).join('')}
            </div>
        </div>
        
        <div style="text-align: center; margin-top: 2rem;">
            <button id="next-btn" class="btn btn-primary" onclick="nextQuestion()" disabled>
                ${currentQuizIndex === currentQuizzes.length - 1 ? 'Finish Quiz' : 'Next Question'}
            </button>
        </div>
    `;
}

// Select an answer
function selectAnswer(answer, index) {
    // Remove previous selections
    document.querySelectorAll('.choice-btn').forEach(btn => {
        btn.classList.remove('selected');
    });
    
    // Mark current selection
    document.querySelectorAll('.choice-btn')[index].classList.add('selected');
    
    // Store the answer
    userAnswers[currentQuizIndex] = answer;
    
    // Enable next button
    document.getElementById('next-btn').disabled = false;
}

// Move to next question or finish quiz
async function nextQuestion() {
    const currentQuiz = currentQuizzes[currentQuizIndex];
    const userAnswer = userAnswers[currentQuizIndex];
    
    // Submit the answer
    try {
        await apiCall('/api/submissions/', {
            method: 'POST',
            body: JSON.stringify({
                user_name: userName,
                selected: userAnswer,
                quiz_id: currentQuiz.id
            })
        });
    } catch (error) {
        console.error('Failed to submit answer:', error);
    }
    
    // Show correct answer briefly
    showAnswerFeedback(currentQuiz, userAnswer);
    
    setTimeout(() => {
        if (currentQuizIndex < currentQuizzes.length - 1) {
            currentQuizIndex++;
            displayCurrentQuiz();
        } else {
            showResults();
        }
    }, 2000);
}

// Show answer feedback
function showAnswerFeedback(quiz, userAnswer) {
    const choices = document.querySelectorAll('.choice-btn');
    const nextBtn = document.getElementById('next-btn');
    
    nextBtn.disabled = true;
    nextBtn.textContent = 'Loading...';
    
    choices.forEach(btn => {
        btn.disabled = true;
        const choice = btn.textContent.trim();
        
        if (choice === quiz.correct_answer) {
            btn.classList.add('correct');
        } else if (choice === userAnswer && choice !== quiz.correct_answer) {
            btn.classList.add('incorrect');
        }
    });
}

// Show results
function showResults() {
    hideAllSections();
    resultsSection.classList.remove('hidden');
    
    // Calculate score
    let correctAnswers = 0;
    currentQuizzes.forEach((quiz, index) => {
        if (userAnswers[index] === quiz.correct_answer) {
            correctAnswers++;
        }
    });
    
    const percentage = Math.round((correctAnswers / currentQuizzes.length) * 100);
    
    // Display results
    const resultsContent = document.getElementById('results-content');
    resultsContent.innerHTML = `
        <div class="score-display">${correctAnswers}/${currentQuizzes.length}</div>
        <div class="score-message">
            You scored ${percentage}%! 
            ${getScoreMessage(percentage)}
        </div>
        <div style="margin-top: 2rem;">
            <h3>Review:</h3>
            ${currentQuizzes.map((quiz, index) => `
                <div style="text-align: left; margin: 1rem 0; padding: 1rem; background: #f8f9fa; border-radius: 8px;">
                    <strong>Q${index + 1}:</strong> ${quiz.question}<br>
                    <span style="color: ${userAnswers[index] === quiz.correct_answer ? '#48bb78' : '#f56565'};">
                        Your answer: ${userAnswers[index]}
                    </span><br>
                    ${userAnswers[index] !== quiz.correct_answer ? 
                        `<span style="color: #48bb78;">Correct answer: ${quiz.correct_answer}</span>` : 
                        '<span style="color: #48bb78;">✓ Correct!</span>'
                    }
                </div>
            `).join('')}
        </div>
    `;
}

// Get score message
function getScoreMessage(percentage) {
    if (percentage >= 90) return "Excellent work! 🌟";
    if (percentage >= 70) return "Great job! 👍";
    if (percentage >= 50) return "Good effort! Keep practicing! 💪";
    return "Keep learning and try again! 📚";
}

// Restart current quiz
function restartCurrentQuiz() {
    currentQuizIndex = 0;
    userAnswers = [];
    showNameModal();
}

// Show topics section
function showTopicsSection() {
    hideAllSections();
    topicsSection.classList.remove('hidden');
    welcomeSection.classList.remove('hidden');
}

// Hide all sections
function hideAllSections() {
    welcomeSection.classList.add('hidden');
    topicsSection.classList.add('hidden');
    quizSection.classList.add('hidden');
    resultsSection.classList.add('hidden');
}

// Show message
function showMessage(message, type = 'info') {
    // Remove existing messages
    const existingMessages = document.querySelectorAll('.message');
    existingMessages.forEach(msg => msg.remove());
    
    // Create new message
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = message;
    
    // Insert at the top of the main content
    const main = document.querySelector('main');
    main.insertBefore(messageDiv, main.firstChild);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        messageDiv.remove();
    }, 5000);
}

// Utility function to handle errors
function handleError(error, userMessage = 'An error occurred') {
    console.error('Error:', error);
    showMessage(userMessage, 'error');
}

// Excel Upload Functions

// Load topics for upload dropdown
async function loadTopicsForUpload() {
    try {
        const topics = await apiCall('/api/topics/');
        const topicSelect = document.getElementById('topic-select');
        
        // Clear existing options except the first one
        topicSelect.innerHTML = '<option value="">Choose a topic...</option>';
        
        // Add topic options
        topics.forEach(topic => {
            const option = document.createElement('option');
            option.value = topic.id;
            option.textContent = topic.title;
            topicSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Failed to load topics for upload:', error);
    }
}

// Handle file selection
function handleFileSelection() {
    const fileInput = document.getElementById('excel-file');
    const uploadBtn = document.getElementById('upload-excel-btn');
    const topicSelect = document.getElementById('topic-select');
    
    // Enable upload button if file is selected and topic is chosen
    const fileSelected = fileInput.files.length > 0;
    const topicSelected = topicSelect.value !== '';
    
    uploadBtn.disabled = !(fileSelected && topicSelected);
}

// Handle topic selection
function handleTopicSelection() {
    handleFileSelection(); // Re-check if upload should be enabled
}

// Download Excel template
async function downloadTemplate() {
    try {
        const response = await fetch('/api/download-template/');
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        // Create blob and download
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'quiz_template.xlsx';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
        
        showMessage('Template downloaded successfully!', 'success');
    } catch (error) {
        console.error('Failed to download template:', error);
        showMessage('Failed to download template', 'error');
    }
}

// Upload Excel file
async function uploadExcelFile() {
    const fileInput = document.getElementById('excel-file');
    const topicSelect = document.getElementById('topic-select');
    const uploadBtn = document.getElementById('upload-excel-btn');
    const resultsDiv = document.getElementById('upload-results');
    
    if (!fileInput.files[0]) {
        showMessage('Please select an Excel file', 'error');
        return;
    }
    
    if (!topicSelect.value) {
        showMessage('Please select a topic', 'error');
        return;
    }
    
    // Disable upload button and show progress
    uploadBtn.disabled = true;
    uploadBtn.textContent = 'Uploading...';
    
    // Show progress bar
    resultsDiv.innerHTML = `
        <h4>Uploading...</h4>
        <div class="upload-progress">
            <div class="upload-progress-bar" style="width: 50%;"></div>
        </div>
    `;
    resultsDiv.classList.remove('hidden');
    
    try {
        // Create FormData
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);
        formData.append('topic_id', topicSelect.value);
        
        // Upload file
        const response = await fetch('/api/upload-quizzes/', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        
        // Update progress bar to 100%
        const progressBar = document.querySelector('.upload-progress-bar');
        if (progressBar) {
            progressBar.style.width = '100%';
        }
        
        // Show results
        setTimeout(() => {
            displayUploadResults(result);
        }, 500);
        
        // Refresh topics and topic dropdown
        await loadTopics();
        await loadTopicsForUpload();
        
    } catch (error) {
        console.error('Upload failed:', error);
        resultsDiv.innerHTML = `
            <h4>Upload Failed</h4>
            <div class="upload-errors">
                <strong>Error:</strong> ${error.message}
            </div>
        `;
        showMessage('Upload failed: ' + error.message, 'error');
    } finally {
        // Reset upload button
        uploadBtn.disabled = false;
        uploadBtn.textContent = '📤 Upload Quizzes';
        
        // Clear file input
        fileInput.value = '';
        handleFileSelection();
    }
}

// Display upload results
function displayUploadResults(result) {
    const resultsDiv = document.getElementById('upload-results');
    
    let html = `<h4>Upload Results</h4>`;
    
    // Summary
    html += `
        <div class="upload-summary">
            <strong>${result.message}</strong><br>
            Created: ${result.created_count} quizzes
        </div>
    `;
    
    // Errors (if any)
    if (result.errors && result.errors.length > 0) {
        html += `
            <div class="upload-errors">
                <strong>Errors encountered:</strong>
                <ul class="error-list">
                    ${result.errors.map(error => `<li>${error}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    resultsDiv.innerHTML = html;
    
    // Show success/error message
    if (result.success) {
        showMessage(result.message, 'success');
    } else {
        showMessage('Upload completed with errors', 'error');
    }
}
