from pydantic import BaseModel


class ScrapeRequest(BaseModel):

    url: str


class UpdateRecordRequest(BaseModel):

    title: str

    headings: list[str]

    paragraphs: list[str]