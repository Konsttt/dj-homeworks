from django.shortcuts import render
from django.template import Context

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
    # можете добавить свои рецепты ;)
    'крутые_щи': {
        'мясо, кг': 1.5,
        'хрящи, г': 500,
        'картошка, шт': 5,
        'капуста, кг': 1,
        'лук, шт': 2,
        'зелень, г': 150,
        'морковь, шт': 2,
        'квашеная капуста, г': 500,
        'перец молотый, г': 5,
        'соль, г': 20,
        'лавровый лист, шт': 3,
    },
}


def get_recipe(request, recipe):
    x = DATA.get(recipe)  # x - вспомогательная переменная. Проверка на None, если нет запрошенного рецепта в DATA.
    if x:
        # Создаём новый словарь при каждом обновлении страницы(при каждом запросе).
        # Иначе, если указано кол-во порций в параметрах запроса, то при обновлении страницы всегда идёт умножение старого значения
        # Т.е. новый объект, вместо ссылки.
        ingredients = dict(x)
    else:
        ingredients = x  # ingredients = None
    servings = request.GET.get('servings')
    if servings and x:  # Если словарь пустой x=None, то умножать на кол-во порций не нужно.
        for key, value in ingredients.items():
            if type(value) == int:
                ingredients[key] = value * int(servings)
            else:
                ingredients[key] = round(value * int(servings), 2)
    context = {'ingredients': ingredients, 'recipe': recipe}
    return render(request, 'calculator/index.html', context)


# Добавил главную страницу, если нет полей в строке запроса.
def main_page(request):
    context = {'text': 'Текст главной страницы'}
    return render(request, 'calculator/main_page.html', context)
