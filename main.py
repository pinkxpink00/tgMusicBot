import asyncio


from aiogram import Bot,Dispatcher
from aiogram.filters import Command,CommandStart
from aiogram.types import Message


TOKEN = "7187016788:AAGmeE7OmOmtELfI8_67f9Fma_icDak-ciM"

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message)-> None:
    await message.answer("Hi")

async def main()-> None:
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
    print("bot working")