from typing import AsyncIterator

from fastapi import HTTPException

from app.db import AsyncSession
from app.models import Note, NoteSchema


class CreateNote:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def execute(self, title: str, content: str) -> NoteSchema:
        async with self.async_session.begin() as session:
            note = await Note.create(session, title, content)
            return NoteSchema.model_validate(note)


class ReadAllNote:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def execute(self) -> AsyncIterator[NoteSchema]:
        async with self.async_session() as session:
            async for note in Note.read_all(session):
                yield NoteSchema.model_validate(note)


class ReadNote:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def execute(self, note_id: int) -> NoteSchema:
        async with self.async_session() as session:
            note = await Note.read_by_id(session, note_id)
            if not note:
                raise HTTPException(status_code=404)
            return NoteSchema.model_validate(note)


class UpdateNote:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def execute(self, note_id: int, title: str, content: str) -> NoteSchema:
        async with self.async_session.begin() as session:
            note = await Note.read_by_id(session, note_id)
            if not note:
                raise HTTPException(status_code=404)

            await note.update(session, title, content)
            await session.refresh(note)
            return NoteSchema.model_validate(note)


class DeleteNote:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def execute(self, note_id: int) -> None:
        async with self.async_session.begin() as session:
            note = await Note.read_by_id(session, note_id)
            if not note:
                return
            await Note.delete(session, note)
