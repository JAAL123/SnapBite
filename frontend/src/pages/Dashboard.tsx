import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';

export default function Dashboard() {
    const logout = useAuthStore((state) => state.logout);
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/login'); 
    };

    return (
        <div className="min-h-screen bg-gray-100 p-8">
            <div className="mx-auto max-w-4xl rounded-2xl bg-white p-6 shadow-xl">
                <div className="flex items-center justify-between border-b pb-4">
                    <h1 className="text-3xl font-extrabold text-gray-800">
                        Mi Panel
                    </h1>
                    <button
                        onClick={handleLogout}
                        className="rounded-lg bg-red-500 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-red-600"
                    >
                        Cerrar Sesión
                    </button>
                </div>

                <div className="mt-8 rounded-lg bg-emerald-50 p-6 text-emerald-800">
                    <p>Aca va el dashboard</p>
                </div>
            </div>
        </div>
    );
}