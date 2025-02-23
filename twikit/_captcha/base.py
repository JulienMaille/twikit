from __future__ import annotations

import re
from typing import TYPE_CHECKING, NamedTuple

from bs4 import BeautifulSoup
from httpx import Response

if TYPE_CHECKING:
    from ..client.client import Client


class UnlockHTML(NamedTuple):
    authenticity_token: str
    assignment_token: str
    needs_unlock: bool
    start_button: bool
    finish_button: bool
    delete_button: bool
    send_email_button: bool
    verify_email_button: bool
    blob: str


class CaptchaSolver:
    client: Client
    max_attempts: int

    CAPTCHA_URL = 'https://x.com/account/access'
    CAPTCHA_SITE_KEY = '0152B4EB-D2DC-460A-89A1-629838B529C9'

    async def get_unlock_html(self) -> tuple[Response, UnlockHTML]:
        headers = {
            'X-Twitter-Client-Language': self.client.language,
            'User-Agent': self.client._user_agent,
            'Upgrade-Insecure-Requests': '1'
        }
        _, response = await self.client.get(
            self.CAPTCHA_URL, headers=headers
        )
        return response, parse_unlock_html(response.text)


    async def confirm_unlock(
        self,
        authenticity_token: str,
        assignment_token: str,
        verification_string: str = None,
        ui_metrics: bool = False,
        email_token: str = None
    ) -> tuple[Response, UnlockHTML]:
        data = {
            'authenticity_token': authenticity_token,
            'assignment_token': assignment_token,
            'lang': self.client.language.split('-')[0],
            'flow': '',
        }
        params = {}
        if verification_string:
            data['verification_string'] = verification_string
            data['language_code'] = self.client.language.split('-')[0]
            params['lang'] = self.client.language.split('-')[0]
        if email_token:
            data['token'] = email_token
        if ui_metrics:
            data['ui_metrics'] = await self.client._ui_metrics()
        headers = {
            'User-Agent': self.client._user_agent,
            'Content-Type': 'application/x-www-form-urlencoded',
            'Upgrade-Insecure-Requests': '1',
            'Referer': self.CAPTCHA_URL
        }
        _, response = await self.client.post(
            self.CAPTCHA_URL, params=params, data=data, headers=headers
        )
        return response, parse_unlock_html(response.text)


def parse_unlock_html(html: str) -> UnlockHTML:
    soup = BeautifulSoup(html, 'lxml')

    authenticity_token = None
    authenticity_token_element = soup.find(
        'input', {'name': 'authenticity_token'}
    )
    if authenticity_token_element is not None:
        authenticity_token: str = authenticity_token_element.get('value')

    assignment_token = None
    assignment_token_element = soup.find('input', {'name': 'assignment_token'})
    if assignment_token_element is not None:
        assignment_token = assignment_token_element.get('value')

    verification_string = soup.find('input', id='verification_string')
    needs_unlock = bool(verification_string)

    gui_lang = soup.find('input', {'name': 'lang'}).attrs['value']
    if gui_lang == 'en':
        start_button = bool(soup.find('input', value='Start'))
        finish_button = bool(soup.find('input', value='Continue to X'))
        delete_button = bool(soup.find('input', value='Delete'))
        send_email_button = bool(soup.find('input', value='Send email'))
        verify_email_button = bool(soup.find('input', value='Verify'))
    elif gui_lang == 'fr':
        start_button = bool(soup.find('input', value='Commencer'))
        finish_button = bool(soup.find('input', value='Continuer sur X'))
        delete_button = bool(soup.find('input', value='Supprimer'))
        send_email_button = bool(soup.find('input', value='Envoyer un email'))
        verify_email_button = bool(soup.find('input', value='Vérifier'))

    iframe = soup.find(id='arkose_iframe')
    blob = re.findall(r'data=(.+)', iframe['src'])[0] if iframe else None

    return UnlockHTML(
        authenticity_token,
        assignment_token,
        needs_unlock,
        start_button,
        finish_button,
        delete_button,
        send_email_button,
        verify_email_button,
        blob
    )
