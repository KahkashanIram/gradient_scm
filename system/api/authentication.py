# system/api/authentication.py

from rest_framework.authentication import SessionAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    Session-based authentication WITHOUT CSRF enforcement.

    Why this exists:
    - Django's SessionAuthentication enforces CSRF by default
    - Next.js admin dashboard runs on a different origin (localhost:3000)
    - This is SAFE for:
        • internal admin APIs
        • GET-only endpoints
        • no state mutation

    DO NOT use this for POST/PUT/DELETE APIs.
    """

    def enforce_csrf(self, request):
        # Intentionally bypass CSRF checks
        return
