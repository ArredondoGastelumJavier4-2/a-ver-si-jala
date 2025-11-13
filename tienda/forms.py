# tienda/forms.py
# ===============================================================
# FORMULARIOS DJANGO PARA LA APP TIENDA
# Cada formulario corresponde directamente con una tabla en la BD:
# tienda_categoria, tienda_proveedor, tienda_producto, tienda_cliente, tienda_venta
# ===============================================================

from django import forms
from .models import Producto, Categoria, Proveedor, Cliente, Venta
from django.contrib.auth.models import User

# ===============================================================
# FORMULARIO 1: PRODUCTO  → Tabla: tienda_producto
# ===============================================================
class ProductoForm(forms.ModelForm):
    """Formulario para crear y editar productos"""
    
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio_venta', 'stock', 'categoria', 'proveedor', 'activo']
        
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre del producto'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ingrese una descripción del producto'
            }),
            'precio_venta': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': '0'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-control'
            }),
            'proveedor': forms.Select(attrs={
                'class': 'form-control'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

        labels = {
            'nombre': 'Nombre del Producto',
            'descripcion': 'Descripción',
            'precio_venta': 'Precio de Venta ($)',
            'stock': 'Cantidad en Stock',
            'categoria': 'Categoría',
            'proveedor': 'Proveedor',
            'activo': '¿Producto Activo?',
        }


# ===============================================================
# FORMULARIO 2: CATEGORÍA  → Tabla: tienda_categoria
# ===============================================================
class CategoriaForm(forms.ModelForm):
    """Formulario para crear y editar categorías"""
    
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
        
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre de la categoría'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ingrese una descripción (opcional)'
            }),
        }

        labels = {
            'nombre': 'Nombre de la Categoría',
            'descripcion': 'Descripción',
        }


# ===============================================================
# FORMULARIO 3: PROVEEDOR  → Tabla: tienda_proveedor
# ===============================================================
class ProveedorForm(forms.ModelForm):
    """Formulario para crear y editar proveedores"""
    
    class Meta:
        model = Proveedor
        fields = ['nombre', 'contacto', 'telefono']
        
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del proveedor'
            }),
            'contacto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del contacto (opcional)'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Teléfono de contacto'
            }),
        }

        labels = {
            'nombre': 'Proveedor',
            'contacto': 'Contacto',
            'telefono': 'Teléfono',
        }


# ===============================================================
# FORMULARIO 4: CLIENTE  → Tabla: tienda_cliente
# ===============================================================
class ClienteForm(forms.ModelForm):
    """Formulario para crear y editar clientes"""
    
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'email', 'telefono', 'direccion']
        
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del cliente'
            }),
            'apellido': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellido del cliente'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Teléfono de contacto'
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Dirección de entrega'
            }),
        }

        labels = {
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'email': 'Correo Electrónico',
            'telefono': 'Teléfono',
            'direccion': 'Dirección',
        }


# ===============================================================
# FORMULARIO 5: VENTA  → Tabla: tienda_venta
# ===============================================================
class VentaForm(forms.ModelForm):
    """Formulario para registrar ventas"""
    
    class Meta:
        model = Venta
        fields = ['cliente', 'producto', 'cantidad']
        
        widgets = {
            'cliente': forms.Select(attrs={
                'class': 'form-control'
            }),
            'producto': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_producto'
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'value': '1'
            }),
        }

        labels = {
            'cliente': 'Cliente',
            'producto': 'Producto',
            'cantidad': 'Cantidad',
        }


class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellidos',
            'email': 'Correo electrónico',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class ClientePerfilForm(forms.ModelForm):
    nombre_completo = forms.CharField(label='Nombre completo', required=False, disabled=True)

    class Meta:
        model = Cliente
        fields = ['nombre_completo', 'nombre', 'apellido', 'telefono', 'direccion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['nombre_completo'].initial = f"{self.instance.nombre} {self.instance.apellido}"
