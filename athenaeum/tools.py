import re
import time
import tqdm
import ujson
import inspect
import sqlparse
from htmlmin import minify
from typing import Dict, Any, List, Protocol
from athenaeum.execute.js import execute_js_code_by_py_mini_racer


def jsonp_to_json(jsonp: str) -> Dict[str, Any]:
    func_name = re.match(r'(?P<func_name>jQuery.*?)\(\{.*\}\)\S*', jsonp).groupdict()['func_name']
    js_code = f'''function {func_name}(o){{return o}};function sdk(){{return JSON.stringify({jsonp})}};'''
    json_str = execute_js_code_by_py_mini_racer(js_code, func_name='sdk')
    json_obj = ujson.loads(json_str)
    return json_obj


def chunk_data(data: List[Any], chunk_size: int) -> List[List[Any]]:
    return [data[i: i + chunk_size] for i in range(0, len(data), chunk_size)]


def compressed_html(html: str, **kwargs: Any) -> str:
    return minify(html, **kwargs)


def format_sql(sql: str, **kwargs) -> str:
    kw = dict(reindent=True,
              keyword_case='upper',
              identifier_case='lower',
              strip_comments=True)
    kw.update(kwargs)
    sql = sqlparse.format(sql, **kw)
    return sql


class Container(Protocol):
    def __init__(self, database, key):
        self.database = database
        self.key = key

    def __len__(self) -> int:
        pass


def show_progress(container: Container, frequency: float = 1.0) -> None:
    total_num = len(container)
    desc = f'database：{container.database}，key：{container.key} 消费速度'
    unit = '条'

    bar = tqdm.tqdm(desc=desc, total=total_num, leave=True, unit=unit)

    sum_num = 0
    while True:
        now_num = len(container)
        pass_num = total_num - now_num
        update_num = pass_num - sum_num
        sum_num += update_num

        bar.update(update_num)

        if sum_num == total_num:
            break

        time.sleep(frequency)


def get_routine_name() -> str:
    return inspect.stack()[1][3]
