const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

export const PASSWORD_RULE_MESSAGE = 'Use at least 8 characters with a letter and a number.'

export interface LoginValues {
  email: string
  password: string
}

export interface SignUpValues {
  fullName: string
  email: string
  password: string
  confirmPassword: string
}

export type AuthFieldErrors<T extends string> = Partial<Record<T, string>>

export function isValidEmail(value: string): boolean {
  return EMAIL_PATTERN.test(value.trim())
}

export function isStrongPassword(value: string): boolean {
  return value.length >= 8 && /[A-Za-z]/.test(value) && /\d/.test(value)
}

export function validateLogin(values: LoginValues): AuthFieldErrors<keyof LoginValues> {
  const errors: AuthFieldErrors<keyof LoginValues> = {}

  if (!values.email.trim()) {
    errors.email = 'Email is required.'
  } else if (!isValidEmail(values.email)) {
    errors.email = 'Enter a valid email address.'
  }

  if (!values.password) {
    errors.password = 'Password is required.'
  }

  return errors
}

export function validateSignUp(values: SignUpValues): AuthFieldErrors<keyof SignUpValues> {
  const errors: AuthFieldErrors<keyof SignUpValues> = {}

  if (!values.fullName.trim()) {
    errors.fullName = 'Full name is required.'
  }

  if (!values.email.trim()) {
    errors.email = 'Email is required.'
  } else if (!isValidEmail(values.email)) {
    errors.email = 'Enter a valid email address.'
  }

  if (!values.password) {
    errors.password = 'Password is required.'
  } else if (!isStrongPassword(values.password)) {
    errors.password = PASSWORD_RULE_MESSAGE
  }

  if (!values.confirmPassword) {
    errors.confirmPassword = 'Please confirm your password.'
  } else if (values.confirmPassword !== values.password) {
    errors.confirmPassword = 'Passwords do not match.'
  }

  return errors
}
