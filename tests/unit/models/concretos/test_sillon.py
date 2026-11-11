import pytest

from src.models.concretos.sillon import Sillon


class TestSillon:
    @pytest.fixture
    def sillon_basico(self):
        return Sillon("Sillón Clásico", "Madera", "Marrón", 700)

    def test_instanciacion_correcta(self, sillon_basico):
        assert sillon_basico.nombre == "Sillón Clásico"
        assert sillon_basico.material == "Madera"
        assert sillon_basico.color == "Marrón"
        assert sillon_basico.precio_base == 700
        assert sillon_basico.capacidad_personas == 2
        assert sillon_basico.tiene_respaldo is True
        assert sillon_basico.material_tapizado is None
        assert sillon_basico.tiene_brazos is True
        assert sillon_basico.es_reclinable is False
        assert sillon_basico.tiene_reposapiés is False

    @pytest.mark.parametrize(
        ("tapizado", "brazos", "reclinable", "reposapies", "precio_esperado"),
        [
            (None, False, False, False, 700),
            ("Tela", True, False, False, 1000),
            ("Cuero", True, True, True, 1330),
        ],
    )
    def test_calcular_precio_aplica_recargos(
        self, tapizado, brazos, reclinable, reposapies, precio_esperado
    ):
        sillon = Sillon(
            "Sillón",
            "Madera",
            "Marrón",
            700,
            material_tapizado=tapizado,
            tiene_brazos=brazos,
            es_reclinable=reclinable,
            tiene_reposapiés=reposapies,
        )

        assert sillon.calcular_precio() == precio_esperado

    def test_precio_base_none_se_convierte_en_cero(self):
        sillon = Sillon("Sillón", "Madera", "Marrón", None)

        assert sillon.precio_base == 0
        assert sillon.calcular_precio() == 100

    def test_obtener_descripcion_incluye_caracteristicas(self):
        sillon = Sillon(
            "Sillón Reclinable",
            "Cuero",
            "Negro",
            700,
            material_tapizado="Cuero",
            es_reclinable=True,
            tiene_reposapiés=True,
        )

        assert sillon.obtener_descripcion() == (
            "Sillón 'Sillón Reclinable': Material=Cuero, Color=Negro, "
            "Capacidad=2 personas, Tapizado=Cuero, Brazos=Sí, "
            "Reclinable=Sí, Reposapiés=Sí, Precio base=$700"
        )
