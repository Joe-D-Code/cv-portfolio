document.addEventListener('DOMContentLoaded', () => {
    const categoryFilter = document.getElementById('category-filter');
    const tableBody = document.querySelector('#products-table tbody');
    const isLoggedIn = document.body.dataset.loggedIn === 'true'; // Get from HTML attribute

    // Initial load
    loadProducts();

    // Filter on change
    categoryFilter.addEventListener('change', loadProducts);

    async function loadProducts() {
        try {
            showLoading(true);
            const category = categoryFilter.value;
            const url = `/grocery_store/api/get_products.php${category === 'all' ? '' : `?category=${encodeURIComponent(category)}`}`;

            const response = await fetch(url);
            const result = await response.json();

            if (!result.success) {
                throw new Error(result.error || 'Failed to load products');
            }

            renderProducts(result.data);
        } catch (error) {
            console.error('Error:', error);
            showError(error.message);
        }
    }

    function renderProducts(products) {
        if (products.length === 0) {
            tableBody.innerHTML = `
                <tr class="loading-row">
                    <td colspan="${isLoggedIn ? 5 : 4}">No products found</td>
                </tr>
            `;
            return;
        }

        tableBody.innerHTML = products.map(product => `
            <tr>
                <td>${product.product_name}</td>
                <td>${product.category}</td>
                <td>£${product.price.toFixed(2)}</td>
                <td><img src="../assets/${product.image_path}" alt="${product.product_name}" height="50"></td>
                ${isLoggedIn ? `<td><button class="add-to-order" data-name="${product.product_name}" data-price="${product.price}">Add to Order</button></td>` : ''}
            </tr>
        `).join('');

        // Add event listeners to all buttons
        document.querySelectorAll('.add-to-order').forEach(button => {
            button.addEventListener('click', () => {
                addToOrder(
                    button.dataset.name,
                    button.dataset.price
                );
            });
        });
    }

    async function addToOrder(productName, price) {
        try {
            const response = await fetch('../api/add_order.php', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    product_name: productName,
                    price: price
                })
            });

            const result = await response.json();
            
            if (result.success) {
                alert('Item added to your order!');
            } else {
                alert('Error: ' + result.error);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Failed to add order');
        }
    }

    function showLoading(show) {
        if (show) {
            tableBody.innerHTML = `
                <tr class="loading-row">
                    <td colspan="${isLoggedIn ? 5 : 4}">Loading products...</td>
                </tr>
            `;
        }
    }

    function showError(message) {
        tableBody.innerHTML = `
            <tr class="error-row">
                <td colspan="${isLoggedIn ? 5 : 4}">⚠️ ${message}</td>
            </tr>
        `;
    }
});