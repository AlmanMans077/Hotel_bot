import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from db import init_db, add_booking, add_room, get_all_rooms, get_bookings_by_name


class BookingForm(StatesGroup):
    waiting_for_room_selection = State()
    waiting_for_name = State()
    waiting_for_date = State()
    waiting_for_duration = State()
    waiting_for_booking_search = State()


TOKEN = "7015850842:AAGR-UbVnwcZ9MisWVLrEkE7IuYIJqkVdX4"

dp = Dispatcher()

button_free_rooms = KeyboardButton(text='Free Rooms')
button_book_room = KeyboardButton(text='Book Room')
button_view_bookings = KeyboardButton(text='View Bookings')
keyboard_markup = ReplyKeyboardMarkup(keyboard=[[button_free_rooms, button_book_room], [button_view_bookings]], resize_keyboard=True)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        f"Hello, {html.bold(html.quote(message.from_user.full_name))}! Welcome to the hotel room booking service.",
        reply_markup=keyboard_markup
    )


@dp.message(lambda message: message.text == 'Free Rooms')
async def free_rooms_handler(message: Message) -> None:
    rooms = get_all_rooms()
    if rooms:
        rooms_list = "\n".join([f"Room {room[1]}, capacity: {room[2]}" for room in rooms])
        await message.answer(f"List of available rooms:\n{rooms_list}")
    else:
        await message.answer("There are no available rooms at the moment.")


@dp.message(lambda message: message.text == 'Book Room')
async def book_room_handler(message: Message, state: FSMContext) -> None:
    await message.answer("Select a room:", reply_markup=ReplyKeyboardRemove())
    rooms = get_all_rooms()
    if rooms:
        rooms_buttons = [KeyboardButton(text=f"Room {room[1]}") for room in rooms]
        rooms_keyboard = ReplyKeyboardMarkup(keyboard=[rooms_buttons], resize_keyboard=True)
        await message.answer("Select a room:", reply_markup=rooms_keyboard)
        await state.set_state(BookingForm.waiting_for_room_selection)
    else:
        await message.answer("There are no available rooms at the moment.")


@dp.message(BookingForm.waiting_for_room_selection)
async def process_room_selection(message: Message, state: FSMContext) -> None:
    selected_room_number = message.text.split(" ")[1]
    rooms = get_all_rooms()
    selected_room = next((room for room in rooms if room[1] == selected_room_number), None)
    if selected_room:
        await state.update_data(room_id=selected_room[0])
        await message.answer("Enter your name:", reply_markup=ReplyKeyboardRemove())
        await state.set_state(BookingForm.waiting_for_name)
    else:
        await message.answer("Invalid room number. Please try again.")


@dp.message(BookingForm.waiting_for_name)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await message.answer("Enter the booking date (DD.MM.YYYY format):")
    await state.set_state(BookingForm.waiting_for_date)


@dp.message(BookingForm.waiting_for_date)
async def process_date(message: Message, state: FSMContext) -> None:
    await state.update_data(date=message.text)
    await message.answer("Enter the booking duration (in days):")
    await state.set_state(BookingForm.waiting_for_duration)


@dp.message(BookingForm.waiting_for_duration)
async def process_duration(message: Message, state: FSMContext) -> None:
    await state.update_data(duration=message.text)
    user_data = await state.get_data()


    add_booking(user_data['room_id'], user_data['name'], user_data['date'], int(user_data['duration']))

    await message.answer(
        f"Booking completed!\n\n"
        f"Room: {html.bold(user_data['room_id'])}\n"
        f"Name: {html.bold(user_data['name'])}\n"
        f"Date: {html.bold(user_data['date'])}\n"
        f"Duration: {html.bold(user_data['duration'])} days",
        reply_markup=keyboard_markup
    )
    await state.clear()


@dp.message(lambda message: message.text == 'View Bookings')
async def view_bookings_handler(message: Message, state: FSMContext) -> None:
    await message.answer("Enter your name to search for bookings:")
    await state.set_state(BookingForm.waiting_for_booking_search)


@dp.message(BookingForm.waiting_for_booking_search)
async def process_booking_search(message: Message, state: FSMContext) -> None:
    bookings = get_bookings_by_name(message.text)
    if bookings:
        bookings_list = "\n\n".join([f"Booking ID: {booking[0]}\nRoom ID: {booking[1]}\nDate: {booking[3]}\nDuration: {booking[4]} days" for booking in bookings])
        await message.answer(f"Your bookings:\n\n{bookings_list}")
    else:
        await message.answer("No bookings found for this name.")


async def main() -> None:
    init_db()
    add_room("101", 2)
    add_room("102", 3)
    add_room("103", 2)
    add_room("104", 3)
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

