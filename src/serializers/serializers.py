from src.infrastructure.db.models.models import Product, Sale
from src.schemes.product_schemes import ProductResponse
from src.schemes.sale_schemes import SaleResponse


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


def serialize_sale_response(sale: Sale, product: Product) -> SaleResponse:
    """
    Serializes a Sale model instance into a SaleResponse schema, including product details.

    :param sale: The Sale instance to be serialized.
    :param product: The Product instance associated with the sale.
    :return: A SaleResponse schema containing sale and product details.
    """
    return SaleResponse(
        id=sale.id,
        product_id=product.id,
        product_name=product.name,
        category_id=product.category.id,
        category_name=product.category.name,
        product_price=product.final_price,
        discount_name=product.discount.name if product.discount else None,
        quantity=sale.quantity,
        sold_at=sale.sold_at,
    )
