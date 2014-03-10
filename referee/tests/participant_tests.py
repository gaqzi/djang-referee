from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from mock import patch

from test_app.models import LimitedParticipant, LimitedParticipantDaily


class LimitedParticipantBase(TestCase):
    model = LimitedParticipant

    def setUp(self):
        self.participant = self.model.objects.create()
        self.times_to_participate = self.participant.participation_times_left

    def _use_up_all_participations(self):
        for i in range(0, self.times_to_participate):
            self.participant.participate()


class LimitedParticipantTest(LimitedParticipantBase):
    model = LimitedParticipant

    def test_should_be_able_to_participate_when_just_created(self):
        self.assertTrue(self.participant.can_participate)

    def test_when_participating_the_times_left_should_be_lowered(self):
        self.participant.participate()

        self.assertEqual(self.participant.participation_times_left,
                         self.times_to_participate - 1)

    def test_when_all_participation_times_has_been_used_mark_it_as_such(self):
        self._use_up_all_participations()

        self.assertTrue(self.participant.last_participated_at is not None)
        self.assertEqual(self.participant.participation_times_left, 0)

    def test_should_raise_an_error_when_participating_more_than_allowed(self):
        self._use_up_all_participations()

        with self.assertRaises(self.model.NoMoreParticipation):

            self.participant.participate()

    def test_should_be_able_to_receive_extra_participations(self):
        self.participant.add_extra_participation()

        self.assertEqual(self.participant.participation_times_left,
                         self.times_to_participate + 1)
        self.assertEqual(self.participant.extra_participations_received, 1)


class ParticipantDailyTest(LimitedParticipantBase):
    model = LimitedParticipantDaily
    day = timedelta(days=1, seconds=1)

    def test_should_be_allowed_to_participate_again_if_a_day_passed(self):
        self._use_up_all_participations()

        with self.assertRaises(self.model.NoMoreParticipation):
            self.participant.participate()

        now = timezone.now() + self.day
        with patch('django.utils.timezone.now') as mock:
            mock.return_value = now
            self.participant.participate()

    def test_should_set_participation_as_finished(self):
        self._use_up_all_participations()

        self.assertTrue(self.participant.last_participated_at is not None)
        self.assertEqual(self.participant.participation_times_left, 0)
        self.assertFalse(self.participant.get_extra_participation_from_time)
