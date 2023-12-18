function getObjects(image, navigate = "") {
  const url = "http://localhost:8000/object_detection/combine"; // Replace with your API endpoint URL

  const payload = {
    image: image,
  };

  const requestOptions = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Requested-With": "XMLHttpRequest",
    },
    body: JSON.stringify(payload),
  };

  fetch(url, requestOptions)
    .then((response) => response.json())
    .then((data) => {
      // console.log("Response:", data);
      sessionStorage.setItem("singleImageData", JSON.stringify(data));

      console.log("Set done");

      if (navigate != "") {
        window.location.href = navigate;
      }

      return data;
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

function getCamObjects(image, navigate = "") {
  const url = "http://localhost:8000/object_detection/cam"; // Replace with your API endpoint URL

  const payload = {
    image: image,
  };

  const requestOptions = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Requested-With": "XMLHttpRequest",
    },
    body: JSON.stringify(payload),
  };

  fetch(url, requestOptions)
    .then((response) => response.json())
    .then((data) => {
      // console.log("Response:", data);
      sessionStorage.setItem("singleImageData", JSON.stringify(data));

      console.log("Set done");

      if (navigate != "") {
        window.location.href = navigate;
      }

      return data;
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}
