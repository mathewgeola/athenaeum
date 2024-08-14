import psutil
from athenaeum.logger import logger
from typing import List


def kill_process_by_port(port: int) -> None:
    for proc in psutil.process_iter(['pid', 'name', 'connections']):
        for conn in proc.connections():
            if conn.laddr.port == port:
                if proc.pid != 0:
                    proc.kill()
                break


def find_process_pids_by_process_name(process_name: str) -> List[int]:
    process_pids: List[int] = []
    for proc in psutil.process_iter(['pid', 'name']):
        proc_info: Dict[str, Any] = proc.info  # type: ignore
        if not process_name.lower() in proc_info['name'].lower():
            continue
        try:
            proc_id = proc_info['pid']
            proc_name = proc_info['name']
            process_pids.append(proc_id)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as exception:
            logger.error(f'查找不到 process_name：{process_name}, exception: {exception}！')
        else:
            logger.success(f'查找到 process_pid：{proc_id}，proc_name：{proc_name}')

    logger.success(f'查找到 process_pids: {process_pids}')
    return process_pids


def kill_process_by_process_pid(process_pid: int) -> None:
    try:
        proc = psutil.Process(process_pid)
        proc.terminate()
        proc.wait(timeout=3)
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired) as exception:
        logger.error(f'无法杀死 process_pid：{process_pid}，exception：{exception}！')
    else:
        logger.success(f'已杀死 process_pid：{process_pid}')


def kill_process_by_process_name(process_name: str) -> None:
    process_pids = find_process_pids_by_process_name(process_name)
    for process_pid in process_pids:
        kill_process_by_process_pid(process_pid)
