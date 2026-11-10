import pytest

from src.models.concretos.silla import Silla


class TestSilla:
    @pytest.fixture
    def silla_basica(self):
        return Silla("Silla Básica", "Madera", "Natural", 50.0)

    def test_instanciacion_correcta(self, silla_basica):
        assert silla_basica.nombre == "Silla Básica"
        assert silla_basica.material == "Madera"
        assert silla_basica.color == "Natural"
        assert silla_basica.precio_base == 50.0
        assert silla_basica.capacidad_personas == 1
        assert silla_basica.tiene_respaldo is True
        assert silla_basica.altura_regulable is False
        assert silla_basica.tiene_ruedas is False

    def test_calcular_precio_sin_recargos(self, silla_basica):
        assert silla_basica.calcular_precio() == 55.0

    def test_calcular_precio_con_caracteristicas_adicionales(self):
        silla = Silla(
            "Silla de Oficina",
            "Metal",
            "Negro",
            100.0,
            tiene_respaldo=True,
            material_tapizado="Cuero",
            altura_regulable=True,
            tiene_ruedas=True,
        )

        assert silla.calcular_precio() == 180.0

    def test_obtener_descripcion_incluye_datos_principales(self):
        silla = Silla(
            "Silla Ejecutiva",
            "Metal",
            "Negro",
            100.0,
            material_tapizado="Tela",
            altura_regulable=True,
            tiene_ruedas=True,
        )

        descripcion = silla.obtener_descripcion()

        assert "Silla: Silla Ejecutiva" in descripcion
        assert "Material: Metal" in descripcion
        assert "Color: Negro" in descripcion
        assert "Capacidad: 1 personas" in descripcion
        assert "Tapizado: Tela" in descripcion
        assert "Altura regulable: Sí" in descripcion
        assert "Ruedas: Sí" in descripcion
        assert "Precio final: $170.0" in descripcion

    @pytest.mark.parametrize(
        ("altura", "resultado"),
        [
            (40, "Altura ajustada a 40 cm"),
            (100, "Altura ajustada a 100 cm"),
            (39, "La altura debe estar entre 40 y 100 cm"),
            (101, "La altura debe estar entre 40 y 100 cm"),
        ],
    )
    def test_regular_altura_valida_el_rango(self, altura, resultado):
        silla = Silla("Silla", "Madera", "Negro", 50.0, altura_regulable=True)

        assert silla.regular_altura(altura) == resultado

    def test_regular_altura_rechaza_silla_no_regulable(self, silla_basica):
        assert silla_basica.regular_altura(70) == (
            "Esta silla no tiene altura regulable"
        )

    def test_es_silla_oficina_solo_si_tiene_altura_y_ruedas(self):
        silla = Silla(
            "Silla Oficina",
            "Metal",
            "Negro",
            100.0,
            altura_regulable=True,
            tiene_ruedas=True,
        )

        assert silla.es_silla_oficina() is True

        silla.tiene_ruedas = False
        assert silla.es_silla_oficina() is False
