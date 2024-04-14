from typing_extensions import Callable

class WrappedFunctionMissingKeyword(BaseException):
    """Raised when wrapped function is missing certain keyword"""

def check_for_keyword_in_kwargs(kwargs: dict, keyword: str, func_name: str) -> None:
    if not keyword in kwargs.keys():
        raise WrappedFunctionMissingKeyword(f'Keyword "{keyword}" is missing in kwargs of {func_name}')