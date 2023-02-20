import sqlite3


def create_database() -> None:
    """
    Creating database and add info
    """

    with sqlite3.connect("data_base/my_shop.db") as shop_data:
        cur = shop_data.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS category (category_id INTEGER PRIMARY KEY,
                                                        category_name TEXT UNIQUE
                                                        )""")
        cur.execute("""CREATE TABLE IF NOT EXISTS items (item_id integer PRIMARY KEY,
                                                        item_name TEXT UNIQUE,
                                                        category INTEGER,
                                                        info TEXT,
                                                        photo TEXT,
                                                        FOREIGN KEY (category) REFERENCES category(category_id)
                                                        )""")

        try:
            insert_category = 'INSERT INTO category(category_name) VALUES(?)'
            insert_items = 'INSERT INTO items(item_name, category, info, photo) VALUES(?,?,?,?)'
            category_data = [
                ('Круассаны',),
                ('Булки',),
                ('Хлеб',),
                ('Торты',),
            ]
            cur.executemany(insert_category, category_data)
            items_data = [
                ("Круассан с малиной", 1, "Такие круассаны с малиной отлично подойдут в качестве завтрака или перекуса,"
                                          " подавать их можно с чашечкой чая или компота.", "media/1/11.jpeg"),
                ("Круассан с лососем", 1, "Ароматный свежевыпеченный круассан с малосолёным лососем, творожно-сливочным"
                                          " сыром, свежими огурчиками и пряной рукколой."
                                          " Для сытного завтрака и перекуса в течение дня — то, что нужно!",
                 "media/1/12.jpeg"),
                ("Круассан с шоколадом", 1, "Воздушные слоеные круассаны с шоколадом – один из самых популярных видов"
                                            " сладкой выпечки. Хрустящее слоеное дрожжевое тесто на сливочном масле,"
                                            " начинка из топленого шоколада и густая шоколадная посыпка сверху.",
                 "media/1/13.jpeg"),
                ("Круассан с сыром", 1, "Воздушный, мягкий, ароматный круассан с сырной начинкой и кунжутной посыпкой."
                                        " Изготовлен по традиционному французскому рецепту, на сливочном масле."
                                        " Круассан идеально дополнит завтрак или станет самостоятельным сытным "
                                        "перекусом.", "media/1/14.jpeg"),
                ("Булочка с маком", 2, "Мягкая сдобная булочка с маковой начинкой, "
                                       "изготовленная с добавлением цветочного мёда."
                                       " Классическое советское лакмоство к чаю и кофе.", "media/2/21.jpeg"),
                ("Булочка с повидлом", 2, "Сдобное булочное изделие, вырабатываемое из муки пшеничной высшего сорта"
                                          " с добавлением сахара, маргарина, молока сухого обезжиренного,"
                                          " ароматизатора «Ванилин» и другого сырья с начинкой из повидла."
                                          " Поверхность смазана яйцом куриным пищевым", "media/2/22.jpeg"),
                ("Булочка с мясом", 2, "Такими булочками не грех и домашних накормить, и друзей угостить.",
                 "media/2/23.jpeg"),
                ("Хлеб с отрубями", 3, "Хлеб с добавлением отрубей, твердой зерновой оболочки. Выпекается он из"
                                       " пшеничной муки, считается полезным и диетическим.", "media/3/31.jpeg"),
                ("Бородинский", 3, "Бородúнский хлеб — хлеб в виде небольшой буханки, который готовят из ржаной"
                                   " и пшеничной муки, солода, патоки, сахара,"
                                   " закваски и приправ – кориандра и тмина.", "media/3/32.jpeg"),
                ("Батон нарезной", 3, "Батон Нарезной является классикой советского и постсоветского пространства,"
                                      " румяная продолговатая булка с аппетитными диагональными надрезами на верхней"
                                      " корочке знакома всем поколениям.", "media/3/33.jpeg"),
                ("Наполеон", 4, "Наши кондитеры готовят «Наполеон» по классическому рецепту: из тончайших коржей,"
                                " смазанных нежным сливочно-заварным кремом."
                                " Воздушный десерт украшают шапкой из слоёной крошки и сахарной пудры.",
                 "media/4/41.jpeg"),
                ("Медовик", 4, "Настоящий медовый торт, отличающийся особым вкусом – нежным, изысканным,"
                               " но при этом абсолютно не приторным", "media/4/42.jpeg"),
                ("Йогуртовый", 4, "Йогуртовый торт – отличный вариант легкого и вкусного десерта. ", "media/4/43.jpeg"),
                ("Чизкейк", 4, "Настоящая американская классика — нежный чизкейк из сливочно-творожной начинки "
                               "с ванильной ноткой на тонкой песочно-миндальной подложке.", "media/4/44.jpeg"),
                ("Маковый", 4, "Маковый торт — это торт из мягких бисквитных коржей с нежной кремовой прослойкой.",
                 "media/4/45.jpeg")
            ]
            cur.executemany(insert_items, items_data)
        except sqlite3.IntegrityError:
            pass
        finally:
            shop_data.commit()


def show_unique_categories() -> list:

    with sqlite3.connect("data_base/my_shop.db") as shop_data:
        cur = shop_data.cursor()
        cur.execute("""SELECT *  FROM category""")
        categories = cur.fetchall()
        return categories


def show_items_in_category(category_id: int) -> list[tuple, ...]:

    with sqlite3.connect("data_base/my_shop.db") as shop_data:
        cur = shop_data.cursor()
        cur.execute(f"""SELECT * FROM items WHERE category = {category_id}""")
        items = cur.fetchall()
        return items