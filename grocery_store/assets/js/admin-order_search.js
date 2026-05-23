document.addEventListener('DOMContentLoaded', function() {
    
    const searchBox = document.getElementById('orderSearchBox');
    if (!searchBox) {
      console.error("Search box element not found");
      return;
    }
    
    const table = document.getElementById('products-table');
    if (!table) {
      console.error("Table element not found");
      return;
    }
    
    const tableRows = table.querySelectorAll('tbody tr');
    
    const noResultsMessage = document.getElementById('noResults');
    if (!noResultsMessage) {
      console.warn("No results message element not found");
    }
    
    function filterTable() {
      const searchTerm = searchBox.value.toLowerCase().trim();
      
      
      let hasVisibleRows = false;
      
      tableRows.forEach(function(row) {
        // Get the order_id cell (first column)
        const orderIdCell = row.cells[0];
        
        if (orderIdCell) {
          const orderId = orderIdCell.textContent.toLowerCase().trim();
          
          if (searchTerm === '' || orderId.includes(searchTerm)) {
            row.style.display = '';
            hasVisibleRows = true;
          } else {
            row.style.display = 'none';
          }
        }
      });
      
      // Show/hide "No results" message
      if (noResultsMessage) {
        noResultsMessage.style.display = hasVisibleRows ? 'none' : 'block';
      }
      
    }
    
    // Add input event listener
    searchBox.addEventListener('input', filterTable);
    
    // Clear search when user presses Escape
    searchBox.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') {
        searchBox.value = '';
        filterTable();
      }
    });
    
  });