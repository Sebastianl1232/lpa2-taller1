import pytest

from src.models.concretos.sofa import Sofa


class TestSofa:
    @pytest.fixture
    def sofa_basico(self):
        return Sofa("Sofa Familiar", "Tela", "Gris", 1000.0)

    def test_instanciacion_correcta(self, sofa_basico):
        assert sofa_basico.nombre == "Sofa Familiar"
        assert sofa_basico.capacidad_personas == 3
        assert sofa_basico.tiene_respaldo is True
        assert sofa_basico.tiene_brazos is True
        assert sofa_basico.es_modular is False
        assert sofa_basico.incluye_cojines is False

    def test_calcular_precio_sin_tapizado(self):
        sofa = Sofa(
            "Sofa",
            "Cuero",
            "Negro",
            1000.0,
            capacidad_personas=3,
            tiene_brazos=False,
        )

        # 1000 * (1.0 + 0.1 respaldo + 0.1 capacidad) = 1200.
        assert sofa.calcular_precio() == 1200.0

    def test_calcular_precio_aplica_caracteristicas(self):
        sofa = Sofa(
            "Sofa Modular",
            "Tela",
            "Azul",
            1000.0,
            capacidad_personas=3,
            material_tapizado="Tela",
            tiene_brazos=True,
            es_modular=True,
            incluye_cojines=True,
        )

        # 1000 * 1.3 + 150 + 200 + 50.
        assert sofa.calcular_precio() == 1700.0

    def test_obtener_descripcion_incluye_caracteristicas(self):
        sofa = Sofa(
            "Sofa Modular",
            "Tela",
            "Azul",
            1000.0,
            material_tapizado="Tela",
            es_modular=True,
            incluye_cojines=True,
        )

        descripcion = sofa.obtener_descripcion()

        assert "Sofá: Sofa Modular" in descripcion
        assert "Material: Tela" in descripcion
        assert "Capacidad: 3 personas" in descripcion
        assert "Tapizado: Tela" in descripcion
        assert "Brazos: Sí" in descripcion
        assert "Modular: Sí" in descripcion
        assert "Incluye cojines: Sí" in descripcion
        assert "Precio final: $1700.0" in descripcion
