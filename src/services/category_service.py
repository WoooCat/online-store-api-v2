from src.exceptions.exceptions import CategoryNotFoundError
from src.infrastructure.db.models.models import Category
from src.repositories.abstract.abstract_category_repository import AbstractCategoryRepository


class CategoryService:
    """Service for handling business logic related to Categories."""

    def __init__(self, category_repo: AbstractCategoryRepository):
        """Initialize the service with a repository instance."""
        self.category_repo = category_repo

    async def get_all_categories(self):
        """Retrieve all categories from the repository."""
        return await self.category_repo.get_all_categories()

    async def add_category(self, category_data: dict) -> Category:
        """Add a new category. If a parent_id is provided, ensure the parent exists."""
        parent_id = category_data.get("parent_id")
        if parent_id is not None:
            await self.get_category_by_id(parent_id)

        new_category = Category(**category_data)
        return await self.category_repo.add_category(new_category)

    async def get_category_by_id(self, category_id: int) -> Category:
        """Retrieve a category by its ID. Raise an error if not found."""
        category = await self.category_repo.get_category_by_id(category_id)
        if not category:
            raise CategoryNotFoundError(category_id=category_id)
        return category

    async def get_category_by_name(self, name: str) -> Category:
        """Retrieve a category by its name. Raise an error if not found."""
        category = await self.category_repo.get_category_by_name(name)
        if not category:
            raise CategoryNotFoundError(name=name)
        return category

    async def update_category_by_id(
        self, category_id: int, updated_data: dict
    ) -> Category:
        """Update a category by its ID. Raise an error if not found."""
        category = await self.category_repo.update_category_by_id(
            category_id, updated_data
        )
        if not category:
            raise CategoryNotFoundError(category_id=category_id)
        return category

    async def delete_category(self, category_id: int) -> None:
        """Delete a category by its ID. Raise an error if not found."""
        success = await self.category_repo.delete_category_by_id(category_id)
        if not success:
            raise CategoryNotFoundError(category_id=category_id)
