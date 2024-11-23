import asyncio
import email as emaillib
import imaplib
import os
import time
from datetime import datetime, timezone, timedelta
import logging


logger = logging.getLogger(__name__)

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
        self.email = email
        self.password = password
        self.wait_email_code = wait_email_code
        self.domain = self._get_imap_domain(email)
        self.imap = imaplib.IMAP4_SSL(self.domain)
    async def login(self):
        try:
            self.imap.login(self.email, self.password)
            self.imap.select("INBOX", readonly=True)
            logger.info(f"Logged into {self.email} on {self.domain}")
        except imaplib.IMAP4.error as e:
            logger.error(f"Error logging into {self.email} on {self.domain}: {e}")
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
                    logger.info(f"({i} of {count}) {msg_from} - {msg_time} - {msg_subj}")
                    if "info@x.com" in msg_from and "confirmation code is" in msg_subj:
                        return msg_subj.split(" ")[-1].strip()
        return None
    async def get_email_code(self) -> str:
        try:
            logger.info(f"Waiting for confirmation code for {self.email}...")
            start_time = time.time()
            while True:
                _, rep = self.imap.select("INBOX")
                msg_count = int(rep[0].decode("utf-8")) if rep and rep[0] else 0
                code = await self._wait_email_code(msg_count, datetime.now(timezone.utc) - timedelta(seconds=30))
                if code:
                    return code
                if self.wait_email_code < time.time() - start_time:
                    raise EmailCodeTimeoutError(f"Email code timeout ({self.wait_email_code} sec)")
                await asyncio.sleep(5)
        except Exception as e:
            self.imap.select("INBOX")
            self.imap.close()
            raise e