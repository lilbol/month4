from rest_framework import serializers
from products.models import Product, Category, Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    # category = CategorySerializer()
    category = serializers.SerializerMethodField()
    # reviews = ReviewSerializer(many=True)
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = 'id title price category reviews count_reviews  all_reviews'.split()

    def get_category(self, product):
        try:
            return product.category.name
        except:
            return 'No category'

    def get_reviews(self, product):
        serializers = ReviewSerializer(Review.objects.filter(author__isnull=False, product=product),
                                       many=True)
        return serializers.data