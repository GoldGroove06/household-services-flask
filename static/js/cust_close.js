

function closeHandler() {
  console.log(uid);
  
  
    fetch(`/close/${uid}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        rating: rating.value,
        remarks: document.getElementById("remarks").value,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.m == "success") {
          window.location.href = "/profile";
        }
      });
  }

