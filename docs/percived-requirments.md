## Final Cumulative Fountain View Hall Requirements

* Before coding, briefly document:

  * Information the program collects
  * Information stored in lists
  * Whether one or multiple lists will be used
  * Calculations performed
  * Information users can search for
  * Functions used to organize the program

* Process an unspecified number of event bookings until the user enters `"done"`.

* For each event, collect:

  * Client name and email
  * Event name/type
  * Guest count
  * Estimated revenue or pricing information
  * Weekend status
  * Standard or premium catering
  * Deposit status

* Store the collected event records in one or more lists.

* Format client names and event types in title case.

* Validate that email addresses contain both `@` and `.`.

* Generate an uppercase event code from the first three letters of the event type and client’s last name, such as `WED-JOH`.

* Deny bookings without a deposit.

* Require manager approval for events exceeding 300 guests.

* Apply:

  * Weekend surcharge
  * Premium-catering fee
  * Large-event discount
  * Automatic wedding cleanup fee

* Calculate the subtotal before discounts.

* Document reasonable assumptions for unspecified prices, fees, discounts, and thresholds.

* Display an approval or denial message and formatted summary for every booking.

* Each summary must include the client, email, event information, event code, guest count, selections, applied fees or discounts, and final charge.

* Use loops to process the stored records.

* Display every record entered.

* Calculate and display:

  * Total events
  * Total guests
  * Total revenue
  * Average guests per event
  * Largest value or event
  * Smallest value or event

* Allow the user to search for a stored client, event, or event code.

* Display whether the searched item was found.

* Use `if`, `elif`, and `else`, comparison operators, and logical operators.

* Use a `while` loop, sentinel value, counters, and accumulators.

* Organize the program into logical functions, including:

  * `get_client_information()`
  * `get_event_information()`
  * `calculate_event_charge()`
  * `calculate_deposit()`
  * `display_reservation_summary()`
  * `main()`

* At least two functions must accept parameters.

* At least three functions must return values.

* Use meaningful function and variable names.

* Comment the purpose of every function.

* Validate numeric input using `try/except`.

* Include at least two exception handlers.

* Use `raise` when a business rule is violated.

* Invalid input must not crash the program; reprompt until valid.

* Produce clear, consistently formatted output.

* Submit at least five test cases demonstrating:

  * Normal operation
  * Boundary or edge cases
  * Invalid input handling
  * Correct calculations
  * Correct program output

* Submit:

  * Brief program-design responses
  * Python source code
  * Test cases
  * A 3–4-minute code walkthrough video demonstrating the program and explaining its validation and processing logic
