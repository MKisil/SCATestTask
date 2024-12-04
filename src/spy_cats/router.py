from fastapi import APIRouter
from sqlalchemy import select

from src.database import async_session_factory
from src.spy_cats.models import SpyCat
from src.spy_cats.schemas import SpyCatCreateScheme, SpyCatGetScheme, SpyCatUpdateSalaryScheme
from src.spy_cats.utils import validate_spy_cat_breed

router = APIRouter(
    prefix="/spy-cats",
    tags=["Spy cats"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
async def create_spy_cat(spy_cat_data: SpyCatCreateScheme):
    is_breed_valid = await validate_spy_cat_breed(spy_cat_data.breed)
    if not is_breed_valid:
        return {"status": "error", "message": "Spy cat 'breed' is not valid."}

    async with async_session_factory() as session:
        spy_cat = SpyCat(**spy_cat_data.model_dump())
        session.add(spy_cat)
        await session.commit()
        await session.refresh(spy_cat)

    return {
        "status": "success",
        "message": "Spy cat created.",
        "data": {"spy_cat": SpyCatGetScheme.model_validate(spy_cat).model_dump()}
    }


@router.delete("/{spy_cat_id}/")
async def delete_spy_cat(spy_cat_id: int):
    async with async_session_factory() as session:
        spy_cat = await session.get(SpyCat, spy_cat_id)
        if spy_cat is None:
            return {"status": "error", "message": "Spy cat not found."}

        await session.delete(spy_cat)
        await session.commit()

    return {"status": "success", "message": "Spy cat deleted.", "data": {"spy_cat_id": spy_cat_id}}


@router.patch("/update-salary/")
async def update_spy_cat_salary(update_info: SpyCatUpdateSalaryScheme):
    async with async_session_factory() as session:
        spy_cat = await session.get(SpyCat, update_info.id)
        if spy_cat is None:
            return {"status": "error", "message": "Spy cat not found."}

        spy_cat.salary = update_info.salary
        await session.commit()
        await session.refresh(spy_cat)

    return {
        "status": "success",
        "message": "Spy cat salary updated.",
        "data": {"spy_cat": SpyCatGetScheme.model_validate(spy_cat).model_dump()}
    }


@router.get("/")
async def get_spy_cats():
    async with async_session_factory() as session:
        result = await session.execute(select(SpyCat))
        spy_cats = result.scalars().all()
        spy_cats = [SpyCatGetScheme.model_validate(spy_cat).model_dump() for spy_cat in spy_cats]

    return {
        "status": "success",
        "message": "Spy cats retrieved.",
        "data": {"spy_cats": spy_cats}
    }


@router.get("/{spy_cat_id}/")
async def get_spy_cat(spy_cat_id: int):
    async with async_session_factory() as session:
        spy_cat = await session.get(SpyCat, spy_cat_id)
        if spy_cat is None:
            return {"status": "error", "message": "Spy cat not found."}

    return {
        "status": "success",
        "message": "Spy cat retrieved.",
        "data": {"spy_cat": SpyCatGetScheme.model_validate(spy_cat).model_dump()}
    }



