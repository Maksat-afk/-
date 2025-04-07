document.getElementById("snack-form").addEventListener("submit", function (event) {
    event.preventDefault();
    let formData = new FormData(this);

    fetch("/add-snack", {
        method: "POST",
        body: formData
    }).then(response => response.json())
      .then(data => alert(data.message))
      .then(() => location.reload());
});

document.getElementById("news-form").addEventListener("submit", function (event) {
    event.preventDefault();
    let formData = new FormData(this);

    fetch("/add-news", {
        method: "POST",
        body: formData
    }).then(response => response.json())
      .then(data => alert(data.message))
      .then(() => location.reload());
});

function deleteSnack(name) {
    fetch("/delete-snack", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name })
    }).then(response => response.json())
      .then(data => alert(data.message))
      .then(() => location.reload());
}

function deleteNews(newsId) {
    fetch("/delete-news", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: newsId })
    }).then(response => response.json())
      .then(data => alert(data.message))
      .then(() => location.reload());
}

function resetSeats() {
    fetch("/reset-seats", { method: "POST" })
        .then(response => response.json())
        .then(data => alert(data.message))
        .then(() => location.reload());
}

function freeSeat(seatId) {
    fetch("/free-seat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ seat_id: seatId })
    }).then(response => response.json())
      .then(data => alert(data.message))
      .then(() => location.reload());
}
