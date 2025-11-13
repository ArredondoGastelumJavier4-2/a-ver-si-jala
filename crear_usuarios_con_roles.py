# Script para crear usuarios con roles (Vendedor, Gerente, Administrador, Cliente)
# Ejecutar con: python manage.py shell < crear_usuarios_con_roles.py

from django.contrib.auth.models import User
from tienda.models import PerfilUsuario
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sistema_tienda.settings")
django.setup()
print("=" * 70)
print("🔐 CREANDO USUARIOS CON ROLES")
print("=" * 70)
print()

# =================== USUARIO 1: VENDEDOR ===================
username_vendedor = 'vendedor'
password = 'vendedor123'

user_vendedor, created = User.objects.get_or_create(
    username=username_vendedor,
    defaults={'email': 'vendedor@tienda.com', 'first_name': 'Carlos', 'last_name': 'Vendedor'}
)
if created:
    user_vendedor.set_password(password)
    user_vendedor.is_staff = False
    user_vendedor.is_superuser = False
    user_vendedor.save()
else:
    user_vendedor.set_password(password)
    user_vendedor.save()

perfil_vendedor, created = PerfilUsuario.objects.get_or_create(
    user=user_vendedor,
    defaults={'rol': 'vendedor', 'telefono': '555-0001', 'departamento': 'Ventas', 'activo': True}
)
if not created:
    perfil_vendedor.rol = 'vendedor'
    perfil_vendedor.telefono = '555-0001'
    perfil_vendedor.departamento = 'Ventas'
    perfil_vendedor.activo = True
    perfil_vendedor.save()

print(f"✅ VENDEDOR creado: {username_vendedor} / {password}")

# =================== USUARIO 2: GERENTE ===================
username_gerente = 'gerente'
password = 'gerente123'

user_gerente, created = User.objects.get_or_create(
    username=username_gerente,
    defaults={'email': 'gerente@tienda.com', 'first_name': 'María', 'last_name': 'Gerente'}
)
if created:
    user_gerente.set_password(password)
    user_gerente.is_staff = False
    user_gerente.is_superuser = False
    user_gerente.save()
else:
    user_gerente.set_password(password)
    user_gerente.save()

perfil_gerente, created = PerfilUsuario.objects.get_or_create(
    user=user_gerente,
    defaults={'rol': 'gerente', 'telefono': '555-0002', 'departamento': 'Gerencia', 'activo': True}
)
if not created:
    perfil_gerente.rol = 'gerente'
    perfil_gerente.telefono = '555-0002'
    perfil_gerente.departamento = 'Gerencia'
    perfil_gerente.activo = True
    perfil_gerente.save()

print(f"✅ GERENTE creado: {username_gerente} / {password}")

# =================== USUARIO 3: ADMINISTRADOR ===================
username_admin = 'administrador'
password = 'admin123'

user_admin, created = User.objects.get_or_create(
    username=username_admin,
    defaults={'email': 'administrador@tienda.com', 'first_name': 'Juan', 'last_name': 'Administrador'}
)
if created:
    user_admin.set_password(password)
    user_admin.is_staff = True
    user_admin.is_superuser = False
    user_admin.save()
else:
    user_admin.set_password(password)
    user_admin.is_staff = True
    user_admin.save()

perfil_admin, created = PerfilUsuario.objects.get_or_create(
    user=user_admin,
    defaults={'rol': 'administrador', 'telefono': '555-0003', 'departamento': 'Administración', 'activo': True}
)
if not created:
    perfil_admin.rol = 'administrador'
    perfil_admin.telefono = '555-0003'
    perfil_admin.departamento = 'Administración'
    perfil_admin.activo = True
    perfil_admin.save()

print(f"✅ ADMINISTRADOR creado: {username_admin} / {password}")

# =================== USUARIO 4: CLIENTE ===================
username_cliente = 'cliente1'
password = 'cliente123'

user_cliente, created = User.objects.get_or_create(
    username=username_cliente,
    defaults={'email': 'cliente1@tienda.com', 'first_name': 'Pedro', 'last_name': 'Cliente'}
)
if created:
    user_cliente.set_password(password)
    user_cliente.is_staff = False
    user_cliente.is_superuser = False
    user_cliente.save()
else:
    user_cliente.set_password(password)
    user_cliente.save()

perfil_cliente, created = PerfilUsuario.objects.get_or_create(
    user=user_cliente,
    defaults={'rol': 'cliente', 'telefono': '555-0004', 'departamento': 'Clientes', 'activo': True}
)
if not created:
    perfil_cliente.rol = 'cliente'
    perfil_cliente.telefono = '555-0004'
    perfil_cliente.departamento = 'Clientes'
    perfil_cliente.activo = True
    perfil_cliente.save()

print(f"✅ CLIENTE creado: {username_cliente} / {password}")

# =================== SUPERUSUARIO ===================
print("👤 Verificando superusuario 'admin'...")
try:
    user_super = User.objects.get(username='admin')
    print(f"✅ Superusuario 'admin' ya existe")
except User.DoesNotExist:
    print("⚠️ Superusuario 'admin' no existe, créalo con: python manage.py createsuperuser")

# =================== RESUMEN ===================
print("\n📊 RESUMEN DE ROLES Y PERMISOS:")
print("Vendedor → Solo puede VER")
print("Gerente → VER, CREAR y EDITAR (no eliminar)")
print("Administrador → Puede hacer TODO")
print("Cliente → Solo su perfil y sus compras")
print("Superusuario → Acceso total")
