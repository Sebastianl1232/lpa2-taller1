import pytest

from src.models.concretos.sofa import Sofa
from src.models.concretos.cama import Cama
from src.models.concretos.sofacama import SofaCama


class TestSofaCama:
    @pytest.fixture
    def sofa_cama(self):
        return SofaCama(
            "Sofa Cama Moderno",
            "Tela",
            "Gris",
            500,
            capacidad_personas=3,
            material_tapizado="tela",
            tamaño_cama="queen",
            incluye_colchon=True,
            mecanismo_conversion="plegable",
        )

    def test_hereda_de_sofa_y_cama(self, sofa_cama):
        assert isinstance(sofa_cama, Sofa)
        assert isinstance(sofa_cama, Cama)
        assert sofa_cama.capacidad_personas == 3
        assert sofa_cama.tamaño_cama == "queen"
        assert sofa_cama.mecanismo_conversion == "plegable"
        assert sofa_cama.modo_actual == "sofa"

    def test_calcular_precio_combina_recargos_de_sofa_y_cama(self, sofa_cama):
        # Sofa: 500 * (1 + 0.1 respaldo + 0.1 tela + 0.1 capacidad)
        # + 150 brazos = 800.
        # Cama queen: +500, colchón: +250.
        assert sofa_cama.calcular_precio() == 1550.0

    def test_convertir_a_cama_y_regresar_a_sofa(self, sofa_cama):
        assert sofa_cama.convertir_a_cama() == (
            "Sofá convertido a cama usando mecanismo plegable"
        )
        assert sofa_cama.modo_actual == "cama"

        assert sofa_cama.convertir_a_cama() == "El sofá-cama ya está en modo cama"

        assert sofa_cama.convertir_a_sofa() == (
            "Cama convertida a sofá usando mecanismo plegable"
        )
        assert sofa_cama.modo_actual == "sofa"
        assert sofa_cama.convertir_a_sofa() == "El sofá-cama ya está en modo sofá"

    @pytest.mark.parametrize(
        ("tamaño", "capacidad_cama"),
        [
            ("individual", 1),
            ("matrimonial", 2),
            ("queen", 2),
            ("king", 2),
        ],
    )
    def test_obtener_capacidad_total(self, tamaño, capacidad_cama):
        sofa_cama = SofaCama(
            "Sofa Cama",
            "Tela",
            "Gris",
            500,
            tamaño_cama=tamaño,
        )

        assert sofa_cama.obtener_capacidad_total() == {
            "como_sofa": 3,
            "como_cama": capacidad_cama,
        }

    def test_descripcion_y_str_incluyen_modo_y_caracteristicas(self, sofa_cama):
        descripcion = sofa_cama.obtener_descripcion()

        assert "Sofá-Cama: Sofa Cama Moderno" in descripcion
        assert "Capacidad: 3 personas" in descripcion
        assert "Tamaño como cama: queen" in descripcion
        assert "Incluye colchón: Sí" in descripcion
        assert "Mecanismo: plegable" in descripcion
        assert "Modo actual: sofa" in descripcion
        assert "Precio final: $1550.0" in descripcion
        assert str(sofa_cama) == "Sofá-cama Sofa Cama Moderno (modo: sofa)"
