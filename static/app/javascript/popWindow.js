function getModal(height){
    return document.getElementById('myModal'+ height)
}

function popWindow(height) {
    modal = getModal(height)
    modal.style.display = "block";
}

function hideWindow(height) {
    modal = getModal(height)
    modal.style.display = "none";
}
