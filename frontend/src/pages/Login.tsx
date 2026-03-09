import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useMutation } from '@tanstack/react-query';
import { authService } from '../services/auth';
import { useAuthStore } from '../store/authStore';

export default function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const navigate = useNavigate();
    const setToken = useAuthStore((state) => state.setToken);

    const loginMutation = useMutation({
        mutationFn: () => authService.login(email, password),
        onSuccess: (data) => {
            setToken(data.access_token);
            console.log("Login exitoso");
            navigate('/dashboard');
        },
    });

    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        loginMutation.mutate();
    };

    return (
        <div className="flex min-h-screen items-center justify-center bg-gray-50 px-4">
            <div className="w-full max-w-md space-y-8 rounded-2xl bg-white p-8 shadow-xl">
                <div className="text-center">
                    <h2 className="text-3xl font-extrabold text-gray-900">Bienvenido a SnapBite</h2>
                    <p className="mt-2 text-sm text-gray-600">Inicia sesión para ver tu progreso calórico</p>
                </div>

                <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
                    {loginMutation.isError && (
                        <div className="rounded-md bg-red-50 p-3 text-sm text-red-600">
                            {/* @ts-ignore - axios error tipado rápido */}
                            {loginMutation.error?.response?.data?.detail || "Error al iniciar sesión"}
                        </div>
                    )}

                    <div className="space-y-4">
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
                    </div>

                    <button
                        type="submit"
                        disabled={loginMutation.isPending}
                        className={`flex w-full justify-center rounded-lg px-4 py-2 text-sm font-medium text-white transition-colors ${loginMutation.isPending ? 'bg-emerald-400 cursor-not-allowed' : 'bg-emerald-600 hover:bg-emerald-700'
                            }`}
                    >
                        {loginMutation.isPending ? 'Conectando...' : 'Iniciar Sesión'}
                    </button>
                </form>

                <div className="text-center text-sm">
                    <span className="text-gray-600">¿No tienes cuenta? </span>
                    <Link to="/register" className="font-medium text-emerald-600 hover:text-emerald-500">
                        Regístrate aquí
                    </Link>
                </div>
            </div>
        </div>
    );
}