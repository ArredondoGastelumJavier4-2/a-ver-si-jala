# tienda/admin.py
from django.contrib import admin
from .models import Categoria, Producto, Proveedor, Cliente, PerfilUsuario

# =================== ADMIN PERFIL DE USUARIO ===================
@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    """Admin personalizado para Perfiles de Usuario"""
    list_display = ('user', 'rol', 'departamento', 'activo', 'fecha_contratacion')
    list_filter = ('rol', 'activo', 'departamento')
    search_fields = ('user__username', 'user__email', 'departamento')
    list_editable = ('rol', 'activo')
    ordering = ('-fecha_contratacion',)


# =================== ADMIN CATEGORÍA ===================
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    """Admin personalizado para Categorías"""
    list_display = ('id', 'nombre', 'fecha_creacion')
    search_fields = ('nombre',)
    list_filter = ('fecha_creacion',)
    ordering = ('nombre',)


# =================== ADMIN PRODUCTO ===================
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    """Admin personalizado para Productos"""
    list_display = ('id', 'nombre', 'categoria', 'precio_venta', 'stock', 'activo', 'fecha_creacion')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('categoria', 'activo', 'fecha_creacion')
    list_editable = ('precio_venta', 'stock', 'activo')
    ordering = ('-fecha_creacion',)


# =================== ADMIN PROVEEDOR ===================
@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    """Admin personalizado para Proveedores"""
    list_display = ('id', 'nombre', 'contacto', 'telefono')
    search_fields = ('nombre', 'contacto', 'telefono')
    list_filter = ('nombre',)
    ordering = ('nombre',)


# =================== ADMIN CLIENTE ===================
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    """Admin personalizado para Clientes"""
    list_display = ('id', 'nombre', 'apellido', 'email', 'telefono', 'fecha_registro')
    search_fields = ('nombre', 'apellido', 'email')
    list_filter = ('fecha_registro',)
    ordering = ('apellido', 'nombre')