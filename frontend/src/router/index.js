import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/home/index.vue'
import Admin from '../components/admin.vue'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home
    },
    {
        path: '/admin',
        name: 'Admin',
        component: Admin
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router
