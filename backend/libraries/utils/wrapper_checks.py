"""Provides wrapper check functions"""


from utils.exc import WrappedFunctionMissingKeyword

def check_for_keyword_in_kwargs(kwargs: dict, keyword: str, func_name: str) -> None:
    if not keyword in kwargs.keys():
        raise WrappedFunctionMissingKeyword(f'Keyword "{keyword}" is missing in kwargs of {func_name}')
