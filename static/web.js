document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("unified-form");
    const fileUpload = document.getElementById("file-upload");
    const previewContainer = document.getElementById("preview-container");
    const loadingBar = document.getElementById("loading-bar");
    const fileLimitMsg = document.getElementById("file-limit-msg");
    const videoOutput = document.getElementById("video-output");
  
    let selectedFiles = [];
  
    fileUpload.addEventListener("change", () => {
      previewContainer.innerHTML = "";
      fileLimitMsg.style.display = "none";
      videoOutput.style.display = "none";
      videoOutput.src = "";
      selectedFiles = Array.from(fileUpload.files);
  
      const imageFiles = selectedFiles.filter(file => file.type.startsWith("image/"));
      const videoFiles = selectedFiles.filter(file => file.type.startsWith("video/"));
  
      if (imageFiles.length > 0 && videoFiles.length > 0) {
        alert("Please upload either images or a single video, not both.");
        fileUpload.value = "";
        selectedFiles = [];
        return;
      }
  
      if (imageFiles.length > 8) {
        fileLimitMsg.style.display = "block";
        fileUpload.value = "";
        selectedFiles = [];
        return;
      }
  
      if (videoFiles.length > 1) {
        alert("Please upload only one video at a time.");
        fileUpload.value = "";
        selectedFiles = [];
        return;
      }
  
      if (videoFiles.length === 1) {
        const videoURL = URL.createObjectURL(videoFiles[0]);
        const video = document.createElement("video");
        video.src = videoURL;
        video.controls = true;
        video.style.maxWidth = "100%";
        previewContainer.appendChild(video);
      } else {
        imageFiles.forEach((file, index) => {
          const reader = new FileReader();
          reader.onload = (e) => {
            const img = document.createElement("img");
            img.src = e.target.result;
            img.alt = `Uploaded Image ${index + 1}`;
            img.dataset.index = index;
            img.className = "preview-image";
            previewContainer.appendChild(img);
          };
          reader.readAsDataURL(file);
        });
      }

    });
  
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      if (selectedFiles.length === 0) return;
  
      const imageFiles = selectedFiles.filter(file => file.type.startsWith("image/"));
      const videoFiles = selectedFiles.filter(file => file.type.startsWith("video/"));
  
      loadingBar.style.width = "100%";
      loadingBar.style.opacity = 1;
  
      try {
        if (videoFiles.length === 1) {
          const formData = new FormData();
          formData.append("video", videoFiles[0]);
  
          const res = await fetch("/predict/video/", {
            method: "POST",
            body: formData,
          });
  
          const data = await res.json();
          if (!res.ok || data.error) throw new Error(data.error || "Video prediction failed");
  
          const fullVideoUrl = window.location.origin + data.video_url;
          previewContainer.innerHTML = "";
          videoOutput.src = fullVideoUrl;
          videoOutput.style.display = "block";
          videoOutput.load();
          videoOutput.play();
  
        } else if (imageFiles.length > 0) {
          const formData = new FormData();
          imageFiles.forEach(file => formData.append("files", file));
  
          const res = await fetch("/predict/images/", {
            method: "POST",
            body: formData,
          });
  
          const data = await res.json();
          if (data.error) throw new Error(data.error);
  
          if (data.result_images && Array.isArray(data.result_images)) {
            data.result_images.forEach((base64Img, i) => {
              const imgTag = previewContainer.querySelector(`img[data-index="${i}"]`);
              if (imgTag) imgTag.src = base64Img;
            });
          } else {
            alert("No result images received.");
          }
        } else {
          alert("Unsupported file type.");
        }
  
      } catch (err) {
        console.error("Detection failed:", err);
        alert("Detection failed. Check logs.");
      } finally {
        loadingBar.style.width = "0%";
        loadingBar.style.opacity = 0;
      }
    });
  });