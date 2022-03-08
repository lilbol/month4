from rest_framework import serializers
from products.models import Product, Category, Review
from rest_framework.exceptions import ValidationError


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


# class ObjectCreateSerialize(serializers.Serializer):
#     name = serializers.CharField()
#     is_active = serializers.BooleanField()
class ReviewCreateSerialize(serializers.Serializer):
    stars = serializers.IntegerField(min_value=1, max_value=5)
    text = serializers.CharField(max_length=100)


class ProductCreatUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=2, max_length=10)
    description = serializers.CharField(required=False)
    price = serializers.FloatField()
    category_id = serializers.IntegerField()
    review = serializers.ListField(child=ReviewCreateSerialize())
    # list_ = serializers.ListField(child=serializers.CharField())
    # object_ = ObjectCreateSerialize()

    def validate_category_id(self, category_id):
        if Category.objects.filter(id=category_id).count() == 0:
            raise ValidationError(f'Category with id={category_id} not found!')
        return category_id

    # def validate(self, attrs):
    #     id = attrs['category_id']
    #     try:
    #         Category.objects.get(id=id)
    #     except Category.DoesNotExist:
    #         raise ValidationError(f'Category with id={id} not found!')
    #     return attrs
