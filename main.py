import os
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Book, Shop, Stock, Sale
from sqlalchemy import create_engine
from dotenv import load_dotenv
import json

load_dotenv()


class Database():

    def __init__(self):

        dialect = str(input('Введите тип базы данных для подключения: \n'
                            'postgresql \n'
                            'mysql \n'
                            'sqlite'
                            )
                      )

        if dialect == 'postgresql':
            login = os.getenv('POSTGRESQL_LOGIN')
            password = os.getenv('POSTGRESQL_PASSWORD')
            print('Лог и пароль переданы')
        elif dialect == 'mysql':
            login = os.getenv('MYSQL_LOGIN')
            password = os.getenv('MYSQL_PASSWORD')
        elif dialect == 'sqlite /n':
            login = os.getenv('SQLITE_LOGIN')
            password = os.getenv('SQLITE_PASSWORD')
        self.engine = create_engine(f"{dialect}://{login}:{password}@localhost:5432/netology_db")
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def create_tables(self):
        create_tables(self.engine)
        print('таблицы созданы')

    def check(self):
        for c in self.session.query(Publisher).all():
            print(c)

        for c in self.session.query(Book).all():
            print(c)

        for c in self.session.query(Shop).all():
            print(c)

        for c in self.session.query(Stock).all():
            print(c)

        for c in self.session.query(Sale).all():
            print(c)

        self.session.close()

    def fill_db_from_json(self):
        with open('tests_data.json', encoding='utf-8') as f:
            json_data = json.load(f)

        for i in json_data:
            if i.get('model') == 'publisher' and i.get('fields').get('name'):
                try:
                    arg = i.get('fields').get('name')
                    arg2 = i.get('pk')
                    pn = Publisher(id=arg2, name=arg)
                    self.session.add(pn)
                    self.session.commit()
                    self.session.close()
                except:
                    pass

            elif i.get('model') == 'book':
                try:
                    arg = i.get('pk')
                    arg2 = i.get('fields').get('title')
                    arg3 = i.get('fields').get('id_publisher')
                    bt1 = Book(id=arg, title=arg2, id_publisher=arg3)
                    self.session.add(bt1)
                    self.session.commit()
                    self.session.close()
                except:
                    pass

            elif i.get('model') == 'shop':
                try:
                    arg = i.get('pk')
                    arg2 = i.get('fields').get('name')
                    sh1 = Shop(id=arg, name=arg2)
                    self.session.add(sh1)
                    self.session.commit()
                    self.session.close()
                except:
                    pass

            elif i.get('model') == 'stock':
                try:
                    arg = i.get('pk')
                    arg2 = i.get('fields').get('id_book')
                    arg3 = i.get('fields').get('id_shop')
                    arg4 = i.get('fields').get('count')
                    st1 = Stock(id=arg, id_book=arg2, id_shop=arg3, count=arg4)
                    self.session.add(st1)
                    self.session.commit()
                    self.session.close()
                except:
                    pass

            elif i.get('model') == 'sale':
                try:
                    arg = i.get('pk')
                    arg2 = i.get('fields').get('price')
                    arg3 = i.get('fields').get('date_sale')
                    arg4 = i.get('fields').get('id_stock')
                    arg5 = i.get('fields').get('count')
                    sa1 = Sale(id=arg, price=arg2, date_sale=arg3, id_stock=arg4, count=arg5)
                    self.session.add(sa1)
                    self.session.commit()
                    self.session.close()
                except:
                    pass

    def show_publisher_shop(self):
        publisher = input('По какому издателю Вы бы хотели получить информацию?: ')
        selected = self.session.query(Book.title, Shop.name, Sale.price, Sale.date_sale)\
            .join(Publisher).join(Stock).join(Shop).join(Sale).filter(Publisher.name.like(publisher))
        for c in selected.all():
            print(f'{c[0]} | {c[1]} | {str(c[2])} | {str(c[3][:10])}')

    def get_shops(self, publisher):
        selection = self.session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).select_from(Shop).\
            join(Stock).\
            join(Book).\
            join(Publisher).\
            join(Sale)
        if publisher.isdigit():
            res = selection.filter(Publisher.id == publisher).all()
        else:
            res = selection.filter(Publisher.name == publisher).all()
        for title, name, price, date_sale in res:
            print(f'{title: <40} | {name: <10} | {price: <8} | {date_sale.strftime("%d-%m-%Y")}')

    def delete(self):
        self.session.query(Sale).delete()
        self.session.query(Stock).delete()
        self.session.query(Shop).delete()
        self.session.query(Book).delete()
        self.session.query(Publisher).delete()
        self.session.commit()
        self.session.close()



# db = Database()

# db.delete()
# db.create_tables()
# db.fill_db_from_json()
# db.check()
# db.show_publisher_shop()

if __name__ == '__main__':
    db = Database()
    publisher = input('Введите имя или ID издателя для поиска магазина: ')
    db.get_shops(publisher)