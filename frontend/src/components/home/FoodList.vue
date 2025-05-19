<script setup>
	import { ref, watch, computed } from "vue";

	const BASE_URL = import.meta.env.VITE_API_URL;

	const props = defineProps({
		selectedLocation: {
			type: Object,
			default: null,
		},
		searchQuery: {
			type: String,
			default: "",
		},
	});

	const foods = ref([]);
	const currentPage = ref(1);
	const totalPages = ref(1);
	const isLoading = ref(false);
	async function fetchFoods() {
		isLoading.value = true;
		try {
			const response = await fetch(
				`${BASE_URL}/foods?page=${currentPage.value}${
					props.searchQuery.trim() ? `&query=${props.searchQuery.trim()}` : ""
				}&page_size=12${
					props.selectedLocation?.city_id ? `&city_id=${props.selectedLocation.city_id}` : ""
				}`
			);
			const data = await response.json();
			foods.value = data.items;
			totalPages.value = data.total_pages;
		} catch (error) {
			console.error("Error fetching foods:", error);
		} finally {
			isLoading.value = false;
		}
	}

	watch(
		() => [props.selectedLocation?.city_id, props.searchQuery],
		() => {
			console.log("Location changed:", props.selectedLocation);
			currentPage.value = 1;
			fetchFoods();
		},
		{ immediate: true }
	);

	watch(currentPage, fetchFoods);
	const pagesToShow = computed(() => {
		const result = [];
		const totalPagesValue = totalPages.value;
		const currentPageValue = currentPage.value;
		result.push(1);
		if (currentPageValue > 3) {
			result.push("...");
		}
		if (currentPageValue > 2) {
			result.push(currentPageValue - 1);
		}
		if (currentPageValue !== 1 && currentPageValue !== totalPagesValue) {
			result.push(currentPageValue);
		}

		if (currentPageValue < totalPagesValue - 1) {
			result.push(currentPageValue + 1);
		}
		if (currentPageValue < totalPagesValue - 2) {
			result.push("...");
		}
		if (totalPagesValue > 1) {
			result.push(totalPagesValue);
		}

		return result;
	});
</script>

<template>
	<div class="food-list">
		<div v-if="isLoading" class="loading">Loading...</div>
		<template v-else>
			<div v-if="foods.length === 0" class="no-results">Không có kết quả nào</div>
			<div v-else class="food-grid">
				<div v-for="food in foods" :key="food.id" class="food-card">
					<img
						:src="food.image_url ?? 'https://www.foody.vn/Style/images/deli-dish-no-image.png'"
						:alt="food.name"
					/>
					<div class="card-body">
						<h3>{{ food.name }}</h3>
						<span class="address">{{ food.address }}</span>
						<div class="categories">
							<span v-for="category in food.categories" :key="category" class="tag">
								{{ category }}
							</span>
							<span v-for="cuisine in food.cuisines" :key="cuisine" class="tag cuisine">
								{{ cuisine }}
							</span>
						</div>
						<div class="rating">
							<span class="stars">★ {{ food.rating_avg }}</span>
							<span class="reviews">({{ food.rating_total_review }} đánh giá)</span>
						</div>
						<div class="status" :class="{ open: food.is_open }">
							{{ food.is_open ? "Mở cửa" : "Đóng cửa" }}
						</div>
					</div>
				</div>
			</div>
			<div class="pagination" v-if="totalPages > 0">
				<button class="navigate" :disabled="currentPage === 1" @click="currentPage = 1">Đầu</button>
				<button class="navigate" :disabled="currentPage === 1" @click="currentPage--">Trước</button>

				<template v-for="(page, index) in pagesToShow" :key="index">
					<!-- Nếu là số trang thì hiển thị nút có thể nhấp -->
					<button
						v-if="page !== '...'"
						class="page"
						@click="currentPage = page"
						:class="{ active: currentPage === page }"
					>
						{{ page }}
					</button>

					<!-- Nếu là dấu ... thì chỉ hiển thị text -->
					<span v-else class="ellipsis">{{ page }}</span>
				</template>

				<button class="navigate" :disabled="currentPage === totalPages" @click="currentPage++">
					Sau
				</button>
				<button
					class="navigate"
					:disabled="currentPage === totalPages"
					@click="currentPage = totalPages"
				>
					Cuối
				</button>
			</div>
		</template>
	</div>
</template>

<style scoped>
	.food-list {
		padding: 2rem;
	}

	.loading,
	.no-location,
	.no-results {
		text-align: center;
		padding: 2rem;
		font-size: 1.2rem;
		color: #666;
	}

	.food-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
		gap: 2rem;
	}

	.food-card {
		background: #fff;
		border-radius: 8px;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
		position: relative;
		overflow: hidden;
	}

	.card-body {
		padding: 1.5rem;
	}

	.food-card h3 {
		min-height: 56px;
		margin: 0 0 1rem;
		color: #333;
		overflow: hidden;
		text-overflow: ellipsis;
		display: -webkit-box;
		-webkit-line-clamp: 2;
		-webkit-box-orient: vertical;
	}

	img {
		width: 100%;
		height: auto;
		border-radius: 8px 8px 0 0;
		object-fit: cover;
	}

	.tag {
		display: inline-block;
		padding: 0.2rem 0.5rem;
		margin: 0.2rem;
		border-radius: 4px;
		background: #f0f0f0;
		font-size: 0.9rem;
	}

	.tag.cuisine {
		background: #e8f5e9;
		color: #2e7d32;
	}

	.address {
		margin: 1rem 0;
		color: #666;
		font-size: 0.9rem;
	}

	.rating {
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}

	.stars {
		color: #ffaa00;
		font-weight: bold;
	}

	.reviews {
		color: #666;
		font-size: 0.9rem;
	}

	.status {
		position: absolute;
		top: 0.5rem;
		right: 0.5rem;
		font-weight: 600;
		padding: 0.2rem 0.5rem;
		border-radius: 4px;
		font-size: 0.8rem;
		background: #ffebee;
		color: #c62828;
	}

	.status.open {
		background: #e8f5e9;
		color: #2e7d32;
	}

	.pagination {
		margin-top: 2rem;
		display: flex;
		justify-content: center;
		align-items: center;
		gap: 1rem;
	}

	.pagination .navigate {
		padding: 0.5rem 1rem;
		border: none;
		background: #ff5a5f;
		color: white;
		border-radius: 4px;
		cursor: pointer;
	}

	.pagination .navigate:disabled {
		background: #ddd;
		cursor: not-allowed;
	}
	.pagination .page {
		font-weight: bold;
		border: none;
		border-radius: 4px;
		padding: 4px 10px;
		border-radius: 1000px;
		cursor: pointer;
	}
	.pagination .page:hover {
		background-color: #DDDDDD;
	}
	.pagination .page.active {
		background-color: #ff5a5f;
		color: white;
	}
</style>
