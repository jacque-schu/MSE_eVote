import aspectlib
from fastapi import HTTPException, status

@aspectlib.Aspect
def auth_check(cutpoint, *args, **kwargs):
    token = kwargs.get('auth_token')
    if not token or not is_token_valid(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Ungültiger oder fehlender Authentifizierungs-Token")
    result = yield aspectlib.Proceed
    yield aspectlib.Return(result)

def is_token_valid(token: str) -> bool:
    # Implementiere echte Token-Prüfung hier
    return token == "geheimer_token"

