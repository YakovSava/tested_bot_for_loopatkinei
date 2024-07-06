from string import ascii_lowercase
from random import choice, randint
from yoomoney import Client, Quickpay

class Yoomoney:

    def __init__(self, data:dict={'token': '', 'account': ''}):
        self._token = data['token']
        self._account = data['account']
        self._client = Client(self._token)

        self._not_important_data = {
            "quickpay_form": "button",
            "targets": "Tested Bot",
            "paymentType": "AC"
        }

    def _get_label(self):
        return "".join("".join(choice(ascii_lowercase) for _ in range(randint(0, 5)))+str(randint(10, 99)) for _ in range(randint(5, 7)))

    def build_quickpay(self, sum:int):
        label = self._get_label()
        return [Quickpay(
            **self._not_important_data,
            receiver=self._account,
            label=label,
            sum=sum
        ).base_url, label]

    def check_pay(self, label:str):
        history = self._client.operation_history(label=label)
        for operation in history.operations:
            if operation.status == 'success':
                return True
        return False