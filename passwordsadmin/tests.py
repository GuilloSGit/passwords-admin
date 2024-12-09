from django.test import TestCase

# Tests for the Password model


class PasswordModelTest(TestCase):
    def test_string_representation(self):
        password = Password(name='Test Password')
        self.assertEqual(str(password), password.name)

    def test_verbose_name_plural(self):
        self.assertEqual(str(Password._meta.verbose_name_plural), 'Passwords')

# Tests for the Password form


class PasswordFormTest(TestCase):
    def test_form(self):
        form = CreatePasswordForm()
        self.assertIn('Nombre de usuario o correo utilizado', form.as_p())
        self.assertIn('URL del sitio', form.as_p())
        self.assertIn('Contraseña', form.as_p())
        self.assertIn('Etiqueta (opcional - 12 caracteres máx.)', form.as_p())
        self.assertIn('Compartir contraseña', form.as_p())
        self.assertIn('Compartir con:', form.as_p())

# Tests for the Password view


class PasswordViewTest(TestCase):
    def test_view(self):
        response = self.client.get('/passwords/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'passwords/passwords.html')

# Tests for the Password admin


class PasswordAdminTest(TestCase):
    def test_admin(self):
        response = self.client.get('/admin/passwordsadmin/password/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/change_list.html')
