import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useMutation } from '@tanstack/react-query';
import { authService } from '../services/auth';
import { useAuthStore } from '../store/authStore';
import { translateError } from '../utils/errorMapper';

export default function Register() {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [localError, setLocalError] = useState<string | null>(null);

    const navigate = useNavigate();
    const setToken = useAuthStore((state) => state.setToken);

    const registerMutation = useMutation({
        mutationFn: async () => {
            await authService.register(name, email, password);
            return authService.login(email, password);
        },
        onSuccess: (data) => {
            setToken(data.access_token);
            console.log("¡Registro y auto-login exitoso!");
            navigate('/dashboard');
        },
    });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        setLocalError(null);

        if (password !== confirmPassword) {
            setLocalError("Las contraseñas no coinciden.");
            return;
        }

        registerMutation.mutate();
    };

    return (
        <div className="flex min-h-screen items-center justify-center bg-gray-50 px-4">
            <div className="w-full max-w-md space-y-8 rounded-2xl bg-white p-8 shadow-xl">

                <div className="text-center">
                    <h2 className="text-3xl font-extrabold text-gray-900">Únete a SnapBite</h2>
                    <p className="mt-2 text-sm text-gray-600">Crea tu cuenta para empezar a registrar tus comidas</p>
                </div>

                <form className="mt-8 space-y-6" onSubmit={handleSubmit}>

                    {localError && (
                        <div className="rounded-md bg-red-50 p-3 text-sm text-red-600">
                            {localError}
                        </div>
                    )}

                    {registerMutation.isError && !localError && (
                        <div className="rounded-md bg-red-50 p-3 text-sm text-red-600">
                            {translateError(registerMutation.error)}
                        </div>
                    )}

                    <div className="space-y-4">
                        <input
                            type="text" required
                            className="block w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-emerald-500 focus:outline-none focus:ring-emerald-500 sm:text-sm"
                            placeholder="Tu nombre (ej. Pepe)"
                            value={name} onChange={(e) => setName(e.target.value)}
                        />
                        <input
                            type="email" required
                            className="block w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-emerald-500 focus:outline-none focus:ring-emerald-500 sm:text-sm"
                            placeholder="Correo electrónico"
                            value={email} onChange={(e) => setEmail(e.target.value)}
                        />
                        <input
                            type="password" required
                            className="block w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-emerald-500 focus:outline-none focus:ring-emerald-500 sm:text-sm"
                            placeholder="Contraseña"
                            value={password} onChange={(e) => setPassword(e.target.value)}
                        />
                        <input
                            type="password" required
                            className="block w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-emerald-500 focus:outline-none focus:ring-emerald-500 sm:text-sm"
                            placeholder="Confirmar Contraseña"
                            value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)}
                        />
                    </div>

                    <button
                        type="submit"
                        disabled={registerMutation.isPending}
                        className={`flex w-full justify-center rounded-lg px-4 py-2 text-sm font-medium text-white transition-colors ${registerMutation.isPending ? 'bg-emerald-400 cursor-not-allowed' : 'bg-emerald-600 hover:bg-emerald-700'
                            }`}
                    >
                        {registerMutation.isPending ? 'Creando cuenta...' : 'Crear Cuenta'}
                    </button>
                </form>

                <div className="text-center text-sm">
                    <span className="text-gray-600">¿Ya tienes una cuenta? </span>
                    <Link to="/login" className="font-medium text-emerald-600 hover:text-emerald-500">
                        Inicia sesión aquí
                    </Link>
                </div>
            </div>
        </div>
    );
}