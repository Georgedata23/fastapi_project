import os
from datetime import datetime
from typing import Dict, Sequence

from fastapi import UploadFile, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, insert, select
import shutil

from app.logging_dir.logging_file import logger
from app.models import Documents, Documents_text
from app.tasks.tasks import img_to_text


class DocumentsDAO:


    @staticmethod
    def copyfile(id_doc: PositiveInt, file_uploaded: UploadFile):
        with open(f"app/doc_static/images/{id_doc}.webp", "wb+") as file:
            shutil.copyfileobj(file_uploaded.file, file)
        logger.info("Изображение добавлено в БД!")


    @staticmethod
    def check_available_file(id_doc: PositiveInt):
        if not os.path.exists(f"app/doc_static/images/{id_doc}.webp"):
            logger.info("Не нашли изображение для удаления!")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Изображение с id: {id_doc} не найдено!")

    @staticmethod
    def remove_and_exception(id_doc: PositiveInt):
        try:
            os.remove(f"app/doc_static/images/{id_doc}.webp")
        except FileNotFoundError:
            logger.warning("Запись удалена, изображение нет(delete)!")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Кто-то изменил/удалил файл во время выполнения запроса, записи стёрты!")




    @classmethod
    async def upload(cls, id_doc: PositiveInt, file_uploaded: UploadFile, session: AsyncSession) -> JSONResponse:

        if os.path.exists(f"app/doc_static/images/{id_doc}.webp"):
            logger.info("Использовали занятый id для загрузки!")
            return JSONResponse(status_code=status.HTTP_200_OK, content="Данный id занят, попробуйте другой!")

        session.add(Documents(id=id_doc,
                    path="app/doc_static/images",
                    date=datetime.now())
                    )
        try:
            await session.commit()
            logger.info("Запись добавили(upload)!")
        except Exception:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                                detail="Ошибка во время добавления записи в БД, попробуйте позже!")

        cls.copyfile(id_doc, file_uploaded)
        return JSONResponse(status_code=status.HTTP_200_OK, content="Запись и изображение сохранены в БД и на диск!")



    @classmethod
    async def delete(cls, id_doc: PositiveInt, session: AsyncSession) -> JSONResponse:

        cls.check_available_file(id_doc)

        await session.execute(delete(Documents_text).filter(Documents_text.id_doc == id_doc))
        # await session.execute(delete(Documents).filter(Documents.id == id_doc))Удаляется через каскад (models.py)
        await session.commit()
        logger.info("Запись удалена(delete)!")

        cls.remove_and_exception(id_doc)

        logger.info("Запись и изображение удалены!")
        return JSONResponse(status_code=status.HTTP_200_OK, content="Записи и файл были удалены!")




class DocTextDAO:


    @staticmethod
    def found_or_no(id_doc: PositiveInt):
        try:
            text_from_img = img_to_text.delay(id_doc).get()
            logger.info("Изображение преобразовано в текст!")
            return  text_from_img
        except FileNotFoundError:
            logger.info("Файл не найден(analyse)!")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Файл не найден!")



    @classmethod
    async def analyse(cls, id_doc: PositiveInt, session: AsyncSession) -> JSONResponse:

        text_from_img = cls.found_or_no(id_doc)

        try:
            await session.execute(insert(Documents_text).values(id = id_doc,
                                   id_doc = id_doc,
                                   text=text_from_img))
            await session.commit()
            logger.info("Текст добавлен в БД!")
        except Exception:
            logger.warning("Текст переведен, но не добавлен в БД!")
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                                detail="Текст не был добавлен в БД!")

        return JSONResponse(status_code=status.HTTP_200_OK, content="Текст прочитан и добавлен в БД!")





    @classmethod
    async def getter_text(cls, id_doc: PositiveInt, session: AsyncSession) -> JSONResponse:

        result = await session.execute(select(Documents_text.text).filter(Documents_text.id == id_doc))
        logger.info("Запрос на возврат текста прошел(getter_text)!")

        a = result.first()

        if not a:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                content="Текст с данным id не найден, используйте метод get_text для его создания!")
        else:
            return JSONResponse(status_code=status.HTTP_200_OK,
                                content=a.text)







