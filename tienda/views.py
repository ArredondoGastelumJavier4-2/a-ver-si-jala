# tienda/views.py
# ===============================================================
# PARTE 6: VISTAS — LÓGICA DE NEGOCIO Y CONTROL DE ACCESO
# ===============================================================

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import Producto, Categoria, Proveedor, Cliente, PerfilUsuario, Venta
from .forms import ProductoForm, CategoriaForm, ProveedorForm, ClienteForm, VentaForm, PerfilUsuarioForm, ClientePerfilForm
from django.contrib.auth.views import LoginView, LogoutView
from django.utils import timezone
from datetime import datetime, time
from django.contrib.auth.models import User

class CustomLoginView(LoginView):
    template_name = 'tienda/login.html'

class CustomLogoutView(LogoutView):
    next_page = 'login'

# ===============================================================
# DECORADOR PERSONALIZADO PARA ROLES
# ===============================================================
def rol_requerido(*roles_permitidos):
    """
    Verifica si el usuario tiene uno de los roles permitidos.
    """
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, 'Debes iniciar sesión para acceder.')
                return redirect('login')

            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            try:
                perfil = request.user.perfil
                if perfil.rol in roles_permitidos:
                    return view_func(request, *args, **kwargs)
                else:
                    messages.error(request, f'⚠️ Acceso denegado. Rol requerido: {", ".join(roles_permitidos)}')
                    return redirect('home')
            except PerfilUsuario.DoesNotExist:
                messages.error(request, 'Tu cuenta no tiene un perfil asignado.')
                return redirect('home')

        return _wrapped_view
    return decorator


# ===============================================================
# VISTA DE LOGIN Y LOGOUT
# ===============================================================
def login_view(request):
    """Iniciar sesión"""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Bienvenido {username}')
                return redirect('home')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = AuthenticationForm()
    return render(request, 'tienda/login.html', {'form': form})


def logout_view(request):
    """Cerrar sesión"""
    logout(request)
    messages.info(request, 'Sesión cerrada correctamente.')
    return redirect('login')


# ===============================================================
# DASHBOARD / HOME
# ===============================================================
@login_required
def home(request):
    hoy = timezone.localdate()  # Fecha local
    if request.user.perfil.rol == 'cliente':
        mis_compras = Venta.objects.filter(cliente__email=request.user.email)
        return render(request, 'tienda/home.html', {'mis_compras': mis_compras})
    inicio = timezone.make_aware(datetime.combine(hoy, time.min))  # 00:00
    fin = timezone.make_aware(datetime.combine(hoy, time.max))     # 23:59:59

    ventas_hoy = Venta.objects.filter(fecha_venta__range=(inicio, fin))

    total_productos = Producto.objects.count()
    total_categorias = Categoria.objects.count()
    total_proveedores = Proveedor.objects.count()
    total_clientes = Cliente.objects.count()
    productos_recientes = Producto.objects.all()[:5]

    total_ventas_dia = sum(v.total for v in ventas_hoy)
    cantidad_ventas = ventas_hoy.count()

    context = {
        'total_productos': total_productos,
        'total_categorias': total_categorias,
        'total_proveedores': total_proveedores,
        'total_clientes': total_clientes,
        'productos_recientes': productos_recientes,
        'ventas_hoy': ventas_hoy,
        'total_ventas_dia': total_ventas_dia,
        'cantidad_ventas': cantidad_ventas,
        'fecha': hoy,
    }
    return render(request, 'tienda/home.html', context)

# ===============================================================
# FORMULARIO 1: PRODUCTO → Tabla: tienda_producto
# ===============================================================
@login_required
@rol_requerido('administrador', 'gerente')
def producto_lista(request):
    productos = Producto.objects.all()
    return render(request, 'tienda/producto_lista.html', {'productos': productos})


@login_required
@rol_requerido('administrador')
def producto_crear(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Producto creado exitosamente.')
            return redirect('producto_lista')
    else:
        form = ProductoForm()
    return render(request, 'tienda/producto_form.html', {'form': form, 'accion': 'Crear'})


@login_required
@rol_requerido('administrador')
def producto_editar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Producto actualizado.')
            return redirect('producto_lista')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'tienda/producto_form.html', {'form': form, 'accion': 'Editar'})


@login_required
@rol_requerido('administrador')
def producto_eliminar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, '🗑️ Producto eliminado.')
        return redirect('producto_lista')
    return render(request, 'tienda/producto_eliminar.html', {'producto': producto})


# ===============================================================
# FORMULARIO 2: CATEGORÍA → Tabla: tienda_categoria
# ===============================================================
@login_required
@rol_requerido('administrador')
def categoria_lista(request):
    categorias = Categoria.objects.all()
    return render(request, 'tienda/categoria_lista.html', {'categorias': categorias})


@login_required
@rol_requerido('administrador')
def categoria_crear(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada.')
            return redirect('categoria_lista')
    else:
        form = CategoriaForm()
    return render(request, 'tienda/categoria_form.html', {'form': form, 'accion': 'Crear'})


@login_required
@rol_requerido('administrador')
def categoria_editar(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría actualizada.')
            return redirect('categoria_lista')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'tienda/categoria_form.html', {'form': form, 'accion': 'Editar'})


@login_required
@rol_requerido('administrador')
def categoria_eliminar(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoría eliminada.')
        return redirect('categoria_lista')
    return render(request, 'tienda/categoria_eliminar.html', {'categoria': categoria})


# ===============================================================
# FORMULARIO 3: PROVEEDOR → Tabla: tienda_proveedor
# ===============================================================
@login_required
@rol_requerido('administrador')
def proveedor_lista(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'tienda/proveedor_lista.html', {'proveedores': proveedores})


@login_required
@rol_requerido('administrador')
def proveedor_crear(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor agregado.')
            return redirect('proveedor_lista')
    else:
        form = ProveedorForm()
    return render(request, 'tienda/proveedor_form.html', {'form': form, 'accion': 'Crear'})


@login_required
@rol_requerido('administrador')
def proveedor_editar(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor actualizado.')
            return redirect('proveedor_lista')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'tienda/proveedor_form.html', {'form': form, 'accion': 'Editar'})


@login_required
@rol_requerido('administrador')
def proveedor_eliminar(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        proveedor.delete()
        messages.success(request, 'Proveedor eliminado.')
        return redirect('proveedor_lista')
    return render(request, 'tienda/proveedor_eliminar.html', {'proveedor': proveedor})


# ===============================================================
# FORMULARIO 4: CLIENTE → Tabla: tienda_cliente
# ===============================================================
@login_required
@rol_requerido('administrador', 'gerente', 'vendedor')
def cliente_lista(request):
    clientes = Cliente.objects.all()
    return render(request, 'tienda/cliente_lista.html', {'clientes': clientes})


from django.contrib.auth.models import User
from .models import Cliente, PerfilUsuario  # 👈 asegúrate de tener esto arriba

@login_required
@rol_requerido('administrador', 'gerente', 'vendedor')
def cliente_crear(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)

            # 🔹 Crear usuario automáticamente
            username = cliente.nombre.lower()
            password = cliente.telefono  # Teléfono será la contraseña

            # Evitar duplicados
            if User.objects.filter(username=username).exists():
                messages.error(request, f"Ya existe un usuario con el nombre '{username}'.")
                return redirect('cliente_lista')

            user = User.objects.create_user(username=username, password=password)
            user.first_name = cliente.nombre
            user.last_name = cliente.apellido
            user.email = cliente.email
            user.save()

            # 🔹 Crear perfil con rol "cliente"
            PerfilUsuario.objects.create(user=user, rol='cliente')

            # 🔹 Asociar cliente con usuario
            cliente.user = user
            cliente.save()

            messages.success(request, f"Cliente '{cliente.nombre_completo}' registrado correctamente.")
            return redirect('cliente_lista')
    else:
        form = ClienteForm()

    return render(request, 'tienda/cliente_form.html', {'form': form, 'accion': 'Crear'})


@login_required
@rol_requerido('administrador', 'gerente', 'vendedor')
def cliente_editar(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente actualizado.')
            return redirect('cliente_lista')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'tienda/cliente_form.html', {'form': form, 'accion': 'Editar'})


@login_required
@rol_requerido('administrador', 'gerente', 'vendedor')
def cliente_eliminar(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente eliminado.')
        return redirect('cliente_lista')
    return render(request, 'tienda/cliente_eliminar.html', {'cliente': cliente})


# ===============================================================
# FORMULARIO 5: VENTA → Tabla: tienda_venta
# ===============================================================
@login_required
@rol_requerido('administrador', 'gerente', 'vendedor')
def venta_lista(request):
    hoy = timezone.now().date()
    ventas_hoy = Venta.objects.filter(fecha_venta__date=hoy)
    total_ventas_dia = sum(venta.total for venta in ventas_hoy)
    cantidad_ventas = ventas_hoy.count()

    context = {
        'ventas_hoy': ventas_hoy,
        'total_ventas_dia': total_ventas_dia,
        'cantidad_ventas': cantidad_ventas,
        'fecha': hoy,
    }
    return render(request, 'tienda/reporte_ventas.html', context)




@login_required
@rol_requerido('administrador', 'gerente', 'vendedor')
def venta_crear(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            venta = form.save(commit=False)
            venta.vendedor = request.user  # 👈 asigna el usuario que crea la venta
            venta.save()
            messages.success(request, 'Venta registrada correctamente.')
            return redirect('reporte_ventas')
    else:
        form = VentaForm()
    return render(request, 'tienda/venta_form.html', {'form': form, 'accion': 'Registrar'})


@login_required
@rol_requerido('administrador')
def venta_eliminar(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    if request.method == 'POST':
        venta.delete()
        messages.success(request, 'Venta eliminada.')
        return redirect('venta_lista')
    return render(request, 'tienda/venta_eliminar.html', {'venta': venta})



@login_required
@rol_requerido('administrador', 'gerente', 'vendedor')
def reporte_ventas(request):
    """Reporte de ventas del día"""
    hoy = timezone.localdate()
    
    # Crear rango de inicio y fin del día en hora local
    inicio = timezone.make_aware(datetime.combine(hoy, time.min))
    fin = timezone.make_aware(datetime.combine(hoy, time.max))

    ventas_hoy = Venta.objects.filter(fecha_venta__range=(inicio, fin))
    total_ventas_dia = sum(venta.total for venta in ventas_hoy)
    cantidad_ventas = ventas_hoy.count()

    context = {
        'ventas_hoy': ventas_hoy,
        'total_ventas_dia': total_ventas_dia,
        'cantidad_ventas': cantidad_ventas,
        'fecha': hoy,
    }
    return render(request, 'tienda/reporte_ventas.html', context)

# tienda/views.py
from .forms import PerfilUsuarioForm, ClientePerfilForm

@login_required
def mi_perfil(request):
    user = request.user
    perfil = getattr(user, 'perfil', None)
    cliente = None

    if hasattr(user, 'cliente'):
        cliente = user.cliente

    if request.method == 'POST':
        user_form = PerfilUsuarioForm(request.POST, instance=user)
        cliente_form = ClientePerfilForm(request.POST, instance=cliente) if cliente else None

        if user_form.is_valid() and (cliente_form is None or cliente_form.is_valid()):
            user_form.save()
            if cliente_form:
                cliente_form.save()
            messages.success(request, '✅ Tu perfil se actualizó correctamente.')
            return redirect('mi_perfil')
    else:
        user_form = PerfilUsuarioForm(instance=user)
        cliente_form = ClientePerfilForm(instance=cliente) if cliente else None

    return render(request, 'tienda/mi_perfil.html', {
        'user_form': user_form,
        'cliente_form': cliente_form,
        'perfil': perfil,
    })

@login_required
@rol_requerido('cliente')
def mis_compras(request):
    """Historial de compras del cliente autenticado"""
    try:
        cliente = request.user.cliente
        compras = Venta.objects.filter(cliente=cliente).order_by('-fecha_venta')
    except Cliente.DoesNotExist:
        messages.warning(request, 'No tienes compras registradas.')
        compras = []

    total_compras = sum(venta.total for venta in compras)

    return render(request, 'tienda/mis_compras.html', {
        'compras': compras,
        'total_compras': total_compras,
    })
