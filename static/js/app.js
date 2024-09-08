document.addEventListener('DOMContentLoaded', function() {
    const diseaseSelect = document.querySelector('[name="disease_choice"]');
    const genderSelect = document.getElementById('gender');

    diseaseSelect.addEventListener('change', function() {
        if (this.value === 'Cancer') {
            genderSelect.style.display = 'block';
        } else {
            genderSelect.style.display = 'none';
        }
    });
});

