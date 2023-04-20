from pydantic import BaseModel


class ReferendaAccount(BaseModel):
    address: str | None
    display: str | None
    identity: bool | None


class ReferendaItem(BaseModel):
    referendum_index: int
    created_block: int
    created_block_timestamp: int
    origins_id: int
    origins: str
    account: ReferendaAccount
    call_module: str
    call_name: str
    status: str
    latest_block_num: int
    latest_block_timestamp: int


class ReferendaV1Item(BaseModel):
    referendum_index: int
    status: str


class ReferendaAddress(BaseModel):
    address: str


class ReferendaVoter(BaseModel):
    account: ReferendaAddress
    amount: int
    status: str
    extrinsic_index: str
    conviction: str
    voting_time: int


class ReferendaV1Voter(BaseModel):
    account: ReferendaAddress
    amount: int
    passed: str
    extrinsic_hash: str
    extrinsic_index: str
    conviction: str
    voting_time: int


class ReferendaData(BaseModel):
    count: int | None
    list: list[ReferendaItem] | list[ReferendaVoter] | list[ReferendaV1Item] | list[ReferendaV1Voter] | None
    account: ReferendaAccount | None


class ReferendaResponse(BaseModel):
    code: int
    data: ReferendaData
    generated_at: int
    message: str
