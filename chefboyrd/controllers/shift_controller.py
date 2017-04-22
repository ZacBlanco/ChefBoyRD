from chefboyrd.models.shifts import Shift

def getFreeShifts():
    """
    This method creates shifts by created an open shift.

    Args:
        shift_start_time: The start time of the shift
        shift_end_time: The end time of the shift
        role: the role that the person must have in order to claim the shift

    Returns: 
        N/A
    """
    free_shifts = []
    for free in Shift.select().where(Shift.name)
        free_shifts.append(free.Shift.id)
    return free_shifts