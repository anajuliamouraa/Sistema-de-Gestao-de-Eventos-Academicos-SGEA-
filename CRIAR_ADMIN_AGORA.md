# 🔑 Criar Superusuário Admin Agora

## Execute estes comandos:

```bash
cd /home/s0ft/Sistema-de-Gestao-de-Eventos-Academicos-SGEA-
source venv/bin/activate
python manage.py shell
```

## Depois cole este código no shell Python:

```python
from users.models import CustomUser
CustomUser.objects.filter(username='admin').delete()
admin = CustomUser.objects.create_superuser(
    username='admin',
    email='admin@sgea.edu.br',
    password='12345',
    first_name='Administrador',
    last_name='Sistema',
    perfil='ORGANIZADOR',
    instituicao_ensino='SGEA'
)
print('✅ Superusuário admin criado com sucesso!')
print('Username: admin')
print('Password: 12345')
exit()
```

## Pronto! Agora você pode:

1. **Iniciar o servidor:**

   ```bash
   python manage.py runserver
   ```

2. **Acessar o Django Admin:**

   - URL: http://127.0.0.1:8000/admin
   - Username: **admin**
   - Password: **12345**

3. **Ou fazer login no sistema:**
   - URL: http://127.0.0.1:8000/users/login
   - Username: **admin**
   - Password: **12345**

---

## ⚠️ Importante

Esta senha (12345) é simples e deve ser usada **APENAS** para:

- ✅ Desenvolvimento
- ✅ Testes
- ✅ Demonstração acadêmica

**Nunca use em produção!**

---

✅ **Tudo configurado e documentado!**
