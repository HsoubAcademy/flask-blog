function likeArticle(articleId) {
    const likeCount = document.getElementById(`likes-count-${articleId}`);
    const likeButton = document.getElementById(`like-button-${articleId}`);

    fetch(`/article/${articleId}/like`, { method: "POST" })
        .then((res) => res.json()).then((data) => {
            likeCount.innerHTML = data["likes"];
            if (data["liked"] === true) {
                likeButton.className = "fas fa-thumbs-up fa-2x";
            }
            else {
                likeButton.className = "far fa-thumbs-up fa-2x";
            }
        });
}