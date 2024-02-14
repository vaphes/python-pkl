# package pkl

# import (
# 	"fmt"
# 	"io"
# 	"os"
# )

# // Logger is the interface for logging messages emitted by the Pkl evaluator.
# //
# // To set a logger, register it on EvaluatorOptions.Logger when building an Evaluator.
# type Logger interface {
# 	// Trace logs the given message on level TRACE.
# 	Trace(message string, frameUri string)

# 	// Warn logs the given message on level WARN.
# 	Warn(message string, frameUri string)
# }

# // NewLogger builds a logger that writes to the provided output stream,
# // using the default formatting.
# func NewLogger(out io.Writer) Logger {
# 	return &logger{out}
# }

# // FormatLogMessage returns the default formatter for log messages.
# func FormatLogMessage(level, message, frameUri string) string {
# 	return fmt.Sprintf("pkl: %s: %s (%s)\n", level, message, frameUri)
# }

# type logger struct {
# 	out io.Writer
# }

# func (s logger) Trace(message string, frameUri string) {
# 	_, _ = s.out.Write([]byte(FormatLogMessage("TRACE", message, frameUri)))
# }

# func (s logger) Warn(message string, frameUri string) {
# 	_, _ = s.out.Write([]byte(FormatLogMessage("WARN", message, frameUri)))
# }

# var _ Logger = (*logger)(nil)

# // StderrLogger is a logger that writes to standard error.
# //
# //goland:noinspection GoUnusedGlobalVariable
# var StderrLogger = NewLogger(os.Stdout)

# // NoopLogger is a logger that discards all messages.
# var NoopLogger = NewLogger(io.Discard)


import dataclasses
import sys
from typing import TextIO


@dataclasses.dataclass
class Logger:
    out: TextIO | None

    def trace(self, message: str, frame_uri: str):
        if self.out is None:
            return
        self.out.write(self.format_log_message("TRACE", message, frame_uri))

    def warn(self, message: str, frame_uri: str):
        if self.out is None:
            return
        self.out.write(self.format_log_message("WARN", message, frame_uri))

    def format_log_message(self, level: str, message: str, frame_uri: str):
        return f"pkl: {level}: {message} ({frame_uri})\n"


def new_logger(out: TextIO | None):
    return Logger(out)


def stderr_logger():
    return new_logger(sys.stderr)


def noop_logger():
    return new_logger(None)
