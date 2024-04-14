const checkoutButton = document.getElementById('checkout-button');
const radioButtons = document.querySelectorAll('input[name="selected_book"]');

checkoutButton.addEventListener('click', function() {
    checkoutButton.classList.add('clicked');
});

radioButtons.forEach(radioButton => {
    radioButton.addEventListener('change', function() {
        checkoutButton.disabled = !document.querySelector('input[name="selected_book"]:checked');
    });
});
document.addEventListener('DOMContentLoaded', function() {
            const radioButtons = document.querySelectorAll('.custom-radio');
            const bookIdInput = document.getElementById('book_id_input');

            radioButtons.forEach(function(radioButton) {
                radioButton.addEventListener('change', function() {
                    if (this.checked) {
                        bookIdInput.value = this.value;
                    }
                });
            });
        });
