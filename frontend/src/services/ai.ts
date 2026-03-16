import api from './api';

export interface AIAnalysisResponse {
    food_name: string;
    calories: number;
    proteins: number;
    carbs: number;
    fats: number;
}

export const aiService = {
    async analyzeImage(file: File): Promise<AIAnalysisResponse> {
        const formData = new FormData();
        formData.append('file', file);

        const response = await api.post('/ai/analyze-web', formData, {
            headers: { 'Content-Type': 'multipart/form-data' },
        });
        return response.data;
    }
};