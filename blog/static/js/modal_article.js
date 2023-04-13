var articleModal = document.getElementById("articleModal");
if (articleModal){
  articleModal.addEventListener("show.bs.modal", function (event) {
    var button = event.relatedTarget;
    var article_url = button.getAttribute("data-bs-url");
    var title = button.getAttribute("data-bs-title");
    var delBtn = articleModal.querySelector("#delBtn");
    var modalTitle = articleModal.querySelector(".modal-body");
    delBtn.setAttribute("href", location.origin + article_url);
    modalTitle.textContent = "حذف مقالة: " + title;
  });
}