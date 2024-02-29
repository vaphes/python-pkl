class EvalError(Exception):
    def __init__(self, error_output: str):
        self.error_output = error_output

    def __str__(self):
        return self.error_output


class InternalError(Exception):
    def __init__(self, error: Exception):
        self.error = error

    def __str__(self):
        return f"an internal error ocurred: {self.error}"
