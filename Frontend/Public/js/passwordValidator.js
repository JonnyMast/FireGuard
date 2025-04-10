// Password validation utility
export default function validatePassword(password) {
  const minLength = 8;
  const hasUpperCase = /[A-Z]/.test(password);
  const hasLowerCase = /[a-z]/.test(password);
  const hasNumbers = /\d/.test(password);
  const hasSpecialChar = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password);

  const errors = [];

  if (password.length < minLength) {
    errors.push(`Password must be at least ${minLength} characters long`);
  }

  if (!hasUpperCase) {
    errors.push("Password must include an uppercase letter");
  }

  if (!hasLowerCase) {
    errors.push("Password must include a lowercase letter");
  }

  if (!hasNumbers) {
    errors.push("Password must include a number");
  }

  if (!hasSpecialChar) {
    errors.push("Password must include a special character");
  }

  return {
    isValid: errors.length === 0,
    errors: errors,
  };
}
