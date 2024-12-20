from __future__ import annotations
from time import sleep
from .base import CaptchaSolver
from enum import Enum
import httpx
import json

class Service(Enum):
    Capsolver = "api.capsolver.com"
    CapMonster = "api.capmonster.cloud"
    AntiCaptcha = "api.anti-captcha.com"
    TwoCaptcha = "api.2captcha.com"


class Capsolver(CaptchaSolver):
    """
    You can automatically unlock the account by passing the `captcha_solver`
    argument when initialising the :class:`.Client`.

    .. code-block:: python

        from twikit.twikit_async import Capsolver, Client
        solver = Capsolver(
            api_key='your_api_key',
            max_attempts=10
        )
        client = Client(captcha_solver=solver)

    Parameters
    ----------
    api_key : :class:`str`
        Capsolver API key.
    service : :class:`Service` default=Service.Capsolver
        Service used for solve captcha
    max_attempts : :class:`int`, default=3
        The maximum number of attempts to solve the captcha.
    get_result_interval : :class:`float`, default=1.0

    use_blob_data : :class:`bool`, default=False
    """

    def __init__(
        self,
        api_key: str,
        service: Service = Service.Capsolver,
        max_attempts: int = 3,
        get_result_interval: float = 2.0,
        use_blob_data: bool = True
    ) -> None:
        self.api_key = api_key
        self.api_url = service.value
        self.get_result_interval = get_result_interval
        self.max_attempts = max_attempts
        self.use_blob_data = use_blob_data

    def create_task(self, task_data: dict) -> dict:
        data = {
            'clientKey': self.api_key,
            'task': task_data
        }
        response = httpx.post(
            f"https://{self.api_url}/createTask",
            json=data,
            headers={'content-type': 'application/json'}
        ).json()
        return response

    def get_task_result(self, task_id: str) -> dict:
        data = {
            'clientKey': self.api_key,
            'taskId': task_id
        }
        response = httpx.post(
            f"https://{self.api_url}/getTaskResult",
            json=data,
            headers={'content-type': 'application/json'}
        ).json()
        return response

    def solve_funcaptcha(self, blob: str) -> dict:
        task_data = {
            'websiteURL': 'https://iframe.arkoselabs.com',
            'websitePublicKey': self.CAPTCHA_SITE_KEY,
            'funcaptchaApiJSSubdomain': 'https://client-api.arkoselabs.com',
        }
        if self.client.proxy is None:
            task_data['type'] = 'FunCaptchaTaskProxyless'
        else:
            task_data['type'] = 'FunCaptchaTask'
            task_data['proxy'] = self.client.proxy

        if self.use_blob_data:
            task_data['data'] = json.dumps({"blob": blob})
        
        task_data['userAgent'] = self.client._user_agent
        print(f"Creating task with use_blob_data: {self.use_blob_data} 'data': {task_data.get('data')}")
        task = self.create_task(task_data)
        print(f"Task created with taskId: {task.get('taskId')} returned errorId: {task.get('errorId')}")
        while True:
            sleep(self.get_result_interval)
            result = self.get_task_result(task['taskId'])
            if 'errorCode' in result:
                print(f"Error code: {result['errorCode']} {result.get('errorDescription')}")
                return None
            if result.get('status') in ('ready', 'failed'):
                return result
