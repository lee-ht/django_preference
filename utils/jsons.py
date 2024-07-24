import json
from typing import Union, Iterable

from django.core import serializers


# 쿼리 수행 후 db 모델 객체를 파이썬 객체로 변환
def obj_to_json(obj: Iterable) -> Union[dict, list]:
    try:
        if not isinstance(obj, Iterable):
            obj = [obj]
        serial = serializers.serialize('json', obj, ensure_ascii=False)
        return json.loads(serial)
    except Exception as e:
        print(e)
        return None
