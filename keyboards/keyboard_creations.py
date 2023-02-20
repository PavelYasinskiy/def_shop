from vk_maria.types import KeyboardMarkup, Button, Color


def category_keyboard(categories_list):
    count = 0
    kboard = KeyboardMarkup(inline=True)
    for category_id, name in categories_list:
        kboard.add_button(Button.Callback(Color.PRIMARY, f'{name}', payload=f"{category_id}"))
        count += 1
        if count == 2:
            kboard.add_row()
            count = 0

    return kboard


def items_keyboard(items_list, item_now):

    kboard = KeyboardMarkup(inline=True)
    back_item = items_list[item_now-1]
    if len(items_list) == (item_now+1):
        forward_item = items_list[0]
    else:
        forward_item = items_list[item_now+1]

    kboard.add_button(Button.Callback(Color.PRIMARY, f'<<<Назад', payload=f"{items_list.index(back_item)}"))
    kboard.add_button(Button.Callback(Color.PRIMARY, f'Вперед>>>', payload=f"{items_list.index(forward_item)}"))
    kboard.add_row()
    kboard.add_button(Button.Callback(Color.NEGATIVE, 'Выбрать категорию', payload={"command": 'Back'}))
    return kboard
