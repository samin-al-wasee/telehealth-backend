from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

import json
import os

from datetime import timedelta, datetime, date
from dateutil.parser import parse

from accountio.models import Organization

from appointmentio.models import (
    WeekDay,
    Shift,
    AppointmentTimeSlot,
)


class Command(BaseCommand):
    help = "Create Appointment Time Slots"

    def handle(self, *args, **kwargs):
        file_path = os.path.join(
            settings.BASE_DIR,
            "appointmentio/management/commands/appointment_schedule_list.json",
        )

        with open(file_path, "r") as file:
            schedule_data = json.load(file)

        try:
            organization = Organization.objects.get(name="CardiCheck")
        except Organization.DoesNotExist:
            raise CommandError("Organization not found!")

        time_slot_list = []

        appointment_duration = parse(schedule_data["appointment_duration"]).time()
        appointment_interval = parse(schedule_data["appointment_interval"]).time()

        organization.appointment_duration = appointment_duration
        organization.appointment_interval = appointment_interval
        organization.save()

        for day_data in schedule_data["week_day"]:
            day_name = day_data["day"]
            off_day = day_data["off_day"]

            week_day, created = WeekDay.objects.get_or_create(
                organization=organization, day=day_name, defaults={"off_day": off_day}
            )

            if not off_day and "shifts" in day_data:
                for shift_data in day_data["shifts"]:
                    shift_label = shift_data["shift_label"]
                    start_time = parse(shift_data["start_time"]).time()
                    end_time = parse(shift_data["end_time"]).time()

                    shift, created = Shift.objects.get_or_create(
                        weekday=week_day,
                        shift_label=shift_label,
                        start_time=start_time,
                        end_time=end_time,
                    )

                    start_time = shift.start_time
                    end_time = shift.end_time

                    while start_time < end_time:
                        schedule_time = datetime.combine(
                            date.today(), start_time.replace(minute=0)
                        )
                        time_slot_list.append(
                            AppointmentTimeSlot(
                                organization=organization,
                                weekday=week_day,
                                schedule_time=schedule_time.strftime("%H:%M"),
                                slot=start_time,
                            )
                        )
                        start_time = (
                            datetime.combine(date.today(), start_time)
                            + timedelta(
                                minutes=appointment_duration.minute
                                + appointment_interval.minute
                            )
                        ).time()

        with transaction.atomic():
            AppointmentTimeSlot.objects.bulk_create(time_slot_list)

        self.stdout.write(self.style.SUCCESS("Appointment time slots created successfully!"))
