# ItemGate Frontend

React + Vite фронтенд приложение для работы с товарами.

## Установка

```bash
npm install
```

## Разработка

```bash
npm run dev
```

Откроется на `http://localhost:3000`

## Сборка

```bash
npm run build
```

## Структура

```
src/
├── App.jsx              - Главный компонент
├── main.jsx             - Entry point
├── api/
│   └── client.js        - API клиент
├── components/
│   ├── ItemCard.jsx     - Карточка товара
│   └── ItemTabs.jsx     - Вкладки копирование/редактирование
└── styles/
    └── index.css        - Глобальные стили
```

## Функции

- ✅ Загрузка товаров из БД
- ✅ Поиск товаров
- ✅ Генерация SEO описания через ИИ
- ✅ Копирование описания и ключевых слов
- ✅ Редактирование товаров (в разработке)

## API Endpoints

- `GET /sima-land/get_items_sellers` - Получить все товары
- `POST /sima-land/search_item_to_word/{word}` - Поиск
- `POST /sima-land/ai_generate_desc_seller/{id_item}` - Генерировать
- `POST /sima-land/loading_words_db/{count}` - Загрузить товары
