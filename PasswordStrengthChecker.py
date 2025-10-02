import re

def check_password(password):
    # Rules
    length_error = len(password) < 8
    digit_error = re.search(r"\d", password) is None
    uppercase_error = re.search(r"[A-Z]", password) is None
    lowercase_error = re.search(r"[a-z]", password) is None
    symbol_error = re.search(r"[@$!%*?&]", password) is None

    # Collect errors
    errors = []
    if check_common_passwords(password):
        errors.append("Password is too common. Choose a more unique password.")
    if length_error:
        errors.append("Password must be at least 8 characters long.")
    if digit_error:
        errors.append("Password must contain at least one number.")
    if uppercase_error:
        errors.append("Password must contain at least one uppercase letter.")
    if lowercase_error:
        errors.append("Password must contain at least one lowercase letter.")
    if symbol_error:
        errors.append("Password must contain at least one special character (@$!%*?&).")

    # Result
    if not errors:
        return "Strong password!"
    else:
        return "Weak password:\n- " + "\n- ".join(errors)

def check_common_passwords(password):
    common_passwords = {'password', '12345678'}
    return password.lower() in common_passwords
    
# Example usage
password = input("Enter a password: ")
print(check_password(password))
