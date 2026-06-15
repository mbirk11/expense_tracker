from rest_framework import serializers

from .models import Category, Expense


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]
        read_only_fields = ["id"]


class ExpenseSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source="category.name",
        read_only=True
    )

    class Meta:
        model = Expense
        fields = [
            "id",
            "category",
            "category_name",
            "title",
            "amount",
            "date",
            "description",
        ]
        read_only_fields = ["id"]

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Amount must be greater than 0."
            )
        return value

    def validate_category(self, value):
        request = self.context.get("request")

        if request and value.user != request.user:
            raise serializers.ValidationError(
                "You can only use your own categories."
            )

        return value