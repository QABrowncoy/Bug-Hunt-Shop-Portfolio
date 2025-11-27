// Global variables
let cart = [];
let isLoggedIn = false;

// Product data
const products = [
    { id: 1, name: "Gaming Laptop", price: 999.99, category: "electronics" },
    { id: 2, name: "Smartphone", price: 599.99, category: "electronics" },
    { id: 3, name: "Tablet", price: 299.99, category: "electronics" },
    { id: 4, name: "Wireless Headphones", price: 149.99, category: "audio" },
    { id: 5, name: "Smart Watch", price: 199.99, category: "wearables" }
];

// Validation patterns and functions
const ValidationRules = {
    name: {
        pattern: /^[a-zA-ZÀ-ÿ\s\-']{2,100}$/,
        minLength: 2,
        maxLength: 100,
        errorMessage: "Name must be 2-100 characters, letters only (hyphens and apostrophes allowed)"
    },
    
    email: {
        pattern: /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/,
        maxLength: 254,
        errorMessage: "Please enter a valid email address (example@domain.com)"
    },
    
    phone: {
        pattern: /^(\+?1[-.\s]?)?(\([0-9]{3}\)|[0-9]{3})[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}$/,
        errorMessage: "Please enter a valid phone number (555-123-4567, (555) 123-4567, or 5551234567)"
    },
    
    username: {
        pattern: /^[a-zA-Z0-9_]{3,50}$/,
        minLength: 3,
        maxLength: 50,
        errorMessage: "Username must be 3-50 characters, letters, numbers, and underscore only"
    },
    
    password: {
        minLength: 8,
        requireUppercase: true,
        requireLowercase: true,
        requireNumber: true,
        errorMessage: "Password must be 8+ characters with uppercase, lowercase, and number"
    },
    
    search: {
        minLength: 3,
        maxLength: 100,
        pattern: /^[a-zA-ZÀ-ÿ0-9\s\-']+$/,
        errorMessage: "Search must be 3-100 characters, letters and numbers only"
    },
    
    message: {
        minLength: 10,
        maxLength: 2000,
        errorMessage: "Message must be 10-2000 characters"
    }
};

// Enhanced validation functions
function validateInput(value, type, fieldName) {
    const rules = ValidationRules[type];
    if (!rules) return { isValid: true, message: "" };
    
    // Trim whitespace
    const trimmed = value.trim();
    
    // Check for empty/whitespace only
    if (!trimmed && (type !== 'phone')) {
        return { isValid: false, message: `${fieldName} is required` };
    }
    
    // Check for HTML/script tags (security)
    if (/<[^>]*>/.test(value)) {
        return { isValid: false, message: `${fieldName} cannot contain HTML tags` };
    }
    
    // Length checks
    if (rules.minLength && trimmed.length < rules.minLength) {
        return { isValid: false, message: `${fieldName} must be at least ${rules.minLength} characters` };
    }
    
    if (rules.maxLength && trimmed.length > rules.maxLength) {
        return { isValid: false, message: `${fieldName} must be no more than ${rules.maxLength} characters` };
    }
    
    // Pattern checks
    if (rules.pattern && !rules.pattern.test(trimmed)) {
        return { isValid: false, message: rules.errorMessage };
    }
    
    // Special password validation
    if (type === 'password') {
        return validatePassword(value);
    }
    
    // Special phone validation (optional field)
    if (type === 'phone' && trimmed) {
        if (!rules.pattern.test(trimmed)) {
            return { isValid: false, message: rules.errorMessage };
        }
    }
    
    return { isValid: true, message: "" };
}

function validatePassword(password) {
    const rules = ValidationRules.password;
    const errors = [];
    
    if (password.length < rules.minLength) {
        errors.push(`at least ${rules.minLength} characters`);
    }
    
    if (rules.requireUppercase && !/[A-Z]/.test(password)) {
        errors.push("one uppercase letter");
    }
    
    if (rules.requireLowercase && !/[a-z]/.test(password)) {
        errors.push("one lowercase letter");
    }
    
    if (rules.requireNumber && !/[0-9]/.test(password)) {
        errors.push("one number");
    }
    
    if (errors.length > 0) {
        return { 
            isValid: false, 
            message: `Password needs: ${errors.join(', ')}`,
            strength: 'weak'
        };
    }
    
    // Calculate strength
    let strength = 'medium';
    if (password.length >= 12 && /[!@#$%^&*(),.?":{}|<>]/.test(password)) {
        strength = 'strong';
    }
    
    return { isValid: true, message: "", strength: strength };
}

function showError(fieldId, message) {
    const errorDiv = document.getElementById(fieldId + 'Error');
    const inputField = document.getElementById(fieldId);
    
    if (errorDiv) {
        errorDiv.textContent = message;
        errorDiv.classList.add('show');
    }
    
    if (inputField) {
        inputField.classList.add('error');
        inputField.classList.remove('valid');
    }
}

function clearError(fieldId) {
    const errorDiv = document.getElementById(fieldId + 'Error');
    const inputField = document.getElementById(fieldId);
    
    if (errorDiv) {
        errorDiv.textContent = "";
        errorDiv.classList.remove('show');
    }
    
    if (inputField) {
        inputField.classList.remove('error');
        inputField.classList.add('valid');
    }
}

// Enhanced search functionality
function searchProducts() {
    const query = document.getElementById('searchInput').value;
    const resultsDiv = document.getElementById('searchResults');
    
    // Validate search input
    const validation = validateInput(query, 'search', 'Search');
    if (!validation.isValid) {
        showError('search', validation.message);
        resultsDiv.innerHTML = `<p style='color: #dc3545;'>${validation.message}</p>`;
        return;
    }
    
    clearError('search');
    
    // Perform case-insensitive partial search
    const trimmedQuery = query.trim().toLowerCase();
    const results = products.filter(product => 
        product.name.toLowerCase().includes(trimmedQuery)
    );
    
    if (results.length === 0) {
        resultsDiv.innerHTML = `<p style='color: #6c757d;'>No products found for "${query}". Try "laptop", "phone", "tablet", "gaming", or "smart".</p>`;
    } else {
        let resultHTML = `<h4>Found ${results.length} product(s):</h4>`;
        results.forEach(product => {
            resultHTML += `
                <div style='padding: 0.5rem; border-bottom: 1px solid #eee;'>
                    <strong>${product.name}</strong> - $${product.price}
                    <button onclick="addToCart('${product.name}', ${product.price})" 
                            style='margin-left: 1rem; padding: 0.25rem 0.5rem; background-color: #28a745; color: white; border: none; border-radius: 3px;'>
                        Add to Cart
                    </button>
                </div>
            `;
        });
        resultsDiv.innerHTML = resultHTML;
    }
}

// Shopping cart functions (keeping original bugs for testing)
function addToCart(productName, price) {
    // BUG: Still allows duplicate items without quantity tracking
    cart.push({ name: productName, price: price });
    
    updateCartDisplay();
    updateCartCalculations();
    
    // Added user feedback
    showNotification(`${productName} added to cart!`, 'success');
}

function updateCartDisplay() {
    const cartItemsDiv = document.getElementById('cartItems');
    
    if (cart.length === 0) {
        cartItemsDiv.innerHTML = "<p>Your cart is empty</p>";
        return;
    }
    
    let cartHTML = "";
    cart.forEach((item, index) => {
        cartHTML += `
            <div class="cart-item">
                <span>${item.name}</span>
                <span>$${item.price}</span>
                <button onclick="removeFromCart(${index})" style="background-color: #e74c3c; color: white; border: none; padding: 5px 10px; border-radius: 3px;">Remove</button>
            </div>
        `;
    });
    
    cartItemsDiv.innerHTML = cartHTML;
}

function updateCartCalculations() {
    // BUG: Still has calculation errors for testing
    const subtotal = cart.reduce((sum, item) => sum + parseFloat(item.price), 0);
    
    // BUG: Tax calculation is still wrong
    const tax = subtotal + 0.085;
    
    // BUG: Shipping logic still backwards
    const shipping = subtotal > 100 ? 5.99 : 0;
    
    // BUG: Total still doesn't include tax
    const total = subtotal + shipping;
    
    document.getElementById('subtotal').textContent = subtotal.toFixed(2);
    document.getElementById('tax').textContent = tax.toFixed(3); // BUG: Still 3 decimal places
    document.getElementById('shipping').textContent = shipping.toFixed(2);
    document.getElementById('total').textContent = total.toFixed(2);
}

function removeFromCart(index) {
    const removedItem = cart[index];
    cart.splice(index, 1);
    updateCartDisplay();
    updateCartCalculations();
    showNotification(`${removedItem.name} removed from cart`, 'info');
}

function clearCart() {
    cart = [];
    updateCartDisplay();
    updateCartCalculations();
    showNotification('Cart cleared', 'info');
    // BUG: Still doesn't reset to initial state properly
}

// Enhanced contact form validation
function submitContactForm(event) {
    event.preventDefault();
    
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const phone = document.getElementById('phone').value;
    const message = document.getElementById('message').value;
    
    let hasErrors = false;
    
    // Validate each field
    const nameValidation = validateInput(name, 'name', 'Name');
    if (!nameValidation.isValid) {
        showError('name', nameValidation.message);
        hasErrors = true;
    } else {
        clearError('name');
    }
    
    const emailValidation = validateInput(email, 'email', 'Email');
    if (!emailValidation.isValid) {
        showError('email', emailValidation.message);
        hasErrors = true;
    } else {
        clearError('email');
    }
    
    const phoneValidation = validateInput(phone, 'phone', 'Phone');
    if (!phoneValidation.isValid) {
        showError('phone', phoneValidation.message);
        hasErrors = true;
    } else {
        clearError('phone');
    }
    
    const messageValidation = validateInput(message, 'message', 'Message');
    if (!messageValidation.isValid) {
        showError('message', messageValidation.message);
        hasErrors = true;
    } else {
        clearError('message');
    }
    
    const resultDiv = document.getElementById('contactResult');
    
    if (hasErrors) {
        resultDiv.innerHTML = "<div class='error-message show'>Please fix the errors above before submitting.</div>";
        return;
    }
    
    // Simulate form submission
    resultDiv.innerHTML = "<div style='color: #17a2b8;'>Sending message...</div>";
    
    setTimeout(() => {
        resultDiv.innerHTML = "<div class='success-message'>Thank you! Your message has been sent successfully.</div>";
        // Clear form after successful submission
        document.getElementById('contactForm').reset();
        updateCharacterCount();
    }, 1500);
}

// Enhanced login functionality
function handleLogin(event) {
    event.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const rememberMe = document.getElementById('rememberMe').checked;
    
    let hasErrors = false;
    
    // Validate username
    const usernameValidation = validateInput(username, 'username', 'Username');
    if (!usernameValidation.isValid) {
        showError('username', usernameValidation.message);
        hasErrors = true;
    } else {
        clearError('username');
    }
    
    // Validate password
    const passwordValidation = validateInput(password, 'password', 'Password');
    if (!passwordValidation.isValid) {
        showError('password', passwordValidation.message);
        hasErrors = true;
    } else {
        clearError('password');
    }
    
    const resultDiv = document.getElementById('loginResult');
    
    if (hasErrors) {
        resultDiv.innerHTML = "<div class='error-message show'>Please fix the validation errors above.</div>";
        return;
    }
    
    // Check credentials (still hardcoded for testing, but now case-insensitive username)
    if (username.toLowerCase() === "admin" && password === "Password123") {
        isLoggedIn = true;
        
        if (rememberMe) {
            localStorage.setItem('rememberUser', username.toLowerCase());
            localStorage.setItem('loginExpiry', Date.now() + (30 * 24 * 60 * 60 * 1000)); // 30 days
        }
        
        resultDiv.innerHTML = "<div class='success-message'>Login successful! Welcome back.</div>";
        document.getElementById('loginLink').textContent = "Logout";
        
        // Clear form after successful login
        document.getElementById('loginForm').reset();
        
    } else {
        // Generic error message (security best practice)
        resultDiv.innerHTML = "<div class='error-message show'>Invalid username or password. Please try again.</div>";
    }
}

// Password strength indicator
function updatePasswordStrength() {
    const password = document.getElementById('password').value;
    const strengthDiv = document.getElementById('passwordStrength');
    
    if (!password) {
        strengthDiv.className = 'strength-indicator';
        return;
    }
    
    const validation = validatePassword(password);
    
    if (validation.isValid) {
        strengthDiv.className = `strength-indicator strength-${validation.strength}`;
    } else {
        strengthDiv.className = 'strength-indicator strength-weak';
    }
}

// Character counter for message field
function updateCharacterCount() {
    const messageField = document.getElementById('message');
    const counter = document.getElementById('messageCount');
    
    if (messageField && counter) {
        const count = messageField.value.length;
        counter.textContent = count;
        
        // Update counter styling based on length
        counter.parentElement.className = 'char-counter';
        if (count > 1800) {
            counter.parentElement.classList.add('danger');
        } else if (count > 1500) {
            counter.parentElement.classList.add('warning');
        }
    }
}

// Input Testing Laboratory functions
function testInput() {
    const testValue = document.getElementById('testInput').value;
    const testType = document.getElementById('testType').value;
    const resultDiv = document.getElementById('testResult');
    
    const validation = validateInput(testValue, testType, 'Test Input');
    
    let resultHTML = `
        <h4>Testing "${testValue}" as ${testType}:</h4>
        <p><strong>Input Value:</strong> "${testValue}"</p>
        <p><strong>Length:</strong> ${testValue.length} characters</p>
        <p><strong>Validation Result:</strong> <span style="color: ${validation.isValid ? '#28a745' : '#dc3545'};">${validation.isValid ? 'VALID' : 'INVALID'}</span></p>
    `;
    
    if (!validation.isValid) {
        resultHTML += `<p><strong>Error Message:</strong> <span style="color: #dc3545;">${validation.message}</span></p>`;
    }
    
    if (testType === 'password' && validation.strength) {
        resultHTML += `<p><strong>Password Strength:</strong> <span style="color: ${getStrengthColor(validation.strength)};">${validation.strength.toUpperCase()}</span></p>`;
    }
    
    resultDiv.innerHTML = resultHTML;
}

function setTestInput(value) {
    document.getElementById('testInput').value = value;
}

function getStrengthColor(strength) {
    switch(strength) {
        case 'weak': return '#dc3545';
        case 'medium': return '#fd7e14';
        case 'strong': return '#28a745';
        default: return '#6c757d';
    }
}

// Notification system
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        padding: 1rem;
        border-radius: 5px;
        color: white;
        font-weight: bold;
        z-index: 10000;
        opacity: 0;
        transition: opacity 0.3s;
    `;
    
    switch(type) {
        case 'success':
            notification.style.backgroundColor = '#28a745';
            break;
        case 'error':
            notification.style.backgroundColor = '#dc3545';
            break;
        case 'warning':
            notification.style.backgroundColor = '#fd7e14';
            break;
        default:
            notification.style.backgroundColor = '#17a2b8';
    }
    
    notification.textContent = message;
    document.body.appendChild(notification);
    
    // Fade in
    setTimeout(() => notification.style.opacity = '1', 10);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.opacity = '0';
        setTimeout(() => document.body.removeChild(notification), 300);
    }, 3000);
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Search input validation on keyup
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keyup', function(e) {
            if (e.key === 'Enter') {
                searchProducts();
            }
        });
    }
    
    // Password strength indicator
    const passwordInput = document.getElementById('password');
    if (passwordInput) {
        passwordInput.addEventListener('input', updatePasswordStrength);
    }
    
    // Character counter for message
    const messageInput = document.getElementById('message');
    if (messageInput) {
        messageInput.addEventListener('input', updateCharacterCount);
        updateCharacterCount(); // Initialize counter
    }
    
    // Real-time validation for all form fields
    const formFields = ['name', 'email', 'phone', 'username'];
    formFields.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (field) {
            field.addEventListener('blur', function() {
                const validation = validateInput(this.value, fieldId, fieldId.charAt(0).toUpperCase() + fieldId.slice(1));
                if (!validation.isValid && this.value.trim()) {
                    showError(fieldId, validation.message);
                } else if (validation.isValid) {
                    clearError(fieldId);
                }
            });
        }
    });
    
    // Check for remembered user
    const rememberedUser = localStorage.getItem('rememberUser');
    const loginExpiry = localStorage.getItem('loginExpiry');
    
    if (rememberedUser && loginExpiry && Date.now() < parseInt(loginExpiry)) {
        const usernameField = document.getElementById('username');
        if (usernameField) {
            usernameField.value = rememberedUser;
        }
    }
});
