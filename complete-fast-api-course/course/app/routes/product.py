import time
from typing import List, Optional

from fastapi import APIRouter, Cookie, Form, Header, Response, status
from fastapi.responses import HTMLResponse
from starlette.responses import PlainTextResponse

from app.custom_log import log

router = APIRouter(prefix="/product", tags=["product"])

products = ["watch", "camera", "phone"]


async def time_consuming_functionality():
    time.sleep(5)
    return "ok"


@router.post("/new")
def create_product(name: str = Form(...)):
    products.append(name)
    return products


@router.get("/all")
async def get_all_products():
    log("[API]", "Call to get all products")
    await time_consuming_functionality()
    data = " ".join(products)
    response = Response(content=data, media_type="text/plain")
    response.set_cookie(key="test_cookie", value="test_cookie_value")
    return response


@router.get("/withheader")
def get_products(
    response: Response,
    custom_header: Optional[str] = Header(None),
    test_cookie: Optional[str] = Cookie(None),
):
    if custom_header:
        response.headers["custom-response-header"] = ", ".join(custom_header)

    return {"data": products, "custom_header": custom_header, "my_cookie": test_cookie}


@router.get(
    "/{id}",
    responses={
        200: {
            "content": {"text/html": {"<div>Product</div>"}},
            "description": "Returns the HTML for an object",
        },
        404: {
            "content": {
                "text/plain": {"Product not available"},
                "description": {"A cleartext error message"},
            }
        },
    },
)
def get_product(id: int):
    if id > len(products):
        out = "Product not available"
        return PlainTextResponse(
            status_code=status.HTTP_404_NOT_FOUND, content=out, media_type="plain/text"
        )
    product = products[id]
    output = """
    <head>
      <style>
        .product {
          width: 500px;
          height: 30px;
          border: 2px inset green;
          background-color: lightblue;
          text-align: center;
        }
      </style>
    </head>
    <div class="product">{product}</div>
    """
    return HTMLResponse(content=output, media_type="text/html")
