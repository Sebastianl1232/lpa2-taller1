import pytest

from src.models.concretos.mesa import Mesa


class TestMesa:
    @pytest.fixture
    def mesa_basica(self):
        return Mesa(
            "Mesa Comedor",
            "Roble",
            "Natural",
            200.0,
            forma="rectangular",
            largo=120.0,
            ancho=80.0,
            altura=75.0,
            capacidad_personas=4,
        )

    def test_instanciacion_correcta(self, mesa_basica):
        assert mesa_basica.nombre == "Mesa Comedor"
        assert mesa_basica.material == "Roble"
        assert mesa_basica.color == "Natural"
        assert mesa_basica.precio_base == 200.0
        assert mesa_basica.forma == "rectangular"
        assert mesa_basica.largo == 120.0
        assert mesa_basica.ancho == 80.0
        assert mesa_basica.altura == 75.0
        assert mesa_basica.capacidad_personas == 4

    def test_calcular_area_y_factor_de_tamano(self, mesa_basica):
        assert mesa_basica.calcular_area() == 9600.0
        assert mesa_basica.calcular_factor_tamaño() == pytest.approx(1.048)

    def test_calcular_precio_de_mesa_rectangular(self, mesa_basica):
        assert mesa_basica.calcular_precio() == 209.6

    @pytest.mark.parametrize(
        ("forma", "capacidad", "precio_esperado"),
        [
            ("redonda", 5, 309.6),
            ("cuadrada", 6, 309.6),
            ("ovalada", 8, 359.6),
        ],
    )
    def test_calcular_precio_aplica_recargos(
        self, mesa_basica, forma, capacidad, precio_esperado
    ):
        mesa_basica.forma = forma
        mesa_basica.capacidad_personas = capacidad

        assert mesa_basica.calcular_precio() == precio_esperado

    def test_obtener_descripcion_incluye_datos_de_la_mesa(self, mesa_basica):
        descripcion = mesa_basica.obtener_descripcion()

        assert "Mesa: Mesa Comedor" in descripcion
        assert "Material: Roble" in descripcion
        assert "Color: Natural" in descripcion
        assert "Forma: rectangular" in descripcion
        assert "Dimensiones: 120.0x80.0x75.0cm (Área: 9600.0cm²)" in descripcion
        assert "Capacidad: 4 personas" in descripcion
        assert "Precio final: $209.6" in descripcion

    @pytest.mark.parametrize(
        ("propiedad", "valor"),
        [
            ("largo", 0),
            ("ancho", -1),
            ("altura", 0),
            ("capacidad_personas", 0),
        ],
    )
    def test_propiedades_numericas_rechazan_valores_no_validos(
        self, mesa_basica, propiedad, valor
    ):
        with pytest.raises(ValueError):
            setattr(mesa_basica, propiedad, valor)

    def test_forma_rechaza_valores_no_validos(self, mesa_basica):
        with pytest.raises(ValueError):
            mesa_basica.forma = "triangular"
