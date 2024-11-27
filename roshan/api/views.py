from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, \
    DestroyAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated , IsAdminUser
from rest_framework import status
from .models import Product , Category , CartItem , Cart
from .serializers import ProductSerializer , CategorySerializer , CartItemSerializer , CartSerializer
from rest_framework.exceptions import NotFound , PermissionDenied

class ProductsList(ListCreateAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [IsAuthenticated()]


class ProductUpdate(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def retrieve(self, request, *args, **kwargs):

        instance = self.get_object()
        instance.visits += 1
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class CategoryList(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [IsAuthenticated()]

class CategoryUpdate(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]


class CategoryProductList(ListCreateAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        category_id = self.kwargs['id']
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise NotFound("Category not found.")

        return Product.objects.filter(category=category)

    def perform_create(self, serializer):
        category_id = self.kwargs['id']
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise NotFound("Category not found.")

        if not self.request.user.is_staff:
            raise PermissionDenied("Unauthorized Access!")

        serializer.save(category=category)

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method == 'POST':
            return [IsAdminUser()]
        return []


class CartAddProduct(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer

    def perform_create(self, serializer):
        product_id = self.kwargs['product_id']
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise NotFound("Product not found")

        cart, created = Cart.objects.get_or_create(user=self.request.user)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            #as cart will only accept one quantity , this line exists
            return Response(
                {"detail": "Product is already in the cart."},
                status=status.HTTP_200_OK
            )

        #couldnt resolve "quantity" bug , so hard coded it to 1
        cart_item.quantity = 1
        cart_item.save()

        return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)


class CartRemoveProduct(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        product_id = self.kwargs['product_id']
        try:
            cart = Cart.objects.get(user=self.request.user)
        except Cart.DoesNotExist:
            raise NotFound("Cart not found")

        try:
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
        except CartItem.DoesNotExist:
            raise NotFound("Product not in cart")

        return cart_item

    def perform_destroy(self, instance):
        instance.delete()


class CartList(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_object(self):
        try:
            return Cart.objects.get(user=self.request.user)
        except Cart.DoesNotExist:
            raise NotFound("Cart not found")


class CartClear(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return Cart.objects.get(user=self.request.user)
        except Cart.DoesNotExist:
            return None

    def perform_destroy(self, instance):
        if instance:
            instance.items.all().delete()

    def delete(self, request, *args, **kwargs):
        cart = self.get_object()
        if cart is None:
            return Response({"detail": "Cart is empty."}, status=status.HTTP_200_OK)

        self.perform_destroy(cart)
        return Response({"detail": "Cart got cleared."}, status=status.HTTP_204_NO_CONTENT)

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response


#not my code
class TokenWithCookieView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        data = response.data
        access_token = data.get('access')
        refresh_token = data.get('refresh')

        # Set tokens in cookies
        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=False,  # Use True in production
            samesite='Lax'
        )
        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            httponly=True,
            secure=False,  # Use True in production
            samesite='Lax'
        )
        return response


class TokenRefreshWithCookieView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        access_token = response.data.get('access')

        # Update access token in cookies
        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=False,  # Use True in production
            samesite='Lax'
        )
        return response

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response({'message': 'Logged out successfully'})
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response