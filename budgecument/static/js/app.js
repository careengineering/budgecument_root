// Modal
function showModal(uid) {
    var modal = document.getElementById('deleteModal');
    var modalText = document.getElementById('modalText');
    var deleteForm = document.getElementById('deleteForm');
    var deleteUid = document.getElementById('deleteUid');

    modal.style.display = "block";
    modalText.textContent = "Bu banka hesabını silmek istediğinize emin misiniz?";
    deleteForm.action = '/bank_accounts/delete/' + uid + '/';  // Set the form action URL
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


//Hide destination
function showHideDestination() {
    var transactionType = document.getElementById('id_transaction_type').value;
    var destinationField = document.getElementById('id_destination_account').parentNode.parentNode;

    if (transactionType == '2') {  // Assuming 'TRANSFER' has value '2', adjust as per your model definition
        destinationField.style.display = 'block';
    } else {
        destinationField.style.display = 'none';
    }
}

document.addEventListener('DOMContentLoaded', function () {
    showHideDestination();  // Initial check when the form loads
});
