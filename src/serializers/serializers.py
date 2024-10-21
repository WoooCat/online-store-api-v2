from src.infrastructure.db.models.models import Product, Sale
from src.schemes.product_schemes import ProductResponse


def serialize_product_response(product: Product) -> ProductResponse:
    """
    Serializes a Product model instance into a ProductResponse schema.

    :return: A ProductResponse schema containing product details.
    """
    return ProductResponse(
        id=product.id,
        name=product.name,
        description=product.description,
        price=product.price,
        final_price=product.final_price,
        category_id=product.category.id,
        category_name=product.category.name,
        discount_id=product.discount_id,
        discount_name=product.discount.name if product.discount else None,
        stock=product.stock,
        reserved_quantity=product.reserved_quantity,
    )
