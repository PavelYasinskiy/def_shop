from vk_maria import Vk, types
from vk_maria.dispatcher import Dispatcher
from vk_maria.dispatcher.fsm import StatesGroup, State, MemoryStorage, FSMContext
from vk_maria.upload import Upload
from decouple import config
from data_base.db_connector import create_database, show_unique_categories, show_items_in_category
from keyboards.keyboard_creations import category_keyboard, items_keyboard

token = config("TOKEN")

vk = Vk(access_token=token)
upload = Upload(vk)
dp = Dispatcher(vk, MemoryStorage())


class User_state(StatesGroup):
    category_selection: State
    item_selection: State


@dp.message_handler(text='Начать')
def start_message(event: types.MessageEvent):
    vk.messages_send(user_id=event.message.from_id,
                     message='Привет, sweety!\nЭто кондитерская. Выбирай категорию)',
                     keyboard=category_keyboard(show_unique_categories()))
    User_state.category_selection.set()


@dp.message_handler(state=User_state.category_selection)
def message_error(event: types.Message):
    vk.messages_send(user_id=event.message.from_id,
                     message='Пожалуйста, используйте кнопки',
                     keyboard=category_keyboard(show_unique_categories()))


@dp.message_handler(state=User_state.item_selection)
def message_error(event: types.Message):
    vk.messages_send(user_id=event.message.from_id,
                     message='Пожалуйста, используйте кнопки')


@dp.callback_handler(state=User_state.item_selection, payload={"command": "Back"})
def back_to_categories(event: types.MessageEvent, state: FSMContext):
    state.update_data(category=None, item=None)
    event.answer(event_data=vk.messages_edit(peer_id=event.peer_id,
                                             conversation_message_id=event.conversation_message_id,
                                             message="Выбирай категорию)",
                                             keyboard=category_keyboard(show_unique_categories())
                                             )
                 )
    User_state.category_selection.set()


@dp.callback_handler(state=User_state.category_selection)
def items_select(event: types.MessageEvent, state: FSMContext):
    state.update_data(category=event.payload, item_select=0)
    showing_item = show_items_in_category(event.payload)
    with open(showing_item[0][4], "rb") as file:
        photo = upload.photo(file)
    photo = upload.photo(open(showing_item[0][4], 'rb'))
    event.answer(event_data=vk.messages_edit(peer_id=event.peer_id,
                                             conversation_message_id=event.conversation_message_id,
                                             message=f"Название: {showing_item[0][1]}"
                                                     f"\n\nОписание: {showing_item[0][3]}",
                                             attachment=photo,
                                             keyboard=items_keyboard(showing_item, 0)
                                             )
                 )
    User_state.item_selection.set()


@dp.callback_handler(state=User_state.item_selection)
def items_select(event: types.MessageEvent, state: FSMContext):
    showing_item = show_items_in_category(state.get_data()["category"])
    item_selected = event.payload
    with open(showing_item[int(item_selected)][4], "rb") as file:
        photo = upload.photo(file)

    event.answer(event_data=vk.messages_edit(peer_id=event.peer_id,
                                             conversation_message_id=event.conversation_message_id,
                                             message=f"Название: {showing_item[int(item_selected)][1]}"
                                                     f"\n\nОписание: {showing_item[int(item_selected)][3]}",
                                             attachment=photo,
                                             keyboard=items_keyboard(showing_item, int(item_selected))
                                             )
                 )
    state.update_data(item_select=int(item_selected))

create_database()
dp.start_polling(debug=True)
