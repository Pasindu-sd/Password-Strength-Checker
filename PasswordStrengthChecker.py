import re

def check_password(password):
    common = {'password', '12345678'}
    errors = []

    if password.lower() in common:
        errors.append("Too common, use a unique password.")
    if len(password) < 8:
        errors.append("Must be at least 8 characters.")
    if not re.search(r"\d", password):
        errors.append("Add at least one number.")
    if not re.search(r"[A-Z]", password):
        errors.append("Add at least one uppercase letter.")
    if not re.search(r"[a-z]", password):
        errors.append("Add at least one lowercase letter.")
    if not re.search(r"[@$!%*?&]", password):
        errors.append("Add at least one special character (@$!%*?&).")

    return "Strong password!" if not errors else "Weak password:\n- " + "\n- ".join(errors)

# Example usage
print(check_password(input("Enter a password: ")))
