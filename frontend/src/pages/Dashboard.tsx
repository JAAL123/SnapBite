import { useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { useAuthStore } from '../store/authStore';
import { foodLogService } from '../services/foodLogs'
import AddFoodModal from '../components/AddFoodModal';
import { useState } from 'react';

export default function Dashboard() {

    const [isModalOpen, setIsModalOpen] = useState(false);
    const logout = useAuthStore((state) => state.logout);
    const navigate = useNavigate();

    const { data: logs, isLoading, isError } = useQuery({
        queryKey: ['foodLogs'],
        queryFn: foodLogService.getMyLogs,
    });

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    return (
        <div className="min-h-screen bg-gray-50 p-4 sm:p-8">
            <div className="mx-auto max-w-6xl">

                <div className="mb-8 flex items-center justify-between rounded-2xl bg-white p-6 shadow-sm">
                    <div>
                        <h1 className="text-3xl font-extrabold text-gray-900">
                            Mi Historial
                        </h1>
                        <p className="text-gray-500 mt-1">Aquí están tus registros recientes</p>
                    </div>
                    <button
                        onClick={() => setIsModalOpen(true)}
                        className="bg-emerald-600 text-white px-6 py-2 rounded-full font-bold shadow-lg hover:bg-emerald-700 transition-all"
                    >
                        + Agregar Comida
                    </button>

                    <AddFoodModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} />
                    <button
                        onClick={handleLogout}
                        className="rounded-lg bg-red-50 px-4 py-2 text-sm font-medium text-red-600 transition-colors hover:bg-red-100"
                    >
                        Cerrar Sesión
                    </button>
                </div>

                {isLoading && (
                    <div className="py-12 text-center text-gray-500">
                        <div className="mx-auto h-8 w-8 animate-spin rounded-full border-4 border-emerald-500 border-t-transparent"></div>
                        <p className="mt-4">Cargando tus comidas...</p>
                    </div>
                )}

                {isError && (
                    <div className="rounded-lg bg-red-50 p-4 text-center text-red-600">
                        Ocurrió un error al cargar el historial.
                    </div>
                )}

                {!isLoading && logs?.length === 0 && (
                    <div className="rounded-2xl bg-white p-12 text-center shadow-sm">
                        <span className="text-6xl">📸</span>
                        <h3 className="mt-4 text-lg font-medium text-gray-900">Aún no hay comidas</h3>
                        <p className="mt-1 text-gray-500">Ve a Telegram y envía tu primera foto para que aparezca aquí.</p>
                    </div>
                )}

                {!isLoading && logs && logs.length > 0 && (
                    <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
                        {logs.map((log) => (
                            <div
                                key={log.id}
                                className="group flex flex-col overflow-hidden rounded-2xl bg-white shadow-sm transition-all hover:shadow-md hover:-translate-y-1"
                            >
                                <div className="relative aspect-square w-full overflow-hidden bg-gray-100">
                                    <img
                                        src={log.image_url}
                                        alt={log.food_name}
                                        className="h-full w-full object-cover transition-transform duration-300 group-hover:scale-105"
                                        loading="lazy"
                                    />
                                    <div className="absolute top-3 right-3 rounded-full bg-black/70 px-3 py-1 text-xs font-bold text-white backdrop-blur-sm">
                                        {log.calories} kcal
                                    </div>
                                </div>

                                <div className="flex flex-1 flex-col p-4">
                                    <h3 className="line-clamp-2 text-lg font-bold text-gray-900">
                                        {log.food_name}
                                    </h3>

                                    <p className="mt-1 text-xs text-gray-500">
                                        {new Date(log.created_at).toLocaleDateString('es-ES', {
                                            weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'
                                        })}
                                    </p>

                                    <div className="mt-auto pt-4">
                                        <div className="grid grid-cols-3 gap-2 text-center text-xs font-medium text-gray-600">
                                            <div className="rounded-md bg-emerald-50 py-1 text-emerald-700">
                                                {log.proteins}g <span className="block text-[10px] text-emerald-500/70">Prot</span>
                                            </div>
                                            <div className="rounded-md bg-blue-50 py-1 text-blue-700">
                                                {log.carbs}g <span className="block text-[10px] text-blue-500/70">Carbs</span>
                                            </div>
                                            <div className="rounded-md bg-orange-50 py-1 text-orange-700">
                                                {log.fats}g <span className="block text-[10px] text-orange-500/70">Grasas</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                )}

            </div>
        </div>
    );
}