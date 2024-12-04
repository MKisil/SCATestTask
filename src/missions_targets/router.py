from fastapi import APIRouter
from sqlalchemy import select

from src.database import async_session_factory
from src.missions_targets.schemas import MissionCreateScheme, MissionGetScheme
from src.spy_cats.models import SpyCat, Mission, Target

router = APIRouter(
    prefix="/missions-targets",
    tags=["Mission/Targets"],
    responses={404: {"description": "Not found"}},
)


@router.post("/create-mission/")
async def create_mission(mission_data: MissionCreateScheme):
    async with async_session_factory() as session:
        spy_cat = await session.get(SpyCat, mission_data.spy_cat_id)
        if spy_cat is None:
            return {"status": "error", "message": "Spy cat not found."}

        spy_cat_mission = await session.execute(select(Mission).filter(Mission.spy_cat_id == spy_cat.id))
        if spy_cat_mission.scalar():
            return {"status": "error", "message": "Spy cat is already on a mission."}

        mission = Mission(spy_cat_id=spy_cat.id)
        if not (1 <= len(mission_data.targets) <= 3):
            return {"status": "error", "message": "Invalid count of targets."}

        session.add(mission)
        await session.commit()
        await session.refresh()

        for target in mission_data.targets:
            target_dict = target.model_dump()
            target_dict["mission_id"] = mission.id
            session.add(Target(**target_dict))

        await session.commit()
        mission = await session.get(Mission, mission.id)
        await session.refresh(mission)

    return {
        "status": "success",
        "message": "Mission created.",
        "data": {"mission": MissionGetScheme.model_validate(mission).model_dump()}
    }
