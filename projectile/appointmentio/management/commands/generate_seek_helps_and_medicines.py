from django.conf import settings
from django.core.management.base import BaseCommand

import json, os
from datetime import date

from appointmentio.models import Medicine, Ingredient, SeekHelp


def generate_medicines():
    file_path = os.path.join(
        settings.BASE_DIR, "appointmentio/management/commands/medicine_list.json"
    )
    with open(file_path, "r") as file:
        medicines_list = json.load(file)

    existing_medicines = list(Medicine.objects.values_list("name", flat=True))

    generated_medicines = []

    ingredient, created = Ingredient.objects.get_or_create(name="empty")

    for medicine_data in medicines_list:
        medicine_name = medicine_data["name"]
        medicine_strength = medicine_data["strength"]
        if medicine_name not in existing_medicines:
            medicine = Medicine(
                name=medicine_name,
                strength=medicine_strength,
                expiration_date=date(2025, 8, 10),
            )
            medicine.save()
            medicine.ingredient.add(ingredient)
            generated_medicines.append(medicine_name)

    return generated_medicines


def generate_seek_helps():
    file_path = os.path.join(
        settings.BASE_DIR, "appointmentio/management/commands/seek_help_list.json"
    )
    with open(file_path, "r") as file:
        seek_help_texts = json.load(file)

    existing_seek_help = list(SeekHelp.objects.values_list("name", flat=True))

    generate_seek_help = []

    for seek_data in seek_help_texts:
        seek_text = seek_data["name"]
        if seek_text not in existing_seek_help:
            seek_help = SeekHelp(name=seek_text)
            seek_help.save()
            generate_seek_help.append(seek_text)

    return generate_seek_help


class Command(BaseCommand):
    help = "Generate a specified number of medicines & seek_help"

    def handle(self, *args, **kwargs):
        generated_medicines = generate_medicines()
        generated_seek_help = generate_seek_helps()

        if generated_medicines:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created medicines: {", ".join(generated_medicines)}'
                )
            )
        else:
            self.stdout.write(self.style.SUCCESS("No new medicines were created."))

        if generated_seek_help:
            self.stdout.write(
                self.style.SUCCESS(f"Successfully created seek help texts")
            )
        else:
            self.stdout.write(self.style.SUCCESS("No seeek help was created."))
