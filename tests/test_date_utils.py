from datetime import date

from src.utils.date_utils import (
    business_days_between,
    is_valid_loan_duration,
    is_within_advance_limit,
    periods_overlap,
    is_overdue,
)


def test_dos_dias_habiles_exactos():
    # TC-08
    start = date(2026, 9, 7)   # lunes
    end = date(2026, 9, 9)     # miércoles

    assert business_days_between(start, end) == 2
    assert is_valid_loan_duration(start, end) is True


def test_supera_dos_dias_habiles():
    # TC-09
    start = date(2026, 9, 7)
    end = date(2026, 9, 10)

    assert business_days_between(start, end) == 3
    assert is_valid_loan_duration(start, end) is False


def test_fin_de_semana_no_cuenta_como_habil():
    start = date(2026, 9, 11)   # viernes
    end = date(2026, 9, 14)     # lunes

    assert business_days_between(start, end) == 1
    assert is_valid_loan_duration(start, end) is True


def test_fecha_devolucion_anterior():
    # TC-10
    start = date(2026, 9, 15)
    end = date(2026, 9, 14)

    assert is_valid_loan_duration(start, end) is False


def test_reserva_exactamente_30_dias_antes():
    today = date(2026, 9, 1)
    start = date(2026, 10, 1)

    assert is_within_advance_limit(
        start,
        today,
    ) is True


def test_reserva_supera_30_dias():
    today = date(2026, 9, 1)
    start = date(2026, 10, 2)

    assert is_within_advance_limit(
        start,
        today,
    ) is False


def test_periodos_superpuestos():
    # Parte de TC-14
    assert periods_overlap(
        date(2026, 9, 10),
        date(2026, 9, 11),
        date(2026, 9, 11),
        date(2026, 9, 12),
    ) is True


def test_periodos_no_superpuestos():
    assert periods_overlap(
        date(2026, 9, 10),
        date(2026, 9, 11),
        date(2026, 9, 12),
        date(2026, 9, 13),
    ) is False


def test_prestamo_atrasado():
    assert is_overdue(
        date(2026, 9, 5),
        "ENTREGADA",
        date(2026, 9, 6),
    ) is True


def test_prestamo_devuelto_no_esta_atrasado():
    assert is_overdue(
        date(2026, 9, 5),
        "DEVUELTA",
        date(2026, 9, 6),
    ) is False