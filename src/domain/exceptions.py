from enum import Enum

class PipelineErrorType(Enum):
    FATAL = "fatal"
    SKIP = "skip"
    WARNING = "warning"


class PipelineError(Exception):

    def __init__(self, message: str, step: str, image_path: str='', error_type: PipelineErrorType = PipelineErrorType.SKIP):
        super().__init__(message)
        self.message = message
        self.image_path = image_path
        self.step = step
        self.error_type = error_type

    def __str__(self):
        return f'{self.step}: {self.message}'
    
