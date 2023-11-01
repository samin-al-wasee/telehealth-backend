from django.contrib import admin

from .models import (
    Achievement,
    Degree,
    Department,
    Doctor,
    DoctorAdditionalConnector,
    Expertise,
    Morbidities,
    Recommendations,
)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    model = Doctor
    list_display = ["uid", "name", "organization"]
    readonly_fields = ["uid", "slug", "serial_number"]


@admin.register(Degree)
class DegreeAdmin(admin.ModelAdmin):
    model = Degree
    list_display = ["uid", "name", "institute", "passing_year", "status"]
    readonly_fields = ["uid"]


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    model = Achievement
    list_display = ["uid", "name", "year"]
    readonly_fields = ["uid"]


@admin.register(Department)
class DeaprtmentAdmin(admin.ModelAdmin):
    model = Department
    list_display = ["uid", "name"]
    readonly_fields = ["uid"]


@admin.register(Expertise)
class ExpertiseAdmin(admin.ModelAdmin):
    model = Expertise
    list_display = ["uid", "name"]
    readonly_fields = ["uid"]


@admin.register(Morbidities)
class MorbiditiesAdmin(admin.ModelAdmin):
    model = Morbidities
    list_display = ["uid", "name", "_expertise", "_department"]
    readonly_fields = ["uid"]

    def _expertise(self, obj):
        return obj.expertise.name

    def _department(self, obj):
        return obj.department.name


@admin.register(Recommendations)
class RecommendationsAdmin(admin.ModelAdmin):
    model = Recommendations
    list_display = ["uid", "name"]
    readonly_fields = ["uid"]


@admin.register(DoctorAdditionalConnector)
class DoctorAdditionalConnectorAdmin(admin.ModelAdmin):
    model = DoctorAdditionalConnector
    list_display = ["doctor", "expertise", "degree", "achievement"]
