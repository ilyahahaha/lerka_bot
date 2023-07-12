from typing import Any, Dict

from common.keyboard import ValidCallbacks
from schemas.bgu import BguCompetitionGroup
from schemas.isu import IsuCompetitionGroup


def get_default_message(name: str, state_data: Dict[str, Any] | None = None) -> str:
    isu_leaderboard = state_data.get(ValidCallbacks.UPDATE_ISU) if state_data else None
    istu_leaderboard = (
        state_data.get(ValidCallbacks.UPDATE_ISTU) if state_data else None
    )
    bgu_leaderboard = state_data.get(ValidCallbacks.UPDATE_BGU) if state_data else None

    message = (
        f"👋 <b>Привет,</b> {name}."
        + "\n\n"
        + "✅ Я создан помочь Лерке мониторить результаты по поступлению в ВУЗы Иркутска."
        + "\n\n"
        + "<b>Текущие результаты:</b>"
        + "\n\n"
        + "1️⃣ <b>ИГУ: </b>"
        + f"\n{isu_leaderboard if isu_leaderboard else '❌ <i>Нет данных</i>'}\n\n"
        + "2️⃣ <b>ИРНИТУ: </b>"
        + f"\n{istu_leaderboard if istu_leaderboard else '❌ <i>Нет данных</i>'}\n\n"
        + "3️⃣ <b>БГУ: </b>"
        + f"\n{bgu_leaderboard if bgu_leaderboard else '❌ <i>Нет данных</i>'}"
    )

    return message


def build_leaderboard(
    result: list[
        IsuCompetitionGroup | IsuCompetitionGroup | BguCompetitionGroup | None
    ],
) -> str | None:
    message = []

    for result in result:
        if result is None:
            continue

        text_string = f"<code>🏆 {result.group} -</code> {result.place} место"
        message.append(text_string)

    return "\n".join(message)
