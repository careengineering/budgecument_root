// Modal
function showModal(uid, modalTextContent, deleteUrl) {
    var modal = document.getElementById('deleteModal');
    var modalText = document.getElementById('modalText');
    var deleteForm = document.getElementById('deleteForm');
    var deleteUid = document.getElementById('deleteUid');

    modal.style.display = "block";
    modalText.textContent = modalTextContent;
    deleteForm.action = deleteUrl;  // Set the form action URL
    deleteUid.value = uid;  // Set the value of hidden input to the bank account uid
}

function closeModal() {
    var modal = document.getElementById('deleteModal');
    modal.style.display = "none";
}

window.onclick = function(event) {
    var modal = document.getElementById('deleteModal');
    if (event.target == modal) {
        modal.style.display = "none";
    }
};



// New transaction field visibilities
document.addEventListener('DOMContentLoaded', function() {
    const transactionTypeField = document.getElementById('id_transaction_type');
    const sourceAccountField = document.getElementById('id_source_account');
    const destinationAccountField = document.getElementById('id_destination_account');
    const descriptionField = document.getElementById('id_description');
    const amountField = document.getElementById('id_amount');
    const sourceAccountDiv = document.getElementById('source_account_field');
    const destinationAccountDiv = document.getElementById('destination_account_field');
    const descriptionDiv = document.getElementById('description_field');
    const amountDiv = document.getElementById('amount_field');

    function toggleFields() {
        const transactionType = transactionTypeField.value;

        if (transactionType === 'deposit' || transactionType === 'withdraw') {
            sourceAccountDiv.style.display = 'block';
            destinationAccountDiv.style.display = 'none';
            descriptionDiv.style.display = 'block';
            amountDiv.style.display = 'block';
        } else if (transactionType === 'transfer') {
            sourceAccountDiv.style.display = 'block';
            destinationAccountDiv.style.display = 'block';
            descriptionDiv.style.display = 'block';
            amountDiv.style.display = 'block';
            updateDestinationAccountOptions();
        } else {
            sourceAccountDiv.style.display = 'none';
            destinationAccountDiv.style.display = 'none';
            descriptionDiv.style.display = 'none';
            amountDiv.style.display = 'none';
        }
    }

    function updateDestinationAccountOptions() {
        const sourceAccountId = sourceAccountField.value;
        if (sourceAccountId) {
            const apiUrl = `/bank_accounts/api/filter_destination_accounts/?source_account=${sourceAccountId}`;
            console.log(`Fetching destination accounts from: ${apiUrl}`);
            fetch(apiUrl)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.error) {
                        console.error('Server error:', data.error);
                        return;
                    }
                    destinationAccountField.innerHTML = '';
                    data.options.forEach(option => {
                        const newOption = document.createElement('option');
                        newOption.value = option.value;
                        newOption.text = option.display;
                        destinationAccountField.appendChild(newOption);
                    });
                })
                .catch(error => {
                    console.error('Fetch error:', error);
                });
        }
    }

    transactionTypeField.addEventListener('change', toggleFields);
    sourceAccountField.addEventListener('change', updateDestinationAccountOptions);

    toggleFields();

    if (transactionTypeField.value === 'transfer') {
        updateDestinationAccountOptions();
    }
});
