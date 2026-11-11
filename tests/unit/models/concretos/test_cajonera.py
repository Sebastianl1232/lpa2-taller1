import pytest

from src.models.concretos.cajonera import Cajonera


class TestCajonera:
    @pytest.fixture
    def cajonera_basica(self):
        return Cajonera("Cajonera Oficina", "Metal", "Negro", 300)

    def test_instanciacion_correcta(self, cajonera_basica):
        assert cajonera_basica.nombre == "Cajonera Oficina"
        assert cajonera_basica.material == "Metal"
        assert cajonera_basica.color == "Negro"
        assert cajonera_basica.precio_base == 300
        assert cajonera_basica.num_cajones == 3
        assert cajonera_basica.tiene_ruedas is False

    @pytest.mark.parametrize(
        ("cajones", "ruedas", "precio_esperado"),
        [
            (3, False, 360),
            (5, True, 430),
            (0, True, 330),
        ],
    )
    def test_calcular_precio_aplica_componentes(
        self, cajones, ruedas, precio_esperado
    ):
        cajonera = Cajonera(
            "Cajonera",
            "Metal",
            "Negro",
            300,
            num_cajones=cajones,
            tiene_ruedas=ruedas,
        )

        assert cajonera.calcular_precio() == precio_esperado

    def test_precio_base_none_se_convierte_en_cero(self):
        cajonera = Cajonera("Cajonera", "Metal", "Negro", None)

        assert cajonera.precio_base == 0
        assert cajonera.calcular_precio() == 60

    def test_obtener_descripcion_incluye_caracteristicas(self, cajonera_basica):
        assert cajonera_basica.obtener_descripcion() == (
            "Cajonera 'Cajonera Oficina': Material=Metal, Color=Negro, "
            "Cajones=3, Ruedas=No, Precio base=$300"
        )
