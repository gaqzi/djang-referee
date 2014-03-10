from __future__ import unicode_literals

from django.db import IntegrityError, models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from datetime_truncate import truncate_day

__all__ = ('LimitedParticipation', 'ExtraParticipationTime')


class LimitedParticipation(models.Model):
    """This model is sliced out of a daily lucky wheel app.

    Reusable model usage to look something like:

    > p = Participant.objects.get(pk=1)
    > p.can_participate
    True
    # If a game of luck, how many chances does this user have
    > p.participation_times_left
    > p.add_extra_participations(n)

    A participant can only participate the amount of times given in
    `participation_times_left` and when all of those has been used up
    the timestamp `last_participated_at` is updated.

    Any extra participations added to the user will be recorded in
    `extra_participations_received`, which is just an informative
    number.

    Any methods that will change anything on the model takes a
    `commit` kwarg that by default is True, it will then automatically
    save the changes to the database.

    """
    class NoMoreParticipation(IntegrityError):
        """Raised when the limited amount has run out for the user. Does not
        necessarily mean the user can't _ever_ enter again.
        """

    participation_times_left = models.PositiveIntegerField(
        default=1,
        help_text=_('The number of times the user currently can participate')
    )
    last_participated_at = models.DateTimeField(null=True, blank=True)
    extra_participations_received = models.PositiveIntegerField(
        default=0,
        help_text=_('If the user has received participation for any reason. '
                    'Just informative.'),
        editable=False,
    )

    class Meta:
        abstract = True

    @property
    def can_participate(self):
        return self.participation_times_left > 0

    def participate(self, commit=True):
        """Have the user participate and reduce the amount of times left to
        participate. Set the `last_participated_at` to now.

        """
        if not self.can_participate:
            raise self.NoMoreParticipation()
        elif self.participation_times_left > 0:
            self.participation_times_left -= 1

        self.last_participated_at = timezone.now()

        if commit:
            self.save()

    def add_extra_participation(self, number=1, commit=True):
        """Adds `number` extra participations and adds that number to the
        `extra_participations_received` attribute.

        """
        self.participation_times_left += number
        self.extra_participations_received += number

        if commit:
            self.save()


class ExtraParticipationTime(LimitedParticipation):
    """Allows the participant to receive an extra participation whenever
    `get_current_period()` is after `last_participated_at`, which
    defaults to midnight for `timezone.now`.

    One assumption is that the very first chance will be received from
    the participant, and as such an empty/None `last_participation_at` will
    not receive an extra participation.

    Any extra participations received from time bonuses will not be
    registered in `extra_participations_received`.

    To override how often a new participation is awarded by time
    change the timestamp returned by `get_current_period()`.

    """
    class Meta:
        abstract = True

    @property
    def can_participate(self):
        return (self.participation_times_left > 0 or
                self.get_extra_participation_from_time)

    @property
    def get_extra_participation_from_time(self):
        """Should the participant be able to partake again because he got
        another go from time?

        """
        return (self.last_participated_at
                and self.get_current_period() >= self.last_participated_at)

    def get_current_period(self):
        """The time that `last_participated_at` must be prior to receive an
        extra participation.

        """
        return truncate_day(timezone.localtime(timezone.now()))

    def _set_finished_participation(self):
        """If `last_participated_at` has never been set then there's no extra
         chances to be had. The default participation is 1 on object
         creation.

        """
        if(self.participation_times_left == 0
           and (not self.last_participated_at or
                self.get_extra_participation_from_time)):
            self.last_participated_at = timezone.now()
