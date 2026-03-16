import { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { aiService, type AIAnalysisResponse } from '../services/ai';
import { foodLogService } from '../services/foodLogs';

export default function AddFoodModal({ isOpen, onClose }: { isOpen: boolean; onClose: () => void }) {
    const [file, setFile] = useState<File | null>(null);
    const [preview, setPreview] = useState<string | null>(null);
    const [analysis, setAnalysis] = useState<AIAnalysisResponse | null>(null);

    const queryClient = useQueryClient();

    // Mutación para analizar con IA
    const aiMutation = useMutation({
        mutationFn: (file: File) => aiService.analyzeImage(file),
        onSuccess: (data) => setAnalysis(data),
    });

    // Mutación para guardar final
    const saveMutation = useMutation({
        mutationFn: (formData: FormData) => foodLogService.uploadLog(formData),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['foodLogs'] });
            handleClose();
        },
    });

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const selectedFile = e.target.files?.[0];
        if (!selectedFile) return;

        const fileName = selectedFile.name.toLowerCase();
        const isValidWebFormat = fileName.endsWith('.jpg') ||
            fileName.endsWith('.jpeg') ||
            fileName.endsWith('.png') ||
            fileName.endsWith('.webp');


        if (!isValidWebFormat) {
            alert("Formato de imagen no soportado. Por favor sube archivos JPG, PNG o WebP.");
            e.target.value = '';
            return;
        }

        setFile(selectedFile);
        if (preview) URL.revokeObjectURL(preview);

        const objectUrl = URL.createObjectURL(selectedFile);
        setPreview(objectUrl);

        aiMutation.mutate(selectedFile);
    };

    const handleClose = () => {
        if (preview) URL.revokeObjectURL(preview);
        setFile(null);
        setPreview(null);
        setAnalysis(null);
        aiMutation.reset(); // Limpia el estado de la mutación
        onClose();
    };

    const handleSave = () => {
        if (!file || !analysis) return;
        const formData = new FormData();
        formData.append('file', file);
        formData.append('food_name', analysis.food_name);
        formData.append('calories', analysis.calories.toString());
        formData.append('proteins', analysis.proteins.toString());
        formData.append('carbs', analysis.carbs.toString());
        formData.append('fats', analysis.fats.toString());
        saveMutation.mutate(formData);
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-md p-4">
            <div className="w-full max-w-md rounded-3xl bg-white shadow-2xl overflow-hidden border border-gray-100">
                <div className="p-6 space-y-6">
                    <div className="flex justify-between items-center">
                        <h2 className="text-2xl font-black text-gray-800 tracking-tight">Nueva Comida</h2>
                        <button onClick={handleClose} className="text-gray-400 hover:text-gray-600 transition-colors">✕</button>
                    </div>

                    {/* Área de Imagen con Preview Corregido */}
                    <div className="relative aspect-square w-full overflow-hidden rounded-2xl bg-gray-100 border-2 border-dashed border-gray-300 flex items-center justify-center">
                        {preview ? (
                            <img
                                src={preview}
                                className="h-full w-full object-cover block" // Agregamos 'block' para forzar renderizado
                                alt="Preview"
                                onLoad={() => console.log("Preview cargado con éxito")}
                            />
                        ) : (
                            <label className="cursor-pointer flex flex-col items-center justify-center w-full h-full">
                                <span className="text-5xl">📸</span>
                                <p className="text-sm font-medium text-gray-500 mt-2 text-center px-4">
                                    Sube una foto para analizar
                                </p>
                                <input
                                    type="file"
                                    className="hidden"
                                    onChange={handleFileChange}
                                    accept=".jpg,.jpeg,.png,.webp,image/jpeg,image/png,image/webp"
                                />
                            </label>
                        )}

                        {/* Overlay de Carga de IA */}
                        {aiMutation.isPending && (
                            <div className="absolute inset-0 bg-white/90 backdrop-blur-sm flex flex-col items-center justify-center animate-in fade-in duration-200">
                                <div className="h-12 w-12 animate-spin rounded-full border-4 border-emerald-500 border-t-transparent shadow-sm"></div>
                                <p className="text-emerald-700 font-black mt-4 text-sm uppercase tracking-tighter">Analizando nutrición...</p>
                            </div>
                        )}
                    </div>

                    {/* Resultados de la IA (Solo lectura, vienen del backend) */}
                    {analysis && (
                        <div className="animate-in slide-in-from-bottom-2 fade-in duration-500">
                            <div className="bg-emerald-50/50 p-4 rounded-2xl border border-emerald-100">
                                <p className="text-[10px] font-black text-emerald-600 uppercase tracking-widest mb-1">Resultado del análisis</p>
                                <h3 className="text-xl font-black text-gray-800 capitalize leading-tight">{analysis.food_name}</h3>

                                <div className="grid grid-cols-4 gap-2 mt-4">
                                    <div className="bg-white p-2 rounded-xl border border-emerald-100/50 shadow-sm text-center">
                                        <span className="block text-lg font-black text-gray-800 leading-none">{analysis.calories}</span>
                                        <span className="text-[9px] font-bold text-gray-400 uppercase tracking-tighter">Kcal</span>
                                    </div>
                                    <div className="bg-white p-2 rounded-xl border border-emerald-100/50 shadow-sm text-center">
                                        <span className="block text-lg font-black text-emerald-600 leading-none">{analysis.proteins}g</span>
                                        <span className="text-[9px] font-bold text-gray-400 uppercase tracking-tighter">Prot</span>
                                    </div>
                                    <div className="bg-white p-2 rounded-xl border border-emerald-100/50 shadow-sm text-center">
                                        <span className="block text-lg font-black text-blue-600 leading-none">{analysis.carbs}g</span>
                                        <span className="text-[9px] font-bold text-gray-400 uppercase tracking-tighter">Carb</span>
                                    </div>
                                    <div className="bg-white p-2 rounded-xl border border-emerald-100/50 shadow-sm text-center">
                                        <span className="block text-lg font-black text-orange-600 leading-none">{analysis.fats}g</span>
                                        <span className="text-[9px] font-bold text-gray-400 uppercase tracking-tighter">Fat</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Acciones */}
                    <div className="flex gap-3 pt-2">
                        <button
                            onClick={handleClose}
                            className="flex-1 py-3.5 font-bold text-gray-400 hover:text-gray-600 hover:bg-gray-50 rounded-2xl transition-all text-sm"
                        >
                            Cancelar
                        </button>
                        <button
                            disabled={!analysis || saveMutation.isPending}
                            onClick={handleSave}
                            className={`flex-[2] py-3.5 rounded-2xl font-black text-white shadow-lg transition-all text-sm uppercase tracking-tight ${!analysis
                                ? 'bg-gray-100 text-gray-300 cursor-not-allowed shadow-none'
                                : 'bg-emerald-600 hover:bg-emerald-700 active:scale-[0.98] shadow-emerald-200'
                                }`}
                        >
                            {saveMutation.isPending ? 'Guardando...' : 'Confirmar Comida'}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}