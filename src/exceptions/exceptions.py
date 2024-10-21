class BaseAppException(Exception):
    """Base exception for all custom exceptions in the application."""

    def __init__(self, message: str, status_code: int = 400, **kwargs):
        formatted_message = message.format(**kwargs)
        super().__init__(formatted_message)
        self.message = formatted_message
        self.status_code = status_code


class CategoryNotFoundError(BaseAppException):
    """Exception raised when a requested category is not found."""

    def __init__(self, category_id: int = None, name: str = None):
        if category_id is not None:
            message = f"Category with ID {category_id} not found."
        elif name is not None:
            message = f"Category with name '{name}' not found."
        else:
            message = "Category not found."
        super().__init__(message, status_code=404)
