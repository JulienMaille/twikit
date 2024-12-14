import asyncio
import email as emaillib
import imaplib
import os
import time
from datetime import datetime, timezone, timedelta
import logging


class EmailLoginError(Exception):
    def __init__(self, message="Email login error"):
        self.message = message
        super().__init__(self.message)


class EmailCodeTimeoutError(Exception):
    def __init__(self, message="Email code timeout"):
        self.message = message
        super().__init__(self.message)


class EmailClient:
    IMAP_MAPPING = {
        "gmail.com": "imap.gmail.com",
        "yahoo.com": "imap.mail.yahoo.com",
        "icloud.com": "imap.mail.me.com",
        "outlook.com": "imap-mail.outlook.com",
        "outlook.fr": "imap-mail.outlook.com",
        "hotmail.com": "imap-mail.outlook.com",
        "aol.com": "imap.aol.com",
        "gmx.com": "imap.gmx.com",
        "zoho.com": "imap.zoho.com",
        "yandex.com": "imap.yandex.com",
        "protonmail.com": "imap.protonmail.com",
        "mail.com": "imap.mail.com",
        "rambler.ru": "imap.rambler.ru",
        "qq.com": "imap.qq.com",
        "163.com": "imap.163.com",
        "126.com": "imap.126.com",
        "sina.com": "imap.sina.com",
        "comcast.net": "imap.comcast.net",
        "verizon.net": "incoming.verizon.net",
        "mail.ru": "imap.mail.ru",
    }

    @classmethod
    def add_imap_mapping(cls, email_domain: str, imap_domain: str):
        cls.IMAP_MAPPING[email_domain] = imap_domain

    @classmethod
    def _get_imap_domain(cls, email: str) -> str:
        email_domain = email.split("@")[1]
        if email_domain in cls.IMAP_MAPPING:
            return cls.IMAP_MAPPING[email_domain]
        return f"imap.{email_domain}"

    def __init__(self, email: str, password: str, wait_email_code: int):
        self.logged_in = False
        self.email = email
        self.password = password
        self.wait_email_code = wait_email_code
        self.domain = self._get_imap_domain(email)
        self.imap = imaplib.IMAP4_SSL(self.domain)

    async def login(self):
        for i in range(3):
            try:
                status, dat = self.imap.login(self.email, self.password)
                if status != "OK" or self.imap.state != "AUTH":
                    raise imaplib.IMAP4.error(f"Error logging into {self.email} on {self.domain}: {status}/{self.imap.state}")
                self.logged_in = True
                break
            except imaplib.IMAP4.error as e:
                self.logged_in = False
                print(f"Error logging into {self.email} on {self.domain} (attempt {i+1}/3): {e}")
                if i == 2:
                    raise EmailLoginError() from e

    async def _wait_email_code(self, count: int, min_t: datetime | None) -> str | None:
        for i in range(count, 0, -1):
            _, rep = self.imap.fetch(str(i), "(RFC822)")
            for x in rep:
                if isinstance(x, tuple):
                    msg = emaillib.message_from_bytes(x[1])
                    msg_time = msg.get("Date", "").split("(")[0].strip()
                    msg_time = datetime.strptime(msg_time, "%a, %d %b %Y %H:%M:%S %z")
                    msg_from = str(msg.get("From", "")).lower()
                    msg_subj = str(msg.get("Subject", "")).lower()
                    print(f"({i} of {count}) {msg_from} - {msg_time} - {msg_subj}")
                    if "info@x.com" in msg_from and "confirmation code is" in msg_subj:
                        return msg_subj.split(" ")[-1].strip(), msg_time
                    elif "verify@x.com" in msg_from and "confirm_your_email" in msg_subj:
                        text = "".join([part.get_payload(decode=True).decode() for part in msg.walk() if
                                        part.get_content_type() == "text/plain"])
                        lines = text.splitlines()
                        lines = [line.strip() for line in lines if line.strip()]  # Remove empty lines and whitespace
                        for line in lines:
                            if line.isdigit() and len(line) == 6:  # Checks for a 6-digit numeric code
                                return line, msg_time
        return None

    async def get_email_code(self) -> tuple[str, datetime] | str:
        try:
            if not self.logged_in:
                try:
                    await self.login()
                except EmailLoginError as e:
                    print(f"Failed to log in: {e}")
                    return None, None
            start_time = time.time()
            while True:
                status, messages = self.imap.select("INBOX", readonly=True)
                if status != "OK":
                    raise imaplib.IMAP4.error(f"Error selecting inbox: {messages}")
                msg_count = int(messages[0].decode("utf-8")) if messages and messages[0] else 0
                code, msg_time = await self._wait_email_code(msg_count, datetime.now(timezone.utc) - timedelta(seconds=30))
                if code:
                    return code, msg_time
                if self.wait_email_code < time.time() - start_time:
                    raise EmailCodeTimeoutError(f"Email code timeout ({self.wait_email_code} sec)")
                await asyncio.sleep(5)
        except Exception as e:
            raise e
