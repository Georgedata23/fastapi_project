import os
from datetime import datetime
from typing import Dict, Sequence

from fastapi import UploadFile, HTTPException, status
from pydantic import PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, insert, select
import shutil

from app.logging_dir.logging_file import logger
from app.models import Documents, Documents_text
from app.tasks.tasks import img_to_text


class DocumentsDAO:

    @classmethod
    async def upload(cls, id_doc: int, file_uploaded:UploadFile, session: AsyncSession) -> dict:

        if os.path.exists(f"app/doc_static/images/{id_doc}.webp"):
            logger.info("Использовали занятый id для загрузки!")
            return {"warning": "Данный id занят, попробуйте другой!"}

        session.add(Documents(id=id_doc,
                    path="app/doc_static/images",
                    date=datetime.now())
                    )
        try:
            await session.commit()
            logger.info("Запись добавили(upload)!")
        except Exception:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Ошибка во время добавления записи в БД, попробуйте позже!")

        with open(f"app/doc_static/images/{id_doc}.webp", "wb+") as file:
            shutil.copyfileobj(file_uploaded.file, file)
        logger.info("Изображение добавлено в БД!")
        return {"result": "Запись и изображение сохранены в БД и на диск!"}


    @classmethod
    async def delete(cls, id_doc: int, session: AsyncSession) -> dict:
        if not os.path.exists(f"app/doc_static/images/{id_doc}.webp"):
            logger.info("Не нашли изображение для удаления!")
            return {"warning": f"Изображение с id: {id_doc} не найдено!"}
        else:
            try:
                await session.execute(delete(Documents_text).filter(Documents_text.id_doc == id_doc))
                # await session.execute(delete(Documents).filter(Documents.id == id_doc))Удаляется через каскад (models.py)
                await session.commit()
                logger.info("Запись удалена(delete)!")

            except Exception:
                logger.warning("Почему-то данные не удалились(delete)!")
                raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Ошибка во время удаления записей в БД, попробуйте позже!")

        try:
            os.remove(f"app/doc_static/images/{id_doc}.webp")
        except FileNotFoundError:
            return {"Error": "Кто-то изменил/удалил файл во время выполнения запроса, записи стёрты!"}
            logger.warning("Запись удалена, изображение нет(delete)!")

        logger.info("Запись и изображение удалены!")
        return {"result": "Записи и файл были удалены!"}


class DocTextDAO:

    @classmethod
    async def analyse(cls, id_doc: PositiveInt, session: AsyncSession):

        try:
            text_from_img = img_to_text.delay(id_doc).get()
            logger.info("Изображение преобразовано в текст!")
        except FileNotFoundError:
            return {"warning": "Файл не найден!"}
            logger.info("Файл не найден(analyse)!")

        try:
            await session.execute(insert(Documents_text).values(id = id_doc,
                                   id_doc = id_doc,
                                   text=text_from_img))
            await session.commit()
            logger.info("Текст добавлен в БД!")
            return {"message": "Текст прочитан и добавлен в БД!"}

        except Exception:
            logger.warning("Текст переведен, но не добавлен в БД!")
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                                detail="Текст не был добавлен в БД!")

    @classmethod
    async def getter_text(cls, id_doc: PositiveInt, session: AsyncSession) -> dict:

        try:
            result = await session.execute(select(Documents_text.text).filter(Documents_text.id == id_doc))
            logger.info("Запрос на возврат текста прошел(getter_text)!")
        except Exception:
            logger.warning("Ошибка, запрос на получение текста не прошел!")
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                                detail="Ошибка сервера, текст не получен!")

        if result.fetchone() is None:
            return {"warning": "Текст с данным id не найден, используйте метод get_text для его создания!"}
        else:
            return {"text": result.scalars().first()}







