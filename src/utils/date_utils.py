from datetime import date, timedelta


def is_business_day(day: date) -> bool:
    """
    Considera hábiles de lunes a viernes.
    No considera feriados.
    """
    return day.weekday() < 5


def business_days_between(
    start_date: date,
    return_date: date,
) -> int:
    """
    Cuenta los días hábiles posteriores a la fecha de inicio
    hasta la fecha de devolución, incluyendo esta última.

    Ejemplo:
    lunes -> martes = 1 día hábil
    lunes -> miércoles = 2 días hábiles
    viernes -> lunes = 1 día hábil
    """
    if return_date <= start_date:
        return 0

    current_date = start_date + timedelta(days=1)
    business_days = 0

    while current_date <= return_date:
        if is_business_day(current_date):
            business_days += 1

        current_date += timedelta(days=1)

    return business_days


def is_valid_loan_duration(
    start_date: date,
    return_date: date,
    max_business_days: int = 2,
) -> bool:
    """
    RN-02 / RN-11

    La devolución debe ser posterior al inicio
    y no superar 2 días hábiles.
    """
    if return_date <= start_date:
        return False

    duration = business_days_between(
        start_date,
        return_date,
    )

    return 1 <= duration <= max_business_days


def is_within_advance_limit(
    start_date: date,
    current_date: date | None = None,
    max_days: int = 30,
) -> bool:
    """
    RN-03

    La reserva no puede comenzar en el pasado
    ni con más de 30 días corridos de anticipación.
    """
    if current_date is None:
        current_date = date.today()

    difference = (start_date - current_date).days

    return 0 <= difference <= max_days


def periods_overlap(
    start_a: date,
    end_a: date,
    start_b: date,
    end_b: date,
) -> bool:
    """
    RN-04

    Dos períodos se superponen si comparten
    al menos una fecha.
    """
    return start_a <= end_b and start_b <= end_a


def is_overdue(
    return_date: date,
    status: str,
    current_date: date | None = None,
) -> bool:
    """
    RN-12

    Un préstamo está atrasado si:
    - sigue ENTREGADO;
    - su fecha de devolución ya venció.
    """
    if current_date is None:
        current_date = date.today()

    return (
        status == "ENTREGADA"
        and current_date > return_date
    )