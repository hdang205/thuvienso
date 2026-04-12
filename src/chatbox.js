/**
 * AI Chatbox Component
 * Floating chat widget for book recommendations
 */

class ChatBox {
  constructor(apiBase = 'http://localhost:8000/api') {
    this.apiBase = apiBase;
    this.isOpen = false;
    this.messages = [];
    this.accessToken = null;
    this.chatboxId = 'chatbox-widget';
    this.loadFromStorage();
    this.initializeUI();
  }

  /**
   * Initialize the chatbox UI
   */
  initializeUI() {
    // Create chatbox container
    const container = document.createElement('div');
    container.id = this.chatboxId;
    container.innerHTML = `
      <div class="chatbox-widget">
        <!-- Toggle button -->
        <button class="chatbox-toggle" id="chatbox-toggle" title="Chat with us">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
          </svg>
        </button>

        <!-- Chat window -->
        <div class="chatbox-window" id="chatbox-window" style="display: none;">
          <div class="chatbox-header">
            <h3>Book Recommendations</h3>
            <button class="chatbox-close" id="chatbox-close" title="Close">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </div>

          <div class="chatbox-messages" id="chatbox-messages"></div>

          <div class="chatbox-input">
            <input 
              type="text" 
              id="chatbox-input" 
              placeholder="What book are you looking for?" 
              autocomplete="off"
            />
            <button id="chatbox-send" title="Send">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="22" y1="2" x2="11" y2="13"></line>
                <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
              </svg>
            </button>
          </div>
        </div>
      </div>
    `;

    document.body.appendChild(container);

    // Add styles
    this.addStyles();

    // Attach event listeners
    document
      .getElementById('chatbox-toggle')
      .addEventListener('click', () => this.toggle());
    document
      .getElementById('chatbox-close')
      .addEventListener('click', () => this.close());
    document
      .getElementById('chatbox-send')
      .addEventListener('click', () => this.sendMessage());
    document
      .getElementById('chatbox-input')
      .addEventListener('keypress', (e) => {
        if (e.key === 'Enter') this.sendMessage();
      });

    // Load chat history
    this.displayMessages();

    // Show initial greeting
    if (this.messages.length === 0) {
      this.addBotMessage(
        '👋 Hi! I can help you find books. Try asking: "books about science" or "fiction novels"'
      );
    }
  }

  /**
   * Add CSS styles for the chatbox
   */
  addStyles() {
    const style = document.createElement('style');
    style.textContent = `
      #chatbox-widget {
        --chatbox-primary: #3b82f6;
        --chatbox-bg: #ffffff;
        --chatbox-text: #1f2937;
        --chatbox-border: #e5e7eb;
      }

      .chatbox-widget {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 9999;
      }

      .chatbox-toggle {
        width: 56px;
        height: 56px;
        border-radius: 50%;
        background-color: var(--chatbox-primary);
        color: white;
        border: none;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        transition: transform 0.2s, box-shadow 0.2s;
        font-size: 0;
        line-height: 0;
      }

      .chatbox-toggle:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
      }

      .chatbox-toggle:active {
        transform: scale(0.95);
      }

      .chatbox-window {
        position: absolute;
        bottom: 80px;
        right: 0;
        width: 380px;
        height: 500px;
        background-color: var(--chatbox-bg);
        border: 1px solid var(--chatbox-border);
        border-radius: 12px;
        box-shadow: 0 5px 40px rgba(0, 0, 0, 0.16);
        display: flex;
        flex-direction: column;
        animation: slideIn 0.3s ease-out;
      }

      @keyframes slideIn {
        from {
          opacity: 0;
          transform: translateY(10px);
        }
        to {
          opacity: 1;
          transform: translateY(0);
        }
      }

      .chatbox-header {
        padding: 16px;
        border-bottom: 1px solid var(--chatbox-border);
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: var(--chatbox-primary);
        color: white;
        border-radius: 12px 12px 0 0;
      }

      .chatbox-header h3 {
        margin: 0;
        font-size: 16px;
        font-weight: 600;
      }

      .chatbox-close {
        background: none;
        border: none;
        color: white;
        cursor: pointer;
        padding: 4px;
        display: flex;
        align-items: center;
        justify-content: center;
      }

      .chatbox-close:hover {
        opacity: 0.8;
      }

      .chatbox-messages {
        flex: 1;
        overflow-y: auto;
        padding: 16px;
        display: flex;
        flex-direction: column;
        gap: 12px;
      }

      .chatbox-message {
        display: flex;
        flex-direction: column;
        gap: 4px;
        animation: fadeIn 0.3s ease-out;
      }

      @keyframes fadeIn {
        from {
          opacity: 0;
          transform: translateY(8px);
        }
        to {
          opacity: 1;
          transform: translateY(0);
        }
      }

      .chatbox-message.user {
        align-items: flex-end;
      }

      .chatbox-message.bot {
        align-items: flex-start;
      }

      .chatbox-bubble {
        padding: 8px 12px;
        border-radius: 12px;
        max-width: 85%;
        word-wrap: break-word;
        font-size: 14px;
        line-height: 1.4;
      }

      .chatbox-message.user .chatbox-bubble {
        background-color: var(--chatbox-primary);
        color: white;
        border-bottom-right-radius: 4px;
      }

      .chatbox-message.bot .chatbox-bubble {
        background-color: #f3f4f6;
        color: var(--chatbox-text);
        border-bottom-left-radius: 4px;
      }

      .chatbox-suggestions {
        display: grid;
        grid-template-columns: 1fr;
        gap: 8px;
        margin-top: 8px;
        max-width: 85%;
      }

      .chatbox-suggestion-btn {
        padding: 8px 12px;
        border: 1px solid var(--chatbox-primary);
        background-color: white;
        color: var(--chatbox-primary);
        border-radius: 8px;
        cursor: pointer;
        font-size: 13px;
        transition: all 0.2s;
      }

      .chatbox-suggestion-btn:hover {
        background-color: var(--chatbox-primary);
        color: white;
      }

      .chatbox-book-item {
        padding: 8px 12px;
        border: 1px solid var(--chatbox-border);
        border-radius: 8px;
        margin-top: 8px;
        max-width: 85%;
        font-size: 13px;
      }

      .chatbox-book-title {
        font-weight: 600;
        color: var(--chatbox-text);
      }

      .chatbox-book-author {
        color: #6b7280;
        font-size: 12px;
      }

      .chatbox-book-category {
        display: inline-block;
        background-color: #e0f2fe;
        color: #0369a1;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 11px;
        margin-top: 4px;
      }

      .chatbox-input {
        padding: 12px;
        border-top: 1px solid var(--chatbox-border);
        display: flex;
        gap: 8px;
        background-color: var(--chatbox-bg);
        border-radius: 0 0 12px 12px;
      }

      .chatbox-input input {
        flex: 1;
        border: 1px solid var(--chatbox-border);
        border-radius: 8px;
        padding: 8px 12px;
        font-size: 14px;
        outline: none;
        transition: border-color 0.2s;
      }

      .chatbox-input input:focus {
        border-color: var(--chatbox-primary);
      }

      .chatbox-input button {
        width: 36px;
        height: 36px;
        background-color: var(--chatbox-primary);
        color: white;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: opacity 0.2s;
      }

      .chatbox-input button:hover {
        opacity: 0.8;
      }

      .chatbox-input button:active {
        opacity: 0.6;
      }

      .chatbox-loading {
        display: inline-block;
        width: 16px;
        height: 16px;
        border: 2px solid #f3f4f6;
        border-top-color: var(--chatbox-primary);
        border-radius: 50%;
        animation: spin 0.8s linear infinite;
      }

      @keyframes spin {
        to { transform: rotate(360deg); }
      }

      /* Mobile responsiveness */
      @media (max-width: 480px) {
        .chatbox-window {
          width: calc(100vw - 40px);
          height: calc(100vh - 120px);
          bottom: 80px;
          right: 50%;
          transform: translateX(50%);
        }
      }
    `;
    document.head.appendChild(style);
  }

  /**
   * Toggle chatbox visibility
   */
  toggle() {
    if (this.isOpen) {
      this.close();
    } else {
      this.open();
    }
  }

  /**
   * Open chatbox
   */
  open() {
    this.isOpen = true;
    document.getElementById('chatbox-window').style.display = 'flex';
    document.getElementById('chatbox-input').focus();
  }

  /**
   * Close chatbox
   */
  close() {
    this.isOpen = false;
    document.getElementById('chatbox-window').style.display = 'none';
  }

  /**
   * Send user message
   */
  async sendMessage() {
    const input = document.getElementById('chatbox-input');
    const message = input.value.trim();

    if (!message) return;

    input.value = '';
    this.addUserMessage(message);

    // Show loading indicator
    this.showLoadingIndicator();

    try {
      const response = await this.fetchRecommendations(message);
      this.removeLoadingIndicator();
      this.displayBotResponse(response);
    } catch (error) {
      this.removeLoadingIndicator();
      this.addBotMessage(
        'Sorry, I encountered an error. Please try again later.'
      );
      console.error('Chat error:', error);
    }
  }

  /**
   * Fetch recommendations from API
   */
  async fetchRecommendations(query) {
    const token = this.accessToken || localStorage.getItem('accessToken');

    if (!token) {
      throw new Error('Not authenticated');
    }

    const response = await fetch(`${this.apiBase}/chat/recommend/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ query }),
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    return await response.json();
  }

  /**
   * Display bot response
   */
  displayBotResponse(response) {
    const { message, suggestions } = response;

    // Add main message
    this.addBotMessage(message);

    // Add book suggestions
    if (suggestions && suggestions.length > 0) {
      suggestions.forEach((book) => {
        this.addBotBookSuggestion(book);
      });
    }
  }

  /**
   * Add user message to chat
   */
  addUserMessage(text) {
    const msg = {
      type: 'user',
      text,
      timestamp: new Date().toISOString(),
    };
    this.messages.push(msg);
    this.renderMessage(msg);
    this.saveToStorage();
  }

  /**
   * Add bot message to chat
   */
  addBotMessage(text) {
    const msg = {
      type: 'bot',
      text,
      timestamp: new Date().toISOString(),
    };
    this.messages.push(msg);
    this.renderMessage(msg);
    this.saveToStorage();
  }

  /**
   * Add book suggestion
   */
  addBotBookSuggestion(book) {
    const msg = {
      type: 'bot-book',
      book,
      timestamp: new Date().toISOString(),
    };
    this.messages.push(msg);
    this.renderBookMessage(msg);
    this.saveToStorage();
  }

  /**
   * Render message in chat
   */
  renderMessage(msg) {
    const messagesDiv = document.getElementById('chatbox-messages');
    const messageEl = document.createElement('div');
    messageEl.className = `chatbox-message ${msg.type}`;

    if (msg.type === 'user') {
      messageEl.innerHTML = `<div class="chatbox-bubble">${this.escapeHtml(msg.text)}</div>`;
    } else if (msg.type === 'bot') {
      messageEl.innerHTML = `<div class="chatbox-bubble">${this.escapeHtml(msg.text)}</div>`;
    }

    messagesDiv.appendChild(messageEl);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
  }

  /**
   * Render book message
   */
  renderBookMessage(msg) {
    const messagesDiv = document.getElementById('chatbox-messages');
    const { book } = msg;

    const messageEl = document.createElement('div');
    messageEl.className = 'chatbox-message bot';

    const bookHtml = `
      <div class="chatbox-book-item">
        <div class="chatbox-book-title">${this.escapeHtml(book.title)}</div>
        <div class="chatbox-book-author">by ${this.escapeHtml(book.author)}</div>
        <div class="chatbox-book-category">${this.escapeHtml(book.category)}</div>
        ${book.description ? `<div style="margin-top: 6px; color: #4b5563; font-size: 12px;">${this.escapeHtml(book.description)}</div>` : ''}
        <div style="margin-top: 6px; color: #10b981; font-weight: 500; font-size: 12px;">
          Available: ${book.available_quantity} copies
        </div>
      </div>
    `;

    messageEl.innerHTML = bookHtml;
    messagesDiv.appendChild(messageEl);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
  }

  /**
   * Show loading indicator
   */
  showLoadingIndicator() {
    const messagesDiv = document.getElementById('chatbox-messages');
    const loadingEl = document.createElement('div');
    loadingEl.className = 'chatbox-message bot';
    loadingEl.id = 'chatbox-loading';
    loadingEl.innerHTML = `<div class="chatbox-bubble"><div class="chatbox-loading"></div></div>`;
    messagesDiv.appendChild(loadingEl);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
  }

  /**
   * Remove loading indicator
   */
  removeLoadingIndicator() {
    const loadingEl = document.getElementById('chatbox-loading');
    if (loadingEl) loadingEl.remove();
  }

  /**
   * Display all messages
   */
  displayMessages() {
    const messagesDiv = document.getElementById('chatbox-messages');
    messagesDiv.innerHTML = '';

    this.messages.forEach((msg) => {
      if (msg.type === 'bot-book') {
        this.renderBookMessage(msg);
      } else {
        this.renderMessage(msg);
      }
    });

    messagesDiv.scrollTop = messagesDiv.scrollHeight;
  }

  /**
   * Save chat history to localStorage
   */
  saveToStorage() {
    const maxMessages = 50; // Keep only last 50 messages
    const messagesToSave = this.messages.slice(-maxMessages);
    localStorage.setItem('chatboxHistory', JSON.stringify(messagesToSave));
  }

  /**
   * Load chat history from localStorage
   */
  loadFromStorage() {
    const stored = localStorage.getItem('chatboxHistory');
    if (stored) {
      try {
        this.messages = JSON.parse(stored);
      } catch (e) {
        console.error('Failed to load chat history:', e);
        this.messages = [];
      }
    }
  }

  /**
   * Escape HTML special characters
   */
  escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
}

// Initialize chatbox when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    const apiBase = window.API_BASE || 'http://localhost:8000/api';
    window.chatbox = new ChatBox(apiBase);
  });
} else {
  const apiBase = window.API_BASE || 'http://localhost:8000/api';
  window.chatbox = new ChatBox(apiBase);
}
