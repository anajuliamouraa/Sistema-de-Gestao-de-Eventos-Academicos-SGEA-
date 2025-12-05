import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class CustomPasswordValidator:
    def __init__(self):
        self.min_length = 8
    
    def validate(self, password, user=None):
        errors = []
        
        if len(password) < self.min_length:
            errors.append(
                ValidationError(
                    _('A senha deve ter no mínimo %(min_length)d caracteres.'),
                    code='password_too_short',
                    params={'min_length': self.min_length},
                )
            )
        
        if not re.search(r'[A-Z]', password):
            errors.append(
                ValidationError(
                    _('A senha deve conter pelo menos uma letra maiúscula.'),
                    code='password_no_upper',
                )
            )
        
        if not re.search(r'[a-z]', password):
            errors.append(
                ValidationError(
                    _('A senha deve conter pelo menos uma letra minúscula.'),
                    code='password_no_lower',
                )
            )
        
        if not re.search(r'\d', password):
            errors.append(
                ValidationError(
                    _('A senha deve conter pelo menos um número.'),
                    code='password_no_digit',
                )
            )
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\;\'`~]', password):
            errors.append(
                ValidationError(
                    _('A senha deve conter pelo menos um caractere especial (!@#$%^&*(),.?":{}|<>).'),
                    code='password_no_special',
                )
            )
        
        if errors:
            raise ValidationError(errors)
    
    def get_help_text(self):
        return _(
            'Sua senha deve conter no mínimo %(min_length)d caracteres, '
            'incluindo letras maiúsculas, minúsculas, números e caracteres especiais.'
        ) % {'min_length': self.min_length}


def validate_phone_number(value):
    if value:
        digits = re.sub(r'\D', '', value)
        
        if len(digits) < 10 or len(digits) > 11:
            raise ValidationError(
                _('Telefone inválido. Use o formato (XX) XXXXX-XXXX'),
                code='invalid_phone'
            )


def validate_image_extension(value):
    import os
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    
    if ext not in valid_extensions:
        raise ValidationError(
            _('Tipo de arquivo não suportado. Use: %(types)s'),
            code='invalid_extension',
            params={'types': ', '.join(valid_extensions)}
        )
