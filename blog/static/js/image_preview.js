function image_preview(event) {
    if (event.target.files.length > 0) {
      var src = URL.createObjectURL(event.target.files[0]);
      var preview = document.getElementsByClassName("ImgPreviewClass")[0];
      preview.src = src;
      preview.style.display = "block";
    }
  }