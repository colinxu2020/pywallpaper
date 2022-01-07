"""
Logging support.

Used Application:
    SVG Generator
    PyWallpaper(https://github.com/colinxu2020/pywallpaper)
Author:
    Colinxu2020
Version:2021.8.30
Last Update: 2021.8.31 10:25(UTC+8)
FilePath: /log3py.py
Version Change:
    2021.8.30: Add this docs string.
    2021.8.26: Create this file.
Classes:
    Level: Creates a level object
    LevelEnum: Enumeration of common log levels(DEBUG, INFO, WARNING, ERROR)
    MuitIWriterWriter: Creates a Writer that can automatically call multiple Writers, and provides a generic wrapper
    Logger: Creates a logger.
    MuitiWriterLogger: Create a logger with different writers for different levels (deprecation warning (2021.8.26), will be removed in a future release)
"""

import enum
import functools
import sys
import time
import typing
from inspect import stack as call_stack

writer = typing.Union[typing.Callable[[str], None], type]


def StdoutWriter(text):
    return sys.stdout.write(text + "\n")


def StderrWriter(text):
    return sys.stderr.write(text + "\n")


def _get_filename():
    for frameinfo in call_stack():
        filename = frameinfo.filename
        if not filename.endswith("log3py.py"):
            return filename


class DefaultDict(dict):
    def __init__(self, *arg, defaults: dict, **kwarg):
        dict.__init__(self, *arg, **kwarg)
        self.defaults = defaults

    def __missing__(self, key):
        return self.defaults[key]


class Level(object):
    def __init__(self: "Level", level: int, string: str) -> None:
        self.level: int = level
        self.str: str = string

    def __gt__(self: "Level", other: object) -> bool:
        if not isinstance(other, Level):
            return NotImplemented
        return self.level > other.level

    def __eq__(self: "Level", other: object) -> bool:
        if not isinstance(other, Level):
            return NotImplemented
        return self.level == other.level

    def __str__(self: "Level") -> str:
        return self.str

    def __repr__(self: "Level") -> str:
        return 'log3py.Level({level}, "{string}")'.format(
            level=self.level, string=str(self)
        )

    def __hash__(self):
        return hash((self.level, self.str))


class Critical(BaseException):
    pass


def WarningWriter(self, text):
    error_writer = (
        self.error_writer
    )  # This function was only being called in Logger class, this class can keep the argument OK  # noqa:E117,E501
    error_writer.write(_get_filename())
    error_writer.write(" WARNING:\n")
    error_writer.write(text)


class LevelEnum(enum.Enum):
    DEBUG: Level = Level(10, "DEBUG")
    INFO: Level = Level(20, "INFO")
    WARNING: Level = Level(30, "WRANING")
    ERROR: Level = Level(40, "ERROR")
    ANY: Level = Level(0, "ANY")
    CRITICAL: Level = Level(50, "CRITICAL")


globals().update({key: value.value for key, value in LevelEnum.__members__.items()})


class MuitiWriterWriter:
    def __init__(self, *writer: writer):
        self.writer = []
        for w in writer:
            self.add(w)

    def write(self, text: str) -> None:
        for w in self.writer:
            w(text)

    def __iter__(self):
        return iter(self.writer)

    def add(self, writer: writer):
        self.writer.append(writer if callable(writer) else writer.write)


class Logger(object):
    def __init__(
        self: "Logger",
        name: str = None,
        level: Level = INFO,  # noqa: F821 # Some const was create on runtime
        writer: writer = StdoutWriter,
        format: str = "{level} : {name} : {time} : {text}",
        error_writer: writer = StderrWriter,
        warning_writer: writer = WarningWriter,
        critical_format: str = "{time} : {text}",
        enable: bool = True,
    ) -> None:
        if not isinstance(writer, MuitiWriterWriter):
            writer = MuitiWriterWriter(writer)
        if not isinstance(error_writer, MuitiWriterWriter):
            error_writer = MuitiWriterWriter(error_writer)
        if warning_writer is WarningWriter:
            warning_writer = functools.partial(warning_writer, self)
        if not isinstance(warning_writer, MuitiWriterWriter):
            warning_writer = MuitiWriterWriter(warning_writer)
        if isinstance(level, str):
            level = globals()[level]

        self.name: str = name
        self.level: Level = level
        self.writer: writer = writer
        self.format: str = format
        self.warning_writer = warning_writer
        self.error_writer = error_writer
        self.enable = enable
        self.critical_format = critical_format

    def debug(self, text: str) -> None:
        self.log(DEBUG, text)  # noqa: F821 # Some const was create on runtime

    def info(self, text: str) -> None:
        self.log(INFO, text)  # noqa: F821 # Some const was create on runtime

    def warning(self, text: str) -> None:
        self.log(
            WARNING, text, writer=self.warning_writer
        )  # noqa: F821 # Some const was create on runtime

    def error(self, text: str) -> None:
        self.log(
            ERROR, text, self.error_writer
        )  # noqa: F821 # Some const was create on runtime

    @staticmethod
    def _throw_critical_exc(text):
        raise Critical(text)

    def critical(self, text: str) -> typing.NoReturn:
        if self.enable:
            self.log(
                CRITICAL,  # noqa: F821 # Some const was create on runtime
                text,
                MuitiWriterWriter(self._throw_critical_exc),
            )

    def _format_log(
        self: "Logger",
        level: typing.Union[Level, str],
        text: str,
        format: typing.Optional[str] = None,
    ) -> str:
        if format is None:
            format = self.format
        filename = _get_filename()
        return format.format(
            level=str(level), name=self.name or filename, text=text, time=time.asctime()
        )

    def log(
        self,
        level: Level,
        text: str,
        writer: typing.Optional[MuitiWriterWriter] = None,
        format: str = None,
    ) -> None:
        if writer is None:
            writer = self.writer
        if level < self.level or not self.enable:
            return
        writer.write(self._format_log(level, text, format=format))


class MuitiWriterLogger(Logger):
    def __init__(
        self: "Logger",
        name: str = "main",
        level: Level = INFO,  # type:ignore  # noqa: F821 # Some const was create on runtime
        writer: writer = StdoutWriter,
        format: str = "{level} : {name} : {time} : {text}",
        error_writer: writer = StderrWriter,
        warning_writer: writer = WarningWriter,
        writers: dict[Level, MuitiWriterWriter] = None,
        enable: bool = True,
    ) -> None:
        if writers is None:
            writers = {}
        Logger.__init__(
            self, name, level, writer, format, error_writer, warning_writer, enable
        )
        for key, writer in writers.values():
            if not isinstance(writer, MuitiWriterWriter):
                writers[key] = MuitiWriterLogger(writer)

        # if level not in writers:
        #     writers[level] = MuitiWriterWriter()
        # writers[level].add(self.writer)
        self.writers = writers

    def log(
        self, level: Level, text: str, writer: typing.Optional[writer] = None
    ) -> None:

        for writers_level, writers in self.writers.items():
            if level < writers_level:
                continue
            writers.write(self._format_log(level, text))
        # if writer is not None:
        # writer.write(self._format_log(level, text))
        Logger.log(self, level, text, writer)
