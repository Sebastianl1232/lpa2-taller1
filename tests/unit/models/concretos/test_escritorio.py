import pytest

from src.models.concretos.escritorio import Escritorio


class TestEscritorio:
    @pytest.fixture
    def escritorio_basico(self):
        return Escritorio("Escritorio", "Madera", "Natural", 600)

    def test_instanciacion_correcta(self, escritorio_basico):
        assert escritorio_basico.nombre == "Escritorio"
        assert escritorio_basico.material == "Madera"
        assert escritorio_basico.color == "Natural"
        assert escritorio_basico.precio_base == 600
        assert escritorio_basico.forma == "rectangular"
        assert escritorio_basico.tiene_cajones is False
        assert escritorio_basico.num_cajones == 0
        assert escritorio_basico.largo == 1.2
        assert escritorio_basico.tiene_iluminacion is False

    @pytest.mark.parametrize(
        ("cajones", "largo", "iluminacion", "forma", "precio_esperado"),
        [
            (0, 1.2, False, "rectangular", 600),
            (3, 1.6, True, "rectangular", 765),
            (2, 1.2, False, "redondo", 680),
        ],
    )
    def test_calcular_precio_aplica_recargos(
        self, cajones, largo, iluminacion, forma, precio_esperado
    ):
        escritorio = Escritorio(
            "Escritorio",
            "Madera",
            "Natural",
            600,
            forma=forma,
            tiene_cajones=cajones > 0,
            num_cajones=cajones,
            largo=largo,
            tiene_iluminacion=iluminacion,
        )

        assert escritorio.calcular_precio() == precio_esperado

    def test_precio_base_none_se_convierte_en_cero(self):
        escritorio = Escritorio("Escritorio", "Madera", "Natural", None)

        assert escritorio.precio_base == 0
        assert escritorio.calcular_precio() == 0

    def test_obtener_descripcion_incluye_caracteristicas(self):
        escritorio = Escritorio(
            "Escritorio Ejecutivo",
            "Madera",
            "Negro",
            800,
            forma="ovalado",
            tiene_cajones=True,
            num_cajones=4,
            largo=1.8,
            tiene_iluminacion=True,
        )

        assert escritorio.obtener_descripcion() == (
            "Escritorio 'Escritorio Ejecutivo': Material=Madera, Color=Negro, "
            "Forma=ovalado, Cajones=4, Largo=1.8m, Iluminación=Sí, Precio base=$800"
        )
