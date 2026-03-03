from io import BytesIO
from django.http import FileResponse, HttpResponse
from rest_framework import status, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import login, logout
from rest_framework.renderers import BaseRenderer
from config import settings
from users.price_estimator import PriceEstimator
from .models import User, WorkOrderPriceEstimate
from .models import WorkOrder, Country, MasterSKUMapping
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    UserLoginSerializer,
    ChangePasswordSerializer,
    UserUpdateSerializer,
    CountrySerializer
)
import os


class UserRegistrationView(generics.CreateAPIView):
    """
    API endpoint for user registration
    POST /api/auth/register/
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        return Response({
            'user': UserSerializer(user).data,
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    """
    API endpoint for user login with session authentication
    POST /api/auth/login/
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = UserLoginSerializer
    
    def post(self, request):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        login(request, user)
        
        return Response({
            'user': UserSerializer(user).data,
            'message': 'Login successful'
        }, status=status.HTTP_200_OK)


class UserLogoutView(APIView):
    """
    API endpoint for user logout
    POST /api/auth/logout/
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        logout(request)
        return Response({
            'message': 'Logout successful'
        }, status=status.HTTP_200_OK)


class CurrentUserView(generics.RetrieveUpdateAPIView):
    """
    API endpoint to get and update current user's profile
    GET /api/auth/user/
    PUT /api/auth/user/
    PATCH /api/auth/user/
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserSerializer


class ChangePasswordView(APIView):
    """
    API endpoint for changing password
    POST /api/auth/change-password/
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            'message': 'Password changed successfully'
        }, status=status.HTTP_200_OK)


class UserListView(generics.ListAPIView):
    """
    API endpoint to list all users (admin only)
    GET /api/auth/users/
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint to retrieve, update, or delete a specific user (admin only)
    GET /api/auth/users/<id>/
    PUT /api/auth/users/<id>/
    DELETE /api/auth/users/<id>/
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class CountryListView(generics.ListAPIView):
    """
    API endpoint to list all countries for frontend use
    GET /api/auth/countries/
    """
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [permissions.IsAuthenticated]
    # Return full list (no pagination) so frontend gets an array
    pagination_class = None


class CountrySKUView(APIView):
    """Return primary and additional SKU lists for a country code.

    GET /api/auth/countries/<code>/skus/
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, code):
        try:
            country = Country.objects.get(code__iexact=code)
        except Country.DoesNotExist:
            return Response({'detail': 'Country not found'}, status=status.HTTP_404_NOT_FOUND)

        def to_obj(m):
            return {
                'id': m.id,
                'master_sku_name': m.master_sku_name,
                'partner_sku_name': m.partner_sku_name,
                'sku_type': m.sku_type,
            }

        primary_list = [to_obj(m) for m in country.primary_skus.all()]
        additional_list = [to_obj(m) for m in country.additional_skus.all()]

        return Response({
            'primary_skus': primary_list,
            'additional_skus': additional_list,
        }, status=status.HTTP_200_OK)


class CountrySKUManageView(APIView):
    """Add or remove MasterSKUMapping instances to/from a Country's SKU lists.

    POST /api/auth/countries/<code>/skus/manage/

    Body JSON: { sku_id: <int>, sku_type: 'primary'|'additional', action: 'add'|'remove' }
    """
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, code):
        try:
            country = Country.objects.get(code__iexact=code)
        except Country.DoesNotExist:
            return Response({'detail': 'Country not found'}, status=status.HTTP_404_NOT_FOUND)

        sku_id = request.data.get('sku_id')
        sku_type = (request.data.get('sku_type') or 'primary').lower()
        action = (request.data.get('action') or '').lower()

        if not sku_id:
            return Response({'detail': 'sku_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            sku = MasterSKUMapping.objects.get(pk=int(sku_id))
        except Exception:
            return Response({'detail': 'Master SKU not found'}, status=status.HTTP_404_NOT_FOUND)

        if sku_type not in ('primary', 'additional'):
            return Response({'detail': 'sku_type must be primary or additional'}, status=status.HTTP_400_BAD_REQUEST)

        if action not in ('add', 'remove'):
            return Response({'detail': "action must be 'add' or 'remove'"}, status=status.HTTP_400_BAD_REQUEST)

        field = country.primary_skus if sku_type == 'primary' else country.additional_skus

        if action == 'add':
            field.add(sku)
        else:
            field.remove(sku)

        # return updated lists (same format as CountrySKUView)
        def to_obj(m):
            return {
                'id': m.id,
                'master_sku_name': m.master_sku_name,
                'partner_sku_name': m.partner_sku_name,
                'sku_type': m.sku_type,
            }

        primary_list = [to_obj(m) for m in country.primary_skus.all()]
        additional_list = [to_obj(m) for m in country.additional_skus.all()]

        return Response({'primary_skus': primary_list, 'additional_skus': additional_list}, status=status.HTTP_200_OK)
    

class IsOwnerOrAdmin(permissions.BasePermission):
    """Object-level permission to allow only owners or staff to edit/delete."""

    def has_object_permission(self, request, view, obj):
        # staff can do anything
        if request.user and request.user.is_staff:
            return True
        # owner can act on their object
        return getattr(obj, 'created_by', None) == request.user


class WorkOrderListCreateView(generics.ListCreateAPIView):
    """List work orders (user-only) and create new work orders."""
    serializer_class = None
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        from .serializers import WorkOrderSerializer
        return WorkOrderSerializer
    
    def get_queryset(self):
        if self.request.user.is_staff:
            work_orders = WorkOrder.objects.all()
        else:
            work_orders = WorkOrder.objects.filter(created_by=self.request.user)
        # send country name along with each work order
        for wo in work_orders:
            wo.country_name = wo.country.name if wo.country else ''
        return work_orders

    def perform_create(self, serializer):
        data = self.request.data
        country_obj = None
        country_val = data.get('country')
        if country_val:
            try:
                if isinstance(country_val, str) and not country_val.isdigit():
                    country_obj = Country.objects.get(code__iexact=country_val)
                else:
                    country_obj = Country.objects.get(id=int(country_val))
            except Exception:
                country_obj = None
        
        # Save and capture instance; ensure created_by set defensively.
        instance = serializer.save(created_by=self.request.user, country=country_obj)
        if not getattr(instance, 'created_by', None):
            instance.created_by = self.request.user
            instance.save()

    def create(self, request, *args, **kwargs):
        """
        Override to surface serializer errors in logs for debugging (DRF will still return 400 with details).
        """
        # reference unused params to silence static checks
        _ = args
        _ = kwargs

        # make a mutable copy of input data
        try:
            data = request.data.copy()
        except Exception:
            data = dict(request.data)

        print("Received work order data:\n", data)
        country_obj = None
        country_val = data.get('country')
        if country_val:
            try:
                if isinstance(country_val, str) and not country_val.isdigit():
                    country_obj = Country.objects.get(code__iexact=country_val)
                else:
                    country_obj = Country.objects.get(id=int(country_val))
            except Exception:
                country_obj = None
        
        if country_obj:
            try:
                data['country'] = int(country_obj.id)
            except Exception:
                data['country'] = country_obj.id

        # Helper to map incoming sku entries (could be dicts like {sku, qty} or plain strings)
        def map_sku_list(input_list, expected_type):
            if not input_list:
                return []
            pks = []
            for item in input_list:
                sku_entry = {}
                if isinstance(item, dict):
                    raw_sku = item.get('sku')
                    sku_entry['qty'] = item.get('qty') or item.get('quantity') or 1
                else:
                    raw_sku = item
                    sku_entry['qty'] = 1

                # resolve raw_sku (could be pk, numeric string, master name, or partner name)
                sku_pk = None
                try:
                    if isinstance(raw_sku, int) or (isinstance(raw_sku, str) and raw_sku.isdigit()):
                        sku_pk = int(raw_sku)
                    else:
                        # try by master_sku_name
                        m = MasterSKUMapping.objects.filter(master_sku_name__iexact=raw_sku).first()
                        if not m:
                            # try partner mapping name
                            m = MasterSKUMapping.objects.filter(partner_mapping__partner_sku_name__iexact=raw_sku).first()
                        if m:
                            sku_pk = m.pk
                except Exception:
                    sku_pk = None

                if sku_pk is None:
                    # unknown SKU, skip
                    continue

                sku_entry['sku'] = sku_pk
                pks.append(sku_entry)
            return pks

        primary_in = data.get('primary_skus') or []
        additional_in = data.get('additional_skus') or []

        data['primary_skus'] = map_sku_list(primary_in, 'Primary')
        data['additional_skus'] = map_sku_list(additional_in, 'Additional')

        serializer = self.get_serializer(data=data, context={'request': request})
        if not serializer.is_valid():
            print("WorkOrder create validation failed: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_create(serializer)
        created_instance = getattr(serializer, 'instance', None)
        if created_instance is not None:
            resp_serializer = self.get_serializer(created_instance)
            return Response(resp_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class WorkOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a work order. Only owner or staff allowed."""
    serializer_class = None
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'Work order deleted'}, status=status.HTTP_200_OK)
         
    def get_serializer_class(self):
        from .serializers import WorkOrderSerializer
        return WorkOrderSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return WorkOrder.objects.all()
        return WorkOrder.objects.filter(created_by=self.request.user, is_active=True)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data.copy() if hasattr(request.data, 'copy') else dict(request.data)
        country_val = data.get('country')
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def get(self, request, pk, *args, **kwargs):
        obj = WorkOrder.objects.filter(pk=pk).select_related('country', 'created_by').first()
        if not obj:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        if not (request.user.is_staff or (obj.created_by_id and obj.created_by_id == request.user.id)):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(obj)
        data = dict(serializer.data)

        def build_sku_list(owner_obj, primary=True):
            items = []
            try:
                qs = []
                if primary:
                    if hasattr(owner_obj, 'primary_sku_items'):
                        qs = owner_obj.primary_sku_items.select_related('sku').all()
                else:
                    if hasattr(owner_obj, 'additional_sku_items'):
                        qs = owner_obj.additional_sku_items.select_related('sku').all()

                for it in qs:
                    sku_obj = it.sku
                    qty = getattr(it, 'quantity', None)
                    item = {
                        'sku_name': getattr(sku_obj, 'master_sku_name', '') or '',
                        'qty': int(qty) if qty is not None else None
                    }
                    items.append(item)
            except Exception:
                # defensive: return what we have if relation not available
                pass
            return items

        data['primary_skus'] = build_sku_list(obj, primary=True)
        data['additional_skus'] = build_sku_list(obj, primary=False)

        return Response(data, status=status.HTTP_200_OK)


class WorkOrderPriceEstimateView(APIView):
    """Calculate price estimate for a given work order."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        obj = WorkOrder.objects.filter(pk=pk).select_related('country', 'created_by').first()
        if not obj:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        estimator = PriceEstimator(obj)
        wo_price_estimator_file_name = estimator.estimate_price()
        print(f'User {request.user.email} requested price estimate for WorkOrder {obj.work_order_number}, generated file: {wo_price_estimator_file_name}')
        # save work order price estimate record
        WorkOrderPriceEstimate.objects.create(
            workorder=obj,
            file_name=wo_price_estimator_file_name,
            created_by=request.user
        )
        return Response({
            'file_name': wo_price_estimator_file_name
        }, status=status.HTTP_200_OK)


class BinaryFileRenderer(BaseRenderer):
    media_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    format = 'xlsx'
    charset = None
    render_style = 'binary'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data
    
class WorkOrderPriceEstimateDownloadView(APIView):
    """Download price estimate file for a given work order."""
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [BinaryFileRenderer]

    def get(self, request):
        """
        GET /api/auth/workorders/price-estimate/download/?file_name=... [&workorder=<id>]

        Returns JSON with file_url. If workorder id is provided, validate existence and permissions.
        """
        file_name = request.query_params.get('file_name')
        # print(f">>>>  Received request to download price estimate file: {file_name}")
        if not file_name:
            return HttpResponse(
                '{"detail": "file_name query parameter is required"}',
                content_type='application/json',
                status=400
            )
        
        # optional workorder id for permission check
        workorder_id = request.query_params.get('workorder') or request.query_params.get('pk')
        if workorder_id:
            try:
                wk_id = int(workorder_id)
                obj = WorkOrder.objects.filter(pk=wk_id).select_related('country', 'created_by').first()
                if not obj:
                    return HttpResponse('{"detail": "WorkOrder not found."}', content_type='application/json', status=404)
                if not (request.user.is_staff or (obj.created_by_id and obj.created_by_id == request.user.id)):
                    return HttpResponse('{"detail": "Permission denied."}', content_type='application/json', status=403)
            except (ValueError, TypeError):
                return HttpResponse('{"detail": "Invalid workorder id"}', content_type='application/json', status=400)

        # file_path = f'price_estimates/{file_name}'
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        response = FileResponse(
            open(file_path, "rb"),
            as_attachment=True,
            filename=file_name,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        return response


class WorkOrderPriceEstimateListView(APIView):
    """List generated price estimator files available to the current user.

    GET /api/auth/workorders/price-estimate/list/
    Returns JSON array of objects: {file_name, workorder_id, workorder_number, size, mtime}
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # fetch WorkOrderPriceEstimate records for this user (or all if staff), and return file info
        if request.user.is_staff:
            estimates = WorkOrderPriceEstimate.objects.select_related('workorder', 'created_by').all()
        else:
            estimates = WorkOrderPriceEstimate.objects.select_related('workorder', 'created_by').filter(created_by=request.user)
        files = []
        for est in estimates:
            wo = est.workorder
            files.append({
                'file_name': est.file_name,
                'workorder_id': wo.id if wo else None,
                'workorder_number': wo.work_order_number if wo else '',
                'size': None,  # size info not stored in DB, could be added if needed
                'mtime': est.generated_at.timestamp() if est.generated_at else None,
                'user_name': getattr(est.created_by, 'email', '') if est.created_by else 'Unknown'
            })

        # # sort by mtime desc
        # files.sort(key=lambda x: x.get('mtime') or 0, reverse=True)
        return Response(files, status=status.HTTP_200_OK)