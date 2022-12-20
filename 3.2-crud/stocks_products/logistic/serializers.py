from rest_framework import serializers

from logistic.models import Product, StockProduct, Stock


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['address', 'positions']

    # Добавление нового склада и новых позиций продуктов на этом складе.
    # POST json запрос содержит address и список positions[{product, quantity, price},...,]
    # если список позиций продуктов пустой, то создаётся только склад
    def create(self, validated_data):
        positions = validated_data.pop('positions')
        stock = super().create(validated_data)
        for position in positions:
            StockProduct.objects.create(stock=stock, **position)
        return stock

    # Изменение позиций на складе работает так:
    # 1) Если есть позиция address, то меняется address данного склада
    # 2) в цикле ищется на данном складе, очередной указанный в json продукты
    # 3) если продукт есть на данном складе, то обновляется информация по данному продукту (кол-во, цена)
    # 4) если таких продуктов на складе нет, то создаются новые записи этих продуктов для данного склада.
    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')
        stock = super().update(instance, validated_data)  # Если в UPDATE json запросе есть address, то обновится.
        for position in positions:
            product = position['product']
            position_stock_product = StockProduct.objects.filter(stock=stock, product=product)
            if position_stock_product.exists():
                update_position = position_stock_product.first()
                update_position.quantity = position['quantity']
                update_position.price = position['price']
                update_position.save()
            else:
                StockProduct.objects.create(stock=stock, **position)
        return stock


#####################################################################################################################
''' Ниже добавил класс для детального отображения /stocks/, чтобы при выводе stocks отображались не id-шники продуктов,
 а вся информация: id, title, description. Для этого использовал depth=1

 Сначала поставил depth=1 и радовался красивым выводам при GET,
 Затем поломал очень много копий с запросами POST/PUT!!111,
 т.к. validated_data - не содержала в себе "product" и это связано с depth=1,
 т.е. в POST request-е "product" присутствует, но метод .is_valid() его не пропускает.
 В общем с depth=1 работает только метод GET.

Эту проблему большинство решает добавлением отдельного detail класса и обработку во ViewSet-е.
https://stackoverflow.com/questions/15883678/django-rest-framework-different-depth-for-post-put'''


# Ниже два класса сделал дополнительно, чтобы был красивый вложенный вывод /stocks/ c названием продуктов.
# Этот код будет работать только для GET запросов.
class ProductDetailPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['id', 'product', 'quantity', 'price']
        depth = 1


class StockDetailSerializer(serializers.ModelSerializer):
    positions = ProductDetailPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['address', 'positions']
