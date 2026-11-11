import pytest

from src.models.concretos.armario import Armario


class TestArmario:
    @pytest.fixture
    def armario_basico(self):
        return Armario("Armario Principal", "Madera", "Blanco", 800)

    def test_instanciacion_correcta(self, armario_basico):
        assert armario_basico.nombre == "Armario Principal"
        assert armario_basico.material == "Madera"
        assert armario_basico.color == "Blanco"
        assert armario_basico.precio_base == 800
        assert armario_basico.num_puertas == 2
        assert armario_basico.num_cajones == 0
        assert armario_basico.tiene_espejos is False

    @pytest.mark.parametrize(
        ("puertas", "cajones", "espejos", "precio_esperado"),
        [
            (2, 0, False, 900),
            (3, 2, False, 1010),
            (4, 4, True, 1220),
        ],
    )
    def test_calcular_precio_aplica_componentes(
        self, puertas, cajones, espejos, precio_esperado
    ):
        armario = Armario(
            "Armario",
            "Madera",
            "Blanco",
            800,
            num_puertas=puertas,
            num_cajones=cajones,
            tiene_espejos=espejos,
        )

        assert armario.calcular_precio() == precio_esperado

    def test_precio_base_none_se_convierte_en_cero(self):
        armario = Armario("Armario", "Madera", "Blanco", None)

        assert armario.precio_base == 0
        assert armario.calcular_precio() == 100

    def test_obtener_descripcion_incluye_caracteristicas(self, armario_basico):
        assert armario_basico.obtener_descripcion() == (
            "Armario 'Armario Principal': Material=Madera, Color=Blanco, "
            "Puertas=2, Cajones=0, Espejos=No, Precio base=$800"
        )
