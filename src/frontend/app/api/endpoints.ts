export const ENDPOINTS = {
  AUTH: {
    REGISTER: '/api/v1/auth/register',
    LOGIN: '/api/v1/auth/login',
    LOGOUT: '/api/v1/auth/logout',
    ME: '/api/v1/auth/me',
    REFRESH: '/api/v1/auth/refresh',
    FORGOT_PASSWORD: '/api/v1/auth/forgot-password',
    RESET_PASSWORD: '/api/v1/auth/reset-password',
    // Endpoint Email Verification & Resend OTP:
    VERIFY_EMAIL: '/api/v1/auth/verify-email',
    RESEND_OTP: '/api/v1/auth/resend-otp',
    GOOGLE_LOGIN: '/api/v1/auth/google/login',
    GOOGLE_CALLBACK: '/api/v1/auth/google/callback'
  }
} as const
