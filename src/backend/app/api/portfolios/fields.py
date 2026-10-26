from decimal import Decimal
from typing import Annotated

from pydantic import BeforeValidator, Field, StringConstraints


def blank_to_none(value):
    # Field opsional yang dikirim kosong ("" atau spasi) disimpan sebagai NULL.
    if isinstance(value, str):
        value = value.strip()
        return value or None
    return value


def text(max_length: int):
    return Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=max_length)]


def optional_text(max_length: int):
    return Annotated[
        Annotated[str, StringConstraints(max_length=max_length)] | None,
        BeforeValidator(blank_to_none),
    ]


CustomerName = text(200)
ProjectName = text(250)
ProjectCode = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=100,
        pattern=r"^[A-Za-z0-9][A-Za-z0-9_\-./]*$",
    ),
]
PartnerRole = text(60)

# Angka rupiah: maksimal 16 digit di depan koma dan 2 desimal (kolom Numeric(18, 2)), tidak boleh negatif.
Money = Annotated[Decimal, Field(ge=0, max_digits=18, decimal_places=2)]
ProjectYear = Annotated[int, Field(ge=1990, le=2100)]
