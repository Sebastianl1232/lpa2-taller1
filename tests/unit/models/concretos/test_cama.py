import pytest

from src.models.concretos.cama import Cama


class TestCama:
    @pytest.fixture
    def cama_basica(self):
        return Cama("Cama Individual", "Madera", "Blanco", 500.0)

    def test_instanciacion_correcta(self, cama_basica):
        assert cama_basica.nombre == "Cama Individual"
        assert cama_basica.material == "Madera"
        assert cama_basica.color == "Blanco"
        assert cama_basica.precio_base == 500.0
        assert cama_basica.tamaño == "individual"
        assert cama_basica.incluye_colchon is False
        assert cama_basica.tiene_cabecera is False

    @pytest.mark.parametrize(
        ("tamaño", "incluye_colchon", "tiene_cabecera", "precio_esperado"),
        [
            ("individual", False, False, 500.0),
            ("matrimonial", False, False, 700.0),
            ("queen", True, False, 1200.0),
            ("king", True, True, 1500.0),
        ],
    )
    def test_calcular_precio_aplica_tamano_y_extras(
        self, tamaño, incluye_colchon, tiene_cabecera, precio_esperado
    ):
        cama = Cama(
            "Cama",
            "Madera",
            "Blanco",
            500.0,
            tamaño=tamaño,
            incluye_colchon=incluye_colchon,
            tiene_cabecera=tiene_cabecera,
        )

        assert cama.calcular_precio() == precio_esperado

    def test_tamaño_rechaza_valores_no_validos(self, cama_basica):
        with pytest.raises(ValueError):
            cama_basica.tamaño = "doble"

    def test_obtener_descripcion_incluye_caracteristicas(self):
        cama = Cama(
            "Cama Queen",
            "Madera",
            "Gris",
            500.0,
            tamaño="queen",
            incluye_colchon=True,
            tiene_cabecera=True,
        )

        descripcion = cama.obtener_descripcion()

        assert "Cama: Cama Queen" in descripcion
        assert "Material: Madera" in descripcion
        assert "Color: Gris" in descripcion
        assert "Tamaño: queen" in descripcion
        assert "Incluye colchón: Sí" in descripcion
        assert "Cabecera: Sí" in descripcion
        assert "Precio final: $1300.0" in descripcion
