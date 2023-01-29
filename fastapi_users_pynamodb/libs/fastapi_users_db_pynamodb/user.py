import uuid
from typing import TYPE_CHECKING, Generic, TypeVar

from app.models.base_model import BaseModel
from fastapi_users.models import ID
from pynamodb.attributes import BooleanAttribute, UnicodeAttribute
from pynamodb.indexes import AllProjection, GlobalSecondaryIndex

UUID_ID = uuid.UUID


class PynamoDbBaseUserEmailIndex(
    GlobalSecondaryIndex["PynamoDbBaseUserTable[UUID_ID]"],
):
    """GlobalSecondaryIndex for email."""

    class Meta:
        index_name = "user-email-index"
        read_capacity_units = 2
        write_capacity_units = 1
        projection = AllProjection()
    email = UnicodeAttribute(hash_key=True)


class PynamoDbBaseUserTable(Generic[ID], BaseModel):
    """Base PynamoDb users table definition."""

    class Meta:
        table_name = "user-table"

    if TYPE_CHECKING:  # pragma: no cover
        id: UnicodeAttribute
        email: str
        email_index: GlobalSecondaryIndex["PynamoDbBaseUserTable[UUID_ID]"]
        hashed_password: str
        is_active: bool
        is_superuser: bool
        is_verified: bool
    else:
        id = UnicodeAttribute(hash_key=True)
        email = UnicodeAttribute(null=False, range_key=True)
        email_index = PynamoDbBaseUserEmailIndex()
        hashed_password = UnicodeAttribute(null=False)
        is_active = BooleanAttribute(null=False, default=True)
        is_superuser = BooleanAttribute(null=False, default=False)
        is_verified = BooleanAttribute(null=False, default=False)


class PynamoDbBaseUserTableUUID(PynamoDbBaseUserTable[UUID_ID]):
    """PynamoDbBaseUserTableUUID."""

    if TYPE_CHECKING:  # pragma: no cover
        id: UnicodeAttribute
    else:
        id: UUID_ID = UnicodeAttribute(hash_key=True)


UP_PYNAMODB = TypeVar("UP_PYNAMODB", bound=PynamoDbBaseUserTableUUID)
