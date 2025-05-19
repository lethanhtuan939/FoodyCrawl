<template>
    <div class="admin">
        <h1>Bảng Quản Trị</h1>
        <div class="admin-content">
            <table class="crawling-table">
                <thead>
                    <tr>
                        <th>Thao tác</th>
                        <th>Mô tả</th>
                        <th>Trạng thái</th>
                        <th>Hành động</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="operation in crawlingOperations" :key="operation.id">
                        <td>{{ operation.name }}</td>
                        <td>{{ operation.description }}</td>
                        <td>
                            <span :class="['status', { 'loading': loading[operation.id] }]">
                                {{ results[operation.id] || 'Chưa bắt đầu' }}
                            </span>
                        </td>
                        <td>
                            <button 
                                @click="startCrawling(operation)"
                                :disabled="loading[operation.id]"
                                class="crawl-button"
                            >
                                {{ loading[operation.id] ? 'Đang xử lý...' : 'Bắt đầu thu thập' }}
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';

const apiUrl = import.meta.env.VITE_API_CRAWL_URL;
const loading = ref({});
const results = ref({});

const crawlingOperations = [
    {
        id: 'crawl-locations',
        name: 'Thu thập địa điểm',
        endpoint: '/api/crawl-locations',
        description: 'Thu thập dữ liệu địa điểm từ nguồn'
    },
    {
        id: 'full-crawl',
        name: 'Thu thập toàn bộ',
        endpoint: '/api/full-crawl',
        description: 'Thu thập toàn bộ dữ liệu'
    },
];

const startCrawling = async (operation) => {
    loading.value[operation.id] = true;
    results.value[operation.id] = 'Đang xử lý...';
    
    try {
        const response = await fetch(`${apiUrl}${operation.endpoint}`);
        const data = await response.json();
        results.value[operation.id] = 'Thành công';
    } catch (error) {
        results.value[operation.id] = `Lỗi: ${error.message}`;
    } finally {
        loading.value[operation.id] = false;
    }
};
</script>

<style scoped>
.admin {
    padding: 2rem;
}

.admin h1 {
    margin-bottom: 2rem;
    color: #2c3e50;
}

.crawling-table {
    width: 100%;
    border-collapse: collapse;
    background: white;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.crawling-table th,
.crawling-table td {
    padding: 1rem;
    text-align: left;
    border-bottom: 1px solid #eee;
}

.crawling-table th {
    background: #f8f9fa;
    font-weight: 600;
    color: #2c3e50;
}

.crawling-table tr:last-child td {
    border-bottom: none;
}

.status {
    display: inline-block;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    font-size: 0.875rem;
}

.status.loading {
    background-color: #fff3cd;
    color: #856404;
}

.crawl-button {
    background-color: #007bff;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.2s;
}

.crawl-button:hover:not(:disabled) {
    background-color: #0056b3;
}

.crawl-button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
}
</style>