from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Todas las credenciales vienen del entorno (.env en local, Environment en Render).
    # No hay valores por defecto con secretos: si falta algo obligatorio, la app no arranca.
    DATABASE_URL: str = ""
    STRIPE_SECRET_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""
    STRIPE_PUBLISHABLE_KEY: str = ""
    # SMS (opcional): si falta alguna de las 3, no se envían SMS.
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_FROM_NUMBER: str = ""
    # Correo: se usa el primer proveedor configurado (Gmail API > SendGrid > Brevo > SMTP).
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    # API HTTP de Brevo (puerto 443, funciona en Render)
    BREVO_API_KEY: str = ""
    # API HTTP de SendGrid (puerto 443, funciona en Render)
    SENDGRID_API_KEY: str = ""
    # API oficial de Gmail (OAuth2, puerto 443). Envia desde tu propia cuenta Gmail.
    GMAIL_CLIENT_ID: str = ""
    GMAIL_CLIENT_SECRET: str = ""
    GMAIL_REFRESH_TOKEN: str = ""
    # Texto que se añade al descriptor del extracto bancario (opcional, ej. "PAGO 1234").
    # El prefijo se configura en Stripe > Settings > Public details.
    STATEMENT_DESCRIPTOR_SUFFIX: str = ""
    FROM_EMAIL: str = ""
    FROM_NAME: str = "Secure Payment"
    APP_URL: str = "http://localhost:8000"
    SECRET_KEY: str = ""
    # Contraseña del panel de administración
    ADMIN_PASSWORD: str = ""

    class Config:
        env_file = ".env"

    @property
    def database_url(self) -> str:
        # Render/Heroku entregan "postgres://", que SQLAlchemy 2 ya no acepta.
        if self.DATABASE_URL.startswith("postgres://"):
            return "postgresql://" + self.DATABASE_URL[len("postgres://"):]
        return self.DATABASE_URL

    @property
    def twilio_enabled(self) -> bool:
        return bool(self.TWILIO_ACCOUNT_SID and self.TWILIO_AUTH_TOKEN and self.TWILIO_FROM_NUMBER)

    def validate_required(self) -> None:
        """Falla al arrancar si falta configuración obligatoria o es insegura."""
        errors = []
        for name in ("DATABASE_URL", "STRIPE_SECRET_KEY", "STRIPE_PUBLISHABLE_KEY",
                     "STRIPE_WEBHOOK_SECRET", "SECRET_KEY", "ADMIN_PASSWORD"):
            if not getattr(self, name):
                errors.append(f"falta {name}")
        if self.SECRET_KEY and len(self.SECRET_KEY) < 32:
            errors.append("SECRET_KEY debe tener al menos 32 caracteres")
        if self.ADMIN_PASSWORD and len(self.ADMIN_PASSWORD) < 12:
            errors.append("ADMIN_PASSWORD debe tener al menos 12 caracteres")
        if errors:
            raise RuntimeError("Configuración inválida: " + "; ".join(errors))


settings = Settings()
