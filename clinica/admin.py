from django.contrib import admin
from .models import Especie, PacienteMascota


class PacienteMascotaInline(admin.TabularInline):
    model = PacienteMascota
    extra = 1


@admin.register(Especie)
class EspecieAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "codigo_clasificacion",
        "activa",
        "total_pacientes_asociados",
    )

    search_fields = (
        "nombre",
        "codigo_clasificacion",
    )

    list_filter = (
        "activa",
        "codigo_clasificacion",
    )

    inlines = (
        PacienteMascotaInline,
    )

    @admin.display(description="Total de pacientes")
    def total_pacientes_asociados(self, obj):
        return obj.pacientes.count()


@admin.register(PacienteMascota)
class PacienteMascotaAdmin(admin.ModelAdmin):
    list_display = (
        "nombre_mascota",
        "nombre_dueno",
        "numero_chip",
        "especie",
        "peso_kg",
        "en_tratamiento",
        "evaluacion_riesgo",
    )

    search_fields = (
        "nombre_mascota",
        "nombre_dueno",
        "numero_chip",
        "especie__nombre",
        "especie__codigo_clasificacion",
    )

    list_filter = (
        "en_tratamiento",
        "especie",
        "especie__codigo_clasificacion",
        "fecha_registro",
    )

    list_editable = (
        "en_tratamiento",
    )

    actions = (
        "dar_de_alta",
        "ingresar_a_tratamiento",
    )

    @admin.action(
        description="Dar de alta a los pacientes seleccionados"
    )
    def dar_de_alta(self, request, queryset):
        cantidad = queryset.update(en_tratamiento=False)

        self.message_user(
            request,
            f"Se marcaron {cantidad} paciente(s) como dados de alta.",
        )

    @admin.action(
        description="Ingresar a tratamiento a los pacientes seleccionados"
    )
    def ingresar_a_tratamiento(self, request, queryset):
        cantidad = queryset.update(en_tratamiento=True)

        self.message_user(
            request,
            f"Se marcaron {cantidad} paciente(s) como en tratamiento.",
        )

    @admin.display(description="Evaluación de riesgo")
    def evaluacion_riesgo(self, obj):
        return "Pendiente de definir"