from .models import Slot
from datetime import datetime

import logging

logging.basicConfig(filename='scheduler.log', filemode='a',
                    format='%(name)s - %(levelname)s - %(message)s\n',
                    level=logging.INFO)


# this function updates slots everyday at 00:00 am
def update_slots():
    logging.info(f"\nAction: Reset Room Slots is_available to True\nLog Time: {datetime.now().time()}")
    slots = Slot.objects.all()
    for slot in slots:
        if not slot.is_available:
            logging.info(
                f"\nRoom name: {slot.room.name}"
                f"\nSlot start time: {slot.start_time}"
                f"\nSlot end time: {slot.start_time}"
                f"\nSlot Booked by User: {slot.booked_by}"
            )
            slot.is_available = True
            slot.booked_by = None
            print(f"Setting is_available of Slot {slot.id} of Room {slot.room.id} "
                  f"to True")
            slot.save()
