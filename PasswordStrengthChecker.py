import re

def check_password(password):
    common = {'password', '12345678'}
    score = 0
    errors = []

    if password.lower() in common:
        errors.append("Too common, use a unique password.")
        score = 0
    if len(password) >= 8: score += 1
    else: errors.append("Must be at least 8 characters.")
    if re.search(r"\d", password): score += 1
    else: errors.append("Add at least one number.")
    if re.search(r"[A-Z]", password): score += 1
    else: errors.append("Add at least one uppercase letter.")
    if re.search(r"[a-z]", password): score += 1
    else: errors.append("Add at least one lowercase letter.")
    if re.search(r"[@$!%*?&]", password): score += 1
    else: errors.append("Add at least one special character (@$!%*?&).")

    level = ["Weak", "Medium", "Strong", "Very Strong"]
    rating = level[min(score, 4) - 1] if score > 0 else "Very Weak"

    result = f"Password strength: {rating}"
    if errors:
        result += "\n- " + "\n- ".join(errors)
    return result

# Example usage
print(check_password(input("Enter a password: ")))
