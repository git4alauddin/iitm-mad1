// ---------------------------------------------------------dialog box------------------------- //
function showConfirmation(deleteUrl) {
    var confirmationDialog = document.getElementById('confirmation-dialog');
    confirmationDialog.style.display = 'flex';
    document.querySelector('.confirm-btn').setAttribute('onclick', 'window.location.href = \'' + deleteUrl + '\';');
}
function hideConfirmation() {
    document.getElementById('confirmation-dialog').style.display = 'none';
}