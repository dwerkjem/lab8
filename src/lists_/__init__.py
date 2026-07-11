"""
Name: Derek R. Neilson
Description: Fountain View Hall event-booking collection manager
"""

# Q: What information will the program collect?
# A:
# - Client name and email
# - Event name and type
# - Guest count
# - Estimated revenue and pricing information
# - Weekend status
# - Catering package
# - Deposit status


# Q: Which information will be stored in lists?
# A: All information for each event booking will be stored as a record
# inside the event_records list.


# Q: Will the solution require one list or multiple lists?
# A: The program will use one main list named event_records. Each item
# will be another list containing all information for one event.


# Q: What calculations will the program perform?
# A:
# - Calculate each event's subtotal
# - Add weekend, premium-catering, and wedding-cleanup fees
# - Apply large-event discounts
# - Calculate each event's final charge
# - Calculate total events, guests, and revenue
# - Calculate average guests per event
# - Determine the largest and smallest events


# Q: What value will the user be able to search for?
# A: The user will be able to search by event code, client name,
# or event name.


# Q: Which functions will organize the program?
# A:
# - get_client_information()
# - get_event_information()
# - calculate_event_charge()
# - calculate_deposit()
# - generate_event_code()
# - display_reservation_summary()
# - display_all_records()
# - search_records()
# - calculate_statistics()
# - main()


def main() -> None: ...
