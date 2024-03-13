document.addEventListener('DOMContentLoaded', () => {
    const updateContainer = document.getElementById('updateContainer');

    async function fetchOrders() {
        try {
            const response = await fetch('http://0.0.0.0:8000/orders/');
            const orders = await response.json();

            // Clear previous content
            updateContainer.innerHTML = '';

            // Loop through each order and append its details as text
            orders.forEach(order => {
                const orderText = `Order ID: ${order.order_id}, Market: ${order.Market}, Price: $${order.Price}, Quantity: ${order.Quantity}, Side: ${order.Side}, Producer: ${order.Producer_name}`;
                const textNode = document.createTextNode(orderText);
                const lineBreak = document.createElement('br');

                updateContainer.appendChild(textNode); // Add the order text
                updateContainer.appendChild(lineBreak); // Add a line break for spacing
            });
        } catch (error) {
            console.error("Failed to fetch orders:", error);
        }
    }
    // Fetch orders on initial load
    fetchOrders();
});