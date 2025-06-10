from abc import (
    ABC,
    abstractmethod,
)
import re
from datetime import datetime
import socket
import sys
from typing import List


# region filters
class ILogFilter(ABC):
    @abstractmethod
    def match(self, text: str) -> bool:
        pass


class SimpleLogFilter(ILogFilter):
    def __init__(self, pattern: str, ignore_case: bool = True):
        self.pattern = pattern.lower() if ignore_case else pattern
        self.ignore_case = ignore_case

    def match(self, text: int) -> bool:
        text_to_check = text.lower() if self.ignore_case else text
        return self.pattern in text_to_check


class ReLogFilter(ILogFilter):
    def __init__(self, regex_pattern: str, flags: int = re.IGNORECASE):
        self.pattern = re.compile(regex_pattern, flags)

    def match(self, text: str) -> bool:
        return bool(self.pattern.search(text))


# endregion


# region handlers (обработчики)
class ILogHandler(ABC):
    @abstractmethod
    def handle(self, text: str) -> None:
        pass


class FileHandler(ILogHandler):
    def __init__(self, filename: str):
        self.filename = filename

    # ИСПРАВЛЕНО
    def handle(self, text: str) -> None:
        try:
            with open(self.filename, "a", encoding="utf-8") as f:
                f.write(f"[{datetime.now()}] {text}\n")
        except (IOError, OSError) as e:
            print(f"Failed to write to log file: {e}")



class SocketHandler(ILogHandler):
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def handle(self, text: str) -> None:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.host, self.port))
                s.sendall(f"[{datetime.now()}] {text}\n".encode("utf-8"))
        except socket.error as e:
            print(f"SocketHandler error: {e}")


class ConsoleHandler(ILogHandler):
    def handle(self, text: str) -> None:
        print(f"[{datetime.now()}] {text}")


class SyslogHandler(ILogHandler):
    def __init__(self, facility: str = "user"):
        self.facility = facility

    def handle(self, text: str) -> None:
        try:
            sys.stderr.write(f"[{datetime.now()}] {text}\n")
        except Exception as e:
            print(f"SyslogHandler error: {e}")


# endregion


class Logger:
    def __init__(
        self, filters: List[ILogFilter] = None, handlers: List[ILogHandler] = None
    ):
        self.filters = filters or []
        self.handlers = handlers or []

    def log(self, text: str) -> None:
        for log_filter in self.filters:
            if not log_filter.match(text):
                return

        for handler in self.handlers:
            handler.handle(text)


if __name__ == "__main__":
    error_filter = SimpleLogFilter("error")
    warn_filter = ReLogFilter(r"warn(ing)?|alert", flags=re.IGNORECASE)

    handlers = [FileHandler("app.log"), ConsoleHandler(), SyslogHandler()]

    logger = Logger(filters=[error_filter, warn_filter], handlers=handlers)

    test_messages = [
        "System started",
        "Warning: Disk space low",
        "User login successful",
        "ERROR: File not found",
        "ALERT: System overheating",
    ]

    print("Демонстрация системы логирования:")
    for msg in test_messages:
        print(f"\nОтправка сообщения: '{msg}'")
        logger.log(msg)
