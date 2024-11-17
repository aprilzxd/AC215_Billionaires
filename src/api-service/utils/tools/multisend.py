from phi.tools.email import EmailTools

class multisend(EmailTools):
    def __init__(
        self,
        receiver_email = None,
        sender_name = None,
        sender_email = None,
        sender_passkey = None,
    ):
        super(multisend, self).__init__(receiver_email, sender_name, sender_email, sender_passkey)

    def email_user(self, subject: str, body: str) -> str:

        try:
            import smtplib
            from email.message import EmailMessage
        except ImportError:
            print("`smtplib` not installed")
            raise

        if not self.receiver_email:
            return "error: No receiver email provided"
        if not self.sender_name:
            return "error: No sender name provided"
        if not self.sender_email:
            return "error: No sender email provided"
        if not self.sender_passkey:
            return "error: No sender passkey provided"

        for email in self.receiver_email:
            msg = EmailMessage()
            msg["Subject"] = subject
            msg["From"] = f"{self.sender_name} <{self.sender_email}>"
            msg["To"] = email
            msg.set_content(body)

            print(f"Sending Email to {email}")
            try:
                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                    smtp.login(self.sender_email, self.sender_passkey)
                    smtp.send_message(msg)
            except Exception as e:
                print(f"Error sending email: {e}")
                return f"error: {e}"

        return "emails sent successfully"