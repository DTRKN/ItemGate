from typing import Dict, Any


def map_api_data_to_item(api_data: dict) -> dict:
    """Маппинг данных из Sima-Land API в структуру Item"""
    return {
        "id_item": str(api_data.get("id", "")),
        "uid": str(api_data.get("uid", "")),
        "sid": str(api_data.get("sid", "")),
        "balance": (
            int(api_data.get("balance", 0))
            if api_data.get("balance") not in [None, ""]
            else 0
        ),
        "name": api_data.get("name", ""),
        "slug": api_data.get("slug", ""),
        "stuff": api_data.get("stuff"),
        "category_id": str(api_data.get("category_id", "")),
        "photoUrl": api_data.get("photoUrl"),
        "image_title": api_data.get("image_title"),
        "price": float(api_data.get("price", 0.0)),
    }