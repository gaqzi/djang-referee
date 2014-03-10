from referee.models import (
    TimePeriodBase,
    LimitedParticipation, ExtraParticipationTime
)


class TimePeriod(TimePeriodBase):
    pass


class LimitedParticipant(LimitedParticipation):
    pass


class LimitedParticipantDaily(ExtraParticipationTime):
    pass
