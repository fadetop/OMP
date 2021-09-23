import json
import logging
from datetime import datetime, timedelta

import pytz
import requests

logger = logging.getLogger('server')


class Alertmanager:
    """
    定义alertmanager的参数及动作
    """

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.headers = {'Content-Type': 'application/json'}
        self.add_url = f'http://{self.ip}:{self.port}/api/v1/silences'
        self.delete_url = f'http://{self.ip}:{self.port}/api/v1/silence'

    @staticmethod
    def format_time(_time):
        """
        时区转换
        """
        if not _time:
            return (datetime.now(tz=pytz.UTC)).strftime(
                "%Y-%m-%dT%H:%M:%SZ")
        if isinstance(_time, datetime):
            return _time.astimezone(tz=pytz.UTC).strftime(
                "%Y-%m-%dT%H:%M:%SZ")
        return None

    def add_setting(self, value, name="env", start_time=None, ends_time=None):
        """
        设置维护模式
        :param value: 值 instance 对应ip， env对应env_name
        :param name: 值的key：instance, env
        :param start_time: startsAt：type: datetime
        :param ends_time: endsAt：type: datetime
        :return: 成功返回： "25b1ea3e-73db-43cd-ae81-a397f9e1bc88" (silenceId)
                失败：None
        """
        start_time_str = self.format_time(start_time)
        if not start_time_str:
            return None
        if not ends_time:
            ends_time = datetime.now() + timedelta(days=30)
        ends_time_str = self.format_time(ends_time)
        if not ends_time_str:
            return None
        data = {
            "matchers": [
                {"name": name, "value": value}
            ],
            "startsAt": start_time_str,
            "endsAt": ends_time_str,
            "createdBy": "api",
            "comment": "Silence",
            "status": {"state": "active"}
        }
        try:
            logger.info(data)
            resp = requests.post(
                self.add_url, data=json.dumps(data),
                headers=self.headers, timeout=5
            ).json()
            if resp.get("status") == "success":
                logger.info(resp)
                return resp.get("data").get("silenceId", None)
        except Exception as e:
            logger.error(str(e))
        return None

    def delete_setting(self, silence_id):
        """
        删除告警屏蔽规则
        :param silence_id: 规则id
        :return: 成功 True， 失败 False
        """
        try:
            resp = requests.delete(f"{self.delete_url}/{silence_id}", timeout=5).json()
        except Exception as e:
            logger.error(str(e))
            return False
        logger.info(resp)
        return resp.get("status") == "success"


if __name__ == '__main__':
    a = Alertmanager('10.0.3.66', '19013')
    # add_result = a.add_setting(value='10.0.3.80', name='instance', start_time=None, ends_time=None)
    # print(add_result)
    del_result = a.delete_setting('d6ecd79d-482d-4da7-a4aa-96888925cfb6')
    print(del_result)