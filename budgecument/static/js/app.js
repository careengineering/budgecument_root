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



//Hide source_account
document.addEventListener('DOMContentLoaded', function() {
    const transactionTypeField = document.getElementById('id_transaction_type');
    const sourceAccountField = document.getElementById('id_source_account');
    const destinationAccountField = document.getElementById('id_destination_account');

    // Function to toggle the visibility of the destination account field
    function toggleDestinationAccountField() {
        if (transactionTypeField.value === 'transfer') {
            destinationAccountField.parentElement.style.display = 'block';
        } else {
            destinationAccountField.parentElement.style.display = 'none';
        }
    }

    // Event listener for changes in the transaction type field
    transactionTypeField.addEventListener('change', toggleDestinationAccountField);
    sourceAccountField.addEventListener('change', toggleDestinationAccountField);

    // Initial call to set the correct visibility based on the initial value
    toggleDestinationAccountField();
});
