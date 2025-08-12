from pydantic import BaseModel, conint

class PaginationParams(BaseModel):
    limit: conint(ge=1, le=100) = 10   # Limit between 1 and 100, default 10
    offset: conint(ge=0) = 0            # Offset >= 0, default 0

    model_config = {
        "from_attributes": True
    }
