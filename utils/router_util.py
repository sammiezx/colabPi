import re

def validate_email(email):
    # Basic email format validation using a regular expression
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return True
    return False

def validate_phone(phone):
    # Advanced phone number format validation (10 digits)
    if re.match(r"^\d{10}$", phone):
        return True
    return False

def validate_username(username):
    # Advanced username validation (alphanumeric characters only, at least 3 characters)
    if re.match(r"^[a-zA-Z0-9_]{3,}$", username):
        return True
    return False

def validate_password(password):
    # Advanced password validation (at least 8 characters, with at least one uppercase, one lowercase, one digit, and one special character)
    if len(password) >= 8 and re.search(r"[A-Z]", password) and re.search(r"[a-z]", password) and re.search(r"\d", password) and re.search(r"[!@#$%^&*()-+=]", password):
        return True
    return False

def validate_bio(bio):
    # Advanced bio validation (maximum 150 characters, no profanity)
    if len(bio) <= 150:
        # Additional check for profanity using a profanity detection library
        if not contains_profanity(bio):
            return True
    return False

# Function to detect profanity in text (this is a placeholder, you'll need to implement it or use an existing library)
def contains_profanity(text):
    # Placeholder implementation
    profanity_list = ["fuck", "nigga", "bitch"]
    for word in profanity_list:
        if word in text:
            return True
    return False

def validate_add_influencer(email, phone, username, password, bio):
    try:
        if not validate_username(username):
            raise AssertionError("Invalid username")
        
        if not validate_email(email):
            raise AssertionError("Invalid email")        

        if not validate_phone(phone):
            raise AssertionError("Invalid phone number")

        if not validate_password(password):
            raise AssertionError("Invalid password")

        if not validate_bio(bio):
            raise AssertionError("Invalid bio")

    except AssertionError as e:
        raise e
    
def validate_add_brand(email, phone, brand_name, username, password, description):
    try:

        if not validate_username(username):
            raise AssertionError("Invalid username")
        
        if not validate_email(email):
            raise AssertionError("Invalid email")        

        if not validate_phone(phone):
            raise AssertionError("Invalid phone number")

        if not validate_password(password):
            raise AssertionError("Invalid password")
        
    except AssertionError as e:
        raise e
