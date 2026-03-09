import api from './api';

export const authService = {
    async login(email: string, password: string) {
        const formData = new URLSearchParams();
        formData.append('username', email);
        formData.append('password', password);

        const response = await api.post('/login/access-token', formData, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
        });
        return response.data;
    },

    async register(name: string, email: string, password: string) {
        const payload = {
            username: name,
            email: email,
            password: password,
        };

        const response = await api.post('/users/', payload);
        return response.data;
    },
};