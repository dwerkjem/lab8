"""

Name: Derek R. Neilson

Description: Fountain View Hall event-booking collection manager

Program Design:
    Information collected:
        Client name and email, event name and type, guest count, estimated
        revenue per guest, start and end dates, catering selection, and
        deposit status.

    Information stored in lists:
        Every collected field, calculated fee, discount, final charge,
        booking status, and generated event code is stored in an event record.

    Lists used:
        The program uses one main list named event_records. Each item in that
        list is another list containing one complete event record.

    Calculations performed:
        Subtotal, weekend surcharge, premium-catering fee, wedding-cleanup
        fee, large-event discount, final charge, required deposit, total
        events, total guests, total revenue, average guests, and the largest
        and smallest events.

    Search options:
        Users can search by client name, event name, or event code.

    Modules used:
        client_info, event_info, pricing, records, models, constants, helpers,
        and main.

Business-rule assumptions:
    The weekend surcharge is $200 per weekend day. Premium catering costs $15
    per guest. Weddings receive a $250 cleanup fee. A deposit is 25% of the
    final charge. Events with at least 60 guests receive a 20% discount.
    Events exceeding 300 guests require manager approval. No holiday fee is
    charged; holidays are counted and displayed for informational purposes.

"""

from lists_.main import main

__all__ = ["main"]
