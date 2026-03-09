const errorTranslations: Record<string, string> = {
    "Incorrect email or password": "El correo o la contraseña son incorrectos.",
    "The user with this email already exists in the system.": "Ya existe una cuenta con este correo electrónico.",
    "Network Error": "No se pudo conectar con el servidor. Revisa tu internet.",
};

export const translateError = (errorResponse: any): string => {
    const detail = errorResponse?.response?.data?.detail || errorResponse?.message;

    if (typeof detail === 'string') {
        return errorTranslations[detail] || "Ocurrió un error inesperado. Intenta nuevamente.";
    }

    return "Ocurrió un error inesperado.";
};