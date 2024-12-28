from fastapi import FastAPI, UploadFile, Depends
from pydantic import PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from app.dao import DocumentsDAO, DocTextDAO
from app.database import get_session

app = FastAPI(title="Image_to_text",
              description="Этот проект позволяет считывать текст с изображения и возвращать его пользователю, \n"
                          " имеет 4 ручки - загрузку(upload_doc),\n"
                          " на удаление - doc_delete, считывание - doc_analyze, вывод клиенту - get_text!")

@app.post("/upload_doc", tags=["Документы"])
async def upload_doc(id_doc: PositiveInt, file: UploadFile, session: AsyncSession = Depends(get_session)) -> dict:
    """
    Позволяет загружать изображение на диск и создавать запись(по id).

    ### Параметры
    - **id_doc**: Integer, идентификатор изображения и записи, первичный
    - **file**: UploadFile, Изображение, сохраняется в .webp
    - **session**: AsyncSession, сессия, взята из get_session

    ### Возможные ответы
    - **200**: Данный id занят, попробуйте другой
    - **200**: Запись и изображение сохранены в БД и на диск
    - **503**: Ошибка во время добавления записи в БД
    """
    return await DocumentsDAO.upload(id_doc, file, session)

@app.delete("/delete_doc", tags=["Документы"])
async def delete_doc(id_doc: PositiveInt, session: AsyncSession = Depends(get_session)) -> JSONResponse:
    """
    Позволяет удалить изображение и запись по id

    ### Параметры
    - **id_doc**: Integer, идентификатор изображения и записи, первичный
    - **session**: AsyncSession, сессия, взята из get_session


    ### Возможные ответы
    - **200**: Изображение с данным id не найдено
    - **200**: Запись и файл удалены
    - **200**: Кто-то изменил/удалил файл во время выполнения запроса, записи стёрты!
    - **503**: Ошибка во время удаления записей в БД
    """
    return await DocumentsDAO.delete(id_doc, session)

@app.post("/doc_analyse", tags=["Документы_текст"])
async def doc_analyse(id_doc: PositiveInt, session: AsyncSession = Depends(get_session)) -> JSONResponse:
    """
    Позволяет прочитать текст с изображения и добавить его в БД

    ### Параметры
    - **id_doc**: Integer, идентификатор изображения и записи, первичный
    - **session**: AsyncSession, сессия, взята из get_session

    ### Возможные ответы
    - **200**: Файл не найден
    - **200**: Текст прочитан и добавлен в БД
    - **503**: Текст не был добавлен в БД
    """
    return await DocTextDAO.analyse(id_doc, session)

@app.get("/get_text", tags=["Документы_текст"])
async def get_text(id_doc: PositiveInt, session: AsyncSession = Depends(get_session)) -> JSONResponse:
    """
    Возвращает текст с картинки из БД

    ### Параметры
    - **id_doc**: Integer, идентификатор изображения и записи, первичный
    - **session**: AsyncSession, сессия, взята из get_session

    ### Возможные ответы
    - **200**: Текст с данным id не найден, используйте метод get_text для его создания!
    - **200**: Возвращает текст из БД
    - **503**: Ошибка сервера, текст не получен
    """
    return await DocTextDAO.getter_text(id_doc, session)
    # return await DocTextDAO.getter_text(id_doc, session)