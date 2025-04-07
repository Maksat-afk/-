document.querySelectorAll(".seat.free").forEach(seat => {
    seat.addEventListener("click", function() {
        let seatId = this.getAttribute("data-seat");
        openModal(seatId);
    });
});

function openModal(seatId) {
    document.getElementById("modal-seat-id").value = seatId;
    document.getElementById("selected-seat-number").innerText = seatId;
    document.getElementById("bookingModal").style.display = "flex"; // ← фикс
}

function closeModal() {
    document.getElementById("bookingModal").style.display = "none";
}

document.getElementById("booking-form").addEventListener("submit", function (e) {
    e.preventDefault();
    let seat_id = document.getElementById("modal-seat-id").value;
    let name = document.getElementById("name").value;
    let phone = document.getElementById("phone").value;
    let time = document.getElementById("time").value;

    fetch("/book-seat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ seat_id, name, phone, time })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message || "Бронирование успешно!");
        closeModal();
        location.reload();
    });
});
