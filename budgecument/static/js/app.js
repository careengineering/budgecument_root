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



// For transfer
document.addEventListener('DOMContentLoaded', function () {
    var transactionTypeField = document.getElementById('id_transaction_type');
    var sourceAccountField = document.getElementById('id_source_account');
    var destinationAccountField = document.getElementById('destination_account_field');
    var destinationAccountInput = document.getElementById('id_destination_account');

    function updateDestinationAccounts() {
        var sourceAccountId = sourceAccountField.value;

        if (transactionTypeField.value === 'transfer' && sourceAccountId) {
            fetch(`/get_destination_accounts/${sourceAccountId}/`)
                .then(response => response.json())
                .then(data => {
                    destinationAccountInput.innerHTML = ''; // Önceki seçenekleri temizle
                    data.forEach(account => {
                        var option = document.createElement('option');
                        option.value = account.id;
                        option.textContent = `${account.name} - ${account.currency}`;
                        option.setAttribute('data-currency', account.currency);
                        destinationAccountInput.appendChild(option);
                    });
                    destinationAccountField.style.display = 'block';
                    destinationAccountInput.disabled = false;
                });
        } else {
            destinationAccountField.style.display = 'none';
            destinationAccountInput.disabled = true;
        }
    }

    transactionTypeField.addEventListener('change', updateDestinationAccounts);
    sourceAccountField.addEventListener('change', updateDestinationAccounts);
    updateDestinationAccounts();
});


fetch(`/get_destination_accounts/${sourceAccountId}/`)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        destinationAccountInput.innerHTML = ''; // Önceki seçenekleri temizle
        data.forEach(account => {
            var option = document.createElement('option');
            option.value = account.id;
            option.textContent = `${account.name} - ${account.currency__code}`;
            destinationAccountInput.appendChild(option);
        });
        destinationAccountField.style.display = 'block';
        destinationAccountInput.disabled = false;
    })
    .catch(error => console.error('There was a problem with the fetch operation:', error));
