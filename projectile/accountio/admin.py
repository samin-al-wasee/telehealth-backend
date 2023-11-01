from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin

from .models import (
    Organization,
    OrganizationUser,
    Descendant,
    Affiliation,
    Examination,
    Investigation,
    Diagnosis,
    PrescriptionAdditionalConnector,
)


class OrganizationUserInline(admin.TabularInline):
    model = OrganizationUser
    extra = 1


@admin.register(Organization)
class OrganizationAdmin(SimpleHistoryAdmin):
    list_display = [
        "uid",
        "name",
        "registration_no",
    ]
    list_filter = ["status", "kind"]
    search_fields = [
        "name",
    ]
    inlines = [OrganizationUserInline]
    readonly_fields = ["uid", "slug", "serial_number"]


@admin.register(Descendant)
class DescendantAdmin(SimpleHistoryAdmin):
    list_display = ["uid", "child", "parent", "updated_at"]
    autocomplete_fields = [
        "parent",
        "child",
    ]
    readonly_fields = ["uid"]


@admin.register(OrganizationUser)
class OrganizationUserAdmin(admin.ModelAdmin):
    list_display = [
        "uid",
        "user",
        "is_default",
    ]
    list_filter = [
        "status",
    ]
    ordering = ("-created_at",)
    search_fields = (
        "user__email",
        "organization__name",
    )
    readonly_fields = ["uid"]

    def _referrer(self, instance):
        referrer = instance.referrer
        return referrer.user.email if referrer else referrer


@admin.register(Affiliation)
class AffiliationAdmin(admin.ModelAdmin):
    model = Affiliation
    list_display = ["uid", "title", "hospital_name", "status"]
    list_filter = ["status"]
    ordering = ("-created_at",)
    readonly_fields = ["uid"]


@admin.register(Examination)
class ExaminationAdmin(admin.ModelAdmin):
    model = Examination
    list_display = ["uid", "name"]
    readonly_fields = ["uid"]


@admin.register(Investigation)
class InvestigationAdmin(admin.ModelAdmin):
    model = Investigation
    list_display = ["uid", "name"]
    readonly_fields = ["uid"]


@admin.register(Diagnosis)
class DiagnosisAdmin(admin.ModelAdmin):
    model = Diagnosis
    list_display = ["uid", "name"]
    readonly_fields = ["uid"]


@admin.register(PrescriptionAdditionalConnector)
class PrescriptionAdditionalConnectorAdmin(admin.ModelAdmin):
    model = PrescriptionAdditionalConnector
    list_display = [
        "uid",
        "_prescription",
        "_treatment",
        "_recommendation",
        "_diagnosis",
        "_investigation",
        "_examination",
        "_primary_disease",
    ]
    readonly_fields = ["uid"]

    def _prescription(self, obj):
        return obj.prescription.uid if obj.prescription else None

    def _treatment(self, obj):
        return obj.treatment.uid if obj.treatment else None

    def _recommendation(self, obj):
        return obj.recommendation.name if obj.recommendation else None

    def _diagnosis(self, obj):
        return obj.diagnosis.name if obj.diagnosis else None

    def _investigation(self, obj):
        return obj.investigation.name if obj.investigation else None

    def _examination(self, obj):
        return obj.examination.name if obj.examination else None

    def _primary_disease(self, obj):
        return obj.primary_disease.name if obj.primary_disease else None
