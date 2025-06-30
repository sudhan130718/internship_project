
  function updateQuantity(change) {
    const input = document.getElementById('quantity');
    let value = parseInt(input.value);
    value = Math.max(1, value + change);
    input.value = value;
    document.getElementById('formQuantity').value = value;
  }

  