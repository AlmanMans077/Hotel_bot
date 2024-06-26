 Overview
This project is a Telegram bot designed for hotel room booking using the `aiogram` library for bot interactions and `sqlite3` for database management. The bot interacts with users to book rooms, view available rooms, and check existing bookings.

 Components
1. **Bot Logic (`bot.py`)**
2. **Database Logic (`db.py`)**
3. **Database File (`booking.db`)**

Bot Logic (`bot.py`)
The main logic for the Telegram bot is handled in the `bot.py` file. This file sets up the bot, defines various command handlers, and manages the flow of booking rooms and viewing bookings.

 Key Libraries and Components:
- **aiogram**: Used for creating and managing the Telegram bot.
  - **Bot** and **Dispatcher**: Classes for creating the bot and handling event dispatching.
  - **html**: Utilities for formatting HTML in messages.
  - **DefaultBotProperties**: Default settings for the bot.
  - **ParseMode**: Enum for parsing modes (e.g., HTML).
  - **CommandStart**: Filter for the `/start` command.
  - **Message**: Class for message handling.
  - **ReplyKeyboardMarkup**, **KeyboardButton**, **ReplyKeyboardRemove**: Classes for creating custom keyboards.
  - **FSMContext**: Context for managing finite state machine states.
  - **StatesGroup**, **State**: Classes for defining states.

#### Main Functions and Handlers:
- **command_start_handler**: Welcomes the user and provides the main menu options.
- **free_rooms_handler**: Lists all available rooms.
- **book_room_handler**: Initiates the room booking process.
- **process_room_selection**: Handles room selection by the user.
- **process_name**: Collects the user's name.
- **process_date**: Collects the booking date.
- **process_duration**: Collects the booking duration and finalizes the booking.
- **view_bookings_handler**: Initiates the booking view process.
- **process_booking_search**: Searches and displays bookings based on the user's name.

#### Finite State Machine (FSM) for Booking:
- **BookingForm**: Defines states for the booking process.
  - **waiting_for_room_selection**
  - **waiting_for_name**
  - **waiting_for_date**
  - **waiting_for_duration**
  - **waiting_for_booking_search**

#### Main Entry Point:
- **main**: Initializes the database, adds sample rooms, and starts the bot polling.

### Database Logic (`db.py`)
The database interactions are managed in the `db.py` file. This includes initializing the database, adding rooms and bookings, and querying data.

#### Key Functions:
- **init_db**: Initializes the database and creates tables if they do not exist.
- **add_booking**: Inserts a new booking into the `bookings` table.
- **add_room**: Inserts a new room into the `rooms` table.
- **get_all_rooms**: Retrieves all rooms from the `rooms` table.
- **get_bookings_by_name**: Retrieves bookings based on the user's name.

#### Database Schema:
- **rooms**: Stores room details.
  - **id** (INTEGER PRIMARY KEY)
  - **room_number** (TEXT)
  - **capacity** (INTEGER)
- **bookings**: Stores booking details.
  - **id** (INTEGER PRIMARY KEY)
  - **room_id** (INTEGER, FOREIGN KEY to `rooms`)
  - **name** (TEXT)
  - **date** (TEXT)
  - **duration** (INTEGER)

### Usage
1. **Set Up**:
   - Install necessary libraries: `pip install aiogram`
   - Ensure the `booking.db` file is in the same directory as your scripts.

2. **Running the Bot**:
   - Execute `bot.py` to start the bot.

3. **Interacting with the Bot**:
   - Use the `/start` command to begin interaction.
   - Use provided keyboard options to book rooms, view available rooms, and check bookings.

### Example
Here's a step-by-step example interaction with the bot:
1. Start the bot: `/start`
2. View available rooms: Click "Free Rooms"
3. Book a room: Click "Book Room"
   - Select a room
   - Enter your name
   - Enter the booking date
   - Enter the booking duration
4. View your bookings: Click "View Bookings"
